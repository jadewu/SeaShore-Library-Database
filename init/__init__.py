from flask import Flask, render_template, request, json, redirect, session, blueprints, url_for, flash
from datetime import datetime
from flaskext.mysql import MySQL
from flask.blueprints import Blueprint
import re
# html.escape() can be used to avoid XSS, but because of current bootstrap,
# it is not convinient to show on original characters on html files

# Customized functions in modules

app = Flask(__name__)
mysql = MySQL()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# MySQL config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'SeaShore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
print("-----Established Database Connection-----")
