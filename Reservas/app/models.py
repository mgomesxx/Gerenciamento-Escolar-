from .__init__ import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.String(10), nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date, nullable=False)
    
    turma_id = db.Column(db.Integer, nullable=False)