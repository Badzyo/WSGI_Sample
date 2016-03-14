"""
This app runs simple local HTTP server on http://localhost:8080
"""
import waitress
from app.wsgi import WSGIApp

waitress.serve(WSGIApp, host='127.0.0.1', port=8080)