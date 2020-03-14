# Extended TID ( Threat Intelligence Director )

## What is Extended TID

ETID is a Public Security Feed Aggregator which download from the INTERNET ( or any other location ) Security Feeds, parse them, clean them and finally expose them as a Web Service for FirePOWER Management Center Security Intelligence Feeds or Threat Intelligence.

Security Intelligence or TID are very easy and efficient ways to block access to thousands of malicious destinations. Just by creating blocking list

But FMC Security Intelligence Feeds or TID need that feed sources to respect a clean text format and a maximum file size. And a feed file must contain one kind of observable : IP addresses, or Domains or URLs. We can't mix kind of observables into a source feed.

ETID does this formatting Job. That means that ETID becomes the Feed Source for FMC.

ETID currently exposes 3 kind of Feeds :

- IP Addresses
- Domains
- URLs

These feeds are exposed to FMC by a embeded web server.

A characteristic of this version of ETID is that it uses SQLITE DBs for everythings we need to store ( feeds list, parsers parameter, outputs )
A reason for this is, in a next step, to make easy to embed the whole application into a FLASK or PHP web applications. And add new features based on the SQLi Database ( sorting, scoring, filtering, curation, etc...)

## Installation

Installing these script is pretty straight forward . You can just copy / and paste them into you python environment but a good practice is to run them into a python virtual environment.

### Install a Python virtual environment

	For Linux/Mac 

	python3 -m venv venv
	source bin activate

	For Windows 

	virtualenv env 
	\env\Scripts\activate.bat 

### git clone the scripts

	git clone https://github.com/pcardotatgit/Extended_TID_version_2.git
	cd Extended_TID_version_2/
	
### install needed modules

	pip install -r requirements.txt
	
## Running the scripts

### 1- Go to the <b>./files</b> directory and edit <b>feeds.txt</b>

Don't change anything in this file except the value  <b>1</b> or <b>0</b>  at the end of each lines

- 1 means : select this feed
- 0 means : ignore this feed

All these feeds had been test ( March 2020 ) and work.

<b>Remark</b> The last feed ( Toulouse black List ) is very big and takes more than 10 minutes to be parsed

### 2- Go to the <u>./scripts</u> Directory and run the <u>1_feeds_ingest_feed_list_to_feeds_db.py</u>

	#python 1_feeds_ingest_feed_list_to_feeds_db.py
	
You must do this every time you modify the <b>feeds.txt</b> file

### 3- Run the <u>2_check_feeds_db_content.py</u> for checking the content of the SQLI DB feed list

	#python 2_check_feeds_db_content.py

### 4- Download the Public Feeds. Run the <u>3_download_public_feeds.py</u> script

	#python 3_download_public_feeds.py
	
Depending on the number of feed into the feed list and their size, this operation will take several minutes to complete.

The result of this operation is the storage of the clean feed into 3 SQLI Tables. One for each kind of observables.  Observables are de duplicated into the tables.

This script is the core of the application. This is this script which update the output feeds.

You will have to run it regularly ( once a day for example ). And the best to do so is to create a batch and add this batch to the CRON JOB list.

### 5- Expose the feeds.  

This is the last step.  You must do it in order to update the feeds exposed to FMC.

You can you 2 scripts for this :

	#python 4_expose_feeds_option-1.py :  Which generate into the ./clean_feeds directory 3 singles files. One for Each Kind of Feeds
	#python 5_expose_feeds_option-2.py :  Which generate into the ./clean_feeds directory several files with a max size equal to 490KB max. Need for FMC
	
The chosen script must be runt just after the 3_download_public_feeds.py in order to make feed updates available for FMC.

### 6- And Of course don't forget to start the web server 

Run the <b>start_web_server.py</b> script located at the root of the ETID directory.

	#python start_web_server.py

The server listen on port 8888

Feeds are exposed at :  <b>http:// { ETID IP Address } /clean_feeds/{feed name }</b>

### 7- Automate Feeds updates

A good practice would be to update de the feeds periodically.  Once a day would be a good frequency.

To do so create a bash named : feed_update.sh into the Extended_TID_version_2 directory

	#!/bin/bash
	./ { path_to_etid }/Extended_TID_version_2/python 3_download_public_feeds.py
	./ { path_to_etid }/Extended_TID_version_2/python 5_expose_feeds_option-2.py

Make it executable

	chmod 777 ./{ path_to_etid }/Extended_TID_version_2/feed_update.sh
	
And then add a daily CRON job

	$ crontab -e
	
Add the following instruction

	@daily /{ path_to_etid }/Extended_TID_version_2/feed_update.sh
	
Save and close

That's it !
