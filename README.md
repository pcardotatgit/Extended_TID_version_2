# Extended TID ( Threat Intelligence Director )

## What is Extended TID

ETID is a Public Security Feed Aggregator which download from the INTERNET ( or any other location ) Security Feeds, parse them, clean them and finally expose them as a Web Service for FirePOWER Management Center Security Intelligence Feeds or Threat Intelligence.

Security Intelligence or TID are very easy and efficient ways to block access to thousands of malicious destinations. Just by creating blocking list

But FMC Security Intelligence Feeds or TID need that feed sources respect a clean text format and a maximum file size.

ETID does this formatting Job. That means that ETID becomes the Feed Source for FMC.

ETID currently exposes 3 kind of Feeds :

- IP Addresses
- Domains
- URLs

These feeds are exposed to FMC by a embeded web server.

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

	git clone https://github.com/pcardotatgit/FDM_Add_Security_Rules.git
	cd FDM_Add_Security_Rules/
