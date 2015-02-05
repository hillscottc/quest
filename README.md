
This is a [Django](https://docs.djangoproject.com/) application for building and managing an archive of Jeapordy quiz show 'clues'. 

Uses BeautifulSoup to scrape clue data from an external site, and custom utilities parse the data into a [Postgresql](http://www.postgresql.org/) database.

[Tastypie](https://django-tastypie.readthedocs.org/) is used to create an api interface to the data, providing the backend for other applications.

The primary interest is in using Django's ORM and Admin to manage the Clues and the api -- backend stuff. 

The client side is expected to be a Node/[Backbone.js](http://backbonejs.org/) app. 
