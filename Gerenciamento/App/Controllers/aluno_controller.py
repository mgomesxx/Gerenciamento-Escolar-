from App import db
from App.Model.aluno_model import Aluno
from App.Model.turma_model import Turma
from datetime import datetime

def get_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def get_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    return aluno.to_dict()

def create_aluno(data):
    turma = Turma.query.get(data.get('turma_id'))
    if not turma:
        return None
    
    novo_aluno = Aluno(
        nome=data.get('nome'),
        idade=data.get('idade'),
        turma_id=data.get('turma_id'),
        data_nascimento=datetime.strptime(data.get('data_nascimento'), '%Y-%m-%d').date() if data.get('data_nascimento') else None,
        nota_primeiro_semestre=data.get('nota_primeiro_semestre'),
        nota_segundo_semestre=data.get('nota_segundo_semestre')
    )

    if novo_aluno.nota_primeiro_semestre is not None and novo_aluno.nota_segundo_semestre is not None:
        novo_aluno.media_final = (novo_aluno.nota_primeiro_semestre + novo_aluno.nota_segundo_semestre) / 2

    db.session.add(novo_aluno)
    db.session.commit()
    return novo_aluno.to_dict()

def update_aluno(aluno_id, data):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return {'error': 'Aluno não encontrado'}

    if 'turma_id' in data:
        turma = Turma.query.get(data.get('turma_id'))
        if not turma:
            return {'error': 'Turma não encontrada'}
        aluno.turma_id = data.get('turma_id')

    aluno.nome = data.get('nome', aluno.nome)
    aluno.idade = data.get('idade', aluno.idade)
    if 'data_nascimento' in data:
        aluno.data_nascimento = datetime.strptime(data.get('data_nascimento'), '%Y-%m-%d').date()
    
    aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)

    if aluno.nota_primeiro_semestre is not None and aluno.nota_segundo_semestre is not None:
        aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2
    
    db.session.commit()
    return aluno.to_dict()

def delete_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return True
    return False