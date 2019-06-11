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

myNBmodel = pickle.load( open('myNBmodel.pkl','rb'))


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
        

def NewsScrapper():
# start

# database

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    breakfastDB = myclient["breakfast"]
    breakfastDB["filteredNews"].drop()
    newsCollection = breakfastDB["filteredNews"]


    # scrap


    user_agent = UserAgent()

    header ={"user-agent":user_agent.random}


    urls={
        "Wired":"https://www.wired.com/feed/rss",
        "Aljazeera":"https://www.aljazeera.com/xml/rss/all.xml",
        "TheGuardian":"https://www.theguardian.com/world/rss",
        "NY Times":"https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
    }


    for url in urls:
        try:
            response =  requests.get(urls[url],headers = header)
            pagesource = response.content
            soup  = BeautifulSoup(pagesource,'xml')
            item_list = soup.find_all('item')

            for post in item_list:

                # categorys=[]
                aDic={}

                title = post.find('title').text # getting title
                pubdate = post.find('pubDate').text # getting publication data
                link  = post.find('link').text    # getting link of the article

                # category_list = post.find_all('category') # category list
                # for category in category_list:
                #     categorys.append(category.text)

                description =  post.find('description').text
                # cleaning the description 
                # soup_description =BeautifulSoup(post.find('description').text,'html.parser')
                # cleaned
                # prediction of category
                category=predictNewsCategory([title+" "+clean_description(description)])
                #-----
                aDic['scrapTime']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                aDic['Publisher']=url
                aDic['Title']=title
                aDic['Publish_Date'] = date_parser.parse(pubdate)
                aDic['Link'] = link
                aDic['Category_Class']=category
                aDic['Description']=clean_description(description)
                # inserting in database
                newsCollection.insert_one(aDic)

        except Exception as e:
            print(e)
            pass


    myclient.close()

if __name__ == '__main__':
    NewsScrapper()

# label = myNBmodel.predict(doc)
    print(predictNewsCategory(doc))
