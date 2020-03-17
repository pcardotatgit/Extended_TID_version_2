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
import requests
import csv
import re
import pandas as pd
import sqlalchemy
import sqlite3
import sys
import ipaddress
from sqlalchemy import create_engine
import time

def read_csv(file):
	'''
	read URL FEEDS List
	'''
	donnees=[]
	with open (file) as csvfile:
		entries = csv.reader(csvfile, delimiter=';')
		for row in entries:
			#print (' print the all row  : ' + row)
			#print ( ' print only some columuns in the rows  : '+row[1]+ ' -> ' + row[2] )	
			row[1]=row[1].lower()	
			payload = {
				"url":row[0],
				"parser":row[1],
				"Type":row[2],
				"output":row[3],
			}			
			donnees.append(payload)
	return (donnees)
	
def read_all_lines_until_first_word_is(file,mot):
	# read the text file line by lines until the first string of the line is what the user has defined
	# if the string is not found, then all lines are read
	# end of file is detected if at the end we read 100 empty lines
	fh = open(file,"r",encoding="utf-8" )
	line=''
	#txt  = fh.readline()
	stop=0
	nb_lignes_vides=0
	while( stop == 0 ):
		txt = fh.readline()
		ii=0
		#debug
		#print(txt)
		if txt !='':
			stop=1
			while( ii < len(txt) ):
				#print (str(ii) + ' : ' + txt[ii] + ' - ')	
				line += txt[ii]				
				ii += 1
				i2=0
				while i2 < len(mot):
					#print (mot[i2])	
					if i2 < len(txt):						
						if txt[i2] != mot[i2]:
							stop=0
					i2 = i2+1
		else:
			#print ('empty line')
			nb_lignes_vides+=1
			if nb_lignes_vides > 100:
				stop=1
	fh.close()
	line=line.replace("\t","<==>")
	print("READ ALL LINES DONE = They are stored in the txt2 variable, ready for the next parsing steps")
	return(line)	
	
def parse_words(texte,filter):	
	#filtre=".*\\"+ filter+"\\s"  // pour se termine par le contenu de filter
	filtre=".*\\"+ filter
	selection = re.findall(filtre, texte)
	data=[]
	for s in selection:
		data.append(s.strip())
	return(data)

def parse(texte,a,mots1:list,mots2:list,start,end,parse_first_line,colomn:list,add_eol):
	# simpler than parse2
	#	a =	delimiter
	# 	colomn  =	colomns to keep  if colomn[0] =999 then keep all colomns
	#	mots1 = 	list of words to find in the line we want to keep. if the first and only word in the list is 'ALLWORDS' then we keep all lines
	# 	mots2 =	list of words to not find in the line we want to keep. if one word is found then the line is not kept
	#	start 	=	if the line begins with this word then start to keep all readed lines  until the [ end ] word is found in a coming line
	# 	end = 	the word which indicates the end of the chunk we parse in the file.
	#	parse_first_line = 1 if we want to parse the first kept line  of the chunk,  and = 0 if we don't want to parse it( we start to parse just the line after the [ start word ]
	#	if add_eol = 1 then add end of Line after every line read, if =0 concatenate all line read together
	lignes = texte.split('\n')
	commencer=0
	output=""
	for ligne in lignes:
		if ligne.find(start) >= 0:
			commencer=1
			if parse_first_line ==1:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 999:
						OK2=1
					if x !='' and OK2:
						# REMPLACEMENT de CARACTERES DEBUT
						x=x.replace('"','')
						x=x.replace(',','')		
						# REMPLACEMENT de CARACTERES FIN		
						x = x + ';'
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")	
				x = x + "\r\n"
				#print(x)
				output=output + x
				#fa.write('\n')				
		if ligne.find(end) >= 0:
			commencer=0
			x = x + "\r\n"
			output=output + x
			#fa.write('\n')
		if commencer:
			if mots1[0] != 'ALLWORDS':
				OK=0
				for x in mots1:
					if x in ligne:
						OK=1
			else:
				OK=1					
			for x in mots2:
				if x in ligne:
					OK=0	
			if OK:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				#i2=i2
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 999:
						OK2=1
					if x !='' and OK2:
						# REMPLACEMENT de CARACTERES DEBUT
						x=x.replace('"','')
						x=x.replace(',','')
						# REMPLACEMENT de CARACTERES FIN
						x = x + ';'
						#print(x)
						if add_eol:
							x = x + "\r\n"
						output=output + x
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")
				#fa.write('\n')	
	print("        		parse() function says : PARSING = OK")
	return(output)
	
