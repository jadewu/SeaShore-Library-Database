from init import *
from init.pattern import check_pattern

delete_user = Blueprint('delete_user', __name__)


@delete_user.route('/deleteUser', methods=['GET'])
def deleteUser():
    if session.get('staff'):
        if request.args.get('id'):
            return render_template('validation_delete_user.html', userno=request.args.get('id'))
        elif request.args.get('id_checked'):
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "delete from customers where customer_id = %s"
            val = (request.args.get('id_checked'))
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            flash("User delete successfully")
            return redirect('/staffHome')
        else:
            return redirect('/staffHome')

    else:
        return redirect('/signIn_staff')