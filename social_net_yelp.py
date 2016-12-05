# Some reused code from 15-388 Practical Data Science
# Eric Lee

# setup library imports
import io, time, json
import requests
from bs4 import BeautifulSoup
import urllib2 #import urlopen
import pandas as pd
import re

# import yelp client library
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


def authenticate(config_filepath):
    """
    Create an authenticated yelp-python client.
    Args:
        config_filepath (string): relative path (from this file) to a file with your Yelp credentials
    Returns:
        client (yelp.client.Client): authenticated instance of a yelp.Client
    """
    with io.open(config_filepath) as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
    return client

x = authenticate("config_secret_yelp.json")

def yelp_search(client, query):
    """
    Make an authenticated request to the Yelp API.
    Args:
        query (string): Search term
    Returns:
        total (integer): total number of businesses on Yelp corresponding to the query
        businesses (list): list of yelp.obj.business.Business objects
    """
    results = client.search(query)
    return (results.total,results.businesses)

num_records, data = yelp_search(x,'Pittsburgh')
print num_records
#print data


def all_restaurants(client, query):
    """
    Retrieve ALL the restaurants on Yelp for a given query.
    Args:
        query (string): Search term
    Returns:
        results (list): list of yelp.obj.business.Business objects
    """
    finallist = []
    page = 0
    results = client.search(query,category_filter="restaurants")
    #print results.total
    time.sleep(0.1)
    while len(finallist) < results.total:
        search_query = client.search(query, offset=page,limit=20,category_filter="restaurants")
        finallist += search_query.businesses 
        time.sleep(0.1) #pause between requests for 0.1 seconds
        #page += 1
        page+=len(search_query.businesses)
    return finallist
    
#data = all_restaurants(x, 'Polish Hill, Pittsburgh')
data2 = all_restaurants(x,'Oakland, Pittsburgh')
#print data2.review_count
print "Done"
def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    Args:
        data (string): String of properly formatted JSON.
    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    finalList = []
    loadedData = json.loads(data)
    for x in loadedData["businesses"]:
        finalList.append(str(x["url"]))
    return finalList

def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.
    Args:
        html (string): String of HTML corresponding to a Yelp restaurant
    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    page = urllib2.urlopen(html).read()
    root = BeautifulSoup(page,"html.parser")#,"lxml")#,"html.parser")
    finalList = []
    
    userid = root.find_all("div", class_="review review--with-sidebar")
    ratings = root.find_all("meta", itemprop="ratingValue")
    date = root.find_all("meta", itemprop="datePublished")
    #text = root.find_all("p", itemprop="description")

    for i in xrange(len(userid)):
        newdict = {}
        newdict["review_id"] = str(userid[i]["data-review-id"])
        newdict["user_id"] = str(userid[i]["data-signup-object"]).replace("user_id:","")
        newdict["rating"] = float(ratings[i+1]["content"])
        newdict["date"] = str(date[i]["content"])
        #newdict["text"] = text[i].get_text()
        finalList.append(newdict)
    
    linkNext = root.find("link",rel="next")
    if linkNext == None:
        nextPage = None
    else:
        nextPage = str(linkNext["href"])
    return (finalList,nextPage)
print "done"
bob1=parse_page("https://www.yelp.com/biz/noodlehead-pittsburgh")
bob=parse_page("http://www.yelp.com/biz/thai-house-millburn?start=60")

#### Make example pandas dataframe

df = pd.DataFrame(columns=["business_id","business_name","arg_rating","review_count","url","reviews"])
#append to df using dictionary approach
row_list = []
for i in xrange(len(data2)): #going through each business object
	dict1 = {}
	#dict1["business_id"] = data2[i].id #unicode
	#dict1["business_name"] = data2[i].name #unicode
	#dict1["arg_rating"] = data2[i].rating #float
	#dict1["review_count"] = data2[i].review_count #int 
	#dict1["url"] = data2[i].url #unicode
	re.split()
	row = ({"business_id":data2[i].id,"business_name":data2[i].name,"arg_rating":data2[i].rating,
		"review_count":data2[i].review_count,"url":data2[i].url,"reviews":0}) #add other things if needed
	dict1.update(row)
	row_list.append(dict1)
df = df.append(row_list)
