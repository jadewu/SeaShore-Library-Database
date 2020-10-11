from init import *
from init.pattern import check_pattern
confirm = Blueprint('confirm', __name__)


@confirm.route('/confirmation', methods=['POST','GET'])
def confirmation():
    type = request.args.get('type')

    if type == 'return':
        request_id = request.args.get('request_id')
        overdue = request.args.get('overdue')
        yes = "/returnRequest?request_id=" + request_id
        no = "/customerHome"
        return render_template('confirmation.html', type=type, yes=yes, no=no, overdue=int(overdue))

    elif type == 'refuse':
        request_id = request.args.get('request_id')
        book = request.args.get('book')
        yes = "/refuseRequest?request_id=" + request_id
        no = "/customerHome"
        return render_template('confirmation.html', type=type, book=book, yes=yes, no=no)

    else:
        return redirect('/')