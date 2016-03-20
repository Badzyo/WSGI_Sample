"""
This app runs simple local HTTP server on http://localhost:8080
"""
import waitress
from app.wsgi import WSGIApp
from app.config import config

waitress.serve(WSGIApp, host=config.server.host, port=config.server.port)