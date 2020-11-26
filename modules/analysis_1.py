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
        # update daily data in last 10 days(top3)
        max_n = 0
        colors = ['ro','bo','go']
        plt.figure(figsize=(10, 7))
        _sum = []
        for i in range(1,11):
            sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= :1 and sysdate - request_start >= :2 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
            val = [i,i-1]
            cursor.execute(sql, val)
            data = cursor.fetchall()
            pre = -1
            counter = 0.15
            sum_c = 0
            for j in range(len(data)):
                plot_y = data[j][0]
                sum_c += data[j][0]
                if pre == plot_y:
                    plot_y -= counter
                    counter += 0.15
                else:
                    counter = 0.15
                    pre = data[j][0]
                plt.plot(11-i,plot_y,colors[j])
                plt.annotate(data[j][1], (11-i, plot_y))
                max_n = max(max_n,data[j][0])
            _sum.append(sum_c)
        _sum.reverse()
        plt.plot(range(1,11),_sum,'g--', label="top 3 sum")
        plt.legend()
        plt.ylabel('Borrowed Numbers')
        plt.title('Top borrowed books curve')
        plt.xticks(range(12),('','10 days ago','9','8','7','6','5','4','3','2','1',''))
        plt.yticks(range(0, max_n + 2))
        plt.savefig('static/images/top3booksCurve.jpg')
        plt.clf()
        plt.figure(figsize=(6, 5))
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
        plt.title('Top 3 frequently borrowed books in last week')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0, data[0][0] + 2))
        else:
            plt.yticks(range(0, 2))
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
        plt.title('Top 3 frequently borrowed books in last month')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0, data[0][0] + 2))
        else:
            plt.yticks(range(0, 2))
        plt.savefig('static/images/top3booksInMonth.jpg')
        plt.clf()
        # update topk frequently borrowed books in last 1 day
        sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 1 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,len(num)+1),num,c = 'blue')
        plt.ylabel('Borrowed Numbers')
        plt.title('Top 3 frequently borrowed books in last day')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0, data[0][0] + 2))
        else:
            plt.yticks(range(0, 2))

        plt.savefig('static/images/top3booksInDay.jpg')
        plt.clf()


        plt.close()
        con.commit()
        cursor.close()
        con.close()

    image_name1 = "/static/images/top3booksInDay.jpg?" + str(time.time())
    image_name2 = "/static/images/top3booksInWeek.jpg?" + str(time.time())
    image_name3 = "/static/images/top3booksInMonth.jpg?" + str(time.time())
    image_name4 = "/static/images/top3booksCurve.jpg?" + str(time.time())
    # show three figures
    return render_template('analysis_1.html', image_name1=image_name1, image_name2=image_name2, image_name3=image_name3, image_name4=image_name4)