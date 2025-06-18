from urllib import parse

def application(environ, start_response):
    status = '200 OK'
    output = ['Olá, mundo!']
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    if content_length > 0:
        fields = parse(environ['wsgi.input'].read(content_length))
        output.append('Seu login: ' + fields.get('login', ''))
        output.append('Sua senha: ' + fields.get('senha', ''))

    headers = [('Contenty-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)
    return [s.encode() for s in output]