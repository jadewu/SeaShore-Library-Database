from init import *
from init.pattern import check_pattern

wait = Blueprint('wait', __name__)


@wait.route('/showWaiting/<_bookStoId>', methods=['GET'])
def showWaiting(_bookStoId):
    # show waiting list

    return render_template('showWaiting.html', bookSto_id = _bookStoId)
