from flask import Flask, send_file, url_for, request, render_template

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def serveMainPage():
    if request.method == 'POST':
        return redirect('/hello_world')
    else:
        return render_template('index.html')

@application.route('/hello_world', methods=['GET', 'POST'])
def sayHello():
    return 'Hello, world!\nLogin: ' + request.form['login'] + request.form['password']

if __name__ == '__main__':
    application.run(debug=True)