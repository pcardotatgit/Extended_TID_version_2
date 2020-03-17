import sys
import sqlite3
	
def read_db(database,table,field):
	liste=[]
	with sqlite3.connect(database) as conn:
		cursor=conn.cursor()
		sql_request = "SELECT " + field + " from " + table
		try:
			cursor.execute(sql_request)
			for resultat in cursor:
				#print(resultat)		
				liste.append(resultat)
		except:
			sys.exit("couldn't read database")
	return(liste)

def main():
	print('This Script Generate for every feeds ( ip_addr, domains, urls ) output file with max size = 490 KB. Due to FMC Limitations')
	database="../bases/exposed_feeds.db"
	print('Clean IP Addresses Feed is exposed into ../clean_feeds directory')
	i = 0
	output_file='../clean_feeds/ip_addresses_'+ str(i) + '.txt'
	fa = open(output_file, "w")
	resultats = read_db(database,"ip_addr","ip")	
	size=0
	if resultats :
		for resultat in resultats:
			size = size +len(resultat[0])
			if size > 430000:
				fa.close()
				i+=1
				output_file='../clean_feeds/ip_addresses_'+ str(i) + '.txt'
				fa = open(output_file, "w")	
				size=0
			#print(resultat[0])
			fa.write(resultat[0])
			fa.write("\n")
	else:
		print('NO RESULTS IN THIS TABLE')
	fa.close()
	print('Clean Domains Feed is exposed into ../clean_feeds directory')
	i = 0
	output_file='../clean_feeds/domains_'+ str(i) + '.txt'
	fa = open(output_file, "w")
	resultats = read_db(database,"domains","domain")	
	size=0
	if resultats :
		for resultat in resultats:
			size = size +len(resultat[0])
			if size > 430000:
				fa.close()
				i+=1
				output_file='../clean_feeds/domains_'+ str(i) + '.txt'
				fa = open(output_file, "w")	
				size=0
			#print(resultat[0])
			fa.write(resultat[0])
			fa.write("\n")
	else:
		print('NO RESULTS IN THIS TABLE')
	fa.close()	
	print('Clean URLs Feeds is exposed into ../clean_feeds directory')
	i = 0
	output_file='../clean_feeds/urls_'+ str(i) + '.txt'
	fa = open(output_file, "w")
	resultats = read_db(database,"urls","url")	
	size=0
	if resultats :
		for resultat in resultats:
			size = size +len(resultat[0])
			if size > 430000:
				fa.close()
				i+=1
				output_file='../clean_feeds/urls_'+ str(i) + '.txt'
				fa = open(output_file, "w")	
				size=0
			#print(resultat[0])
			fa.write(resultat[0])
			fa.write("\n")
	else:
		print('NO RESULTS IN THIS TABLE')
	fa.close()
	
if __name__=='__main__':
	main()
	print()
	print('ALL FEEDS ARE EXPOSED')