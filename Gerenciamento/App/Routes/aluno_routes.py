# app/routes/aluno_routes.py

from flask import Blueprint, request, jsonify
from app.controllers import aluno_controller

aluno_bp = Blueprint('aluno_bp', __name__, url_prefix='/alunos')

@aluno_bp.route('/', methods=['GET'])
def get_alunos():
    """
    Lista todos os alunos
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Uma lista de todos os alunos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              idade:
                type: integer
              data_nascimento:
                type: string
                format: date
              nota_primeiro_semestre:
                type: number
              nota_segundo_semestre:
                type: number
              media_final:
                type: number
              turma_id:
                type: integer
              turma_descricao:
                type: string
    """
    alunos = aluno_controller.get_alunos()
    return jsonify(alunos)

@aluno_bp.route('/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    """
    Busca um aluno por ID
    ---
    tags:
      - Alunos
    parameters:
      - name: aluno_id
        in: path
        type: integer
        required: true
        description: ID único do aluno.
    responses:
      200:
        description: Detalhes do aluno.
      404:
        description: Aluno não encontrado.
    """
    aluno = aluno_controller.get_aluno(aluno_id)
    if aluno:
        return jsonify(aluno)
    return jsonify({'error': 'Aluno não encontrado'}), 404

@aluno_bp.route('/', methods=['POST'])
def create_aluno():
    """
    Cria um novo aluno
    ---
    tags:
      - Alunos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - turma_id
          properties:
            nome:
              type: string
              description: Nome do aluno.
            idade:
              type: integer
              description: Idade do aluno.
            data_nascimento:
              type: string
              format: date
              example: "2005-10-20"
            nota_primeiro_semestre:
              type: number
              format: float
            nota_segundo_semestre:
              type: number
              format: float
            turma_id:
              type: integer
              description: ID da turma à qual o aluno pertence.
    responses:
      201:
        description: Aluno criado com sucesso.
      400:
        description: Dados insuficientes na requisição.
      404:
        description: Turma informada não foi encontrada.
    """
    data = request.get_json()
    if not data or not 'nome' in data or not 'turma_id' in data:
        return jsonify({'error': 'Dados insuficientes'}), 400
    
    novo_aluno = aluno_controller.create_aluno(data)
    if not novo_aluno:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify(novo_aluno), 201

@aluno_bp.route('/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    """
    Atualiza um aluno existente
    ---
    tags:
      - Alunos
    parameters:
      - name: aluno_id
        in: path
        type: integer
        required: true
        description: ID do aluno a ser atualizado.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            data_nascimento:
              type: string
              format: date
            nota_primeiro_semestre:
              type: number
              format: float
            nota_segundo_semestre:
              type: number
              format: float
            turma_id:
              type: integer
    responses:
      200:
        description: Aluno atualizado com sucesso.
      404:
        description: Aluno ou Turma não encontrado(a).
    """
    data = request.get_json()
    aluno_atualizado = aluno_controller.update_aluno(aluno_id, data)
    if 'error' in aluno_atualizado:
        return jsonify(aluno_atualizado), 404
    return jsonify(aluno_atualizado)

@aluno_bp.route('/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    """
    Deleta um aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: aluno_id
        in: path
        type: integer
        required: true
        description: ID do aluno a ser deletado.
    responses:
      200:
        description: Aluno deletado com sucesso.
      404:
        description: Aluno não encontrado.
    """
    sucesso = aluno_controller.delete_aluno(aluno_id)
    if sucesso:
        return jsonify({'message': 'Aluno deletado com sucesso'})
    return jsonify({'error': 'Aluno não encontrado'}), 404