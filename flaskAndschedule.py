# -*- coding: utf-8 -*-
"""
        Another example is:

        0 */12 * * * sudo python /var/www/PythonProgramming/PythonProgramming/user-data-tracking.py

        The above cron job runs every 12 hours. Another version of this cron is:

"""



"""
This script is a simple example you can use to schedule task with flask 
microframework and schedule (https://github.com/dbader/schedule).
I've found it on on stackoverflow!
"""

import time
import schedule

from flask import Flask, request
from threading import Thread


#n
from nep_scrap import NewsScrapper 

app = Flask(__name__)

start_time = time.time()

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

@app.route('/', methods=['GET'])
def index():
    return '<html>test</html>'

if __name__ == '__main__':
    schedule.every(90).seconds.do(job)
#     schedule.every(6).hours.do(job)

    t = Thread(target=run_schedule)
    t.start()
#     print("Start time: " + str(start_time))
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)