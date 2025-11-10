# app/routes/turma_routes.py

from flask import Blueprint, request, jsonify
from app.controllers import turma_controller

turma_bp = Blueprint('turma_bp', __name__, url_prefix='/turmas')

@turma_bp.route('/', methods=['GET'])
def get_turmas():
    """
    Lista todas as turmas
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Uma lista de turmas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              descricao:
                type: string
              ativo:
                type: boolean
              professor_id:
                type: integer
              professor_nome:
                type: string
    """
    turmas = turma_controller.get_turmas()
    return jsonify(turmas)

@turma_bp.route('/<int:turma_id>', methods=['GET'])
def get_turma(turma_id):
    """
    Busca uma turma por ID
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: turma_id
        type: integer
        required: true
        description: ID da turma a ser buscada
    responses:
      200:
        description: Detalhes da turma
      404:
        description: Turma não encontrada
    """
    turma = turma_controller.get_turma(turma_id)
    if turma:
        return jsonify(turma)
    return jsonify({'error': 'Turma não encontrada'}), 404

@turma_bp.route('/', methods=['POST'])
def create_turma():
    """
    Cria uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - descricao
            - professor_id
          properties:
            descricao:
              type: string
            ativo:
              type: boolean
              default: true
            professor_id:
              type: integer
    responses:
      201:
        description: Turma criada com sucesso
      400:
        description: Dados insuficientes
      404:
        description: Professor não encontrado
    """
    data = request.get_json()
    if not data or not 'descricao' in data or not 'professor_id' in data:
        return jsonify({'error': 'Dados insuficientes'}), 400
    
    nova_turma = turma_controller.create_turma(data)
    if not nova_turma:
        return jsonify({'error': 'Professor não encontrado'}), 404

    return jsonify(nova_turma), 201

@turma_bp.route('/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    """
    Atualiza uma turma existente
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: turma_id
        type: integer
        required: true
        description: ID da turma a ser atualizada
      - in: body
        name: body
        schema:
          type: object
          properties:
            descricao:
              type: string
            ativo:
              type: boolean
            professor_id:
              type: integer
    responses:
      200:
        description: Turma atualizada com sucesso
      404:
        description: Turma ou Professor não encontrado
    """
    data = request.get_json()
    turma_atualizada = turma_controller.update_turma(turma_id, data)

    if 'error' in turma_atualizada:
        return jsonify(turma_atualizada), 404
    
    return jsonify(turma_atualizada)

@turma_bp.route('/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    """
    Deleta uma turma
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: turma_id
        type: integer
        required: true
        description: ID da turma a ser deletada
    responses:
      200:
        description: Turma deletada com sucesso
      404:
        description: Turma não encontrada
    """
    sucesso = turma_controller.delete_turma(turma_id)
    if sucesso:
        return jsonify({'message': 'Turma deletada com sucesso'})
    return jsonify({'error': 'Turma não encontrada'}), 404