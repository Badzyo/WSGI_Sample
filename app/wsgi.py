from .dbmanagers.base import db
import json


class WSGIApp:
    """
    Implemention of WSGI interface according to PEP-0333
    """
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        response = Response(self.environ)
        self.start(response.status, response.headers)
        yield response.body


class Response:
    """
    Response builder.
    If URL path is unresolved, it generates a bytearray
    containing the HTTP request method and URL path
    """

    def __init__(self, environ):
        self.environ = environ
        self.__calculate_response()

    def __calculate_response(self):
        self.headers = [('Content-type', 'text/plain')]
        self.status = '200 OK'
        method = self.environ['REQUEST_METHOD']
        path = self.environ['PATH_INFO']

        # GET /last
        if path == '/last' and method == 'GET':
            self.body = json.dumps(db.read_last_data(),
                                   ensure_ascii=False)
            self.body = bytearray(self.body, 'utf-8')

        # POST /import
        elif path == '/import' and method == 'POST':
            try:
                data = self.environ['wsgi.input'].read()
                db.write_data(json.loads(data.decode('utf-8')))
                self.body = b'OK'
            except:
                self.body = b'FAIL'

        # other unresolved requests
        else:
            self.body = bytearray('{}:{}'.format(method, path), 'utf-8')
