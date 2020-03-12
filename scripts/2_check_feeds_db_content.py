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
import sys
import sqlite3
	
def read_db(database,table):
	liste=[]
	with sqlite3.connect(database) as conn:
		cursor=conn.cursor()
		sql_request = "SELECT * from `"+table+"`"
		print(sql_request)
		try:
			cursor.execute(sql_request)
			for resultat in cursor:
				#print(resultat)		
				liste.append(resultat)
		except:
			sys.exit("couldn't read database")
	return(liste)

def main():
	#resultats = read_db('C:/patrick/zazou_dev/zazou_etid/www/livre/files/bases/etid.db','=','1')	
	#resultats = read_db('../bases/python_parsers.db','python_parsers','parser_name','=','PARSER 10')	
	resultats = read_db('../bases/etid.db','feeds',)	
	if resultats :
		for resultat in resultats:
			print(resultat)
	else:
		print('NO RESULTS')
if __name__=='__main__':
	main()
