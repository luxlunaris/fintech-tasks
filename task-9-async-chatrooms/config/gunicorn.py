"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count

bind = "0.0.0.0:5000"
limit_request_line = 0
worker_class = "aiohttp.worker.GunicornWebWorker"
workers = cpu_count()
access_logfile = "logs.log"
preload_app = True
