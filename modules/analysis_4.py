from init import *
from init.pattern import check_pattern
import time
from datetime import date

ana4 = Blueprint('ana4', __name__)

def months(d1, d2):
    return d1.month - d2.month + 12*(d1.year - d2.year)

def plotoneline(data):
    counter = 0
    amount = []
    max_amount = 0
    max_index = 0
    print(data)
    for i in range(len(data)):
        amount.append(data[i])
        if data[i] > max_amount:
            max_index = i
            max_amount = data[i]
    amount.reverse()
    return (amount, len(data) - max_index, max_amount)


@ana4.route('/analysis_4', methods=['POST', 'GET'])
def analysis_4():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        _start = request.form['startTime4'].split('-')
        _stop = request.form['stopTime4'].split('-')
        _interval = request.form['interval4']

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

            # update library income in last week/month
            plt.figure(figsize=(10, 7))
            sql = "select round(sysdate-start_time), event_type, count(event_id) from events where round(sysdate - start_time) <= :2 and round(sysdate - start_time) >= :1 group by round(sysdate-start_time), " \
                  "event_type order by round(sysdate-start_time) "
            val = [delta0, delta1]
            cursor.execute(sql, val)
            odata = cursor.fetchall()
            print(odata)
            data1 = [0 for _ in range(delta0-delta1+1)]
            data2 = [0 for _ in range(delta0-delta1+1)]
            for d in odata:
                if d[1] == 'C':
                    data1[d[0]] = int(d[2])
                else:
                    print(d[0])
                    data2[d[0]] = int(d[2])
            amount1, max_index1, max_amount1 = plotoneline(data1)
            amount2, max_index2, max_amount2 = plotoneline(data2)
            print(max_index1, max_amount1)
            max_amount = max(max_amount1, max_amount2)

            plt.plot(range(1, delta0-delta1+2), amount1, 'o--', color='green', label='campaign')
            plt.plot(range(1, delta0-delta1+2), amount2, 'o--', color='orange', label='exhibition')
            show_max1 = '[' + str(max_index1) + ' ' + str(max_amount1) + ']'
            plt.annotate(show_max1, (max_index1, max_amount1))
            show_max2 = '[' + str(max_index2) + ' ' + str(max_amount2) + ']'
            plt.annotate(show_max2, (max_index2, max_amount2))
            plt.ylabel('Number of events')
            plt.title('Number of events')
            plt.xlabel('Days')
            plt.xticks(range(0, delta0-delta1+2))
            if len(data1) > 0 or len(data2) > 0:
                plt.yticks(range(0, int(max_amount) + 5))
            # if(len(data) > 0):
            #     plt.ylim([0, max(data[:][0])+1])
            # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
            plt.legend()
            plt.savefig('static/images/events.jpg')

        else:
            # update daily data in last 12 months(top3)
            delta0 = months(today, start)
            delta1 = months(today, stop)
            print(delta1, delta0)

            plt.clf()
            plt.figure(figsize=(12, 5))
            sql = "select round(months_between(sysdate,start_time)), event_type, count(event_id) from events where round(months_between(sysdate,start_time)) <= :2 and round(months_between(sysdate,start_time)) >= :1  group by round(months_between(sysdate,start_time)), event_type order by round(months_between(sysdate,start_time)) "
            val = [delta0, delta1]
            cursor.execute(sql, val)
            odata = cursor.fetchall()

            data1 = [0 for _ in range(delta0-delta1+1)]
            data2 = [0 for _ in range(delta0-delta1+1)]
            for d in odata:
                if d[1] == 'C':
                    data1[d[0]] = int(d[2])
                else:
                    data2[d[0]] = int(d[2])
            amount1, max_index1, max_amount1 = plotoneline(data1)
            amount2, max_index2, max_amount2 = plotoneline(data2)
            max_amount = max(max_amount1, max_amount2)

            plt.plot(range(1, delta0-delta1+2), amount1, 'o--', color='green', label='campaign')
            plt.plot(range(1, delta0-delta1+2), amount2, 'o--', color='orange', label='exhibition')
            show_max1 = '[' + str(max_index1) + ' ' + str(max_amount1) + ']'
            plt.annotate(show_max1, (max_index1, max_amount1))
            show_max2 = '[' + str(max_index2) + ' ' + str(max_amount2) + ']'
            plt.annotate(show_max2, (max_index2, max_amount2))
            plt.ylabel('Number of events')
            plt.title('Number of events')
            plt.xlabel('Months')
            plt.xticks(range(0, delta0-delta1+2))
            if len(data1) > 0 or len(data2) > 0:
                plt.yticks(range(0, int(max_amount) + 5))
            plt.legend()
            plt.savefig('static/images/events.jpg')
        plt.close()
        con.commit()
        cursor.close()
        con.close()

    # image1_name = "/static/images/eventsInWeek.jpg?" + str(time.time())
    # image2_name = "/static/images/eventsInMonth.jpg?" + str(time.time())
    image1_name = "/static/images/events.jpg?" + str(time.time())

    # show three figures
    # return render_template('analysis_4.html', image1_name=image1_name, image2_name=image2_name)
    return render_template('analysis_4.html', image1_name=image1_name)
