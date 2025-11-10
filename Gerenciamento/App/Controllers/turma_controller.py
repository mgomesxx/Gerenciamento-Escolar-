from app import db
from app.models.turma_model import Turma
from app.models.professor_model import Professor

def get_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def get_turma(turma_id):
    turma = Turma.query.get(turma_id)
    return turma.to_dict() if turma else None

def create_turma(data):
    professor = Professor.query.get(data.get('professor_id'))
    if not professor:
        return None
    
    nova_turma = Turma(
        descricao=data.get('descricao'),
        ativo=data.get('ativo', True),
        professor_id=data.get('professor_id')
    )
    db.session.add(nova_turma)
    db.session.commit()
    return nova_turma.to_dict()

def update_turma(turma_id, data):
    turma = Turma.query.get(turma_id)
    if not turma:
        return {'error': 'Turma não encontrado'}
    
    if 'professor_id' in data:
        professor = Professor.query.get(data.get('professor_id'))
        if not professor:
            return {'error': 'Professor não encontrado'}
        turma.professor_id = data.get('professor_id')

    turma.descricao = data.get('descricao', turma.descricao)
    turma.ativo = data.get('ativo', turma.ativo)
    db.session.commit()
    return turma.to_dict()

def delete_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if turma:
        db.session.delete(turma)
        db.session.commit()
        return True
    return False