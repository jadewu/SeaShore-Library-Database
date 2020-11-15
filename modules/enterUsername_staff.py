from init import *
from init.pattern import check_pattern
enter_username_staff = Blueprint('enter_username_staff', __name__)

@enter_username_staff.route('/enterUsername_staff',methods=['POST','GET'])
def enterUsername_staff():
    if session.get('staff'):
        if request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor()
            _username = request.form['inputUsername']
            sql = "select count(*) from employees where employee_username = %s"
            cursor.execute(sql, _username)
            num = cursor.fetchall()[0][0]
            cursor.close()
            conn.close()
            if(num == 1):
                session['staff_tmp'] = _username
                return redirect('/changePassword_staff')
            else:
                flash("Username does not exist")
                return redirect('/enterUsername_staff')
        else:
            return render_template('enterUsername_staff.html')
    else:
        return redirect('/signIn_staff')