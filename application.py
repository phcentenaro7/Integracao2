from flask import Flask, send_file

application = Flask(__name__)

@application.route('/')
def serveMainPage():
    return send_file('index.html')

@application.route('/hello_world')
def sayHello():
    return "Hello, world!"

if __name__ == '__main__':
    application.run(debug=True)