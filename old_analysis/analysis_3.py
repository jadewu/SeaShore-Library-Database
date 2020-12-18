from init import *
from init.pattern import check_pattern
import time
from datetime import date

def months(d1, d2):
    return d1.month - d2.month + 12*(d1.year - d2.year)

ana3 = Blueprint('ana3', __name__)
@ana3.route('/analysis_3', methods=['POST','GET'])
def analysis_3():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        _start = request.form['startTime3'].split('-')
        _stop = request.form['stopTime3'].split('-')
        _interval = request.form['interval3']

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
            print(delta1, delta0)

            # daily income
            plt.figure(figsize=(10, 7))
            sql = "select round(sysdate-request_start),sum(bill_amount) from customer_request where round(sysdate - request_start) <= :2 and round(sysdate - request_start) >= :1 group by round(sysdate-request_start) order by round(sysdate-request_start)"
            val = [delta0, delta1]
            cursor.execute(sql, val)
            data = cursor.fetchall()
            print(data)
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
            while counter < delta0+1:
                amounts.append(0)
                counter+=1
            amounts.reverse()
            max_index = delta0+1-max_index
            print(amounts)
            plt.plot(range(1,delta0-delta1+2),amounts,'o--', c = 'green')
            show_max = '[' + str(max_index) + ' ' + str(max_amount) + ']'
            plt.annotate(show_max, (max_index, max_amount))
            plt.ylabel('Income')
            plt.title('Daily Income')
            plt.xlabel('Days')
            plt.xticks(range(0,delta0-delta1+2))
            if len(data) > 0:
                interm = (int(max_amount) + 5) // 10
                plt.yticks(range(0,int(max_amount)+5,interm))
            else:
                plt.yticks(range(0, 2))
                plt.ylim([-0.2,1.2])
            # if(len(data) > 0):
            #     plt.ylim([0, max(data[:][0])+1])
            # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
            plt.savefig('static/images/income.jpg')

        else:
            # update daily data in last 12 months(top3)
            delta0 = months(today, start)
            delta1 = months(today, stop)
            print(delta1, delta0)

            plt.clf()
            plt.figure(figsize=(12, 5))
            sql = "select round(months_between(sysdate,request_start)),sum(bill_amount) from customer_request where round(months_between(sysdate,request_start)) <= :2 and round(months_between(sysdate,request_start)) >= :1 group by round(months_between(sysdate,request_start)) order by round(months_between(sysdate,request_start)) "
            val = [delta0, delta1]
            cursor.execute(sql, val)
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
            while counter < delta0+1:
                amounts.append(0)
                counter+=1
            amounts.reverse()
            max_index = delta0+1 - max_index
            plt.plot(range(1,delta0-delta1+2),amounts,'o--',c = 'orange')
            show_max = '[' + str(max_index) + ' ' + str(max_amount) + ']'
            plt.annotate(show_max, (max_index, max_amount))
            plt.ylabel('Income')
            plt.title('Income in a month')
            plt.xlabel('Days(in a month)')
            plt.xticks(range(0,delta0-delta1+2))
            if len(data) > 0:
                interm = (int(max_amount) + 5) // 10
                plt.yticks(range(0,int(max_amount)+5,interm))
            else:
                plt.yticks(range(0, 2))
                plt.ylim([-0.2,1.2])
            # if(len(data) > 0):
            #     plt.ylim([0, max(data[:][0])+1])
            # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
            plt.savefig('static/images/income.jpg')
        plt.close()
        con.commit()
        cursor.close()
        con.close()

    image1_name = "/static/images/income.jpg?" + str(time.time())
    # image1_name = "/static/images/incomeInWeek.jpg?" + str(time.time())
    # image2_name = "/static/images/incomeInMonth.jpg?" + str(time.time())

    # show three figures
    # return render_template('analysis_3.html', image1_name=image1_name, image2_name=image2_name)
    return render_template('analysis_3.html', image1_name=image1_name)