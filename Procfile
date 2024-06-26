web: gunicorn TIPOINTICROIX.wsgi --timeout 120 --workers=3 --threads=3 --worker-connections=1000
worker: uvicorn uvicorn_worker:app --port 8765