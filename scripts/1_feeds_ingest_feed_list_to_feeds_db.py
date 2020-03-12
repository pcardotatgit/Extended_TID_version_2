'''
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('../files/feeds.txt')
#df = pd.read_csv('donnees.txt',delimiter=',',names = ['firstname', 'lastname', 'phone', 'email'])
engine = create_engine('sqlite:///../bases/etid.db')
df.to_sql('feeds', con=engine, if_exists='replace')   #with this one you can truncat an existing database
#df.to_sql('feeds', con=engine, if_exists='append')   #with this one you can append date to an existing database
 

