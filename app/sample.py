"""
This app runs a simple local HTTP server on http://localhost:8080
It uses Waitress WSGI server
"""
import waitress


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
        self.__calculateResponse()

    def __calculateResponse(self):
        self.headers = [('Content-type', 'text/plain')]
        self.status = '200 OK'
        self.body = bytearray(self.environ['REQUEST_METHOD'] + ': ' +
                              self.environ['PATH_INFO'],
                              'utf-8')


waitress.serve(WSGIApp, host='127.0.0.1', port=8080)
