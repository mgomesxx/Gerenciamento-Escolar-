from flask import Blueprint, jsonify, request
from app.controllers import atividade_controller

atividade_bp = Blueprint('atividade_bp', __name__, url_prefix='/atividades')

@atividade_bp.route('/', methods=['GET'])
def get_atividades():
    """
    Lista todas as atividades
    ---
    tags:
      - Atividades
    responses:
      200:
        description: Uma lista de todas as atividades
        schema:
          type: array
          items:
            $ref: '#/definitions/Atividade'
    """
    atividades = atividade_controller.get_atividades()
    return jsonify(atividades)

@atividade_bp.route('/<int:atividade_id>', methods=['GET'])
def get_atividade(atividade_id):
    """
    Busca uma atividade por ID
    ---
    tags:
      - Atividades
    parameters:
      - in: path
        name: atividade_id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da atividade
        schema:
          $ref: '#/definitions/Atividade'
      404:
        description: Atividade não encontrada
    """
    atividade = atividade_controller.get_atividade(atividade_id)
    if atividade:
        return jsonify(atividade)
    return jsonify({'error': 'Atividade não encontrada'}), 404

@atividade_bp.route('/', methods=['POST'])
def create_atividade():
    """
    Cria uma nova atividade
    ---
    tags:
      - Atividades
    parameters:
      - in: body
        name: body
        schema:
          id: Atividade
          required:
            - turma_id
            - professor_id
            - nome_atividade
          properties:
            nome_atividade:
              type: string
            descricao:
              type: string
            peso_porcento:
              type: integer
            data_entrega:
              type: string
              format: date
              example: "2025-11-20"
            turma_id:
              type: integer
            professor_id:
              type: integer
    responses:
      201:
        description: Atividade criada com sucesso
      400:
        description: Dados insuficientes
      404:
        description: Turma ou Professor não encontrado no serviço de gerenciamento
    """
    data = request.get_json()
    if not data or not 'turma_id' in data or not 'professor_id' in data:
        return jsonify({'error': 'Dados insuficientes'}), 400

    atividade, status_code = atividade_controller.create_atividade(data)
    return jsonify(atividade), status_code

@atividade_bp.route('/<int:atividade_id>', methods=['PUT'])
def update_atividade(atividade_id):
    """
    Atualiza uma atividade existente
    ---
    tags:
      - Atividades
    parameters:
      - in: path
        name: atividade_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Atividade'
    responses:
      200:
        description: Atividade atualizada com sucesso
      404:
        description: Atividade, Turma ou Professor não encontrado
    """
    data = request.get_json()
    atividade, status_code = atividade_controller.update_atividade(atividade_id, data)
    return jsonify(atividade), status_code

@atividade_bp.route('/<int:atividade_id>', methods=['DELETE'])
def delete_atividade(atividade_id):
    """
    Deleta uma atividade
    ---
    tags:
      - Atividades
    parameters:
      - in: path
        name: atividade_id
        type: integer
        required: true
    responses:
      200:
        description: Atividade deletada com sucesso
      404:
        description: Atividade não encontrada
    """
    sucesso = atividade_controller.delete_atividade(atividade_id)
    if sucesso:
        return jsonify({'message': 'Atividade deletada com sucesso'})
    return jsonify({'error': 'Atividade não encontrada'}), 404