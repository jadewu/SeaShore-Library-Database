from init import *
from init.pattern import check_pattern
sign_up = Blueprint('sign_up', __name__)

@sign_up.route('/showSignUp')
def showSignUp():
    return render_template('signUp.html')

@sign_up.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        # print(request.url)
        # print(request.args)

        _username = request.form['inputUsername']
        _firstname = request.form['inputFirstname']
        _lastname = request.form['inputLastname']
        _password = request.form['inputPassword']

        if not check_pattern(_username, "str"):
            return json.dumps({'response': 'Enter valid Username'})
        if not check_pattern(_firstname, "str"):
            return json.dumps({'response': 'Enter valid First Name'})
        if not check_pattern(_lastname, "str"):
            return json.dumps({'response': 'Enter valid Last Name'})
        if not check_pattern(_password, "pwd"):
            return json.dumps({'response': 'Enter valid Password'})

        conn = mysql.connect()
        cursor = conn.cursor()
        # _hashed_password = generate_password_hash(_password)

        # customers: customer_id, customer_username, customer_firstname, customer_lastname, customer_password, timestamp

        # check whether username exists
        sql = "select customer_id from customers where customer_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        if data:
            return json.dumps({'response': "Username Exists"})

        # insert information
        sql = "insert into customers (customer_username, customer_firstname, customer_lastname, customer_password) values (%s, %s, %s, %s)"
        val = (_username, _firstname, _lastname, _password)
        cursor.execute(sql, val)

        # get information
        sql = "select customer_id from customers where customer_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        session['user'] = data[0][0]
        print(data)
        return json.dumps({'response': "success"})

    except Exception as e:
        return json.dumps({'error':str(e)})
