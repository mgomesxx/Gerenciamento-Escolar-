import os

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../reservas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GERENCIAMENTO_SERVICE_URL = os.environ.get('GERENCIAMENTO_SERVICE_URL', 'http://gerenciamento-service:5000')


    RESTX_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False
    RESTX_ERROR_404_HELP = False