# -*- coding: utf-8 -*-
"""
Basic Yelp website scraper using urllib & BeautifulSoup
Created on Sun Jun 14 20:31:13 2015
"""

from urllib import *
from bs4 import BeautifulSoup
#import re
from threading import Thread
''' 
#List of Yelp URL's to scrape
url=['http://www.yelp.com/biz/yiassoo-cupertino', 'http://www.yelp.com/biz/philz-coffee-cupertino', 'http://www.yelp.com/biz/ikes-lair-cupertino-2', 'http://www.yelp.com/biz/caffe-macs-cupertino-3']
'''
#Scraping function
def scrape(ur):
 
          html = urlopen(ur).read()
          soup = BeautifulSoup(html)
          title = soup.find('h1',itemprop="name")
          '''
          reviewNum = soup.find('span',itemprop="reviewCount")
          reviewNum.append(" Reviews")
          saddress = soup.find('span',itemprop="streetAddress")
          postalcode = soup.find('span',itemprop="postalCode")
          print(reviewNum.text)
          print (saddress.text)
          print (postalcode.text)
          print ("-------------------")
          '''
          return title.text

'''
threadlist = []
#making threads
while i<len(url):
          t = Thread(target=scrape,args=(url[i],))
          t.start()
          threadlist.append(t)
          i=i+1
 
for b in threadlist:
          b.join()
'''
