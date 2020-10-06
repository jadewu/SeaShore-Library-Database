from init import *
from init.pattern import check_pattern
receipt = Blueprint('receipt', __name__)

@receipt.route('/showReceipt', methods=['POST','GET'])
def showReceipt():
    # show receipt
    bill_id  = request.args.get('bill_id')
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "select * from receipts where bill_id = %s"
    val = bill_id
    cursor.execute(sql, val)
    data = cursor.fetchall()
    print(data)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('receipt.html', receipt_info = data[0])
