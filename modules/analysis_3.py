from init import *
from init.pattern import check_pattern
import time
ana3 = Blueprint('ana3', __name__)
@ana3.route('/analysis_3', methods=['POST','GET'])
def analysis_3():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use('agg')
        # update library income in last week/month
        plt.figure(figsize=(10, 7))
        con = cx_Oracle.connect(user, pw, dsn)
        cursor = con.cursor()
        sql = "select round(sysdate-request_start),sum(bill_amount) from customer_request where sysdate - request_start <= 7 group by round(sysdate-request_start) order by round(sysdate-request_start)"
        cursor.execute(sql)
        data = cursor.fetchall()
        max_amount = 0
        amounts = []
        counter = 0
        max_index = 0
        for i in range(len(data)):
            while(data[i][0]>counter):
                amounts.append(0)
                counter+=1
            if int(data[i][1]) > max_amount:
                max_amount = int(data[i][1])
                max_index = counter
            amounts.append(data[i][1])
            counter+=1
        while counter < 8:
            amounts.append(0)
            counter+=1
        amounts.reverse()
        max_index = 8-max_index
        plt.plot(range(1,9),amounts,'o--', c = 'green')
        show_max = '[' + str(max_index) + ' ' + str(max_amount) + ']'
        plt.annotate(show_max, (max_index, max_amount))
        plt.ylabel('Income')
        plt.title('Income in a week')
        plt.xlabel('Days(in a week)')
        plt.xticks(range(0,10))
        if len(data) > 0:
            interm = (int(max_amount) + 5) // 10
            plt.yticks(range(0,int(max_amount)+5,interm))
        else:
            plt.yticks(range(0, 2))
            plt.ylim([-0.2,1.2])
        # if(len(data) > 0):
        #     plt.ylim([0, max(data[:][0])+1])
        # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
        plt.savefig('static/images/incomeInWeek.jpg')

        plt.clf()
        plt.figure(figsize=(12, 5))
        sql = "select round(sysdate-request_start),sum(bill_amount) from customer_request where sysdate - " \
              "request_start <= 30 group by round(sysdate-request_start) order by round(sysdate-request_start) "
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        num = []
        max_amount = 0
        amounts = []
        counter = 0
        max_index = 0
        for i in range(len(data)):
            while(data[i][0]>counter):
                amounts.append(0)
                counter+=1
            if int(data[i][1]) > max_amount:
                max_amount = int(data[i][1])
                max_index = counter
            amounts.append(data[i][1])
            counter+=1
        while counter < 31:
            amounts.append(0)
            counter+=1
        amounts.reverse()
        max_index = 31 - max_index
        plt.plot(range(1,32),amounts,'o--',c = 'orange')
        show_max = '[' + str(max_index) + ' ' + str(max_amount) + ']'
        plt.annotate(show_max, (max_index, max_amount))
        plt.ylabel('Income')
        plt.title('Income in a month')
        plt.xlabel('Days(in a month)')
        plt.xticks(range(0,32, 3))
        if len(data) > 0:
            interm = (int(max_amount) + 5) // 10
            plt.yticks(range(0,int(max_amount)+5,interm))
        else:
            plt.yticks(range(0, 2))
            plt.ylim([-0.2,1.2])
        # if(len(data) > 0):
        #     plt.ylim([0, max(data[:][0])+1])
        # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
        plt.savefig('static/images/incomeInMonth.jpg')
        plt.close()
        con.commit()
        cursor.close()
        con.close()

    image1_name = "/static/images/incomeInWeek.jpg?" + str(time.time())
    image2_name = "/static/images/incomeInMonth.jpg?" + str(time.time())

    # show three figures
    return render_template('analysis_3.html', image1_name=image1_name, image2_name=image2_name)