from init import *
from init.pattern import check_pattern
new_book = Blueprint('new_book', __name__)

@new_book.route('/newBook',methods=['POST','GET'])
def newBook():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == 'POST':
        _bookname = request.form['bookName']
        _copies = request.form['copies']
        _shelfid = request.form['shelfid']
        _shelflevel = request.form['shelfLevel']
        _authorfirstname = request.form['authorFirstName']
        _authorlastname = request.form['authorLastName']
        error = ""

        if len(_bookname) > 32:
            error += 'book name length should be less than 32; '
        if int(_copies) <= 0:
            error += 'copies cannot be 0 or negative; '
        if len(_authorfirstname) > 32:
            error += 'author first name length should be less than 32; '
        if len(_authorlastname) > 32:
            error += 'author last name length should be less than 32; '
        if len(error) > 0:
            flash(error)
            return redirect('/newBook')
        conn = mysql.connect()
        cursor = conn.cursor()
        # insert information
        sql = "insert into books (book_name, author_firstname, author_lastname) values (%s, %s, %s)"
        val = (_bookname, _authorfirstname, _authorlastname)
        cursor.execute(sql, val)

        sql = "SELECT LAST_INSERT_ID()"
        cursor.execute(sql)
        book_id = cursor.fetchall()[0][0]

        # _instock = 'Y'
        _sc = 1
        # insert information
        sql = "insert into books_storage (shelf_level, book_id, shelf_id) values (%s,%s,%s)"
        val = (_sc, book_id, _shelfid)
        for i in range(int(_copies)):
            cursor.execute(sql, val)

        conn.commit()
        cursor.close()
        conn.close()
        flash('book set up successfully!')
        return redirect('/manageBook')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "select shelf_id from shelves"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('new_book.html', shelves = data)