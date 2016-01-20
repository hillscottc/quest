# About
A web application for accessing an archive of questions. 

# Technical Components
- The database is [PostgreSQL](http://www.postgresql.org/).

# Tech notes

## Installation
        
## Init and load the database

   $ psql
    shill=# create user quest_acct with login createdb password 'XXX';
    shill=# create database quest_db with encoding 'utf8' owner quest_acct;
    $ django-admin load_samples    
    
To load the database from a json file ([srcmunge](https://github.com/hillscottc/srcmunge.git)): 

    $ django-admin load_clues temp/clues.json
