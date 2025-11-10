from app import db

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship('Professor', back_populates='turmas')
    alunos = db.relationship('Aluno', back_populates='turma', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'professor_id': self.professor_id,
            'professor_nome': self.professor.nome if self.professor else None
        }