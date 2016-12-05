import pandas as pd
from urlparse import urlparse
import urllib2
from bs4 import BeautifulSoup
import time
###read in pickle file
df = pd.read_pickle("yelp2.pkl")

### fill in reviews column

def get_all_reviews(url,finallist):
	finalList = []
	review = parse_page(url)[0]
	nextt = parse_page(url)[1]
	if nextt == None: #no more reviews
		#print parse_page(url)[0]
		#return parse_page(url)[0]
		finallist+=review
		#print finallist
		#print len(finallist)
		x = finallist
		return x
	else:
		print "next page"
		finallist+=review
		get_all_reviews(nextt,finallist)
	return finallist

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
#bob1=parse_page("https://www.yelp.com/biz/noodlehead-pittsburgh")
#bob=parse_page("http://www.yelp.com/biz/thai-house-millburn?start=60")
df["reviews"] = df["reviews"].astype(object)
start_time = time.time()
print start_time
for i in xrange(30,len(df)):
	url = df["url"][i]
	#x = urlparse(str(url))
	#clean_url = x.scheme+"://"+x.netloc+x.path
	print("# "+str(i+30)+" is Done. "+str(len(df)-i-30)+" left to go.")
	df.set_value(i,"reviews", get_all_reviews(url,[]))
	elapsed_time = time.time() - start_time
	print elapsed_time
print "ALL DONE SAVE PLS."
