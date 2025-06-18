from urllib import parse

def application(environ, start_response):
    status = '200 OK'
    output = ['<html><body>', 'Olá, mundo!']
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    if content_length > 0:
        fields = parse(environ['wsgi.input'].read(content_length))
        output.append('Seu login: ' + fields.get('login', ''))
        output.append('Sua senha: ' + fields.get('senha', ''))
    output.append('</body></html>')

    headers = [('Contenty-Type', 'text/html; charset=utf-8'),
               ('Content-Length', str(sum([len(s) for s in output]) + 1))]

    start_response(status, headers)
    return [s.encode('utf-8') for s in output]