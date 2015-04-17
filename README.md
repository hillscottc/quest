# About
A web application for accessing an archive of questions. 

# Technical Components
- The database is [PostgreSQL](http://www.postgresql.org/).

# Tech notes

## Installation
        
## Init and load the database
In psql...

    drop database quest_db;
    create database quest_db WITH OWNER quest_acct ENCODING 'UTF8';
    
To load the database from a json file ([srcmunge](https://github.com/hillscottc/srcmunge.git)): 

    django-admin load_clues temp/clues.json


