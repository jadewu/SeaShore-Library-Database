from init import *
from init.pattern import check_pattern
home_page_staff = Blueprint('home_page_staff', __name__)

@home_page_staff.route('/staffHome')
def staffHome():
    if session.get('staff'):
        conn = mysql.connect()
        cursor = conn.cursor()
        if(request.method == 'POST'):
            # get specific customer's information by first name and last name
            sql = "select customer_id, customer_username, customer_firstname, customer_lastname from customers where customer_firstname = %s and customer_lastname = %s"
            val = (request.form['cust_first_name'], request.form['cust_last_name'])
            cursor.execute(sql, val)
        else:
            # get 10 customers' information
            sql = "select customer_id, customer_username, customer_firstname, customer_lastname from customers limit 10"
            cursor.execute(sql)

        data = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()
        # parameters
        return render_template('customerHome_staff.html', user_info = data)

    else:
        return redirect('/signIn_staff')
