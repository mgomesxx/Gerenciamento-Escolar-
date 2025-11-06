from .database import db

class Turma(db.Model):
    __tablename__ = 'turma'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    alunos = db.relationship('Aluno', backref='turma', lazy=True)