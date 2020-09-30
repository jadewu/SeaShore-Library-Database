from init import *
from init.pattern import check_pattern

check_request_staff = Blueprint('check_request_staff', __name__)

@check_request_staff.route('/checkRequest_staff', methods=['POST','GET'])
def checkRequest_staff():
    if session.get('staff'):
        conn = mysql.connect()
        cursor = conn.cursor()
        # get all requests
        sql = "select a.request_id, a.request_status, a.request_start, a.request_stop, a.book_sto_id, c.book_name from requests a join books_storage b on a.book_sto_id = b.book_sto_id join books c on c.book_id = b.book_id where a.customer_id = %s"
        val = []
        if request.args.get('id'):
            val.append(request.args.get('id'))
            session['cust_name'] = request.args.get('id')
        else:
            val.append(session['cust_name'])
        cursor.execute(sql, val)
        data = cursor.fetchall()
        # get all book names
        headers = ('request_id', 'request_status', 'request_start', 'request_stop', 'book_sto_id', 'book_name')
        conn.commit()
        cursor.close()
        conn.close()
        # parameters
        return render_template('show_requests_staff.html', request_info=data, headers=headers)

    else:
        return redirect('/signIn_staff')