from init import *
import collections
from init.pattern import check_pattern
reserve = Blueprint('reserve', __name__)

@reserve.route('/showRooms')
def showRooms():
    print("here")
    if not session.get('user'):
        return render_template('signIn.html')

    print("ROOMs")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "select room_id from rooms;"
    cursor.execute(sql)
    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    rooms = collections.defaultdict(list)
    for row in data:
        flr = str(row[0])[0]
        rooms[flr].append(row[0])
    print(rooms)

    return render_template('rooms.html', rooms = rooms)

@reserve.route('/showDates', methods=['POST','GET'])
def showDates():
    # show bill
    _customer = session['user']
    _roomID = request.args.get('room_id')
    _ndates = 2
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "select datediff(reservation_date, curdate()) as diff from rooms_has_reservations a " \
          "join reservations b where a.room_id = %s and a.reservation_id = b.reservation_id and 0 <= datediff(" \
          "b.reservation_date, curdate()) and datediff(b.reservation_date, curdate()) <= %s order by diff; "
    val = (_roomID, _ndates)
    cursor.execute(sql, val)
    reserved = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    dates = []
    for i in range(_ndates+1):
        dates.append([datetime.date.today() + datetime.timedelta(days=i), 1])
    for row in reserved:
        dates[row[0]][1] = 0
    print(dates)

    return render_template('reserveRoom.html', room_id = _roomID, dates = dates)

@reserve.route('/reserveRoom', methods=['POST','GET'])
def reserveRoom():
    # show bill
    _customer = session['user']
    _roomID = request.args.get('room_id')
    _date = request.args.get('date')
    conn = mysql.connect()
    cursor = conn.cursor()

    # (str_to_date('2020-10-07', '%Y-%m-%d'), 20);
    sql = "insert into reservations (reservation_date, customer_id) values (str_to_date(%s, %s), %s)"
    val = (_date, '%Y-%m-%d', _customer)
    cursor.execute(sql, val)
    print("success")

    sql = "SELECT LAST_INSERT_ID()"
    cursor.execute(sql)
    _resid = cursor.fetchall()[0][0]
    print(_resid)

    sql = "insert into rooms_has_reservations (room_id, reservation_id) values (%s, %s)"
    val = (_roomID, _resid)
    cursor.execute(sql, val)

    conn.commit()
    cursor.close()
    conn.close()

    reservation_info = {}
    reservation_info["Reservation ID"] = _resid
    reservation_info["Room ID"] = _roomID
    reservation_info["Floor"] = str(_roomID)[0]
    reservation_info["Reserved Date"] = _date


    return render_template('showReservation.html', reservation_info = reservation_info)
