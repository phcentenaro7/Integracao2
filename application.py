from flask import Flask, send_file, request

application = Flask(__name__)

@application.route('/')
def serveMainPage():
    return send_file('index.html')

@application.route('/hello_world', methods=['POST'])
def sayHello():
    return 'Hello, world!\nLogin: ' + request.form.get('login') + '\nSenha: ' + request.form.get('senha')

if __name__ == '__main__':
    application.run(debug=True)