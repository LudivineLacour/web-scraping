#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:59:24 2020

@author: ludivinelacour
"""

from utils import get_json, get_specialities, get_db_connexion 

import pandas as pd
import time

def save_database(df,speciality_search,engine):
    # Save the data in a database
    
    # reset index to have a unique id for each row
    df=df.reset_index()
    # fill nan values with top specialities
    if 'top_specialities' in df.columns:
        df.speciality=df.speciality.fillna(str(df['top_specialities']))
    # If no top_specialities columns and still nan values, fill with the speciality searched

    df.speciality.fillna(speciality_search, inplace=True)
    # drop useless columns before saving the data
    col_to_drop=['id','index','is_directory','cloudinary_public_id','exact_match','top_specialities']
    for col in col_to_drop:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

    # send data into the database
    df.to_sql('doctors', engine, if_exists='append',index=False)
    

def get_database(specialities_slug=[],list_of_specialities=[]):
    
    database='doctolib_scrap'
    engine=get_db_connexion(database)
    
    # Final scrapping for all specialities
    base_url='https://www.doctolib.fr'
    location='france'
    failed_db=[]
    
    for i in range(len(specialities_slug)):
        
        df_final=pd.DataFrame()
        speciality=specialities_slug[i]
        page_num=0
        doctors=True
        print("speciality: ", speciality, " location: ", location)
        
        while doctors:
        
            page_num+=1
    
            final_url=f"{base_url}/{speciality}/{location}?page={page_num}"
            print(f'/{speciality}/{location}?page={page_num}')
    
            result=get_json(final_url, speciality, location, page_num)
            data_doctors=result['data']['doctors']
            data_directory=result['data']['directory_doctors']
            #variable doctors allows to set the while loop to False when there is no more results
            doctors=(len(data_doctors)!=0) or (len(data_directory)!=0)
    
            if len(data_doctors)>0:
                data=pd.json_normalize(data_doctors)
                data['doctolib_profile']=True
                df_final=df_final.append(data)
    
            if len(data_directory)>0:
                data=pd.json_normalize(data_directory)
                data=data.rename(columns={'zip_code':'zipcode'})
                data['doctolib_profile']=False
                data['profile_id']=-1
                df_final=df_final.append(data)
    
            time.sleep(0.3)
        print("Save to database")
        try:
            save_database(df_final,list_of_specialities[i],engine)
            print("Saved to database")
        except:
            print("Failed to save in database: ", speciality)
            failed_db.append(speciality)
            
    return failed_db


if __name__=='__main__':
    list_of_specialities_slug, list_of_specialities = get_specialities()
    failed_db = get_database(list_of_specialities_slug,list_of_specialities)