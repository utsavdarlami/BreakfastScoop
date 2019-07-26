#*************************** 
#********* IMPORT **********
#*************************** 

#for flask
from flask import Flask,render_template

# for database
from flask_pymongo import PyMongo

# for scheduler

import time
import schedule
from threading import Thread
from gevent import monkey

# our news Scrapper 
# from nep_scrap import NewsScrapper 
# from totalscrap import TotalNewsScrap
from asyncscrap import TotalNewsScrap

#others
import json
import os

#    ****************************************************** 


app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/breakfast"
mongo = PyMongo(app)


#home page

""" all the routess """
@app.route("/")
def home():
    all_news              = mongo.db.totalNews.find()

    news_sports           = mongo.db.totalNews.find({"Category": "SPORTS"})
    news_tech             = mongo.db.totalNews.find({"Category": "TECH"})
    news_business         = mongo.db.totalNews.find({"Category": "BUSINESS"})
    news_worldnews        = mongo.db.totalNews.find({"Category": "WORLDNEWS"})
    news_entertainment    = mongo.db.totalNews.find({"Category": "ENTERTAINMENT"})
    news_politics         = mongo.db.totalNews.find({"Category": "POLITICS"})
    news_science          = mongo.db.totalNews.find({"Category": "SCIENCE"})
    news_arts             = mongo.db.totalNews.find({"Category": "ARTS_CULTURE"})
    #single view
    # single_sports         = mongo.db.totalNews.find_one({"Category": "SPORTS"})

    return render_template('changehome.html',
                            news_sports=news_sports[1:6],
                            news_tech=news_tech[1:6],
                            news_business=news_business[1:6],
                            news_worldnews=news_worldnews[1:6],
                            news_entertainment=news_entertainment[1:6],
                            news_politics=news_politics[1:6],
                            news_science=news_science[1:6],
                            news_arts=news_arts[1:6],
                            all_news=all_news[1:96]
                        )
#category urls
@app.route("/sports/")
def sports():
    news_list = mongo.db.totalNews.find({"Category": "SPORTS"})
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',TitleOfPage="Sports",news_list =news_list)

@app.route("/technology/")
def technology():
    news_list = mongo.db.totalNews.find({"Category": "TECH"})
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',TitleOfPage="Technology",news_list =news_list)

@app.route("/business/")
def business():
    news_list = mongo.db.totalNews.find({"Category": "BUSINESS"})
    #news_list = mongo.db.allNews.find()
    return render_template('db.html',TitleOfPage="Business",news_list =news_list)

@app.route("/worldnews/")
def worldnews():
    news_list = mongo.db.totalNews.find({"Category": "WORLDNEWS"})
    #news_list = mongo.db.allNews.find()
    return render_template('db.html',TitleOfPage="Worldnews",news_list =news_list)

@app.route("/entertainment/")
def entertainment():
    news_list = mongo.db.totalNews.find({"Category": "ENTERTAINMENT"})
    #news_list = mongo.db.allNews.find()
    return render_template('db.html',TitleOfPage="Entertainment",news_list =news_list)
@app.route("/politics/")
def politics():
    news_list = mongo.db.totalNews.find({"Category": "POLITICS"})
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',TitleOfPage="Politics",news_list =news_list)

@app.route("/science/")
def science():
    news_list = mongo.db.totalNews.find({"Category": "SCIENCE"})
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',TitleOfPage="Science",news_list =news_list)


@app.route("/arts_culture/")
def arts_culture():
    news_list = mongo.db.totalNews.find({"Category": "ARTS_CULTURE"})
    #news_list = mongo.db.allNews.find()
    return render_template('db.html',TitleOfPage="Arts And Culture",news_list =news_list)


#---end---
@app.route("/api/")
def test1():
    # static/data/test_data.json
    json_file = os.path.join(app.static_folder, 'data', 'index_all.json')
    with open(json_file) as test_file:
        data = json.loads(test_file.read())

    return render_template('index.html',data =(data))

@app.route("/nepal/")
def test2():
    news_list = mongo.db.allNews.find().sort("Publish_Date")
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',TitleOfPage="Nepal News",news_list =news_list)


"""@app.route("/api3/")
def test3():
    x = mongo.db.allNews.insert({ 
        "Publisher": "utsav times",
        "Title": "black sheepp",
        "Publish_Date": datetime.now(),
        "Link": "https:\/\/thehimalayantimes.com\/horoscopes\/sagittarius\/sagittarius-may-25-4\/",
        "Category": [" (Nov 22 - Dec 21)"],
        "Description": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    })
    return "data added"""

"""-------------------------"""
@app.route("/pre/")
def predict():
    news_list = mongo.db.filteredNews.find({"Category_Class": "ENTERTAINMENT"})
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',news_list =news_list)

"""---------s"""
@app.route("/about/")
def about():
    return "About!"


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return "No such url"

"""flask end """

"""
    app scheduler

"""

# def job():
#     print("Nep -Scrapped")
#     # NewsScrapper()
#     nep_scrap()
#     """
#         print("Running periodic task!")
#         print("Elapsed time: " + str(time.time() - start_time))
#     """

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)   
"""

## End of scheduler

"""
    
if __name__=='__main__':
    # schedule.every(2).minutes.do(job)
    # schedule.every(6).hours.do(job)

    #hours
    monkey.patch_all()

    # schedule.every(6).hours.do(TotalNewsScrap)
    # schedule.every(6).hours.do(AW_scrap)
    # schedule.every(6).hours.do(technology_scrap)
    # schedule.every(6).hours.do(sports_scrap)
    # schedule.every(6).hours.do(business_scrap)

    #minutes
    schedule.every(2).minutes.do(TotalNewsScrap)
    # schedule.every(10).minutes.do(AW_scrap)
    # schedule.every(10).minutes.do(technology_scrap)
    # schedule.every(10).minutes.do(sports_scrap)
    # schedule.every(10).minutes.do(business_scrap)



    t = Thread(target=run_schedule)
    t.start()

    app.run(port=4000,debug=True,use_reloader=False)
     