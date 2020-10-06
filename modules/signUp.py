from init import *
from init.pattern import check_pattern
sign_up = Blueprint('sign_up', __name__)

@sign_up.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method == "GET":

        conn = mysql.connect()
        cursor = conn.cursor()

        # get questions
        sql = "select * from questions"
        cursor.execute(sql)
        questions = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('signUp.html', questions = questions)
    else:
        try:
            # print(request.url)
            # print(request.args)
            _username = request.form['inputUsername']
            _firstname = request.form['inputFirstname']
            _lastname = request.form['inputLastname']
            _question = request.form['inputQuestion']
            _password = request.form['inputPassword']
            _answer = request.form['inputAnswer']

            if not check_pattern(_username, "str"):
                return json.dumps({'response': 'Enter valid Username'})
            if not check_pattern(_firstname, "letter"):
                return json.dumps({'response': 'Enter valid First Name'})
            if not check_pattern(_lastname, "letter"):
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
            sql = "insert into customers (customer_username, customer_firstname, customer_lastname, customer_password, question, customer_answer) values (%s, %s, %s, %s, %s, %s)"
            val = (_username, _firstname, _lastname, _password, _question, _answer)
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
