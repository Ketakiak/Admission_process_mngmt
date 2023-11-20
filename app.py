from flask import Flask, redirect, url_for, request, render_template,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abhiket666'
app.config['MYSQL_DB'] = 'admission'
app.secret_key = 'loggedin'
mysql = MySQL(app)


@app.route("/")
def fun1():
    return render_template("register.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'uname' in request.form and 'pwd' in request.form:
        username = request.form['uname']
        psw = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adm_info WHERE username = % s AND psw = % s', (username, psw,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['std_id']
            session['uname'] = account['username']
            session['psw'] = account['psw']
            msg = 'Logged in successfully!'
            return render_template('info.html')
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg = msg)
    return render_template('login.html')



@app.route('/registered', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'sid' in request.form and 'sname' in request.form and 'did' in request.form and 'dname' in request.form and 'cid' in request.form and 'cname' in request.form and 'uname' in request.form and 'pwd' in request.form and 'mail' in request.form and 'fees' in request.form :
        stdid = request.form['sid']
        stdname = request.form['sname']
        deptid = request.form['did']
        deptname = request.form['dname']
        csid = request.form['cid']
        csname = request.form['cname']
        username = request.form['uname']
        password = request.form['pwd']
        email = request.form['mail']
        fees = request.form['fees']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adm_info WHERE std_id = % s', (stdid, ))
        account = cursor.fetchone()
        if account:
            msg = 'Student already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO adm_info VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (stdid,stdname,deptid,deptname,csid,csname,username, email, password,fees, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
    #return "<h3> hi {} <br/> your email id is {} </h3> <br/> <h1> {}</h1>".format(username,email, msg)

@app.route('/info', methods =['GET', 'POST'])
def info():
   # msg = ''
    if request.method == 'POST' and 'sid' in request.form:
        stdid = request.form['sid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM adm_info WHERE std_id=%s", (stdid,))
        student_details = cursor.fetchall()
        if student_details:
            stdid = request.form['sid']
            #return f"Student ID: {std_id}, Name: {std_name}, Departmrnt ID: {dept_id},Department name:{dept_name},course ID and name:{c_id},{c_name},Username:{username},Email:{email},Fees:{fees}"
            #cursor.execute("SELECT * FROM adm_info")
            #specific_row = next((row for row in student_details if row['std_id'] == stdid), None)
            #rows = cursor.fetchall()
            return render_template('get_info.html',rows = student_details)
        else:
            return "Student not found."
        





if __name__ == "__main__" :
     app.run(debug=True)