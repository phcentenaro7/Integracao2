from flask import Flask, send_file, url_for, request, render_template, redirect, abort
import mysql.connector
import redis

application = Flask(__name__)
usersDB = mysql.connector.connect(user='admin', password='admin', database='server')
activeUsersDB = redis.Redis(host='localhost', port=6379, decode_responses=True)

@application.route('/', methods=['GET'])
def serveMainPage():
    return render_template('index.html')

@application.route('/verify', methods=['GET', 'POST'])
def verifyLogin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['senha']
        userIP = request.remote_addr

        if activeUsersDB.exists(userIP) > 0:
            return redirect(url_for('sayHello', userIP=userIP))
        
        cursor = usersDB.cursor(buffered=True, dictionary=True)
        query = ("SELECT * FROM users "
                 "WHERE (username=%s OR email=%s) AND password=%s")
        cursor.execute(query, (login, login, password))
        if cursor.rowcount > 0:
            activeUsersDB.lpush(userIP, str(0))
            activeUsersDB.lpush(userIP, login)
            activeUsersDB.expire(userIP, 60)
            cursor.close()
            return redirect(url_for('sayHello', userIP=userIP))
        cursor.close()
        return redirect('/')
    
@application.route('/remaining_time/<userIP>', methods=['GET'])
def getRemainingTime(userIP):
    if activeUsersDB.exists(userIP) > 0:
        return str(activeUsersDB.ttl(userIP))
    return str(0)

@application.route('/hello_world/<userIP>', methods=['GET', 'POST'])
def sayHello(userIP):
    if userIP != request.remote_addr or activeUsersDB.exists(userIP) == 0:
        return redirect('/')
    activeUsersDB.expire(userIP, 60)
    login = activeUsersDB.lindex(userIP, 0)
    activity = int(activeUsersDB.lindex(userIP, 1)) + 1
    activeUsersDB.lset(userIP, 1, str(activity))
    cursor = usersDB.cursor(buffered=True, dictionary=True)
    query = ("SELECT * FROM users "
                "WHERE username=%s OR email=%s")
    cursor.execute(query, (login, login))
    row = cursor.fetchone()
    cursor.close()
    username = row['username']
    email = row['email']
    age = row['age']
    country = row['country']
    return render_template('account.html', username=username, email=email, age=age, country=country, userIP=userIP)

if __name__ == '__main__':
    application.run(debug=True)