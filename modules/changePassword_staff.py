from init import *
from init.pattern import check_pattern
change_password_staff = Blueprint('change_password_staff', __name__)

@change_password_staff.route('/changePassword_staff',methods=['POST','GET'])
def changePassword_staff():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        _username = request.form['inputUsername']
        _answer = request.form['answer']
        _newpassword = request.form['inputPassword']
        _oripassword = request.form['oriPassword']
        _question = request.form['inputQuestion']
        sql = "select employee_password, question, employee_answer from employees where employee_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        if len(data) == 0:
            flash("Wrong username.")
            cursor.close()
            conn.close()
            return redirect('/changePassword_staff')
        ans = data[0]
        if not check_password_hash(str(ans[0]),_oripassword):
            flash("Incorrect original password.")
            cursor.close()
            conn.close()
            return redirect('/changePassword_staff')
        if ans[1] != _question:
            flash("Incorrect security question.")
            cursor.close()
            conn.close()
            return redirect('/changePassword_staff')
        if ans[2] == _answer:
            error = ""
            if not check_pattern(_newpassword, "pwd"):
                error += 'Enter valid new Password; '
            if len(error) > 0:
                flash(error)
                return redirect('/changePassword_staff')

            sql = "update employees set employee_password = %s where employee_username = %s"
            val = (generate_password_hash(_newpassword), _username)
            cursor.execute(sql, val)
            flash("Password changed succesfully")
            conn.commit()
            cursor.close()
            conn.close()
            if session.get('staff'):
                return redirect('/staffHome')
            else:
                session.pop('staff_tmp', None)
                return redirect('/signIn_staff')
        else:
            flash("Incorrect security question answer.")
            cursor.close()
            conn.close()
            return redirect('/changePassword_staff')
    else:
        if session.get('staff'):
            sql = "select employee_username,question from employees where employee_id = %s"
            cursor.execute(sql, session.get('staff'))
            data = cursor.fetchall()
            username = data[0][0]
            # get questions
            sql = "select * from questions"
            cursor.execute(sql)
            questions = cursor.fetchall()
        else:
            username = session.get('staff_tmp')
            # get questions
            sql = "select * from questions"
            cursor.execute(sql)
            questions = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('changePassword_staff.html', username=username, questions=questions)