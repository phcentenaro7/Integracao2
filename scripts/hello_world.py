def application(environ, start_response):
    status = '200 OK'
    output = 'Hello, world!'

    headers = [("Contenty-type", "text/plain")]

    start_response(status, headers)
    return [output.encode()]