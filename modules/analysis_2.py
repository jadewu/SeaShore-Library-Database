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

        # update topk frequently borrowed books in last week
        sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= 7 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1] + " " + data[i][2], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,4),num,c = 'blue')
        plt.ylabel('Interaction Numbers')
        plt.title('Top 3 active users in last week')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0,data[0][0]+2))
        plt.savefig('static/images/top3usersInWeek.jpg')
        plt.clf()
        # update topk frequently borrowed books in last month
        sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= 31 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1] + " " + data[i][2], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,4),num,c = 'blue')
        plt.ylabel('Interaction Numbers')
        plt.title('Top 3 active users in last month')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0,data[0][0]+2))
        plt.savefig('static/images/top3usersInMonth.jpg')
        plt.clf()
        # update topk frequently borrowed books in last 1 dat
        sql = "select count(request_id),customer_firstname,customer_lastname,customer_id from customer_request where request_status <> 'W' and sysdate - request_start <= 1 group by customer_firstname,customer_lastname,customer_id order by 1 desc FETCH NEXT 3 ROWS ONLY"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(len(data))
        num = []
        for i in range(len(data)):
            plt.annotate(data[i][1] + " " + data[i][2], (i+1, data[i][0]))
            num.append(int(data[i][0]))
        plt.scatter(range(1,4),num,c = 'blue')
        plt.ylabel('Interaction Numbers')
        plt.title('Top 3 active users in last day')
        plt.xticks(range(0,5))
        if len(data) > 0:
            plt.yticks(range(0,data[0][0]+2))
        plt.savefig('static/images/top3usersInDay.jpg')
        plt.clf()


        plt.close()
        con.commit()
        cursor.close()
        con.close()
    image_name1 = "/static/images/top3usersInDay.jpg?" + str(time.time())
    image_name2 = "/static/images/top3usersInWeek.jpg?" + str(time.time())
    image_name3 = "/static/images/top3usersInMonth.jpg?" + str(time.time())
    # show three figures
    return render_template('analysis_2.html', image_name1=image_name1, image_name2=image_name2, image_name3=image_name3)