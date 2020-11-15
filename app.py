from init import *
from modules.homePage import home_page
from modules.signIn import sign_in
from modules.signUp import sign_up
from modules.resources import res
from modules.bookStorage import sto
from modules.request import req
from modules.bill import bill
from modules.receipt import receipt
from modules.reserveRoom import reserve
from modules.confirmation import confirm

from modules.signIn_staff import sign_in_staff
from modules.signUp_staff import sign_up_staff
from modules.homePage_staff import home_page_staff
from modules.manageEvent import manage_event
from modules.newEvent import new_event
from modules.manageBook import manage_book
from modules.newBook import new_book
from modules.changeInfo_staff import change_info_staff
from modules.checkRequest_staff import check_request_staff
from modules.deleteRequest_staff import delete_request_staff
from modules.changePassword_staff import change_password_staff
from modules.enterUsername_staff import enter_username_staff
from modules.enterUsername import enter_username
from modules.changePassword import change_password
from modules.newSecurityQuestion import new_security_question
from modules.analysis_1 import ana

app = Flask(__name__)
app.register_blueprint(home_page)
app.register_blueprint(sign_in)
app.register_blueprint(sign_up)
app.register_blueprint(res)
app.register_blueprint(sto)
app.register_blueprint(req)
app.register_blueprint(bill)
app.register_blueprint(receipt)
app.register_blueprint(reserve)
app.register_blueprint(confirm)
app.register_blueprint(enter_username)
app.register_blueprint(change_password)

app.register_blueprint(home_page_staff)
app.register_blueprint(sign_in_staff)
app.register_blueprint(sign_up_staff)
app.register_blueprint(manage_event)
app.register_blueprint(new_event)
app.register_blueprint(manage_book)
app.register_blueprint(new_book)
app.register_blueprint(change_info_staff)
app.register_blueprint(check_request_staff)
app.register_blueprint(delete_request_staff)
app.register_blueprint(change_password_staff)
app.register_blueprint(enter_username_staff)
app.register_blueprint(new_security_question)
app.register_blueprint(ana)

from flask import Flask, render_template, request, json, redirect, session, blueprints
from flaskext.mysql import MySQL
from flask.blueprints import Blueprint
import re
# html.escape() can be used to avoid XSS, but because of current bootstrap,
# it is not convinient to show on original characters on html files

# Customized functions in modules


app.secret_key = 'seashore-library-secrete-key'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/changeProfile')
def changeProfile():

    return render_template('signUp.html')

@app.route('/showRooms')
def showRooms():
    # show all rooms 'floor', 'postition' -> 
    return render_template('signUp.html')


# log out current user
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# log out current user
@app.route('/logout_staff')
def logout_staff():
    session.pop('staff', None)
    return redirect('/')


""" Waiting List Logic:
        Once a book returned, assume returned book re_book_sto_id

        select requests
        where book_sto_id = re_book_sto_id, status = W
        order by last_edit_time
"""
"""
    select date, beforeNoon
    where room_id = room1, date, beforeNoon
    reservations:
    input: currentdate- 9.22
            reservations: date, beforeNoon
            
    dates = [9.22,]
    beforeNoons = [1,]

    df = day_different(9.22,dates[0])   0
    x = (int)!beforeNoons[0]            0

    A[0,0,0,1,0,0]
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
