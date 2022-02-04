# Introduction

DelibeRating is a Django web app that aims to make decision-making easier for individuals and groups trying to decide where to eat.


# Getting Started
    
1. Install project dependencies:
    $ pip install -r requirements.txt
    
2. Apply the migrations:
    $ python manage.py migrate
    
3. Install PostgreSQL, then create two databases 'deliberating' & 'deliberating_cache_table', and a user.

4. Create the cache:
    $ python manage.py createcachetable

5. Obtain a Yelp Fusion API Key.

6. Update the dev.json file according to your environment.

7. You can now, finally, run the development server with:

    $ python manage.py runserver