def parse2(texte,a,mots1:list,mots2:list,start,end,parse_first_line,colomn:list,add_eol,add_eol_when,one_time):
	#	a =	delimiter
	# 	colomn  =	colomns to keep  if colomn[0] =999 then keep all colomns
	#	mots1 = 	list of words to find in the line we want to keep. if the first and only word in the list is 'ALLWORDS' then we keep all lines
	# 	mots2 =	list of words to not find in the line we want to keep. if one word is found then the line is not kept
	#	start 	=	if the line begins with this word then start to keep all readed lines  until the [ end ] word is found in a coming line
	# 	end = 	the word which indicates the end of the chunk we parse in the file.
	#	parse_first_line = 1 if we want to parse the first kept line  of the chunk,  and = 0 if we don't want to parse it( we start to parse just the line after the [ start word ]
	#	if add_eol = 1 then add end of Line after every line read, if =0 if you want to concatenate in a line all parsed words all line read together
	#	add_eol_when = add a new line character when the word is found in the line
	#	one_time : If = 1 then stop parsing when [ end ] reached. If = 0  parse again if [ start ] is found again in the file
	lignes = texte.split('\n')
	commencer=0
	do_it_again=1
	output=""
	x=""
	lignes_out=[]
	for ligne in lignes:
		#if ligne.find(start) >= 0 and do_it_again==1:
		#debug
		#print (ligne)
		if (ligne.find(start) >= 0 and do_it_again==1) or (start=="ALL_LINES"):
			# debug
			#print (ligne)
			commencer=1
			if parse_first_line ==1:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 999:
						OK2=1
					if x !='' and OK2:
						# clean unwanted characters in the parsed word : double quotes, comma, semi column
						x=x.replace('"','')
						x=x.replace(',','')	
						x=x.replace(':','')	
						x=x.replace(';','')
						# add comma to separate parsed word		
						x = x + ';'
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")	
				if ligne.find(add_eol_when) >= 0:						
					x = x + "\r\n"	
				#print(x)
				output=output + x
				#fa.write('\n')				
		if ligne.find(end) >= 0:
			commencer=0
			# debug
			#print("END WORD FOUND THEN STOP TO PARSE LINES")
			if one_time==1:
				do_it_again=0
				# debug
				#print("==> But do it again ON")
			lignes_out.append(output)
		if commencer:
			# debug
			#print("START = OK")
			if mots1[0] != 'ALLWORDS':
				# debug
				#print("====> NOT ALL_WORDS")
				OK=0
				for x in mots1:
					# debug
					#print("======> check for word : ",x)
					if x in ligne:
						OK=1
						# debug
						#print("========> YES FOUND")
					#else:
						#print("========> NO WORD FOUND")
			else:
				OK=1					
			for x in mots2:
				if x in ligne:
					OK=0	
			if OK:
				#debug
				#print(" ===> OK = 1")
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				#i2=i2
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 999:
						OK2=1
					if x !='' and OK2:
						# clean unwanted characters in the parsed word : double quotes, comma, semi column
						x=x.replace('"','')
						x=x.replace(',','')	
						x=x.replace(':','')	
						x=x.replace(';','')
						# add comma to separate parsed word	
						x = x + ','
						#debug 
						#print(x)
						if add_eol:
							#print('a',x)
							x = x + "\r\n"	
							lignes_out.append(output)
							output=""							
						if x.find(add_eol_when) >= 0:
							lignes_out.append(output)
							x = x + "\n"
							#output=""
						output=output + x
					i2=i2+1
	print("        		parse2() function says : PARSING = OK")
	return(lignes_out)
	

