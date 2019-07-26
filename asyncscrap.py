import timeit

#for scrapping
from bs4 import BeautifulSoup
# import requests
from fake_useragent import UserAgent
import grequests

# from fake_useragent import UserAgent
#date parser
from dateutil import parser as date_parser
from datetime import datetime
# mongodb
import pymongo

#other imports
import random

"""
==========================================================
"""


##---prediction part
import pickle

news_category ={0:'POLITICS',
            1:'ENTERTAINMENT',
            2:'WORLDNEWS',         
            3:'BUSINESS',          
            4:'SPORTS',            
            5:'ARTS_CULTURE',      
            6:'SCIENCE' ,           
            7:'TECH'}

doc= ["Patriots' Cardona promoted to lieutenant in Navy Joe Cardona, who has spent his entire NFL career with the Patriots balancing his football and active-duty commitments, has been promoted to the rank of lieutenant in the U.S. Navy."]

myNBmodel = pickle.load( open('myCBmodel.pkl','rb'))


def predictNewsCategory(text_doc):
    global news_category
    label = myNBmodel.predict(text_doc)
    return (news_category[label[0]])

"""====================================================="""




def clean_description(description):
    soup_description =BeautifulSoup(description,'html.parser')
    if (soup_description.find('p')==None):
        c_description = soup_description.text
    else:
        c_description = soup_description.find("p").text
    return c_description
    
def TotalNewsScrap():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    breakfastDB = myclient["breakfast"]
    breakfastDB["totalNews"].drop()

    newsCollection = breakfastDB["totalNews"]
    urls={
        "Wired":"https://www.wired.com/feed/rss",
        "Aljazeera":"https://www.aljazeera.com/xml/rss/all.xml",
        "TheGuardian":"https://www.theguardian.com/world/rss",
        "NY Times":"https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
        "Times Of India":"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "RT News":"https://www.rt.com/rss/news/",
        "onlinekhabar":"http://english.onlinekhabar.com/feed",
        "The himalayan times":"https://thehimalayantimes.com/feed/",
        "setopati":"https://setopati.net/feed",
        "espn":"https://www.espn.com/espn/rss/news",
        "skysports":"https://www.skysports.com/rss/12040",
        "sportskeeda":"https://www.sportskeeda.com/feed",
        "cbs_soccer":"https://www.cbssports.com/rss/headlines/soccer/",
        "cbs_tennis":"https://www.cbssports.com/rss/headlines/tennis/",
        "Wall Street JOurnal":"https://feeds.a.dj.com/rss/RSSWSJD.xml",
        "MIT Technology review":"https://www.technologyreview.com/topnews.rss", 
        "CNET":"https://www.cnet.com/rss/news/",
        "Tech meme":"https://www.techmeme.com/feed.xml",
        # "BBC Tech":"http://feeds.bbci.co.uk/news/technology/rss.xml"
        "NY Times":"https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "CNBC":"http://www.cnbc.com/id/19746125/device/rss/rss.xml",
        "Fortune":"http://fortune.com/feed/",
        "Yahoo News":"https://www.yahoo.com/news/rssindex",
    }

    user_agent = UserAgent()

    header ={"user-agent":user_agent.random}

    # start = timeit.timeit()
    all_requests = (grequests.get(urls[url],headers=header) for url in urls)

    responses = grequests.map(all_requests)

    # print(responses)
    for response,url in zip(responses,urls):
        try:
            # print(response)
            pagesource = response.content
            soup  = BeautifulSoup(pagesource,'xml')
            item_list = soup.find_all('item')
            for post in item_list:
                categorys=[]
                aDic={}
                title = post.find('title').text # getting title
                pubdate = post.find('pubDate').text # getting publication data
                link  = post.find('link').text    # getting link of the article
                description =  post.find('description').text
                # soup_description =BeautifulSoup(post.find('description').text,'html.parser')
                # cleaned
                category=predictNewsCategory([title+" "+clean_description(description)])
                aDic['scrapTime']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                aDic['Publisher']=url
                aDic['Title']=title
                aDic['Publish_Date'] = date_parser.parse(pubdate)
                aDic['Link'] = link
                aDic['Category']=category
                aDic['Description']=clean_description(description)
                newsCollection.insert_one(aDic)
        except Exception as e:
            print(e)
        #     pass

    # end = timeit.timeit()

    print("-------Sucess---------------")

    # print(end-start)
if __name__=="__main__":
    TotalNewsScrap()