from waitress import serve
from TIPOINTICROIX.wsgi import application  # Remplacez 'votre_projet' par le nom de votre projet

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=9000)