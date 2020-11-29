from init import *
from init.pattern import check_pattern
import time
ana2 = Blueprint('ana2', __name__)
@ana2.route('/analysis_2', methods=['POST','GET'])
def analysis_2():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use('agg')

        con = cx_Oracle.connect(user, pw, dsn)
        cursor = con.cursor()

        max_n = 0
        colors = ['ro', 'bo', 'go']
        plt.figure(figsize=(10, 7))
        _sum = []
        for i in range(1, 11):
            sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= :1 and sysdate - request_start >= :2 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
            val = [i, i - 1]
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
                plt.plot(11 - i, plot_y, colors[j])
                plt.annotate(data[j][1], (11 - i, plot_y))
            _sum.append(sum_c)
            max_n = max(max_n, sum_c)
        _sum.reverse()
        plt.plot(range(1, 11), _sum, 'g--', label="top 3 sum")
        plt.legend()
        plt.ylabel('Interactions number')
        plt.title('Top active users daily')
        plt.xticks(range(12), ('', '10 days ago', '9', '8', '7', '6', '5', '4', '3', '2', '1', ''))
        plt.yticks(range(0, max_n + 2))
        plt.savefig('static/images/top3usersCurve.jpg')
        plt.clf()

        # update daily data in last 12 months(top3)
        max_n = 0
        _sum = []
        plt.figure(figsize=(12, 11))
        for i in range(1, 13):
            sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and months_between(sysdate,request_start) <= :1 and months_between(sysdate,request_start) >= :2 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
            val = [i, i - 1]
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
                plt.plot(13 - i, plot_y, colors[j])
                plt.annotate(data[j][1], (13 - i, plot_y))
            max_n = max(max_n, sum_c)
            _sum.append(sum_c)
        _sum.reverse()
        plt.plot(range(1, 13), _sum, 'g--', label="top 3 sum")
        plt.legend()
        plt.ylabel('Interactions number')
        plt.title('Top active users monthly')
        plt.xticks(range(14), ('', '12 months ago', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', ''))
        plt.yticks(range(0, max_n + 2))
        plt.savefig('static/images/top3usersCurveMonthly.jpg')
        plt.clf()

        # # update topk frequently borrowed books in last week
        # sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= 7 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(len(data))
        # num = []
        # for i in range(len(data)):
        #     plt.annotate(data[i][1] + " " + data[i][2], (i+1, data[i][0]))
        #     num.append(int(data[i][0]))
        # plt.scatter(range(1,4),num,c = 'blue')
        # plt.ylabel('Interaction Numbers')
        # plt.title('Top 3 active users in last week')
        # plt.xticks(range(0,5))
        # if len(data) > 0:
        #     plt.yticks(range(0,data[0][0]+2))
        # else:
        #     plt.yticks(range(0,2))
        # plt.savefig('static/images/top3usersInWeek.jpg')
        # plt.clf()
        # # update topk frequently borrowed books in last month
        # sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= 31 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(len(data))
        # num = []
        # for i in range(len(data)):
        #     plt.annotate(data[i][1] + " " + data[i][2], (i+1, data[i][0]))
        #     num.append(int(data[i][0]))
        # plt.scatter(range(1,4),num,c = 'blue')
        # plt.ylabel('Interaction Numbers')
        # plt.title('Top 3 active users in last month')
        # plt.xticks(range(0,5))
        # if len(data) > 0:
        #     plt.yticks(range(0,data[0][0]+2))
        # plt.savefig('static/images/top3usersInMonth.jpg')
        # plt.clf()
        # # update topk frequently borrowed books in last 1 dat
        # sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= 1 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(len(data))
        # num = []
        # for i in range(len(data)):
        #     plt.annotate(data[i][1] + " " + data[i][2], (i+1, data[i][0]))
        #     num.append(int(data[i][0]))
        # plt.scatter(range(1,4),num,c = 'blue')
        # plt.ylabel('Interaction Numbers')
        # plt.title('Top 3 active users in last day')
        # plt.xticks(range(0,5))
        # if len(data) > 0:
        #     plt.yticks(range(0,data[0][0]+2))
        # plt.savefig('static/images/top3usersInDay.jpg')
        # plt.clf()
        # if len(data) > 0:
        #     plt.yticks(range(0,data[0][0]+2))
        # else:
        #     plt.yticks(range(0,2))

        plt.close()
        con.commit()
        cursor.close()
        con.close()
    # image_name1 = "/static/images/top3usersInDay.jpg?" + str(time.time())
    # image_name2 = "/static/images/top3usersInWeek.jpg?" + str(time.time())
    # image_name3 = "/static/images/top3usersInMonth.jpg?" + str(time.time())

    image_name4 = "/static/images/top3usersCurve.jpg?" + str(time.time())
    image_name5 = "/static/images/top3usersCurveMonthly.jpg?" + str(time.time())
    # show three figures
    # return render_template('analysis_2.html', image_name1=image_name1, image_name2=image_name2, image_name3=image_name3)
    return render_template('analysis_2.html', image_name5=image_name5, image_name4=image_name4)