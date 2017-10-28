# NBAI - A prediction system for basketball statistics.

Step 1:
	Open up your internet browser.

Step 2:
	Go to the website http://nbai.ddns.net/


# Setup From Scratch
These instructions assume you're using Ubuntu, preferably 16.04.  If you are using another version of Ubuntu, you'll have to check the [MongoDB Docs](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to verify you are using the correct link when creating your list file when installing MongoDB.  You also need python installed on your system (python is typically packaged with Ubuntu so install may not be required).

## Setup Git

First, let's install Git, clone this repo, and cd into the correct directory:

```
sudo apt-get install git
git clone https://github.com/RyanDanielOMara/nbai.git
cd nbai
```


## Setup Server

Install virtualenv and python-pip.
```
sudo apt-get install virtualenv
sudo apt-get install python-pip
```

Create your environment, and install dependencies in this environment.
```
virtualenv env
env/bin/pip install flask
env/bin/pip install mongokit
env/bin/pip install nba_py
env/bin/pip install -I pymongo==2.8
```

Your environment should be all set.  To verify:
```
env/bin/python
>> import mongokit
>> import flask
>> import nba_py
```
If you get no errors, your environment is all set!

## Setup Database

First, let's install MongoDB (if any of these commands fail for you, they may be outdated - check the [docs](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to get the most recent installation instructions).

Import the public key used by the package management system.

`sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6`

Create a list file for MongoDB (for Ubuntu 16.04, check docs linked above if running another version).

`echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list`

Reload local package database.

`sudo apt-get update`

Install the MongoDB Package.

sudo apt-get install -y mongodb-org

Startup MongoDB (you will have to do this everytime you restart your system).

`sudo service mongod start`

Backfill the Database.
* Basic backfill
    * `./src/backfill.py`
* Extensive backfill (add missing player bios, update all player bios - takes up to 15 minutes longer)
    * `./src/backfill.py -a -u`

Your server and database should now be fully setup!

## Startup Server

After setting up both the server and database, we are ready to start the server.

Ensure that MongoDB is running, if it isn't, run:

`sudo service mongod start`


Now start the server.

`./src/server.py`

You should know be able to navigate your web browswer to the printed localhost (typically http://0.0.0.0:5000).

The NBAI site is now running locally!

## Possible error messages: 
* nba_py not found/installed
    * run `env/bin/python pip install nba_py` from the root project directory
* mongo connection error
    * Ensure that mongodb is installed
        * `sudo apt-get install mongodb-org-server` 
    * Start the Mongo service
        * `sudo service mongod start`

Once you have this, you're ready to start hosting web traffic.
