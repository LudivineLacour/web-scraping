#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:59:24 2020

@author: ludivinelacour
"""

from utils import get_json, get_specialities, get_db_connexion 

import pandas as pd
import time

def get_database(specialities_slug=[]):
    
    # Final scrapping for all specialities
    base_url='https://www.doctolib.fr'
    location='france'
    #speciality='stomatologue'
    df_final=pd.DataFrame()
    
    for i in range(len(specialities_slug)):
        
        speciality=specialities_slug[i]
        page_num=0
        doctors=True
        print("speciality: ", speciality, " location: ", location)
        
        while doctors:
        
            page_num+=1
    
            final_url=f"{base_url}/{speciality}/{location}?page={page_num}"
    
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
    
            time.sleep(0.5)
    
    return df_final

    
def save_database(df):
    # Save the data in a database
    database='doctolib_db'
    
    engine=get_db_connexion(database)
    
    # reset index to have a unique id for each row
    df=df.reset_index()
    # drop useless columns before saving the data
    col_to_drop=['id','index','is_directory','cloudinary_public_id','exact_match']
    df=df.drop(col_to_drop,axis=1)
    # convert top_specialities into string type
    df.top_specialities.fillna('[]', inplace=True)
    df.top_specialities=df.top_specialities.astype(str).convert_dtypes()

    # send data into the database
    df.to_sql('doctors', engine, if_exists='replace',index=False)

if __name__=='__main__':
    list_of_specialities_slug, list_of_specialities = get_specialities()
    df=get_database(list_of_specialities_slug)
    save_database(df)