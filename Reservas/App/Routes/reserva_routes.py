from flask import Blueprint, request, jsonify
from app.controllers import reserva_controller

reserva_bp = Blueprint('reserva_bp', __name__, url_prefix='/reservas')

@reserva_bp.route('/', methods=['GET'])
def get_reservas():
    """
    Lista todas as reservas
    ---
    tags:
      - Reservas
    responses:
      200:
        description: Uma lista de todas as reservas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              num_sala:
                type: integer
              lab:
                type: boolean
              data:
                type: string
                format: date
              turma_id:
                type: integer
    """
    reservas = reserva_controller.get_reservas()
    return jsonify(reservas), 200

@reserva_bp.route('/<int:reserva_id>', methods=['GET'])
def get_reserva(reserva_id):
    """
    Busca uma reserva por ID
    ---
    tags:
      - Reservas
    parameters:
      - in: path
        name: reserva_id
        type: integer
        required: true
        description: ID da reserva
    responses:
      200:
        description: Detalhes da reserva
      404:
        description: Reserva não encontrada
    """
    reserva = reserva_controller.get_reserva(reserva_id)
    if reserva:
        return jsonify(reserva)
    else:
        return jsonify({"error": "Reserva não encontrada"}), 404

@reserva_bp.route('/', methods=['POST'])
def create_reserva():
    """
    Cria uma nova reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - turma_id
            - data
          properties:
            num_sala:
              type: integer
            lab:
              type: boolean
            data:
              type: string
              format: date
              example: "2025-10-30"
            turma_id:
              type: integer
    responses:
      201:
        description: Reserva criada com sucesso
      400:
        description: Dados insuficientes
      404:
        description: Turma não encontrada no serviço de gerenciamento
    """
    data = request.get_json()
    if not data or not 'turma_id' in data or not 'data' in data:
        return jsonify({"error": "Dados insuficientes (id da turma e data são obrigatórios)"}), 400
    nova_reserva, status_code = reserva_controller.create_reserva(data)
    return jsonify(nova_reserva), status_code

@reserva_bp.route('/<int:reserva_id>', methods=['PUT'])
def update_reserva(reserva_id):
    """
    Atualiza uma reserva existente
    ---
    tags:
      - Reservas
    parameters:
      - in: path
        name: reserva_id
        type: integer
        required: true
        description: ID da reserva a ser atualizada
      - in: body
        name: body
        schema:
          type: object
          properties:
            num_sala:
              type: integer
            lab:
              type: boolean
            data:
              type: string
              format: date
            turma_id:
              type: integer
    responses:
      200:
        description: Reserva atualizada com sucesso
      404:
        description: Reserva não encontrada ou Turma não encontrada
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados insuficientes"}), 400
    reserva_atualizada, status_code = reserva_controller.update_reserva(reserva_id, data)
    return jsonify(reserva_atualizada), status_code

@reserva_bp.route('/<int:reserva_id>', methods=['DELETE'])
def delete_reserva(reserva_id):
    """
    Deleta uma reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: path
        name: reserva_id
        type: integer
        required: true
        description: ID da reserva a ser deletada
    responses:
      200:
        description: Reserva deletada com sucesso
      404:
        description: Reserva não encontrada
    """
    deletado = reserva_controller.delete_reserva(reserva_id)
    if deletado:
        return jsonify({"message": "Reserva deletada com sucesso"})
    return jsonify({"error": "Reserva não encontrada"}), 404