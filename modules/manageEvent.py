from init import *
from init.pattern import check_pattern

manage_event = Blueprint('manage_event', __name__)


@manage_event.route('/manageEvent')
def manageEvent():
    if session.get('staff'):
        conn = mysql.connect()
        cursor = conn.cursor()
        # get all events
        sql = "select event_id, event_type, start_time, stop_time from events"
        # sql = "select event_id, event_name, event_type, start_time, stop_time from events"
        cursor.execute(sql)
        data = cursor.fetchall()

        headers = ['event_id', 'event_type', 'start_time', 'stop_time']
        # headers = ['event_id', 'event_name', 'event_type', 'start_time', 'stop_time']

        conn.commit()
        cursor.close()
        conn.close()
        # parameters
        return render_template('manage_event.html', event_info=data, headers=headers)

    else:
        return redirect('/signIn_staff')
