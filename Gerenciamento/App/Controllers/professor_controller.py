from app import db
from app.models.professor_model import Professor

def get_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def get_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if professor:
        return professor.to_dict()
    return None

def create_professor(data):
    novo_professor = Professor(
        nome=data.get('nome'),
        idade=data.get('idade'),
        materia=data.get('materia'),
        observacoes=data.get('observacoes')
    )

    db.session.add(novo_professor)
    db.session.commit()
    return novo_professor.to_dict()

def update_professor(professor_id, data):
    professor = Professor.query.get(professor_id)
    if professor:
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)
        db.session.commit()
        return professor.to_dict()
    return None

def delete_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if professor:
        db.session.delete(professor)
        db.session.commit()
        return True
    return False