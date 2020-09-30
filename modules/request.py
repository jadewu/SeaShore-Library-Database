from init import *
from init.pattern import check_pattern
req = Blueprint('req', __name__)
id = 0
@req.route('/showRequest/<_bookStoId>', methods=['GET'])
def showRequest(_bookStoId):
    global id
    id = _bookStoId
    return render_template('request.html', booksto_id = _bookStoId)

@req.route('/cusRequest', methods=['POST','GET'])
def cusRequest():
    _bookStoId = id
    _customer = session['user']
    _start = request.form['reqStartDate']
    _stop = request.form['reqStopDate']
    print(_bookStoId, _customer, _start, _stop)
    if not _customer:
        return "please sign in"
    if _start and _stop and _customer and _bookStoId:  # check all fields filled
        # MySQL ops

        conn = mysql.connect()
        cursor = conn.cursor()

        # insert request, and the trigger in request will generate bill
        sql = "insert into requests (request_status, request_start, request_stop, customer_id, book_sto_id) values (%s, %s, %s, %s, %s)"
        val = ('Y', _start, _stop, _customer, _bookStoId)
        cursor.execute(sql, val)

        print("here")
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/showBill')
    else:
        return redirect('/showRequest')




