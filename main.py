# -*- coding: utf-8 -*-
"""
Foodbox is a web application for recommending local food joints based in Python

@author: Alex Shan, Jonathan Yao
"""

import os
from google.appengine.ext.webapp import template
import webapp2
import cgi
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
from scrape import *
from yelp import *

import jinja2

businesses = {}
businessNames = []
i = 0
locInput = ""

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        current_dir = os.path.dirname(__file__)
        index_path = os.path.join(current_dir, 'templates', 'projectfood.html')
        self.response.write(template.render(index_path, {}))

class Foodbox(webapp2.RequestHandler):
    def post(self):
        current_dir = os.path.dirname(__file__)
        global locInput
        locInput = self.request.get('content')
        
        #dataTuple = foodbox(input)
            #search based on TERM input; type of place
        dataTuple = getData(locInput)
            #search based on LOCATION input; general location of restaurant

        global businesses
        businesses = dataTuple[0]
        global businessNames
        businessNames = dataTuple[1]
        business = businesses[businessNames[0]]
        
        #Old method of retrieving data from JSON
        #business = data.get('businesses')
        #num = random.randint(0,19)

        #BUSINESS DATA
        loc = business['location']
        city = loc['city']
        address = loc['display_address'][0]
        state = loc['state_code']
        name = namer(business['id'])
        restaurant = name[:name.find(city)-1]
        rating = float(business['rating'])
        starsImg = business['rating_img_url_large']
        img = transform(business['image_url'])
        genre = business['categories'][0][0]
        url = business['url']

        template_values = {
        'restaurant':restaurant,
        'city':city,
        'state':state,
        'stars':starsImg,
        'genre':genre,
        'img':img,
        'address':address,
        'city':city,
        'url':url
        }
        
        template = JINJA_ENVIRONMENT.get_template('result.html')
        self.response.write(template.render(template_values))

class Foodbox2(webapp2.RequestHandler):
    def get(self):
        dataTuple = getData()
        businesses = dataTuple[0]
        businessNames = dataTuple[1]

    def post(self):
            current_dir = os.path.dirname(__file__)

            global i
            if (i<4 and i>=0):
                i += 1
            else:
                i = 0

            business = businesses[businessNames[i]]

            loc = business['location']
            city = loc['city']
            address = loc['display_address'][0]
            state = loc['state_code']
            name = namer(business['id'])
            restaurant = name[:name.find(city)-1]
            rating = float(business['rating'])
            starsImg = business['rating_img_url_large']
            img = transform(business['image_url'])
            genre = business['categories'][0][0]
            url = business['url']

            template_values = {
            'restaurant':restaurant,
            'city':city,
            'state':state,
            'stars':starsImg,
            'genre':genre,
            'img':img,
            'address':address,
            'city':city,
            'url':url
            }

            template = JINJA_ENVIRONMENT.get_template('result.html')
            self.response.write(template.render(template_values))

class Foodbox3(webapp2.RequestHandler):
    def get(self):
        dataTuple = getData()
        businesses = dataTuple[0]
        businessNames = dataTuple[1]

    def post(self):
            current_dir = os.path.dirname(__file__)

            global i
            if (i<=4 and i>0):
                i -= 1
            else:
                i = 4

            business = businesses[businessNames[i]]

            loc = business['location']
            city = loc['city']
            address = loc['display_address'][0]
            state = loc['state_code']
            name = namer(business['id'])
            restaurant = name[:name.find(city)-1]
            rating = float(business['rating'])
            starsImg = business['rating_img_url_large']
            img = transform(business['image_url'])
            genre = business['categories'][0][0]
            url = business['url']

            template_values = {
            'restaurant':restaurant,
            'city':city,
            'state':state,
            'stars':starsImg,
            'genre':genre,
            'img':img,
            'address':address,
            'city':city,
            'url':url
            }

            template = JINJA_ENVIRONMENT.get_template('result.html')
            self.response.write(template.render(template_values))

class ShowMore(webapp2.RequestHandler):
    def get(self):
        dataTuple = getData()
        businesses = dataTuple[0]
        businessNames = dataTuple[1]

    def post(self):
        current_dir = os.path.dirname(__file__)
        showmemore()

        dataTuple = getData(locInput)
            #search based on LOCATION input; general location of restaurant

        global businesses
        businesses = dataTuple[0]
        global businessNames
        businessNames = dataTuple[1]
        business = businesses[businessNames[0]]
        
        #Old method of retrieving data from JSON
        #business = data.get('businesses')
        #num = random.randint(0,19)

        #BUSINESS DATA
        loc = business['location']
        city = loc['city']
        address = loc['display_address'][0]
        state = loc['state_code']
        name = namer(business['id'])
        restaurant = name[:name.find(city)-1]
        rating = float(business['rating'])
        starsImg = business['rating_img_url_large']
        img = transform(business['image_url'])
        genre = business['categories'][0][0]
        url = business['url']

        template_values = {
        'restaurant':restaurant,
        'city':city,
        'state':state,
        'stars':starsImg,
        'genre':genre,
        'img':img,
        'address':address,
        'city':city,
        'url':url
        }
        
        template = JINJA_ENVIRONMENT.get_template('result.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home', MainPage),
    ('/result', Foodbox),
    ('/next', Foodbox2),
    ('/prev', Foodbox3),
    ('/results', ShowMore)
], debug=True)