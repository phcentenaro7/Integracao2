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
        cursor = usersDB.cursor(buffered=True)
        query = ("SELECT * FROM users "
                 "WHERE (username=%s OR email=%s) AND password=%s")
        cursor.execute(query, (login, login, password))
        if cursor.rowcount > 0:
            print(request.remote_addr)
            print(login)
            activeUsersDB.setex(request.remote_addr, 60, (login, 0))
            cursor.close()
            return redirect(url_for('sayHello', login=login, password=password))
        cursor.close()
        abort(404)
        

@application.route('/hello_world/<login>/<password>', methods=['GET', 'POST'])
def sayHello(login, password):
    return 'Hello, world!\nLogin: ' + login + '\nSenha: ' + password

if __name__ == '__main__':
    application.run(debug=True)