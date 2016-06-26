# -*- coding: utf-8 -*-
"""
Modified Yelp API python framework based on sample code provided by Yelp
Developed for use with Foodbox application
"""

"""
Based on Yelp API v2.0 code sample, using Search API to query for businesses
by search term and location, and the Business API to query additional
information about the top results.

Please refer to http://www.yelp.com/developers/documentation for the API documentation.
This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python yelp.py --term="bars" --location="San Francisco, CA"`
"""
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import key
import oauth2
import random

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
SEARCH_NUM = 0
OFFSET = 0

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = key.consKey()
CONSUMER_SECRET = key.consSecret()
TOKEN = key.token()
TOKEN_SECRET = key.tokenSecret()



def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))
    
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    #print u'Querying {0} ...'.format(url)

    req = urllib2.Request(signed_url)
    conn = urllib2.urlopen('http://www.yelp.com')
    try:
        conn = urllib2.urlopen(signed_url, None)
        response = json.loads(conn.read())
    except urllib2.HTTPError:
            return 'Oops! Invalid input, please try again.'
    finally:
        conn.close()

    return response
    
def search(term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset':OFFSET
    }

    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']

    #print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(len(businesses),business_id)

    response = get_business(business_id)

    #print u'Result for business "{0}" found:'.format(business_id)
    #pprint.pprint(response, indent=2)


def transform(url):
    temp = url
    if(url.find('/ms') != -1):
        temp = url[:url.find('/ms')]+'/o'+url[url.find('/ms')+3:]
    return temp
    
def namer(name):
    temp = ""
    for i in range(len(name)):
        if(i==0):
            temp += name[i].upper()
        elif(name[i] == '-'):
            temp += " "
        elif(name[i-1] == '-'):
            temp+= name[i].upper()
        else:
            temp += name[i]
    return temp

def foodbox(term):
    data = {}
    num = 0
    #business = []
    if not term:
        data = search(DEFAULT_TERM, DEFAULT_LOCATION)
        num = random.randint(0,SEARCH_LIMIT-1)
    else:
        data = search(term, DEFAULT_LOCATION)
    business = data.get('businesses')
    return (business, num)

def foodboxLoc(location):
    data = {}
    num = 0
    #business = []
    if not location:
        data = search(DEFAULT_TERM, DEFAULT_LOCATION)
        num = random.randint(0,SEARCH_LIMIT-1)
    else:
        data = search(DEFAULT_TERM, location)
    business = data.get('businesses')
    return (business, num)

def createIndex():
    index = []
    while (len(index) < 5):
        new = random.randint(0,SEARCH_LIMIT-1)
        while(new in index):
            new = random.randint(0,SEARCH_LIMIT-1)
        index.append(new)
    return index

def showmemore():
    global OFFSET
    OFFSET += 20
    return OFFSET

def getData(location):
    nums = createIndex()
    data = {}
    if not location:
        data = search(DEFAULT_TERM, DEFAULT_LOCATION)
    else:
        data = search(DEFAULT_TERM, location)

    if ( isinstance(data, basestring) ):
        return ('Oops!', 'Looks like there was something wrong with your input. Please try again.')

    if not data:
        return
    else:
        businesses = data.get('businesses')
        businessNames = []
        for i in range(len(nums)):
            businessNames.append(businesses[nums[i]]['id'])
        businessData={}
        for i in range(len(nums)):
            businessData[businessNames[i]] = get_business(businessNames[i])
        return (businessData, businessNames)

def query(term, location):
    nums = createIndex()
    data = {}
    if not location:
        data = search(term, DEFAULT_LOCATION)
    elif not term:
        data = search(DEFAULT_TERM, location)
    else:
        data = search(term, location)
    businesses = data.get('businesses')
    businessNames = []
    for i in range(len(nums)):
        businessNames.append(businesses[nums[i]]['id'])
    businessData={}
    for i in range(len(nums)):
        businessData[businessNames[i]] = get_business(businessNames[i])
    return (businessData, businessNames)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()
'''
data = search(DEFAULT_TERM, DEFAULT_LOCATION)
businesses = data.get('businesses')

num = 0

name = namer(businesses[num]['id'])
rating = businesses[num]['rating']
img = transform(businesses[num]['image_url'])
genre = businesses[num]['categories'][0][0]
openorclosed = businesses[num]['is_closed']
loc = businesses[num]['location']
'''
