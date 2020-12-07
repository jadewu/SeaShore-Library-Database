from init import *
from init.pattern import check_pattern
sign_up_staff = Blueprint('sign_up_staff', __name__)

@sign_up_staff.route('/signUp_staff',methods=['POST','GET'])
def signUp_staff():
    if(request.method == 'POST'):
        _username = request.form['inputUsername']
        _firstname = request.form['inputFirstname']
        _lastname = request.form['inputLastname']
        _password = request.form['inputPassword']
        _question = request.form['inputQuestion']
        _answer = request.form['inputAnswer']
        error = ""
        if not check_pattern(_username, "str"):
            error += 'Enter valid Username; '
        if not check_pattern(_firstname, "str"):
            error += 'Enter valid First Name; '
        if not check_pattern(_lastname, "str"):
            error += 'Enter valid Last Name; '
        if not check_pattern(_password, "pwd"):
            error += 'Enter valid Password; '
        if(len(error) > 0):
            flash(error)
            return redirect('/signUp_staff')


        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)

        # customers: customer_id, customer_username, customer_firstname, customer_lastname, customer_password, timestamp

        # check whether username exists
        sql = "select employee_id from employees where employee_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        if data:
            flash("Username exists")
            return redirect('/signUp_staff')

        # insert information
        sql = "insert into employees (employee_username, employee_firstname, employee_lastname, employee_password, question, employee_answer) values (%s, %s, %s, %s, %s, %s)"
        val = (_username, _firstname, _lastname, _hashed_password, _question, _answer)
        cursor.execute(sql, val)

        # get information
        sql = "select employee_id from employees where employee_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        session['staff'] = data[0][0]
        return redirect('/signIn_staff')
    else:

        conn = mysql.connect()
        cursor = conn.cursor()

        # get questions
        sql = "select * from questions"
        cursor.execute(sql)
        questions = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('signUp_staff.html', questions = questions)
