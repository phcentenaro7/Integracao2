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

        if activeUsersDB.get(userIP) != None:
            activeUsersDB.expire(userIP, 60)
            return redirect(url_for('sayHello', login=login, password=password))
        
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
    
@application.route('/remaining_time/<userIP>', methods=['POST'])
def getRemainingTime(userIP):
    if len(activeUsersDB.keys(userIP)) > 0:
        return activeUsersDB.ttl(userIP)
    return 0

@application.route('/hello_world/<userIP>', methods=['GET', 'POST'])
def sayHello(userIP):
    login = activeUsersDB.lindex(userIP, 0)
    cursor = usersDB.cursor(buffered=True)
    query = ("SELECT * FROM users "
                "WHERE username=%s OR email=%s")
    cursor.execute(query, (login, login))
    cursor.fetchall()
    username = cursor['username']
    email = cursor['email']
    age = cursor['age']
    country = cursor['country']
    cursor.close()
    return render_template('account.html', username=username, email=email, age=age, country=country, userIP=userIP)

if __name__ == '__main__':
    application.run(debug=True)