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


# our news Scrapper 
from nep_scrap import NewsScrapper 

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
    return render_template('home.html')

@app.route("/api/")
def test1():
    # static/data/test_data.json
    json_file = os.path.join(app.static_folder, 'data', 'index_all.json')
    with open(json_file) as test_file:
        data = json.loads(test_file.read())

    return render_template('index.html',data =(data))

@app.route("/api2/")
def test2():
    news_list = mongo.db.allNews.find().sort("Publish_Date")
    #news_list = mongo.db.allNews.find()

    return render_template('db.html',news_list =news_list)


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

@app.route("/api3/")
def test3():
    international_news =mongo.db.newNews.find().sort("Publish_Date")
    return render_template('db.html',news_list =international_news)


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

def job():
    print("Scrapped")
    NewsScrapper()
    """
        print("Running periodic task!")
        print("Elapsed time: " + str(time.time() - start_time))
    """

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)   
"""

## End of scheduler

"""
    
if __name__=='__main__':
    # schedule.every(2).minutes.do(job)
    schedule.every(6).hours.do(job)

    t = Thread(target=run_schedule)
    t.start()

    app.run(host="0.0.0.0",port=4000,debug=True,use_reloader=False)
     