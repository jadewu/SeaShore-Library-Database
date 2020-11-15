from init import *
from init.pattern import check_pattern
enter_username = Blueprint('enter_username', __name__)

@enter_username.route('/enterUsername',methods=['POST','GET'])
def enterUsername():
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        _username = request.form['inputUsername']
        sql = "select count(*) from customers where customer_username = %s"
        cursor.execute(sql, _username)
        num = cursor.fetchall()[0][0]
        cursor.close()
        conn.close()
        if(num == 1):
            session['user_tmp'] = _username
            return redirect('/changePassword')
        else:
            flash("Username does not exist")
            return redirect('/enterUsername')
    else:
        return render_template('enterUsername.html')