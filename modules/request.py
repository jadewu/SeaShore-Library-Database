from init import *
from init.pattern import check_pattern
req = Blueprint('req', __name__)

@req.route('/cusRequest', methods=['POST','GET'])
def cusRequest():
    if not session.get('user'):
        return render_template('signIn.html')
    _customer = session['user']
    _bookStoId = request.args.get('_bookStoId')
    print(_bookStoId)
    if request.method == "GET":
        conn = mysql.connect()
        cursor = conn.cursor()

        # check books_storage instock is 'Y' or 'N'
        sql = "select instock, last_edit from books_storage where book_sto_id = %s"
        val = (_bookStoId)
        cursor.execute(sql, val)
        instock = cursor.fetchall()[0][0]
        #last_edit = cursor.fetchall()[0][1]
        print(instock)

        # display all waiting requests for this book storage
        sql = "select request_id, request_start, customer_id from requests where (book_sto_id = %s and " \
              "request_status = 'W') order by request_id asc; "
        val = (_bookStoId)
        cursor.execute(sql, val)
        waiting_list = cursor.fetchall()

        # refresh waiting list if the book_sto is instock
        # the request which generated long ago will be removed from waiting list, i.e. status 'F'
        # if instock == 'Y':
        #     for i in range(len(waiting_list)):
        #         if waiting_list[]

        cols = ["#", "Request ID", "Request Start", "Customer ID"]

        if instock == 'N':
            # cols = ["#", "Request ID", "Request Start", "Customer ID"]

            # check whether the customer has already requested for this storage
            flg = 1
            for i in range(len(waiting_list)):
                if waiting_list[i][2] == _customer:
                    flg = 0
            if flg:
                sql = "insert into requests (request_status, customer_id, book_sto_id) values ('W', %s, %s)"
                val = (_customer, _bookStoId)
                cursor.execute(sql, val)
                sql = "select request_id, request_start, customer_id from requests where (book_sto_id = %s and " \
                      "request_status = 'W') order by request_id asc; "
                val = (_bookStoId)
                cursor.execute(sql, val)
                waiting_list = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        if instock == 'Y' and (len(waiting_list) == 0 or _customer == waiting_list[0][2]):
            if len(waiting_list) > 0:
                session['waiting_for_delete_request'] = waiting_list[0][0]
            return render_template('request.html', booksto_id=_bookStoId)
        else:
            return render_template('waitingList.html', bookSto_id=_bookStoId, cols = cols, waiting_list = waiting_list)
    else:
        _bookStoId = request.form['bookstoID']
        _stop = request.form['reqStopDate']
        print(_bookStoId, _customer, _stop)
        if not _customer:
            return "please sign in"
        # if _start and _stop and _customer and _bookStoId:  # check all fields filled
        # MySQL ops


        conn = mysql.connect()
        cursor = conn.cursor()

        # check whether there exists waiting request to be deleted (waiting_for_delete_request)
        if session.get('waiting_for_delete_request'):
            sql = "delete from requests where request_id = %s"
            val = (session['waiting_for_delete_request'])
            cursor.execute(sql, val)
            session.pop('waiting_for_delete_request', None)

        # insert request
        sql = "insert into requests (request_status, request_stop, customer_id, book_sto_id) values (%s, %s, %s, %s)"
        val = ('Y', _stop, _customer, _bookStoId)
        cursor.execute(sql, val)

        sql = "update books_storage set instock = 'N' where book_sto_id = %s"
        val = (_bookStoId)
        cursor.execute(sql, val)

        sql = "SELECT LAST_INSERT_ID()"
        cursor.execute(sql)
        _id = cursor.fetchall()[0][0]

        print("here")
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/showBill?request_id='+str(_id))

@req.route('/refuseRequest', methods=['POST', 'GET'])
def refuseRequest():
    _requestID = request.args.get('request_id')
    conn = mysql.connect()
    cursor = conn.cursor()

    # update request status from Waiting to Finished
    sql = "update requests set request_status = 'F' where request_id = %s"
    val = (_requestID)
    cursor.execute(sql, val)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/customerHome')

@req.route('/returnRequest', methods=['POST', 'GET'])
def returnRequest():
    _requestID = request.args.get('request_id')
    conn = mysql.connect()
    cursor = conn.cursor()

    # update request status from Yes to Finished
    sql = "update requests set request_status = 'F' where request_id = %s"
    val = (_requestID)
    cursor.execute(sql, val)

    # update book_storage instock from N to Y
    sql = "select book_sto_id from requests where request_id = %s"
    val = (_requestID)
    cursor.execute(sql, val)
    _bookStoID = cursor.fetchall()[0][0]
    sql = "update books_storage set instock = 'Y' where book_sto_id = %s"
    val = (_bookStoID)
    cursor.execute(sql, val)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/customerHome')