from marshmallow import Schema, fields

class ProfessorSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    idade = fields.Int()
    materia = fields.Str()
    observacoes = fields.Str()

class TurmaSchema(Schema):
    id = fields.Int(dump_only=True)
    descricao = fields.Str(required=True)
    professor_id = fields.Int(required=True)
    ativo = fields.Bool()
    
    professor = fields.Nested(ProfessorSchema, dump_only=True, only=("id", "nome"))

class AlunoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    idade = fields.Int()
    turma_id = fields.Int(required=True)
    data_nascimento = fields.Date(format="%Y-%m-%d")
    nota_primeiro_semestre = fields.Float()
    nota_segundo_semestre = fields.Float()
    media_final = fields.Float(dump_only=True)
    
    turma = fields.Nested(TurmaSchema, dump_only=True, only=("id", "descricao"))

professor_schema = ProfessorSchema()
professores_schema = ProfessorSchema(many=True)
turma_schema = TurmaSchema()
turmas_schema = TurmaSchema(many=True)
aluno_schema = AlunoSchema()
alunos_schema = AlunoSchema(many=True)