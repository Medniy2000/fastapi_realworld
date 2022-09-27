import multiprocessing

from src.app.config.settings import LAUNCH_MODE, LaunchMode

name = "Gunicorn config for application"

bind = "0.0.0.0:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = 2

if LAUNCH_MODE == LaunchMode.PRODUCTION.value:
    workers = multiprocessing.cpu_count() * 2 + 1
