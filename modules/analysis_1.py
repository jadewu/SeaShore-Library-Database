from init import *
from init.pattern import check_pattern
import time
ana = Blueprint('ana', __name__)
@ana.route('/analysis_1', methods=['POST','GET'])
def analysis_1():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use('agg')

        con = cx_Oracle.connect(user, pw, dsn)
        cursor = con.cursor()

        # update topk frequently borrowed books in last week
        sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 7 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,4),num,c = 'blue')
        plt.ylabel('Borrowed Numbers')
        plt.title('Top 3 frequently borrowed books in a week')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0,data[0][0]+2))
        plt.savefig('static/images/top3booksInWeek.jpg')
        plt.clf()
        # update topk frequently borrowed books in last month
        sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 31 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,4),num,c = 'blue')
        plt.ylabel('Borrowed Numbers')
        plt.title('Top 3 frequently borrowed books in a month')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0,data[0][0]+2))
        plt.savefig('static/images/top3booksInMonth.jpg')
        plt.clf()
        # update topk frequently borrowed books in last 1 dat
        sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 1 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,4),num,c = 'blue')
        plt.ylabel('Borrowed Numbers')
        plt.title('Top 3 frequently borrowed books today')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0,data[0][0]+2))
        plt.savefig('static/images/top3booksInDay.jpg')
        plt.clf()


        plt.close()
        con.commit()
        cursor.close()
        con.close()

    image_name1 = "/static/images/top3booksInDay.jpg?" + str(time.time())
    image_name2 = "/static/images/top3booksInWeek.jpg?" + str(time.time())
    image_name3 = "/static/images/top3booksInMonth.jpg?" + str(time.time())
    # show three figures
    return render_template('analysis_1.html', image_name1=image_name1, image_name2=image_name2, image_name3=image_name3)