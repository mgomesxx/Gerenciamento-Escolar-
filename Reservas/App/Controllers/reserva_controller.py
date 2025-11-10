from app import db
from app.models.reserva_model import Reserva
import requests
import os
from datetime import datetime

SERVICO_GERENCIAMENTO_URL = os.environ.get('SERVICO_GERENCIAMENTO_URL', 'http://localhost:5001')

def turma_existe(turma_id):
    try:
        url = f"{SERVICO_GERENCIAMENTO_URL}/turmas/{turma_id}"
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
def get_reservas():
    reservas = Reserva.query.all()
    return [reserva.to_dict() for reserva in reservas]

def get_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    return reserva.to_dict() if reserva else None

def create_reserva(data):
    turma_id = data.get('turma_id')
    if not turma_id or not turma_existe(turma_id):
        return {"error": "Turma não encontrada"}, 404
    
    nova_reserva = Reserva(
        num_sala = data.get('num_sala'),
        lab = data.get('lab', False),
        data = datetime.strptime(data.get('data'), '%Y-%m-%d').date() if data.get('data') else None,
        turma_id = turma_id
    )

    db.session.add(nova_reserva)
    db.session.commit()
    return nova_reserva.to_dict(), 201

def update_reserva(reserva_id, data):
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return {"error": "Reserva não encontrada"}, 404

    if 'turma_id' in data:
        turma_id = data['turma_id']
        if not turma_existe(turma_id):
            return {"error": "Turma não encontrada"}, 404
        reserva.turma_id = turma_id

    reserva.num_sala = data.get('num_sala', reserva.num_sala)
    reserva.lab = data.get('lab', reserva.lab)

    if 'data' in data:
        reserva.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
    
    db.session.commit()
    return reserva.to_dict(), 200

def delete_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        db.session.delete(reserva)
        db.session.commit()
        return True
    return False