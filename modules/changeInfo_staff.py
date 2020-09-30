from init import *
from init.pattern import check_pattern
change_info_staff = Blueprint('change_info_staff', __name__)

@change_info_staff.route('/changeInfo_staff',methods=['POST','GET'])
def changeInfo_staff():
    if session.get('staff'):
        if(request.method == 'POST'):
            _username = request.form['inputUsername']
            _firstname = request.form['inputFirstname']
            _lastname = request.form['inputLastname']
            error = ""
            if not check_pattern(_username, "str"):
                error += 'Enter valid Username; '
            if not check_pattern(_firstname, "str"):
                error += 'Enter valid First Name; '
            if not check_pattern(_lastname, "str"):
                error += 'Enter valid Last Name; '
            if(len(error) > 0):
                flash(error)
                return redirect('/changeInfo_staff')


            conn = mysql.connect()
            cursor = conn.cursor()

            # check whether username exists
            sql = "select employee_id from employees where employee_username = %s"
            val = _username
            cursor.execute(sql, val)
            data = cursor.fetchall()
            if data:
                flash("Username exists")
                return redirect('/changeInfo_staff')

            # update information
            sql = "update employees set employee_username = %s, employee_firstname = %s, employee_lastname = %s where employee_id = %s"
            val = (_username, _firstname, _lastname, session['staff'])
            cursor.execute(sql, val)

            conn.commit()
            cursor.close()
            conn.close()
            flash("Personal information changed successfully!")
            return redirect('/staffHome')
        else:
            return render_template('changeInfo_staff.html')
    else:
        return redirect('/signIn_staff')