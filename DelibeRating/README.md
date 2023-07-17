# Introduction

DelibeRating is a Django web app that aims to make decision-making easier for individuals and groups trying to decide where to eat.


# Getting Started
    
1. Install project dependencies:
    $ pip install -r requirements.txt
    
2. Install PostgreSQL, then create a database 'deliberating', and a user ('nathanrcobb' by default) with the ability to login and create tables.

3. (Temporarily) In this database, create tables 'deliberating_cache_table' and 'app_customuser' (with 'username' primary key).

4. Apply the migrations:
    $ python manage.py migrate

5. Create the cache:
    $ python manage.py createcachetable

6. Obtain a Yelp Fusion API Key.

7. Update the dev.json file according to your environment.

8. You can now, finally, run the development server with:

    $ python manage.py runserver