from init import *
from init.pattern import check_pattern
receipt = Blueprint('receipt', __name__)

@receipt.route('/showReceipt', methods=['POST','GET'])
def showReceipt():
    # show receipt
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.args.get('bill_id'):
        bill_id  = request.args.get('bill_id')
    else:
        request_id = request.args.get('request_id')
        sql = "select bill_id from bills where request_id = %s"
        val = (request_id)
        cursor.execute(sql, val)
        bill_id = cursor.fetchall()[0][0]

    sql = "select * from receipts where bill_id = %s"
    val = (bill_id)
    cursor.execute(sql, val)
    data = cursor.fetchall()
    print(data)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('receipt.html', receipt_info = data[0])
