from flask import Flask, send_file, url_for, request, render_template, redirect

application = Flask(__name__)

@application.route('/', methods=['GET'])
def serveMainPage():
    return render_template('index.html')

@application.route('/verify', methods=['GET', 'POST'])
def verifyLogin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['senha']
        return redirect(url_for('sayHello', login=login, password=password))

@application.route('/hello_world/<login>/<password>', methods=['GET', 'POST'])
def sayHello(login, password):
    return 'Hello, world!\nLogin: ' + login + '\nSenha: ' + password

if __name__ == '__main__':
    application.run(debug=True)