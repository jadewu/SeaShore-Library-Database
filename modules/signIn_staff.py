from init import *
from init.pattern import check_pattern
sign_in_staff = Blueprint('sign_in_staff', __name__)

@sign_in_staff.route('/showSignIn_staff')
def showSignIn_staff():
    return render_template('signIn_staff.html')

@sign_in_staff.route('/signIn_staff', methods=['POST', 'GET'])
def signIn_staff():
    if(request.method == 'POST'):

        _username = request.form['inputUsername']
        _password = request.form['inputPassword']
        # connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "select * from employees where employee_username = %s"
        val = _username
        cursor.execute(sql, val)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(data) > 0 and check_password_hash(str(data[0][4]),_password):
            session['staff'] = data[0][0] # log user into session
            return redirect('/staffHome')
        else:
            flash("username or password incorrect")
            return redirect('/signIn_staff')

    else:
        return render_template('signIn_staff.html')
