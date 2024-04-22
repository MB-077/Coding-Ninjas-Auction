import os
from os import environ

bind = '0.0.0.0:' + os.environ.get('PORT', '8000')
workers = 3
threads = 3
worker_class = 'gthread'