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
        cursor.execute(sql, val)
        data = cursor.fetchall()

        # get customer's requests
        sql = "select a.request_id, request_status, request_start, request_stop, a.book_sto_id, book_name, " \
              "bill_id from requests a join books_storage b join books c join bills d where a.customer_id = %s and " \
              "a.book_sto_id = b.book_sto_id and b.book_id = c.book_id and a.request_id = d.request_id "
        val = cid
        cursor.execute(sql, val)
        cols = (("ID", "Status", "Start", "Stop", "Book Storage ID", "Book Name", "Receipt", "Operation"))
        requests = cursor.fetchall()

        sql = "select bill_id from bills"

        conn.commit()
        cursor.close()
        conn.close()
        print(requests)
        # parameters
        user_info = {"User Name": data[0][1], "First Name": data[0][2], "Last Name": data[0][3]}
        return render_template('customerHome.html', user_info=user_info, requests=requests, cols=cols)
    else:
        return redirect('/signIn')
