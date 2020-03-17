# coding: utf-8
'''
Copyright (c) 2020 Cisco and/or its affiliates.

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
import sqlalchemy


print('This Script Generate single files for every feeds')
db_name = "../bases/exposed_feeds.db"
table_name = "ip_addr"

engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql_table(table_name, engine)

out_df = df[['ip']]
#save result to csv file
out_df.to_csv(r'../clean_feeds/ip_addresses.txt',index = None, header=False)
print('Clean IP Addresses Feed is exposed into ./clean_feeds directory')

table_name = "domains"

engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql_table(table_name, engine)

out_df = df[['domain']]
#save result to csv file
out_df.to_csv(r'../clean_feeds/domains.txt',index = None, header=False)
print('Clean Domains Feed is exposed into ./clean_feeds directory')

table_name = "urls"

engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql_table(table_name, engine)

out_df = df[['url']]
#save result to csv file
out_df.to_csv(r'../clean_feeds/urls.txt',index = None, header=False)
print('Clean URLs Feeds is exposed into ./clean_feeds directory')
print()
print('ALL FEEDS ARE EXPOSED')