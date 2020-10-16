from init import *
from init.pattern import check_pattern
new_event = Blueprint('new_event', __name__)

@new_event.route('/newEvent',methods=['POST','GET'])
def newEvent():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if request.method == 'POST':
        # _eventName = request.form['eventName']
        _eventType = request.form['eventType']
        _startTime = request.form['startTime']
        _stopTime = request.form['stopTime']
        error = ""
        startDate = datetime.strptime(_startTime, '%Y-%m-%d')
        stopDate = datetime.strptime(_stopTime, '%Y-%m-%d')
        # if len(_eventName) > 32:
        #     error += 'event name length should be less than 32; '
        if startDate < datetime.now():
            error += 'start time should be greater than current time'
        if startDate > stopDate:
            error += 'start time should be less than stop time'
        if len(error) > 0:
            flash(error)
            return redirect('/newEvent')

        conn = mysql.connect()
        cursor = conn.cursor()

        # insert information
        sql = "insert into events (event_type, start_time, stop_time) values (%s, %s, %s)"
        val = (_eventType, _startTime, _stopTime)
        # sql = "insert into events (event_name, event_type, start_time, stop_time) values (%s, %s, %s, %s)"
        # val = (_eventName, _eventType, _startTime, _stopTime)
        cursor.execute(sql, val)

        conn.commit()
        cursor.close()
        conn.close()
        flash('event created successfully!')
        return redirect('/manageEvent')
    else:
        return render_template('new_event.html')