from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="farmeasy"

def connect():
    return mysql.connector.connect(host="localhost",database='farmeasy', user="root", passwd="")

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        connection = connect()
        userDetails = request.form
        if userDetails['active-log-panel']=='register':
            name = userDetails['name']
            email = userDetails['email']
            phone= userDetails['phone']
            addr= userDetails['addr']
            role= userDetails['role']
            cur = connection.cursor()
            cur.execute("INSERT INTO user(user_id, user_name, user_email, user_phone, user_address, user_role) VALUES(%s, %s, %s, %s, %s, %s)",(6,name, email, phone, addr, role))
            connection.commit()
            cur.close()
            return redirect('/users')
        else  :
            username = userDetails['username']
            password= userDetails['password']
            cur1 = connection.cursor()
            returnusername=cur1.execute("SELECT * FROM login ORDER BY user_id")
            print(returnusername)
            rusername=cur1.fetchall()
            loginlength=len(rusername)
            connection.commit()
            cur1.close()
            for i in range (0,loginlength):
                if username in rusername[i] and password in rusername[i] :
                    flag=0
                    break
                else :
                    flag=1
            if flag==0 :
                return redirect('/logindetails')
            else :
                return redirect ('/')        
    return render_template('index.html')

@app.route('/users')

def users():
    connection= connect()
    cur = connection.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    print(resultValue)
    userDetails = cur.fetchall()
    return render_template('users.html',userDetails=userDetails)

@app.route('/logindetails')

def login():
    connection= connect()
    cur1 = connection.cursor()
    resultValue = cur1.execute("SELECT * FROM login")
    print(resultValue)
    loginDetails = cur1.fetchall()
    return render_template('login.html',loginDetails=loginDetails)

if __name__ == '__main__':
    app.run(debug=True)