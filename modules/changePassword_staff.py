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
        sql = "select employee_answer from employees where employee_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        if len(data) == 0:
            flash("Wrong username.")
            cursor.close()
            conn.close()
            return redirect('/changePassword')
        ans = data[0][0]
        if ans == _answer:
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
            question = data[0][1]
        else:
            username = session.get('staff_tmp')
            sql = "select question from employees where employee_username = %s"
            cursor.execute(sql, username)
            question = cursor.fetchall()[0][0]
            cursor.close()
            conn.close()
        return render_template('changePassword_staff.html', username=username, question=question)