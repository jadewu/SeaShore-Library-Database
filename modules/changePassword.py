from init import *
from init.pattern import check_pattern
change_password = Blueprint('change_password', __name__)

@change_password.route('/changePassword',methods=['POST','GET'])
def changePassword():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        _username = request.form['inputUsername']
        _oripassword = request.form['oriPassword']
        _question = request.form['inputQuestion']
        _answer = request.form['answer']
        _newpassword = request.form['inputPassword']
        sql = "select customer_password, question, customer_answer from customers where customer_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        if len(data) == 0:
            flash("Wrong username.")
            cursor.close()
            conn.close()
            return redirect('/changePassword')
        ans = data[0]
        if not check_password_hash(str(ans[0]),_oripassword):
            flash("Incorrect original password.")
            cursor.close()
            conn.close()
            return redirect('/changePassword')
        if ans[1] != _question:
            flash("Incorrect security question.")
            cursor.close()
            conn.close()
            return redirect('/changePassword')
        if ans[2] == _answer:
            error = ""
            if not check_pattern(_newpassword, "pwd"):
                error += 'Enter valid new Password; '
            if len(error) > 0:
                flash(error)
                return redirect('/changePassword_staff')

            sql = "update customers set customer_password = %s where customer_username = %s"
            val = (generate_password_hash(_newpassword), _username)
            cursor.execute(sql, val)
            flash("Password changed succesfully")
            conn.commit()
            cursor.close()
            conn.close()
            if session.get('user'):
                return redirect('/customerHome')
            else:
                session.pop('user_tmp', None)
                return redirect('/signIn')
        else:
            flash("Incorrect security question answer.")
            cursor.close()
            conn.close()
            return redirect('/changePassword')
    else:
        if session.get('user'):
            sql = "select customer_username from customers where customer_id = %s"
            cursor.execute(sql, session.get('user'))
            data = cursor.fetchall()
            username = data[0][0]
            # get questions
            sql = "select * from questions"
            cursor.execute(sql)
            questions = cursor.fetchall()
        else:
            username = session.get('user_tmp')
            # get questions
            sql = "select * from questions"
            cursor.execute(sql)
            questions = cursor.fetchall()

        cursor.close()
        conn.close()
        return render_template('changePassword.html', username=username, questions=questions)