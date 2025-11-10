from app import db
from app.models.atividade_model import Atividade
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
    
def professor_existe(professor_id):
    try:
        url = f"{SERVICO_GERENCIAMENTO_URL}/professores/{professor_id}"
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
def get_atividades():
    atividades = Atividade.query.all()
    return [atividade.to_dict() for atividade in atividades]

def get_atividade(atividade_id):
    atividade = Atividade.query.get(atividade_id)
    return atividade.to_dict() if atividade else None

def create_atividade(data):
    turma_id = data.get('turma_id')
    professor_id = data.get('professor_id')

    if not turma_id or not turma_existe(turma_id):
        return {"error": "Turma não encontrada"}, 404

    if not professor_id or not professor_existe(professor_id):
        return {"error": "Professor não encontrado"}, 404
    
    nova_atividade = Atividade(
        nome = data.get('nome'),
        descricao = data.get('descricao'),
        peso_nota = data.get('peso_nota'),
        data_entrega = datetime.strptime(data.get('data_entrega'), '%Y-%m-%d').date() if data.get('data_entrega') else None,
        turma_id = turma_id,
        professor_id = professor_id
    )

    db.session.add(nova_atividade)
    db.session.commit()
    return nova_atividade.to_dict(), 201

def update_atividade(atividade_id, data):
    atividade = Atividade.query.get(atividade_id)
    if not atividade:
        return {"error": "Atividade não encontrada"}, 404

    if 'turma_id' in data:
        turma_id = data['turma_id']
        if not turma_existe(turma_id):
            return {"error": "Turma não encontrada"}, 404
        atividade.turma_id = turma_id

    if 'professor_id' in data:
        professor_id = data['professor_id']
        if not professor_existe(professor_id):
            return {"error": "Professor não encontrado"}, 404
        atividade.professor_id = professor_id

    atividade.nome = data.get('nome', atividade.nome)
    atividade.descricao = data.get('descricao', atividade.descricao)
    atividade.peso_nota = data.get('peso_nota', atividade.peso_nota)

    if 'data_entrega' in data:
        atividade.data_entrega = datetime.strptime(data['data_entrega'], '%Y-%m-%d').date()
    
    db.session.commit()
    return atividade.to_dict(), 200

def delete_atividade(atividade_id):
    atividade = Atividade.query.get(atividade_id)
    if atividade:
        db.session.delete(atividade)
        db.session.commit()
        return True
    return False