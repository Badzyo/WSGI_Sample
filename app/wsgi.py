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
    As an example, it generates a bytearray
    containing the HTTP request method and URL path
    """
    def __init__(self, environ):
        self.environ = environ
        self.__calculate_response()

    def __calculate_response(self):
        self.headers = [('Content-type', 'text/plain')]
        self.status = '200 OK'
        self.body = bytearray(self.environ['REQUEST_METHOD'] + ': ' +
                              self.environ['PATH_INFO'],
                              'utf-8')
