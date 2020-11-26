from init import *
from init.pattern import check_pattern
help_ = Blueprint('help_', __name__)
@help_.route('/help', methods=['POST','GET'])
def help():
    return render_template('help.html')
