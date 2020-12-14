from init import *
from init.pattern import check_pattern
bill = Blueprint('bill', __name__)
@bill.route('/showBill', methods=['POST','GET'])
def showBill():
    # show bill
    request_id = request.args.get('request_id')
    if request.method == "POST":
        _customer = session['user']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "select bill_id, request_id from bills where request_id = %s"
        val = request_id
        cursor.execute(sql, val)
        data = cursor.fetchall()
        print()
        bill_id, req_id = data[0][0], data[0][1]

        sql = "select customer_firstname, customer_lastname from customers where customer_id = %s"
        val = _customer
        cursor.execute(sql, val)
        customer_name = cursor.fetchall()[0]

        sql = "insert into receipts (holder_first_name, holder_last_name, bill_id) values (%s, %s, %s)"
        val = (customer_name[0], customer_name[1], bill_id)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        print(data)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(('/showReceipt?bill_id='+str(bill_id)))
    else:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "select request_start, request_stop from requests where request_id = %s"
        val = request_id
        cursor.execute(sql, val)
        request_info = cursor.fetchall()[0]

        sql = "insert into bills(bill_amount, request_id) values (datediff(%s, %s) * 0.5, %s)"
        val = (request_info[1], request_info[0], request_id)
        cursor.execute(sql, val)

        sql = "select * from bills where request_id = %s"
        val = request_id
        cursor.execute(sql, val)
        data = cursor.fetchall()
        print(data)
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('bill.html', bill_info = data[0])
