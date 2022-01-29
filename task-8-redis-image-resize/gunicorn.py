"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count

bind = "0.0.0.0:5000"
limit_request_line = 0
workers = cpu_count()
preload_app = True
