from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from .config import Config


db = SQLAlchemy()
migrate = Migrate()
api = Api(
    version='1.0', 
    title='API de Gerenciamento Escolar',
    description='API CRUD para Professores, Turmas e Alunos',
    doc='/doc/' 
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)


    from .routes import professor_ns, turma_ns, aluno_ns
    api.add_namespace(professor_ns)
    api.add_namespace(turma_ns)
    api.add_namespace(aluno_ns)

    return app