import datetime
import json
import string

import dateparser
import dbconfig

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

DB = DBHelper()
categories = ['mugging', 'break-in']


def formate_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


def sanitize(userinput):
    whitelist = string.letters + string.digits + "!?$%,.;-'()&"
    return filter(lambda x: x in whitelist, userinput)


@app.route("/")
def home(error_message=None):
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(e)
        crimes = None
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get['userinput']
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()


@app.route('/submitcrime', methods=['POST'])
def submitecrime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = formate_date(request.form.get("date"))
    if not date:
        return home("Invalide date.Please use yyyy-mm-dd")
    try:
        longitude = float(request.form.get("longitude"))
        latitude = float(request.form.get("latitude"))
    except ValueError:
        return home()
    description = sanitize(request.form.get("description"))
    DB.add_crime(category, date, latitude, longitude, description)
    return home()


@app.route('/clear', )
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


if __name__ == '__main__':
    app.run(port=5001, debug=True)
