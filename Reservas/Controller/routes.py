import os
import requests
from flask import request, jsonify, current_app
from Model.reserva_model import db, Reserva


def setup_routes(app):

    

    @app.route('/reservas', methods=['GET'])
    def list_reservas():
        """
        Lista todas as reservas
        ---
        tags:
          - Reservas
        summary: Lista todas as reservas cadastradas
        responses:
          200:
            description: Lista de reservas
        """
        reservas = Reserva.query.all()
        return jsonify([{
            'id': r.id,
            'num_sala': r.num_sala,
            'lab': r.lab,
            'data': r.data,
            'turma_id': r.turma_id
        } for r in reservas]), 200

    @app.route('/reservas', methods=['POST'])
    def create_reserva():
        """
        Cria uma nova reserva
        ---
        tags:
          - Reservas
        summary: Cria uma nova reserva de sala/laboratório
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - num_sala
                - data
                - turma_id
              properties:
                num_sala:
                  type: integer
                  example: 101
                lab:
                  type: boolean
                  example: true
                data:
                  type: string
                  format: date
                  example: "2025-10-22"
                turma_id:
                  type: integer
                  example: 1
        responses:
          201:
            description: Reserva criada com sucesso
          400:
            description: Turma não encontrada
          502:
            description: Erro ao consultar serviço de Gerenciamento
        """

        payload = request.json
        turma_id = payload.get("turma_id")

        base = request.environ.get(
            "GERENCIAMENTO_BASE_URL") or current_app.config["GERENCIAMENTO_BASE_URL"]
        try:
            resp = requests.get(f"{base}/turmas/{turma_id}")
        except requests.exceptions.RequestException:
            return {"mensagem": "Erro ao se comunicar com o serviço de Gerenciamento"}, 502

        if resp.status_code == 404:
            return {"mensagem": f"Turma {turma_id} não encontrada no serviço de Gerenciamento"}, 400
        if resp.status_code >= 400:
            return {"mensagem": "Erro ao consultar serviço de Gerenciamento"}, 502

        r = Reserva(
            num_sala=payload.get("num_sala"),
            lab=payload.get("lab", False),
            data=payload["data"],
            turma_id=turma_id
        )
        db.session.add(r)
        db.session.commit()

        return r.to_dict(), 201

    @app.route('/reservas/<int:id>', methods=['GET'])
    def get_reserva(id):
        """
        Obtém uma reserva pelo ID
        ---
        tags:
          - Reservas
        summary: Recupera uma reserva específica
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
            description: ID da reserva
        responses:
          200:
            description: Reserva encontrada
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return jsonify({'mensagem': 'Reserva não encontrada'}), 404
        return jsonify({
            'id': r.id,
            'num_sala': r.num_sala,
            'lab': r.lab,
            'data': r.data,
            'turma_id': r.turma_id
        }), 200

    @app.route('/reservas/<int:id>', methods=['PUT'])
    def update_reserva(id):
        """
        Atualiza uma reserva existente
        ---
        tags:
          - Reservas
        summary: Atualiza os dados de uma reserva
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  num_sala: { type: string }
                  lab: { type: boolean }
                  data: { type: string }
                  turma_id: { type: integer }
        responses:
          200:
            description: Reserva atualizada com sucesso
          404:
            description: Reserva não encontrada
          400:
            description: Turma inexistente ou dados inválidos
        """
        r = Reserva.query.get(id)
        if not r:
            return jsonify({'mensagem': 'Reserva não encontrada'}), 404

        data = request.get_json()

        turma_id = data.get('turma_id')
        if turma_id:
            base = request.environ.get(
                "GERENCIAMENTO_BASE_URL") or current_app.config["GERENCIAMENTO_BASE_URL"]

            try:
                resp = requests.get(f"{base}/turmas/{turma_id}")
            except requests.exceptions.RequestException:
                return jsonify({"mensagem": "Erro ao se comunicar com o serviço de Gerenciamento"}), 502

            if resp.status_code == 404:
                return jsonify({"mensagem": f"Turma {turma_id} não encontrada no serviço de Gerenciamento"}), 400
            elif resp.status_code >= 400:
                return jsonify({"mensagem": "Erro ao consultar serviço de Gerenciamento"}), 502

            r.turma_id = turma_id

        r.num_sala = data.get('num_sala', r.num_sala)
        r.lab = data.get('lab', r.lab)
        r.data = data.get('data', r.data)

        db.session.commit()
        return jsonify({'mensagem': 'Reserva atualizada com sucesso'}), 200

    @app.route('/reservas/<int:id>', methods=['DELETE'])
    def delete_reserva(id):
        """
        Deleta uma reserva existente
        ---
        tags:
          - Reservas
        summary: Remove uma reserva do banco de dados
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        responses:
          200:
            description: Reserva deletada com sucesso
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return jsonify({'mensagem': 'Reserva não encontrada'}), 404
        db.session.delete(r)
        db.session.commit()
        return jsonify({'message': 'Reserva deletada'}), 200