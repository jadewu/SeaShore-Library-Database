from init import *
from init.pattern import check_pattern
import time
from datetime import date

def months(d1, d2):
    return d1.month - d2.month + 12*(d1.year - d2.year)

ana = Blueprint('ana', __name__)
@ana.route('/analysis_1', methods=['POST','GET'])
def analysis_1():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        _start = request.form['startTime1'].split('-')
        _stop = request.form['stopTime1'].split('-')
        _interval = request.form['interval1']

        today = date.today()
        start = date(int(_start[0]), int(_start[1]), int(_start[2]))
        stop = date(int(_stop[0]), int(_stop[1]), int(_stop[2]))

        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use('agg')
        con = cx_Oracle.connect(user, pw, dsn)
        cursor = con.cursor()

        if _interval == "Daily":
            # update daily data in last 10 days(top3)
            delta0 = (today - start).days
            delta1 = (today - stop).days

            max_n = 0
            colors = ['ro','bo','go']
            plt.figure(figsize=(10, 7))
            _sum = []
            print(delta1, delta0)
            for i in range(delta1, delta0+1):
                sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and " \
                      "sysdate - request_start <= :1 and sysdate - request_start >= :2 group by book_id, book_name order " \
                      "by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY "
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
                    plt.plot(delta0-i,plot_y,colors[j])
                    plt.annotate(data[j][1], (delta0-i, plot_y))
                max_n = max(max_n, sum_c)
                _sum.append(sum_c)
            _sum.reverse()
            plt.plot(range(0,delta0-delta1+1),_sum,'g--', label="top 3 sum")
            plt.legend()
            plt.ylabel('Borrowed Numbers')
            plt.title('Top borrowed books daily from ' + request.form['startTime1'] + ' to ' + request.form['stopTime1'])
            plt.xticks(range(delta0-delta1+2))
            plt.yticks(range(0, max_n + 2))
            plt.savefig('static/images/top3booksCurve.jpg')
            plt.clf()

        else:
            # update daily data in last 12 months(top3)
            delta0 = months(today, start)
            delta1 = months(today, stop)
            print(delta1, delta0)

            max_n = 0
            _sum = []
            colors = ['ro', 'bo', 'go']
            plt.figure(figsize=(10, 9))
            for i in range(delta1,delta0+1):
                sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and " \
                      "months_between(sysdate,request_start) <= :1 and months_between(sysdate,request_start) >= :2 group " \
                      "by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY "
                val = [i,i-1]
                cursor.execute(sql, val)
                data = cursor.fetchall()
                pre = -1
                counter = 0.25
                sum_c = 0
                for j in range(len(data)):
                    plot_y = data[j][0]
                    sum_c += data[j][0]
                    if pre == plot_y:
                        plot_y -= counter
                        counter += 0.25
                    else:
                        counter = 0.25
                        pre = data[j][0]
                    plt.plot(delta0-i,plot_y,colors[j])
                    plt.annotate(data[j][1], (delta0-i, plot_y))
                max_n = max(max_n, sum_c)
                _sum.append(sum_c)
            _sum.reverse()
            plt.plot(range(0,delta0-delta1+1),_sum,'g--', label="top 3 sum")
            plt.legend()
            plt.ylabel('Borrowed Numbers')
            plt.title('Top borrowed books monthly from ' + request.form['startTime1'] + ' to ' + request.form['stopTime1'])
            plt.xticks(range(delta0-delta1+2))
            plt.yticks(range(0, max_n + 2))
            # plt.savefig('static/images/top3booksCurveMonthly.jpg')
            plt.savefig('static/images/top3booksCurve.jpg')
            plt.clf()



        # plt.figure(figsize=(6, 5))
        # # update topk frequently borrowed books in last week
        # sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 7 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(len(data))
        # num = []
        # for i in range(len(data)):
        #     plt.annotate(data[i][1], (i+1, data[i][0]))
        #     num.append(int(data[i][0]))
        # plt.scatter(range(1,4),num,c = 'blue')
        # plt.ylabel('Borrowed Numbers')
        # plt.title('Top 3 frequently borrowed books in last week')
        # plt.xticks(range(0,5))
        # if len(data) > 0:
        #     plt.yticks(range(0, data[0][0] + 2))
        # else:
        #     plt.yticks(range(0, 2))
        # plt.savefig('static/images/top3booksInWeek.jpg')
        # plt.clf()
        # # update topk frequently borrowed books in last month
        # sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 31 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(len(data))
        # num = []
        # for i in range(len(data)):
        #     plt.annotate(data[i][1], (i+1, data[i][0]))
        #     num.append(int(data[i][0]))
        # plt.scatter(range(1,4),num,c = 'blue')
        # plt.ylabel('Borrowed Numbers')
        # plt.title('Top 3 frequently borrowed books in last month')
        # plt.xticks(range(0,5))
        # if len(data) > 0:
        #     plt.yticks(range(0, data[0][0] + 2))
        # else:
        #     plt.yticks(range(0, 2))
        # plt.savefig('static/images/top3booksInMonth.jpg')
        # plt.clf()
        # # update topk frequently borrowed books in last 1 day
        # sql = "select count(request_id),book_name,book_id from customer_request where request_status <> 'W' and sysdate - request_start <= 1 group by book_id, book_name order by 1 desc OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(len(data))
        # num = []
        # for i in range(len(data)):
        #     plt.annotate(data[i][1], (i+1, data[i][0]))
        #     num.append(int(data[i][0]))
        # plt.scatter(range(1,len(num)+1),num,c = 'blue')
        # plt.ylabel('Borrowed Numbers')
        # plt.title('Top 3 frequently borrowed books in last day')
        # plt.xticks(range(0,5))
        # if len(data) > 0:
        #     plt.yticks(range(0, data[0][0] + 2))
        # else:
        #     plt.yticks(range(0, 2))
        #
        # plt.savefig('static/images/top3booksInDay.jpg')
        # plt.clf()


        plt.close()
        con.commit()
        cursor.close()
        con.close()

    # image_name1 = "/static/images/top3booksInDay.jpg?" + str(time.time())
    # image_name2 = "/static/images/top3booksInWeek.jpg?" + str(time.time())
    # image_name3 = "/static/images/top3booksInMonth.jpg?" + str(time.time())
    image_name4 = "/static/images/top3booksCurve.jpg?" + str(time.time())
    # image_name5 = "/static/images/top3booksCurveMonthly.jpg?" + str(time.time())
    # show three figures
    # return render_template('analysis_1.html', image_name5=image_name5,
    #                        image_name4=image_name4)
    return render_template('analysis_1.html', image_name4=image_name4)
    # return render_template('analysis_1.html', image_name1=image_name1, image_name2=image_name2, image_name3=image_name3, image_name4=image_name4)