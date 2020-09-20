from flask import Flask, render_template, request, json, redirect, session, url_for, jsonify
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import html
# html.escape() can be used to avoid XSS, but because of current bootstrap,
# it is not convinient to show on original characters on html files


app = Flask(__name__)
mysql = MySQL()

app.secret_key = 'seashore-library-webpages'

# MySQL config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2020DB!!'
app.config['MYSQL_DATABASE_DB'] = 'SeaShore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
print("-----Established Database Connection-----")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    if session.get('user'):
        print(session.get('user'))
        return redirect('/customerHome')
    else:
        return redirect('/showSignIn')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signIn.html')

@app.route('/validateLogIn', methods=['POST'])
def validateLogIn():
    try:
        # print(request.url)
        # print(request.form)

        _username = request.form['inputUsername']
        _password = request.form['inputPassword']

        # connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        # customers: customer_id, c_username, c_firstname, c_lastname, c_password, timestamp
        sql = "select * from customers where c_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()

        if len(data) > 0:
            print(data[0])
            #if check_password_hash(str(data[0][4]),_password):
            if _password == data[0][4]:
                session['user'] = data[0][0] # log user into session
                return redirect('/customerHome')
            else:
                return render_template('error.html',error = 'Wrong Password.')
        else:
            return render_template('error.html',error = 'Wrong Username.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/showSignUp')
def showSignUp():
    return render_template('signUp.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        # print(request.url)
        # print(request.args)

        _username = request.form['inputUsername']
        _firstname = request.form['inputFirstname']
        _lastname = request.form['inputLastname']
        _password = request.form['inputPassword']

        if _username and _firstname and _lastname and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)

            # customers: customer_id, c_username, c_firstname, c_lastname, c_password, timestamp
            # insert information
            sql = "insert into customers (c_username, c_firstname, c_lastname, c_password) values (%s, %s, %s, %s)"
            val = (_username, _firstname, _lastname, _password)
            cursor.execute(sql, val)

            # get information
            sql = "select * from customers where c_username = %s"
            val = _username
            cursor.execute(sql, val)
            data = cursor.fetchall()

            conn.commit()
            cursor.close()
            conn.close()

            session['user'] = data[0][0]
            print(data)
            return json.dumps({'response': "user"})

        else:
            return json.dumps({'response':'Enter the required fields'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/customerHome')
def customerHome():
    if session.get('user'):
        cid = session.get('user')
        print("customer id: ", cid)

        conn = mysql.connect()
        cursor = conn.cursor()

        # customers: customer_id, c_username, c_firstname, c_lastname, c_password, timestamp

        # get customer's information
        sql = "select customer_id, c_username, c_firstname, c_lastname from customers where customer_id = %s"
        val = cid
        cursor.execute(sql, cid)
        data = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        # parameters
        user_info = {"User Name": data[0][1], "First Name": data[0][2], "Last Name": data[0][3]}
        return render_template('customerHome.html', user_info = user_info)

    else:
        return render_template('error.html', error='Unauthorized Access')


# log out current user
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
