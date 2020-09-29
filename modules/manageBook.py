from init import *
from init.pattern import check_pattern

manage_book = Blueprint('manage_book', __name__)


@manage_book.route('/manageBook')
def manageBook():
    if session.get('staff'):
        conn = mysql.connect()
        cursor = conn.cursor()
        # get all books
        sql = "select book_id, book_name from books"
        cursor.execute(sql)
        data = cursor.fetchall()

        headers = ['book_id', 'book_name']
        conn.commit()
        cursor.close()
        conn.close()
        # parameters
        return render_template('manage_book.html', book_info=data, headers=headers)

    else:
        return redirect('/signIn_staff')