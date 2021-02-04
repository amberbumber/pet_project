web: flask db upgrade; flask translate compile; gunicorn microblog:app
worker: rq worker $REDIS_URL microblog-tasks
