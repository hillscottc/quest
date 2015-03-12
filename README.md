# About
A web application for accessing an archive of questions. 

# Technical Components
- [Django](https://docs.djangoproject.com/) and [Tastypie](https://django-tastypie.readthedocs.org/) are used to serve the Clue data. 
- The database is [PostgreSQL](http://www.postgresql.org/).
- Uses modularized Javascript components via [Node.js](http://node.js.org), built with [Browserify](http://browserify.org/). 
- The Javascript app framework is [Backbone.js](http://backbonejs.org/)


# Tech notes


## Installation

    npm install
    
Rebuild the browser.js by using the build command in the package.json. It calls browserify.
    
    npm run build    
    
## Load the database
The database is loaded from a local json file at `questproj/fixtures/clues.json`, 
provided by [srcmunge](https://github.com/hillscottc/srcmunge.git).

    $ django-admin load_clues questproj/fixtures/clues.json


