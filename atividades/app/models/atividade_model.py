from app import db
from app.models.atividade_model import Atividade
from app.models.nota_model import Nota
import requests
import os

SERVICO_GERENCIAMENTO_URL = os.environ.get('SERVICO_GERENCIAMENTO_URL', 'http://localhost:5001')

def aluno_existe(aluno_id):
    """Verifica se o Aluno existe no serviço de Gerenciamento."""
    try:
        url = f"{SERVICO_GERENCIAMENTO_URL}/alunos/{aluno_id}"
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

def atividade_existe(atividade_id):
    """Verifica se a Atividade existe no banco de dados local."""
    return Atividade.query.get(atividade_id) is not None

def get_notas():
    notas = Nota.query.all()
    return [nota.to_dict() for nota in notas]

def get_nota(nota_id):
    nota = Nota.query.get(nota_id)
    return nota.to_dict() if nota else None

def create_nota(data):
    aluno_id = data.get('aluno_id')
    atividade_id = data.get('atividade_id')

    if not aluno_id or not aluno_existe(aluno_id):
        return {'error': 'Aluno não encontrado no serviço de gerenciamento'}, 404

    if not atividade_id or not atividade_existe(atividade_id):
        return {'error': 'Atividade não encontrada neste serviço'}, 404

    nova_nota = Nota(
        nota=data.get('nota'),
        aluno_id=aluno_id,
        atividade_id=atividade_id
    )

    db.session.add(nova_nota)
    db.session.commit()
    return nova_nota.to_dict(), 201

def update_nota(nota_id, data):
    nota_obj = Nota.query.get(nota_id)
    if not nota_obj:
        return {'error': 'Nota não encontrada'}, 404

    if 'aluno_id' in data:
        aluno_id = data.get('aluno_id')
        if not aluno_existe(aluno_id):
            return {'error': 'Aluno não encontrado no serviço de gerenciamento'}, 404
        nota_obj.aluno_id = aluno_id

    if 'atividade_id' in data:
        atividade_id = data.get('atividade_id')
        if not atividade_existe(atividade_id):
            return {'error': 'Atividade não encontrada neste serviço'}, 404
        nota_obj.atividade_id = atividade_id

    nota_obj.nota = data.get('nota', nota_obj.nota)
    db.session.commit()
    return nota_obj.to_dict(), 200

def delete_nota(nota_id):
    nota_obj = Nota.query.get(nota_id)
    if nota_obj:
        db.session.delete(nota_obj)
        db.session.commit()
        return True
    return False