from init import *
from init.pattern import check_pattern
new_security_question = Blueprint('new_security_question', __name__)

@new_security_question.route('/newSecurityQuestion',methods=['POST','GET'])
def newSecurityQuestion():
    if not session.get('staff'):
        return redirect('/signIn_staff')
    if(request.method == 'POST'):
        _question = request.form['question']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "insert into questions(question) values(%s)"
        cursor.execute(sql, _question)
        conn.commit()
        cursor.close()
        conn.close()
        flash("New security question added successfully.")
        return redirect('/newSecurityQuestion')
    else:
        return render_template('newSecurityQuestion.html')