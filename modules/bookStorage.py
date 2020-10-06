from init import *
from init.pattern import check_pattern

sto = Blueprint('sto', __name__)


@sto.route('/bookStorage/<_bookId>', methods=['GET'])
def bookStorage(_bookId):
    # get book id
    print(_bookId)
    conn = mysql.connect()
    cursor = conn.cursor()

    # get room info of the copy
    sql = "select a.book_sto_id, a.instock, a.shelf_id, a.shelf_level, b.room_id from books_storage a join shelves b on " \
          "a.shelf_id = b.shelf_id where a.book_id = %s order by a.book_sto_id; "
    val = _bookId
    cursor.execute(sql, val)
    sto_info_insto = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('bookStorage.html', sto_info_insto=sto_info_insto)
