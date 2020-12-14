from init import *
from init.pattern import check_pattern

show_events = Blueprint('show_events', __name__)


@show_events.route('/showEvents')
def showEvents():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        # get all events
        # sql = "select event_id, event_type, start_time, stop_time from events"
        sql = "select event_id, event_name, event_type, start_time, stop_time from events"
        cursor.execute(sql)
        data = cursor.fetchall()
        # headers = ['event_id', 'event_type', 'start_time', 'stop_time']
        headers = ['event_id', 'event_name', 'event_type', 'start_time', 'stop_time']

        conn.commit()
        cursor.close()
        conn.close()
        # parameters
        return render_template('show_events.html', event_info=data, headers=headers)

    else:
        return redirect('/signIn')