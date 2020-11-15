from init import *
from init.pattern import check_pattern
change_password = Blueprint('change_password', __name__)

@change_password.route('/changePassword',methods=['POST','GET'])
def changePassword():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        _username = request.form['inputUsername']
        _answer = request.form['answer']
        _newpassword = request.form['inputPassword']
        sql = "select customer_answer from customers where customer_username = %s"
        val = _username
        cursor.execute(sql, val)
        ans = cursor.fetchall()[0][0]
        if ans == _answer:
            error = ""
            if not check_pattern(_newpassword, "pwd"):
                error += 'Enter valid new Password; '
            if len(error) > 0:
                flash(error)
                return redirect('/changePassword_staff')

            sql = "update customers set customer_password = %s where customer_username = %s"
            val = (_newpassword, _username)
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
            sql = "select customer_username,question from customers where customer_id = %s"
            cursor.execute(sql, session.get('user'))
            data = cursor.fetchall()
            username = data[0][0]
            question = data[0][1]
        else:
            username = session.get('user_tmp')
            sql = "select question from customers where customer_username = %s"
            cursor.execute(sql, username)
            question = cursor.fetchall()[0][0]
            cursor.close()
            conn.close()
        return render_template('changePassword.html', username=username, question=question)