from flask import Flask, send_file, url_for, request, render_template

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def serveMainPage():
    if request.method == 'POST':
        return redirect(url_for('hello_world', login=request.form['login'], password=request.form['senha']))
    else:
        return render_template('index.html')

@application.route('/hello_world', methods=['GET', 'POST'])
def sayHello(login, password):
    return 'Hello, world!\nLogin: ' + login + password

if __name__ == '__main__':
    application.run(debug=True)