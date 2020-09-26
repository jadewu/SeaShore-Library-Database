from init import *
from init.pattern import check_pattern
home_page = Blueprint('home_page', __name__)

@home_page.route('/customerHome')
def customerHome():
    if session.get('user'):
        cid = session.get('user')
        print("customer id: ", cid)

        conn = mysql.connect()
        cursor = conn.cursor()

        # customers: customer_id, customer_username, customer_firstname, customer_lastname, customer_password, timestamp

        # get customer's information
        sql = "select customer_id, customer_username, customer_firstname, customer_lastname from customers where customer_id = %s"
        val = cid
        cursor.execute(sql, cid)
        data = cursor.fetchall()

        # get customer's requests
        # book_name, status, start_time, stop_time, <LINK> -> bill, receipt

        conn.commit()
        cursor.close()
        conn.close()

        # parameters
        user_info = {"User Name": data[0][1], "First Name": data[0][2], "Last Name": data[0][3]}
        return render_template('customerHome.html', user_info = user_info)
    else:
        return render_template('signIn.html')