def query(URL,index):
	res = requests.get(URL)
	fichier="./temp/feed.txt"
	with open(fichier, "w", encoding="utf-8") as file:
		file.write(res.text)
	return(1)
	
def valid_ip(address):
	try: 
		addr=ipaddress.ip_address(address)
		#print(addr)
		return True
	except:
		return False
		
def read_db(database,table,field,operator,value):
	liste=[]
	with sqlite3.connect(database) as conn:
		cursor=conn.cursor()
		sql_request = "SELECT * from `"+table+"` where `"+field+"` "+operator+" '"+value+"'"
		#print(sql_request)
		try:
			cursor.execute(sql_request)
			for resultat in cursor:
				#print(resultat)		
				liste.append(resultat)
		except:
			sys.exit("couldn't read database")
	return(liste)	


def main():	
	# Loop into all Activated Feeds stored into the databas
	#df_domains = pd.DataFrame (Data_domains, columns = ['domain'])
	#df_urls = pd.DataFrame (Data_urls, columns = ['urls'])		
			
	db_name = "etid.db"
	table_name = "feeds"
	db_name3 = "exposed_feeds.db"
	ip_addrs=[]
	domains=[]
	urls=[]	
	ip_addrs_score=[]
	domains_score=[]
	urls_score=[]		
	engine3 = sqlalchemy.create_engine("sqlite:///../bases/%s" % db_name3, execution_options={"sqlite_raw_colnames": True})
	engine = sqlalchemy.create_engine("sqlite:///../bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
	df = pd.read_sql_table(table_name, engine)
	#  feed table variables : index ;  url  ;  parser_name  ;  type  ; output_prefixe ; description
	feeds_list=df.loc[df.Selected == 1]
	
	for index,row in feeds_list.iterrows():
		print()
		print("====> GOTO NEXT FEED =========>")
		print("")
		print("========================================================================================================================================")
		print("- STEP 1 : Loading the following public feed :")	
		print('      	feed : ',row['url'],' => Parser Name : ', row['parser_name'],'')		
		#print()
		#download the feed into temp directory as feed.txt file
		query(row["url"],index)
		index+=1		
		print("	==> OK DONE. Downloaded to ./temp/feeds.txt. Lets put it now into the txt2 variable")
		engine2 = sqlalchemy.create_engine("sqlite:///../bases/python_parsers.db", execution_options={"sqlite_raw_colnames": True})
		replace_df = pd.read_sql_table('search_and_replace', engine2)
		replace_list=replace_df.loc[replace_df.parser_name == row['parser_name']]
		if replace_list.empty:
			replace_strings=0		
			print ('	===> Remark : String Replace List is empty => we will skip this step. The parser name is : ',row['parser_name'])
		else:
			new_df=replace_df[['index','origin_string','destination_string']]
			replace_strings=1	
			print ('	===> Remark : String Replace List is NOT an empty List ')

		#input('This Feed had been downloaded. Type [ Enter ] to parse it\n It may take a while. Wait until prompt comes back ! ')
		# Let s parse the file
		print("========================================================================================================================================")
		print ('- STEP 2 :  Read the downloaded ./temp/feeds.txt file and store the result into the txt2 CSV Table variable. It could take a while if the source size is large !')
		file_to_read="./temp/feed.txt"
		txt2=read_all_lines_until_first_word_is(file_to_read,'*****')
		#debug
		#print(txt2)
		print('	==> DONE')
		print("========================================================================================================================================")
		print('- STEP 3 : PARSING ')
		print('	==> Loading parser details from sqli DB')		   	
		if row['parser_name']=='Toulouse':
			print("	==> Parser Name is : Toulouse . This is a predifine parser for Toulouse Black List. This is a very big feed. it Will take 10 mins to parse it ! ")
			#PARSER FOR  TOULOUSE  BLACK LIST
			#configure the parser
			mots_ok=['adult','agressif','arjel','malware','bitcoin','drogue','gambling','phishing']
			mots_nok=['#']
			colonnes=[999,1]
			mot_debut_de_groupe = "adult"			
			mot_fin_de_groupe = "*****"		
			#parse all lines into txt2 buffer
			result1 = parse(txt2,';',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes,1)
			# parse again the result in order to keep only domains ( words containing a dot '.' ) 
			list_result=[]
			list_result=result1.split("\n")
			result0=[]
			for mot in list_result:				
				if mot.find(".") >= 0:				
					result0.append(mot)				
		else:
			resultats = read_db('../bases/python_parsers.db','python_parsers','parser_name','=',row['parser_name'])	
			if resultats :
				for resultat in resultats:
					#print('=+>',resultat)
					if resultat[4].find('space')>=0:
						delimiter=resultat[4].replace('space',' ')
					elif resultat[4].find('tab')>=0:
						delimiter=resultat[4].replace('tab','\t')
					else:
						delimiter=resultat[4]
					liste_tmp=resultat[6].split(',')
					keep_lines_which_contains=[]
					for mot in liste_tmp:
						keep_lines_which_contains.append(mot)				
					liste_tmp=resultat[7].split(',')
					and_then_dont_keep_lines_which_contains=[]
					for mot in liste_tmp:
						and_then_dont_keep_lines_which_contains.append(mot)
						
					start_to_parse_when_found=resultat[8]
					stop_to_parse_when_found=resultat[9]
					
					liste_tmp=resultat[5].split(',')
					columns=[]
					for mot in liste_tmp:					
						columns.append(int(mot))					
					if len(columns)==0: 
						columns.append(999)
						
					parse_first_line=resultat[10]					
					add_eol_after_each_readed_line=resultat[11].strip()
					add_eol_after_each_readed_line=int(add_eol_after_each_readed_line)			
					add_a_new_line_when_found=resultat[12]			
					Parse_group_only_one_time=resultat[13].strip()
					Parse_group_only_one_time=int(Parse_group_only_one_time)				
			else:
				print('	==>NO RESULTS')	
				# for parsing debugging purpose	
				#keep_lines_which_contains=['.']
				#and_then_dont_keep_lines_which_contains=['#']	
				#start_to_parse_when_found='ALL_LINES'
				#stop_to_parse_when_found='*****?****'
				#columns=[2,10]
				#parse_first_line=0
				#add_eol_after_each_readed_line=1
				#add_a_new_line_when_found='*****???****'
				#Parse_group_only_one_time=0
					
			#for debug
			print('	PARSERs details are :')
			print()
			print('	PARSER NAME : ',resultat[1])
			print('	delimiter : >>',delimiter,'<< delimiter to use in the read line to seperate words')
			print('	words_ok : ',keep_lines_which_contains,"<<< we keep this read line only if we find one of these words into it ( separator must be , ). ALLWORDS = keep all lines")
			print('	words_Nok : ',and_then_dont_keep_lines_which_contains,"<<< but if we find one of these word into it, then we don t keep this line")
			print('	start_to_parse_when_found : ',start_to_parse_when_found,"<<< Start to parse the lines in the file when we find this word at the begining fo the line. parse all lines if equal to : ALL_LINES")
			print('	AND THEN stop_to_parse_when_found : ',stop_to_parse_when_found,"<<< stop to parse the file, when this word is found in the line")
			print('	Columns to keep : ',columns,"<<< all result will be stored into csv like columns. Give the Column number to keep. 999 = Keep all columns")
			print('	parse_first_line : ',parse_first_line,"<<< By default the first line of the file is not parsed")
			print('	add_eol_after_each_readed_line : ',add_eol_after_each_readed_line,"<<< 1 = Add a Carriage Return to resulting line after every parsed lines, 0 = Add a Carriage Return only when the add_a_new_line_when_found  word is found")
			print('	add_a_new_line_when_found : ',add_a_new_line_when_found,"<<< Add a Carriage Return only when this word is found")
			print('	Parse_group_only_one_time : ',Parse_group_only_one_time," <<< 0 = stop to parse file when stop_to_parse_when_found is found, 1 = start again when start_to_parse_when_found is found again")
			print()
			print('	==> Parse Datas stored into the txt2 variable')
			# for debugging
			#print ('txt2',delimiter,keep_lines_which_contains,and_then_dont_keep_lines_which_contains,start_to_parse_when_found,stop_to_parse_when_found,parse_first_line,columns,add_eol_after_each_readed_line,add_a_new_line_when_found,Parse_group_only_one_time)	
			#debug
			#print(txt2)
			result0 = parse2(txt2,delimiter,keep_lines_which_contains,and_then_dont_keep_lines_which_contains,start_to_parse_when_found,stop_to_parse_when_found,parse_first_line,columns,add_eol_after_each_readed_line,add_a_new_line_when_found,Parse_group_only_one_time)
		
		#debug
		#print (result0)

		print("	===> DONE txt2 variable parsed - all parsed words are stored into the result0 list")
		print("========================================================================================================================================")
		print('- STEP 4 : Then, Search And Replace clean UP for every lines in result0 ')
		print('           AND isolate ip_addr , domains and URLs')
		print('           AND create temporay output files for this feed into the /output directory')
		print('           Be patient, it could take a lot of time ! ')
		result=[]
		for mot in result0:		
			#debug
			#print('mot = ',mot)
			mot=mot.replace(";","")	
			mot=mot.replace("\r","")				
			mot=mot.replace("\n","")
			mot=mot.replace("\\","/")				
			mot=mot.replace(",","")
			# cleanup operation
			if replace_strings==1:
				#print ('===> Search and Replace = 1. Then Let s do some string clean up on parsed data ')
				for index, row2 in new_df.iterrows():
					#print(row2['origin_string'],' to => ', row2['destination_string'])	
					mot=mot.replace(row2['origin_string'],row2['destination_string'])
				#print ('===> Search and Replace DONE ')
			i=len(mot)
			#mot=mot[0:-1]
			if mot.find(".") >= 0 and mot.find(" ") < 0:
				if mot.find("|") >= 0:
					list_IPs=mot.split('|');
					for address in list_IPs:
						address+="(IP_ADDR)"
						result.append(address)
						#if address not in result:
							#result.append(address)
				else:
					#print(mot)
					if valid_ip(mot):
						mot+="(IP_ADDR)"					
					else:
						if mot.find("/") >= 0:
							mot+="(URL)"
						else:
							mot+="(DOMAIN)"
					#print(mot)
					result.append(mot)
					#if mot not in result:
						#result.append(mot)
		print('	===> DONE')
		print("========================================================================================================================================")
		print('- STEP 5 : Save resulting clean feed outputs in the [ ./output ] Directory')	
		# save content of the result[]  list
		# entry with (IP_ADDR) keyword will be saved into xxx_ip_addresses.txt file
		# entry with (DOMAIN) keyword will be saved into xxx_domains.txt file
		# entry with (URL) keyword will be saved into xxx_urls.txt file
		resulting_output="./output/ip_addr_"+row["output_prefixe"]+".txt"
		fa = open(resulting_output, "w")	
		resulting_output="./output/domains_"+row["output_prefixe"]+".txt"
		fb = open(resulting_output, "w")
		resulting_output="./output/urls_"+row["output_prefixe"]+".txt"
		fc = open(resulting_output, "w")			
		for observable in result:
			#debug
			#print(observable)
			observable=observable.replace("\r","")
			observable=observable.replace("\n","")
			if observable.find("(IP_ADDR)") >= 0:
				objet=observable.split("(")
				#print(objet[0])
				fa.write(objet[0])
				fa.write("\n")
				if objet[0]!="":
					ip_addrs.append(objet[0])
					ip_addrs_score.append('100')
			elif observable.find("(DOMAIN)") >= 0:
				objet=observable.split("(")
				mot_test=objet[0].replace(".","0")
				mot_test=mot_test.replace("-","0")
				if mot_test.isnumeric()==0:					
					fb.write(objet[0])
					fb.write("\n")
					if objet[0]!="":
						domains.append(objet[0])
						domains_score.append('100')							
			elif observable.find("(URL)") >= 0:
				objet=observable.split("(")
				fc.write(objet[0])
				fc.write("\n")
				if objet[0]!="":
					objet[0]=objet[0].replace("http/","http:/")
					objet[0]=objet[0].replace("https/","https:/")
					urls.append(objet[0])
					urls_score.append('100')	
			else:
				fc.write(objet[0])
				fc.write("\n")		
		fa.close()				
		fb.close()
		fc.close()
		print('	==> ALL DONE FOR THIS FEED ! =>')
	
	print("========================================================================================================================================")		
	print ("===========================================  ALL PUBLIC FEEDS HAD BEEN PARSED  ==========================================================")
	print("========================================================================================================================================")		
	print("========================================================================================================================================")
	print('- STEP 6 : create PANDA dataframes for each group of observables ( IPs, domains and URLs ) ')		
	Data_ips={}
	dict = {"ip": ip_addrs }
	Data_ips.update(dict)

	dict = {"score": ip_addrs_score }
	Data_ips.update(dict)
	
	Data_domains={}
	dict = {"domain": domains }
	Data_domains.update(dict)
	
	dict = {"score": domains_score }
	Data_domains.update(dict)			

	Data_urls={}
	dict = {"url": urls }
	Data_urls.update(dict)

	dict = {"score": urls_score }
	Data_urls.update(dict)		
					
	df_ips = pd.DataFrame (Data_ips, columns = ['ip','score'])
	df_domains = pd.DataFrame (Data_domains, columns = ['domain','score'])
	df_urls = pd.DataFrame (Data_urls, columns = ['url','score'])	
	print('	===> Panda Dataframes OK')		
	print('	====>De deduplicate data into dataframes =>')	
	
	df_ips.drop_duplicates(keep = 'first', inplace = True) 
	df_domains.drop_duplicates( keep = 'first', inplace = True) 
	df_urls.drop_duplicates(keep = 'first', inplace = True) 
	
	print('	=====>De duplication Done ')
	print("========================================================================================================================================")

	print('- STEP 7 : Append Dataframes into sqli databases =>')
	print("")	
	table_name2 = 'ip_addr'	
	df_ips.to_sql(table_name2, con=engine3, if_exists='replace')

	table_name2 = 'domains'	
	df_domains.to_sql(table_name2, con=engine3, if_exists='replace')

	table_name2 = 'urls'	
	df_urls.to_sql(table_name2, con=engine3, if_exists='replace')	
	print('	==> DONE all observables are into the SQLI Database')
	print()	
	print("========================================================================================================================================")	
	print()	
						
if __name__ == '__main__':
	start_time = time.time()
	main()
	print("========================================================================================================================================")	
	
	print('=================================>   ALL DONE  FOR ALL FEEDS  :-) ( They are ready to be exposed )<=================================')
	print()
	print("execution time : %s secondes ---" % (time.time() - start_time))
	#input('ENTER ANYTHING TO CLOSE THIS WINDOWS ! ')
