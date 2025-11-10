from app import db

class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(200))
    peso_nota = db.Column(db.Integer)
    data_entrega = db.Column(db.Date)

    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)

    notas = db.relationship('Nota', back_populates='atividade', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'peso_nota': self.peso_nota,
            'data_entrega': str(self.data_entrega) if self.data_entrega else None,
            'turma_id': self.turma_id,
            'professor_id': self.professor_id
        }