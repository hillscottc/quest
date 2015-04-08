# About
A web application for accessing an archive of questions with backbone and node

# Technical Components
- [Django](https://docs.djangoproject.com/) and [Tastypie](https://django-tastypie.readthedocs.org/) are used to serve the Clue data. 
- The database is [PostgreSQL](http://www.postgresql.org/).
- Uses modularized Javascript components via [Node.js](http://node.js.org), built with [Browserify](http://browserify.org/). 
- The Javascript app framework is [Backbone.js](http://backbonejs.org/)


# Tech notes


## Compile and run

    npm run build && django-admin runserver


## Installation

    npm install
    
Rebuild the browser.js by using the build command in the package.json. It calls browserify.
    
    npm run build    

        
## Init and load the database
In psql...

    drop database quest_db;
    create database quest_db WITH OWNER quest_acct ENCODING 'UTF8';
    
   
The database is loaded from a local json file at `questproj/fixtures/clues.json`, 
provided by [srcmunge](https://github.com/hillscottc/srcmunge.git).

    django-admin load_clues questproj/fixtures/clues.json


