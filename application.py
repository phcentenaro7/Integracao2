from flask import Flask, send_file, url_for, request, render_template, redirect, abort
import mysql.connector

application = Flask(__name__)
usersDB = mysql.connector.connect(user='admin', password='admin', database='server')

@application.route('/', methods=['GET'])
def serveMainPage():
    return render_template('index.html')

@application.route('/verify', methods=['GET', 'POST'])
def verifyLogin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['senha']
        cursor = usersDB.cursor()
        query = ("SELECT * FROM users"
                 "WHERE (username=%s OR email=%s) AND password=%s")
        cursor.execute(query, (login, login, password))
        if len(cursor) > 0:
            cursor.close()
            return redirect(url_for('sayHello', login=login, password=password))
        cursor.close()
        abort(404)
        

@application.route('/hello_world/<login>/<password>', methods=['GET', 'POST'])
def sayHello(login, password):
    return 'Hello, world!\nLogin: ' + login + '\nSenha: ' + password

if __name__ == '__main__':
    application.run(debug=True)