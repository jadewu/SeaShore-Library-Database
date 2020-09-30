from init import *
from init.pattern import check_pattern
bill = Blueprint('bill', __name__)
bill_id, req_id = 0, 0
@bill.route('/showBill', methods=['POST','GET'])
def showBill():
    # show bill
    if request.method == "POST":
        _customer = session['user']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "select bill_id, request_id from bills where bill_id = (select max(bill_id) from bills)"
        cursor.execute(sql)
        data = cursor.fetchall()
        bill_id, req_id = data[0][0], data[0][1]

        sql = "select customer_firstname, customer_lastname from customers where customer_id = %s"
        val = _customer
        cursor.execute(sql, val)
        customer_name = cursor.fetchall()[0]

        sql = "insert into receipts (holder_first_name, holder_last_name, bill_id, request_id) values (%s, %s, %s, %s)"
        val = (customer_name[0], customer_name[1], bill_id, req_id)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        print(data)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/showReceipt')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "select * from bills where bill_id = (select max(bill_id) from bills)"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('bill.html', bill_info = data[0])
