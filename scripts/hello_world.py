from flask import Flask

application = Flask(__name__)

@application.route('/hello_world')
def sayHello():
    return "Hello, world!"

if __name__ == '__main__':
    application.run(debug=True)