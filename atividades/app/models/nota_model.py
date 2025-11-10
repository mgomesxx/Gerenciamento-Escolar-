from app import db

class Nota(db.Model):
    __tablename__ = 'notas'

    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float)

    aluno_id = db.Column(db.Integer, nullable=False)

    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    atividade = db.relationship('Atividade', back_populates='notas')

    def to_dict(self):
        return {
            'id': self.id,
            'nota': self.nota,
            'aluno_id': self.aluno_id,
            'atividade_id': self.atividade_id,
            'nome_atividade': self.atividade.nome_atividade if self.atividade else None
        }