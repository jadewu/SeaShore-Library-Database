from init import *
from init.pattern import check_pattern
import time
ana4 = Blueprint('ana4', __name__)

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
    return (amount, len(data)-max_index, max_amount)

@ana4.route('/analysis_4', methods=['POST','GET'])
def analysis_4():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == "POST":
        import matplotlib
        import matplotlib.pyplot as plt
        # update library income in last week/month
        matplotlib.use('agg')

        con = cx_Oracle.connect(user, pw, dsn)
        cursor = con.cursor()
        sql = "select round(sysdate-start_time), event_type, count(event_id) from events where round(sysdate-start_time) <=7 group by round(sysdate-start_time), event_type order by round(sysdate-start_time)"
        cursor.execute(sql)
        odata = cursor.fetchall()

        data1 = [0 for _ in range(8)]
        data2 = [0 for _ in range(8)]
        for d in odata:
            if d[1] == 'C':
                data1[d[0]] = int(d[2])
            else:
                data2[d[0]] = int(d[2])
        amount1, max_index1, max_amount1 = plotoneline(data1)
        amount2, max_index2, max_amount2 = plotoneline(data2)
        print(max_index1, max_amount1)
        max_amount = max(max_amount1, max_amount2)

        plt.plot(range(1, 9),amount1, 'o--', color='green', label='campaign')
        plt.plot(range(1, 9), amount2, 'o--', color='orange', label='exhibition')
        show_max1 = '[' + str(max_index1) + ' ' + str(max_amount1) + ']'
        plt.annotate(show_max1, (max_index1, max_amount1))
        show_max2 = '[' + str(max_index2) + ' ' + str(max_amount2) + ']'
        plt.annotate(show_max2, (max_index2, max_amount2))
        plt.ylabel('Number of events')
        plt.title('Number of events in a week')
        plt.xlabel('Days(in a week)')
        plt.xticks(range(0,10))
        if len(data1) > 0 or len(data2) > 0:
            plt.yticks(range(0,int(max_amount)+5))
        # if(len(data) > 0):
        #     plt.ylim([0, max(data[:][0])+1])
        # plt.savefig('/Users/qiao/Documents/GitHub/SeaShore-Library-Database/top3booksInWeek.png')
        plt.legend()
        plt.savefig('static/images/eventsInWeek.jpg')

        plt.clf()
        plt.figure(figsize=(12, 5))
        sql = "select round(sysdate-start_time), event_type, count(event_id) from events where round(sysdate-start_time) <=7 group by round(sysdate-start_time), event_type order by round(sysdate-start_time)"
        cursor.execute(sql)
        odata = cursor.fetchall()

        data1 = [0 for _ in range(31)]
        data2 = [0 for _ in range(31)]
        for d in odata:
            if d[1] == 'C':
                data1[d[0]] = int(d[2])
            else:
                data2[d[0]] = int(d[2])
        amount1, max_index1, max_amount1 = plotoneline(data1)
        amount2, max_index2, max_amount2 = plotoneline(data2)
        max_amount = max(max_amount1, max_amount2)

        plt.plot(range(1, 32),amount1, 'o--', color='green', label='campaign')
        plt.plot(range(1, 32), amount2, 'o--', color='orange', label='exhibition')
        show_max1 = '[' + str(max_index1) + ' ' + str(max_amount1) + ']'
        plt.annotate(show_max1, (max_index1, max_amount1))
        show_max2 = '[' + str(max_index2) + ' ' + str(max_amount2) + ']'
        plt.annotate(show_max2, (max_index2, max_amount2))
        plt.ylabel('Number of events')
        plt.title('Number of events in a month')
        plt.xlabel('Days(in a month)')
        plt.xticks(range(0, 32, 3))
        if len(data1) > 0 or len(data2) > 0:
            plt.yticks(range(0,int(max_amount)+5))
        plt.legend()
        plt.savefig('static/images/eventsInMonth.jpg')
        plt.close()
        con.commit()
        cursor.close()
        con.close()

    image1_name = "/static/images/eventsInWeek.jpg?" + str(time.time())
    image2_name = "/static/images/eventsInMonth.jpg?" + str(time.time())

    # show three figures
    return render_template('analysis_4.html', image1_name=image1_name, image2_name=image2_name)