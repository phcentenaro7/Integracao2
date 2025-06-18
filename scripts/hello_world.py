from cgi import parse_qs

def application(environ, start_response):
    status = '200 OK'
    output = 'Olá, mundo!<br>'
    content_length = environ.get('CONTENT_LENGTH', 0)
    if content_length > 0:
        fields = parse_qs(environ['wsgi.input'].read(content_length))
        output += 'Seu login: ' + fields.get('login', '') + '<br>'
        output += 'Sua senha: ' + fields.get('senha', '') + '<br>'

    headers = [('Contenty-type', 'text/plain')]

    start_response(status, headers)
    return [output.encode()]