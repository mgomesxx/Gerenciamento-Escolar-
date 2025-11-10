# servico-atividades/app/routes/nota_routes.py

from flask import Blueprint, request, jsonify
from app.controllers import nota_controller

nota_bp = Blueprint('nota_bp', __name__, url_prefix='/notas')

@nota_bp.route('/', methods=['GET'])
def get_notas():
    """
    Lista todas as notas
    ---
    tags:
      - Notas
    responses:
      200:
        description: Uma lista de todas as notas
        schema:
          type: array
          items:
            $ref: '#/definitions/Nota'
    """
    notas = nota_controller.get_notas()
    return jsonify(notas)

@nota_bp.route('/<int:nota_id>', methods=['GET'])
def get_nota(nota_id):
    """
    Busca uma nota por ID
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: nota_id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da nota
        schema:
          $ref: '#/definitions/Nota'
      404:
        description: Nota não encontrada
    """
    nota = nota_controller.get_nota(nota_id)
    if nota:
        return jsonify(nota)
    return jsonify({'error': 'Nota não encontrada'}), 404

@nota_bp.route('/', methods=['POST'])
def create_nota():
    """
    Cria uma nova nota (atribui uma nota a um aluno para uma atividade)
    ---
    tags:
      - Notas
    parameters:
      - in: body
        name: body
        schema:
          id: Nota
          required:
            - aluno_id
            - atividade_id
            - nota
          properties:
            nota:
              type: number
              format: float
            aluno_id:
              type: integer
            atividade_id:
              type: integer
    responses:
      201:
        description: Nota criada com sucesso
      400:
        description: Dados insuficientes
      404:
        description: Aluno ou Atividade não encontrado
    """
    data = request.get_json()
    if not data or not 'aluno_id' in data or not 'atividade_id' in data:
        return jsonify({'error': 'Dados insuficientes'}), 400

    nota, status_code = nota_controller.create_nota(data)
    return jsonify(nota), status_code

@nota_bp.route('/<int:nota_id>', methods=['PUT'])
def update_nota(nota_id):
    """
    Atualiza uma nota existente
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: nota_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Nota'
    responses:
      200:
        description: Nota atualizada com sucesso
      404:
        description: Nota, Aluno ou Atividade não encontrado
    """
    data = request.get_json()
    nota, status_code = nota_controller.update_nota(nota_id, data)
    return jsonify(nota), status_code

@nota_bp.route('/<int:nota_id>', methods=['DELETE'])
def delete_nota(nota_id):
    """
    Deleta uma nota
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: nota_id
        type: integer
        required: true
    responses:
      200:
        description: Nota deletada com sucesso
      404:
        description: Nota não encontrada
    """
    deletado = nota_controller.delete_nota(nota_id)
    if deletado:
        return jsonify({'message': 'Nota deletada com sucesso'})
    return jsonify({'error': 'Nota não encontrada'}), 404