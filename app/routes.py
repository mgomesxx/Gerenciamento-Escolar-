from flask import request
from flask_restx import Namespace, Resource, fields
from .__init__ import db
from .models import Professor, Turma, Aluno
from .schemas import (
    professor_schema, professores_schema, 
    turma_schema, turmas_schema, 
    aluno_schema, alunos_schema
)

def calcular_media(data):
    n1 = data.get('nota_primeiro_semestre') if isinstance(data, dict) else getattr(data, 'nota_primeiro_semestre', None)
    n2 = data.get('nota_segundo_semestre') if isinstance(data, dict) else getattr(data, 'nota_segundo_semestre', None)
    
    if n1 is not None and n2 is not None:
        return (n1 + n2) / 2
    return None

# =================================================================
# PROFESSOR NAMESPACE
# =================================================================

professor_ns = Namespace('professores', description='Operações CRUD de Professores')

professor_model = professor_ns.model('Professor', {
    'nome': fields.String(required=True),
    'idade': fields.Integer(),
    'materia': fields.String(),
    'observacoes': fields.String()
})

@professor_ns.route('/')
class ProfessorList(Resource):
    def get(self):
        professores = Professor.query.all()
        return professores_schema.dump(professores), 200

    @professor_ns.expect(professor_model, validate=True)
    def post(self):
        try:
            data = professor_schema.load(professor_ns.payload)
            novo_professor = Professor(**data)
            db.session.add(novo_professor)
            db.session.commit()
            return professor_schema.dump(novo_professor), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

@professor_ns.route('/<int:id>')
@professor_ns.param('id', 'ID do Professor')
class ProfessorResource(Resource):
    def get(self, id):
        professor = Professor.query.get_or_404(id)
        return professor_schema.dump(professor), 200

    @professor_ns.expect(professor_model)
    def put(self, id):
        professor = Professor.query.get_or_404(id)
        try:
            data = professor_schema.load(professor_ns.payload, partial=True)
            for key, value in data.items():
                setattr(professor, key, value)
            db.session.commit()
            return professor_schema.dump(professor), 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    def delete(self, id):
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return '', 204

# =================================================================
# TURMA NAMESPACE
# =================================================================

turma_ns = Namespace('turmas', description='Operações CRUD de Turmas')

turma_model = turma_ns.model('Turma', {
    'descricao': fields.String(required=True),
    'professor_id': fields.Integer(required=True),
    'ativo': fields.Boolean()
})

@turma_ns.route('/')
class TurmaList(Resource):
    def get(self):
        turmas = Turma.query.all()
        return turmas_schema.dump(turmas), 200

    @turma_ns.expect(turma_model, validate=True)
    def post(self):
        try:
            data = turma_schema.load(turma_ns.payload)
            if not Professor.query.get(data['professor_id']):
                return {'message': f"Professor com ID {data['professor_id']} não encontrado."}, 404
            
            nova_turma = Turma(**data)
            db.session.add(nova_turma)
            db.session.commit()
            return turma_schema.dump(nova_turma), 201
        except Exception as e:
            db.session.rollback()
            return {'message': f"Erro ao criar turma: {str(e)}"}, 400

@turma_ns.route('/<int:id>')
@turma_ns.param('id', 'ID da Turma')
class TurmaResource(Resource):
    def get(self, id):
        turma = Turma.query.get_or_404(id)
        return turma_schema.dump(turma), 200

    @turma_ns.expect(turma_model, validate=False)
    def put(self, id):
        turma = Turma.query.get_or_404(id)
        try:
            data = turma_schema.load(turma_ns.payload, partial=True)
            for key, value in data.items():
                setattr(turma, key, value)
            db.session.commit()
            return turma_schema.dump(turma), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f"Erro ao atualizar turma: {str(e)}"}, 400

    def delete(self, id):
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return '', 204

# =================================================================
# ALUNO NAMESPACE
# =================================================================

aluno_ns = Namespace('alunos', description='Operações CRUD de Alunos e Notas')

aluno_model = aluno_ns.model('Aluno', {
    'nome': fields.String(required=True),
    'idade': fields.Integer(),
    'turma_id': fields.Integer(required=True),
    'data_nascimento': fields.Date(),
    'nota_primeiro_semestre': fields.Float(),
    'nota_segundo_semestre': fields.Float(),
})

@aluno_ns.route('/')
class AlunoList(Resource):
    def get(self):
        alunos = Aluno.query.all()
        return alunos_schema.dump(alunos), 200

    @aluno_ns.expect(aluno_model, validate=True)
    def post(self):
        try:
            data = aluno_schema.load(aluno_ns.payload)
            if not Turma.query.get(data['turma_id']):
                return {'message': f"Turma com ID {data['turma_id']} não encontrada."}, 404
            
            data['media_final'] = calcular_media(data)
            
            novo_aluno = Aluno(**data)
            db.session.add(novo_aluno)
            db.session.commit()
            return aluno_schema.dump(novo_aluno), 201
        except Exception as e:
            db.session.rollback()
            return {'message': f"Erro ao criar aluno: {str(e)}"}, 400

@aluno_ns.route('/<int:id>')
@aluno_ns.param('id', 'ID do Aluno')
class AlunoResource(Resource):
    def get(self, id):
        aluno = Aluno.query.get_or_404(id)
        return aluno_schema.dump(aluno), 200

    @aluno_ns.expect(aluno_model, validate=False)
    def put(self, id):
        aluno = Aluno.query.get_or_404(id)
        
        try:
            data = aluno_schema.load(aluno_ns.payload, partial=True)
            
            for key, value in data.items():
                setattr(aluno, key, value)
            
            aluno.media_final = calcular_media(aluno)
            
            db.session.commit()
            return aluno_schema.dump(aluno), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f"Erro ao atualizar aluno: {str(e)}"}, 400

    def delete(self, id):
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return '', 204