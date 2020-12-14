from init import *
from init.pattern import check_pattern
res = Blueprint('res', __name__)


@res.route('/showResources')
def showResources():
    # get TOP 10 books
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "select * from books;"
    cursor.execute(sql)
    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    print(data)
    return render_template('resources.html', data = data)

@res.route('/searchBook',methods=['POST','GET'])
def searchBook():
    _bookname = request.form['inputBookname']

    conn = mysql.connect()
    cursor = conn.cursor()

    # get all books whose name includes the input

    sql = "select * from books where book_name like %s;"
    val = "%" + _bookname + "%"
    cursor.execute(sql, val)
    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    print(data)
    return render_template('resources.html', data = data)

