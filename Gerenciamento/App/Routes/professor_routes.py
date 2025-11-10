from flask import Blueprint, request, jsonify
from app.controllers import professor_controller

professor_bp = Blueprint('professor_bp', __name__, url_prefix='/professores')

@professor_bp.route('/', methods=['GET'])
def get_professores():
    """
    Lista todos os professores
    ---
    tags:
      - Professores
    responses:
      200:
        description: Uma lista de professores
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
              materia:
                type: string
              observacoes:
                type: string
    """
    professores = professor_controller.get_professores()
    return jsonify(professores)

@professor_bp.route('/<int:professor_id>', methods=['GET'])
def get_professor(professor_id):
    """
    Busca um professor por ID
    ---
    tags:
      - Professores
    parameters:
      - in: path
        name: professor_id
        type: integer
        required: true
        description: ID do professor a ser buscado
    responses:
      200:
        description: Detalhes do professor
      404:
        description: Professor não encontrado
    """
    professor = professor_controller.get_professor(professor_id)
    if professor:
        return jsonify(professor)
    return jsonify({'error': 'Professor não encontrado'}), 404

@professor_bp.route('/', methods=['POST'])
def create_professor():
    """
    Cria um novo professor
    ---
    tags:
      - Professores
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
            observacoes:
              type: string
    responses:
      201:
        description: Professor criado com sucesso
    """
    data = request.get_json()
    if not data or not 'nome' in data:
        return jsonify({'error': 'Dados insuficientes'}), 400
    
    novo_professor = professor_controller.create_professor(data)
    return jsonify(novo_professor), 201

@professor_bp.route('/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    """
    Atualiza um professor existente
    ---
    tags:
      - Professores
    parameters:
      - in: path
        name: professor_id
        type: integer
        required: true
        description: ID do professor a ser atualizado
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
            observacoes:
              type: string
    responses:
      200:
        description: Professor atualizado com sucesso
      404:
        description: Professor não encontrado
    """
    data = request.get_json()
    professor_atualizado = professor_controller.update_professor(professor_id, data)
    if professor_atualizado:
        return jsonify(professor_atualizado)
    return jsonify({'error': 'Professor não encontrado'}), 404

@professor_bp.route('/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    """
    Deleta um professor
    ---
    tags:
      - Professores
    parameters:
      - in: path
        name: professor_id
        type: integer
        required: true
        description: ID do professor a ser deletado
    responses:
      200:
        description: Professor deletado com sucesso
      404:
        description: Professor não encontrado
    """
    deletado = professor_controller.delete_professor(professor_id)
    if deletado:
        return jsonify({'message': 'Professor deletado com sucesso'})
    return jsonify({'error': 'Professor não encontrado'}), 404