from init import *
from init.pattern import check_pattern
home_page_staff = Blueprint('home_page_staff', __name__)

@home_page_staff.route('/staffHome',methods=['POST','GET'])
def staffHome():
    if session.get('staff'):
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            # get specific customer's information by first name and last name
            sql = "select customer_id, customer_username, customer_firstname, customer_lastname from customers where customer_firstname = %s and customer_lastname = %s"
            val = (request.form['cust_first_name'], request.form['cust_last_name'])
            cursor.execute(sql, val)
        else:
            # get 10 customers' information
            sql = "select customer_id, customer_username, customer_firstname, customer_lastname from customers limit 10"
            cursor.execute(sql)

        data = cursor.fetchall()

        sql = "select employee_id, employee_username, employee_firstname, employee_lastname from employees where employee_id = %s"
        val = (session['staff'])
        cursor.execute(sql, val)
        personal_info = cursor.fetchall()

        sql = "select cust_hist_id, customer_username, customer_firstname, customer_lastname, delete_date from cust_history"
        cursor.execute(sql)
        delete_info = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()
        # parameters
        return render_template('customerHome_staff.html', user_info = data, personal_info = personal_info, delete_info=delete_info)

    else:
        return redirect('/signIn_staff')
