#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:21:31 2020

@author: ludivinelacour
"""

from utils import get_json, get_specialities, get_db_connexion 

import pandas as pd
import re
from datetime import datetime
import time


def get_user_search(list_of_specialities):
    
    while True:
        # Ask the user what kind of doctors they are looking for
        speciality_search=input('What kind of doctor are you looking for?\n')
    
        specialities_match=tuple(i for i in list_of_specialities if re.search(speciality_search,i,re.IGNORECASE))
        if len(specialities_match)>0:
            print('Matched specialities: ', specialities_match)
            break
        else:
            print('No matching specialities. Try again.')
            
    #Ask the user where they would like to consult
    location_search=input('Where would you like to find this doctor? (please enter a zipcode)\n')
        
    return specialities_match, location_search


def get_db_results(specialities_match,location_search):
   
    spe_match=str(specialities_match)
    print(spe_match)
    if len(specialities_match)==1:
        spe_match=spe_match.replace(',','')
    print(spe_match)    
    
    database='doctolib_scrap'
    engine=get_db_connexion(database)
    
    query='SELECT name_with_title, speciality, address, zipcode, city, case when doctolib_profile = 1 then "True" else "False" end as has_doctolib_profile, link FROM doctors WHERE zipcode = {} and speciality in {}'.format(location_search, spe_match)
    print(query)
    db=pd.read_sql_query(query,engine)
    print(db)
    return db


def get_next_availability(link):
    
    # get the all slugs to put in url request
    doctor_slug=link[(re.search('(.*/){2}',link).end()):]
    pos_spe=re.search('^\/(.*?)\/',link)
    speciality_slug=pos_spe.group(1)
    pos_location=re.search('\/.*\/(.*?)\/',link)
    location_slug=pos_location.group(1)
    # 1. Get enriched data for each profile (agendas_id and visit_motive_id)
    enriched_url=f'https://www.doctolib.fr/booking/{doctor_slug}.json'
    enriched_result=get_json(enriched_url,speciality_slug,location_slug,page_num=1)
    # extract all visit_motives_id
    visit_motives="-".join(pd.json_normalize(enriched_result['data']['visit_motives'])['id'].astype(str).tolist())
    # extract all agenda_id
    agendas="-".join(pd.json_normalize(enriched_result['data']['agendas'])['id'].astype(str).tolist())
    today=datetime.today().strftime('%Y-%m-%d')
    
    # 2. Get the next availability
    availability_url=f'https://www.doctolib.fr/availabilities.json?start_date={today}&visit_motive_ids={visit_motives}&agenda_ids={agendas}&limit=4'
    availability_result=get_json(availability_url,speciality_slug,location_slug,page_num=1)
    
    availabilities=pd.json_normalize(availability_result)

    if "next_slot" in availabilities.columns:
        next_availability=availabilities.next_slot[0]
    else:
        data=pd.json_normalize(availability_result['availabilities'])
        next_availability=data[data.slots.astype(str)!="[]"].date.min()
    
    return next_availability


def doctors_availability(db):
    
    doctolib_profile=db[db['has_doctolib_profile']=="True"]
    
    doctolib_profile = doctolib_profile.assign(next_availability = doctolib_profile.link.apply(get_next_availability).tolist())
    
    return doctolib_profile[['name_with_title','next_availability']]


if __name__=='__main__':
    list_of_specialities_slug,list_of_specialities=get_specialities()
    specialities_match, location_search=get_user_search(list_of_specialities)
    db=get_db_results(specialities_match, location_search)
    time.sleep(3)
    if len(db)==0:
        print("Sorry no doctors available in your location")
    else:
        print("Let's find the availabilities for doctors thanks to their doctolib profiles...")
        final_df=doctors_availability(db)
        time.sleep(3)
        print(final_df)
    