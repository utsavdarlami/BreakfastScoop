
"""

/.local/share/virtualenvs/BreakFast-vYJ3fvFQ/bin/activate

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
        

def NewsScrapper():
# start

# database

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    breakfastDB = myclient["breakfast"]
    breakfastDB["allNews"].drop()
    newsCollection = breakfastDB["allNews"]


    # scrap


    user_agent = UserAgent()

    header ={"user-agent":user_agent.random}


    urls = {
        "onlinekhabar":"http://english.onlinekhabar.com/feed",
        "the himalayan times":"https://thehimalayantimes.com/feed/",
        "setopati":"https://setopati.net/feed"
        }


    for url in urls:
        try:
            response =  requests.get(urls[url],headers = header)
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
                # cleaning the description 
                soup_description =BeautifulSoup(post.find('description').text,'html.parser')
                # cleaned
                aDic['scrapTime']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                aDic['Publisher']=url
                aDic['Title']=title
                aDic['Publish_Date'] = date_parser.parse(pubdate)
                aDic['Link'] = link
                aDic['Category']=categorys
                aDic['Description']=clean_description(description)
                # inserting in database
                newsCollection.insert_one(aDic)

        except Exception as e:
            print(e)
            pass


    myclient.close()

if __name__ == '__main__':
    NewsScrapper()