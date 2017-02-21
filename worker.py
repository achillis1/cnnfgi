import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safety.settings")

import redis
from rq import Worker, Queue, Connection

import django
django.setup()

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()