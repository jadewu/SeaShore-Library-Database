from init import *
from init.pattern import check_pattern
req = Blueprint('req', __name__)

@req.route('/cusRequest', methods=['POST','GET'])
def cusRequest():
    if not session.get('user'):
        return render_template('signIn.html')
    _bookStoId = request.args.get('_bookStoId')
    print(_bookStoId)
    if request.method == "GET":
        return render_template('request.html', booksto_id=_bookStoId)
    else:
        _bookStoId = request.form['bookstoID']
        _customer = session['user']
        _start = request.form['reqStartDate']
        _stop = request.form['reqStopDate']
        print(_bookStoId, _customer, _start, _stop)
        if not _customer:
            return "please sign in"
        # if _start and _stop and _customer and _bookStoId:  # check all fields filled
        # MySQL ops

        conn = mysql.connect()
        cursor = conn.cursor()

        # insert request, and the trigger in request will generate bill
        sql = "insert into requests (request_status, request_start, request_stop, customer_id, book_sto_id) values (%s, %s, %s, %s, %s)"
        val = ('Y', _start, _stop, _customer, _bookStoId)
        cursor.execute(sql, val)

        sql = "SELECT LAST_INSERT_ID()"
        cursor.execute(sql)
        _id = cursor.fetchall()[0][0]

        print("here")
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/showBill?bill_id='+str(_id))




