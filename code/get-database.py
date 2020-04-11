#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:59:24 2020

@author: ludivinelacour
"""

import pandas as pd
import requests as r
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time
import json
import unicodedata
import pymysql
from sqlalchemy import create_engine


def get_specialities():
# Get the list of specialities
url='https://www.doctolib.fr/specialities'

headers="user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
headers=dict([i.split(': ') for i in headers.split('\n')])

r.get(url,headers=headers)
html=r.get(url,headers=headers).content
soup=BeautifulSoup(html)

list_of_specialties_slug=[i["href"].strip('/') for i in soup.select('h1+div a')]
list_of_specialties=[i.text for i in soup.select('h1+div a')]
list_of_specialties