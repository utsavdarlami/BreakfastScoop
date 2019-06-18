
"""


"""

#for scrapping
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

# from fake_useragent import UserAgent
#date parser
from dateutil import parser as date_parser
from datetime import datetime
# mongodb
import pymongo

#other imports
import random

def clean_description(description):
    soup_description =BeautifulSoup(description,'html.parser')
    if (soup_description.find('p')==None):
        c_description = soup_description.text
    else:
        c_description = soup_description.find("p").text
    return c_description
 
def NewScrap(urls,dbName):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    breakfastDB = myclient["breakfast"]
    breakfastDB[dbName].drop()
    newsCollection = breakfastDB[dbName]

    user_agent = UserAgent()

    header ={"user-agent":user_agent.random}


    for url in urls:
        try:
            response =  requests.get(urls[url],headers=header)
            pagesource = response.content
            soup  = BeautifulSoup(pagesource,'xml')
            item_list = soup.find_all('item')

            for post in item_list:

                categorys=[]
                aDic={}

                title = post.find('title').text # getting title
                pubdate = post.find('pubDate').text # getting publication data
                link  = post.find('link').text    # getting link of the article

                category_list = post.find_all('category') # category list
                for category in category_list:
                    categorys.append(category.text)

                description =  post.find('description').text
                soup_description =BeautifulSoup(post.find('description').text,'html.parser')
                # cleaned
                aDic['scrapTime']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                aDic['Publisher']=url
                aDic['Title']=title
                aDic['Publish_Date'] = date_parser.parse(pubdate)
                aDic['Link'] = link
                aDic['Category']=categorys
                aDic['Description']=clean_description(description)
                newsCollection.insert_one(aDic)

        except Exception as e:
            print(e)
            pass


def AW_scrap():
    #For Wired,Aljazeera
    dbName="newNews"
    urls={
        "Wired":"https://www.wired.com/feed/rss",
        "Aljazeera":"https://www.aljazeera.com/xml/rss/all.xml",
        "TheGuardian":"https://www.theguardian.com/world/rss",
        "NY Times":"https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
        "Times Of India":"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "RT News":"https://www.rt.com/rss/news/" 
    }
     
    NewScrap(urls,dbName)
    print("AW-scrapped")

def nep_scrap():
    #for nepali news site 
    dbName="allNews"
    urls = {
        "onlinekhabar":"http://english.onlinekhabar.com/feed",
        "the himalayan times":"https://thehimalayantimes.com/feed/",
        "setopati":"https://setopati.net/feed"
    }
    NewScrap(urls,dbName)
    print("NEP-scrapped")

def sports_scrap():
    #for sports news
    dbName="sportsNews"
    urls={
        "espn":"https://www.espn.com/espn/rss/news",
        "skysports":"https://www.skysports.com/rss/12040",
        "sportskeeda":"https://www.sportskeeda.com/feed",
        "cbs_soccer":"https://www.cbssports.com/rss/headlines/soccer/",
        "cbs_tennis":"https://www.cbssports.com/rss/headlines/tennis/"
    }
    NewScrap(urls,dbName)
    print("SPORTS-scrapped")

# More need for Sports, Technology
def technology_scrap():
    dbName="technologyNews"
    urls={
        "Wall Street JOurnal":"https://feeds.a.dj.com/rss/RSSWSJD.xml",
        "MIT Technology review":"https://www.technologyreview.com/topnews.rss", 
        "CNET":"https://www.cnet.com/rss/news/",
        "Tech meme":"https://www.techmeme.com/feed.xml",
        # "BBC Tech":"http://feeds.bbci.co.uk/news/technology/rss.xml"
        "NY Times":"https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    }
    NewScrap(urls,dbName)
    print("TECHNOLOGY-scrapped")


def business_scrap():
    dbName="businessNews"
    urls={
        # "CNN Money":"http://rss.cnn.com/rss/money_topstories.rss",
        "CNBC":"http://www.cnbc.com/id/19746125/device/rss/rss.xml",
        "Fortune":"http://fortune.com/feed/",
        "Yahoo Finance":"https://finance.yahoo.com/news/rssindex" 
    }
    
    NewScrap(urls,dbName)
    print("business-scrapped")
   
