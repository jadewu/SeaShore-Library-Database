from init import *
from init.pattern import check_pattern

delete_request_staff = Blueprint('delete_request_staff', __name__)


@delete_request_staff.route('/deleteRequest_staff', methods=['GET'])
def deleteRequest_staff():
    if session.get('staff'):
        if request.args.get('id'):
            return render_template('validation_delete_request.html', request_id=request.args.get('id'))
        elif request.args.get('id_checked'):
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "delete from requests where request_id = %s"
            val = (request.args.get('id_checked'))
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            flash("Request delete successfully")
            return redirect('/checkRequest_staff')
        else:
            return redirect('/staffHome')

    else:
        return redirect('/signIn_staff')