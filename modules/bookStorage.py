from init import *
from init.pattern import check_pattern
sto = Blueprint('sto', __name__)


@sto.route('/bookStorage')
def bookStorage():
    # get book id
    book_id = request.args.get("id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "select * from books limit 10;"
    cursor.execute(sql)
    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    print(data)
    # 1. show all books -> <LINK> storage -> book_storages ([Link] -> request.html(get))
    #               [book_name, author_name]
    # 2. search by book name -> show all book_storages() of this book ([Link] -> request.html(get))
    return render_template('resources.html', data = data)

@res.route('/searchBook',methods=['POST','GET'])
def searchBook():
    _bookname = request.form['inputBookname']

    conn = mysql.connect()
    cursor = conn.cursor()

    # get all books whose name includes the input

    sql = "select * from books where book_name like %s limit 10;"
    val = "%" + _bookname + "%"
    cursor.execute(sql, val)
    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    print(data)
    return render_template('resources.html', data = data)

