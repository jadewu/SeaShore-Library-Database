from init import *
from init.pattern import check_pattern
ana = Blueprint('ana', __name__)
@ana.route('/analysis_1', methods=['POST','GET'])
def analysis_1():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        import matplotlib
        import matplotlib.pyplot as plt
        # update topk frequently borrowed books in last week/month/year
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "select count(a.request_id) as 'mycount', b.book_id as 'book' " \
              "from requests a inner join books_storage b on a.book_sto_id = b.book_sto_id " \
              "where CURDATE() - a.request_start <= 7 and a.request_status <> 'W' group by book order by mycount desc limit 3"
        cursor.execute(sql)
        data = cursor.fetchall()
        # get book names
        max_number = 0
        x = []
        y = []
        z = []
        for i in range(len(data)):
            sql = "select book_name from books where book_id = %s"
            val = data[i][1]
            cursor.execute(sql,val)
            name = cursor.fetchall()[0][0]
            x.append(i+1)
            y.append(data[i][0])
            z.append(name)
            max_number = max(max_number, data[i][0])
        plt.scatter(x, y)
        for i, txt in enumerate(z):
            plt.annotate(txt, (x[i], y[i]))
        plt.ylabel('Borrowed Numbers')
        plt.title('Top 3 frequently borrowed books')
        plt.xlim([0, 4])
        plt.ylim([0, max_number+1])
        # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
        plt.savefig('images/top3booksInWeek.jpg')
        plt.close()
        conn.commit()
        cursor.close()
        conn.close()


    # show three figures
    return render_template('analysis_1.html')
