from init import *
from init.pattern import check_pattern
receipt = Blueprint('receipt', __name__)

@receipt.route('/showReceipt')
def showReceipt():
    # show receipt
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "select * from receipts where receipt_id = (select max(receipt_id) from receipts)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('receipt.html', receipt_info = data[0])
