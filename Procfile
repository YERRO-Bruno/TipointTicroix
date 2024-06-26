web: gunicorn TIPOINTICROIX.wsgi --timeout 120 --workers=3 --threads=3 --worker-connections=1000
worker: uvicorn uvicorn_worker:app --host 0.0.0.0 --port 8765