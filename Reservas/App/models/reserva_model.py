from app import db

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date)

    turma_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'num_sala': self.num_sala,
            'lab': self.lab,
            'data': str(self.data) if self.data else None,
            'turma_id': self.turma_id
        }