web: gunicorn TIPOINTICROIX.wsgi --timeout 120 --workers=3 --threads=3 --worker-connections=1000
worker: python -X python -m asgi --log-config /workspace/log_config.yaml