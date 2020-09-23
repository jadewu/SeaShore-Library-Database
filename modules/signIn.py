from init import *
from init.pattern import check_pattern
sign_in = Blueprint('sign_in', __name__)

@sign_in.route('/showSignIn')
def showSignIn():
    return render_template('signIn.html')

@sign_in.route('/signIn', methods=['POST', 'GET'])
def signIn():
    try:
        # print(request.url)
        # print(request.form)

        _username = request.form['inputUsername']
        _password = request.form['inputPassword']

        if not check_pattern(_username, "str"):
            return json.dumps({'response': 'Enter valid Username'})
        if not check_pattern(_password, "pwd"):
            return json.dumps({'response': 'Enter valid Password'})

        # connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        # customers: customer_id, customer_username, customer_firstname, customer_lastname, customer_password, timestamp
        sql = "select * from customers where customer_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(data) > 0:
            print(data[0])
            #if check_password_hash(str(data[0][4]),_password):
            if _password == data[0][4]:
                session['user'] = data[0][0] # log user into session
                return json.dumps({'response': "success"})
            else:
                return json.dumps({'response': "Wrong Password"})
        else:
            return json.dumps({'response': "Wrong Username"})

    except Exception as e:
        return json.dumps({'response': str(e)})
