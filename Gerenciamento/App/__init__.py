from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)
  db.init_app(app)
  Swagger(app)

  from .routes.professor_routes import professor_bp
  app.register_blueprint(professor_bp)

  from .routes.turma_routes import turma_bp
  app.register_blueprint(turma_bp)

  from .routes.aluno_routes import aluno_bp
  app.register_blueprint(aluno_bp)
  
  return app