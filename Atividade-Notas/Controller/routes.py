import requests
from flask import request, jsonify, current_app
from Model.database import db
from Model.atividades_model import Atividades
from Model.notas_model import Notas
from datetime import datetime


def setup_routes(app):

    @app.route('/atividades', methods=['GET'])
    def listar_atividades():
        """
        Lista todas as atividades
        ---
        tags:
          - atividades
        summary: Lista todas as atividades cadastradas
        responses:
            200:
                description: Lista de atividades
            400:
                description: Nenhuma atividade cadastrada
        """

        atividades = Atividades.query.all()

        if not atividades:
            return jsonify({'mensagem': 'Nenhuma atividade cadastrada!'}), 400
        
        return jsonify([{
            'id': atv.id,
            'nome_atividade': atv.nome_atividade,
            'descricao': atv.descricao,
            'peso_porcento': atv.peso_porcento,
            'data_entrega': atv.data_entrega,
            'turma_id': atv.turma_id,
            'professor_id': atv.professor_id
        } for atv in atividades]), 200
    
    @app.route('/atividades/<int:id>', methods=['GET'])
    def get_atividade(id):
        """
        Obtém uma atividade pelo ID
        ---
        tags:
          - atividades
        summary: Recupera uma atividade específica
        parameters:
          - in: path
            name: id
            schema:
              type: integer
            required: true
            description: ID da atividade
        responses:
          200:
            description: Atividade encontrada
          404:
            description: Atividade não encontrada
        """

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'mensagem': 'Atividade não encontrada!'}) , 404
        
        return jsonify({
            'id': atv.id,
            'nome_atividade': atv.nome_atividade,
            'descricao': atv.descricao,
            'peso_porcento': atv.peso_porcento,
            'data_entrega': atv.data_entrega,
            'turma_id': atv.turma_id,
            'professor_id': atv.professor_id
        }), 200
    
    @app.route('/atividades', methods=['POST'])
    def create_atividade():
        """
        Cria uma nova atividade
        ---
        tags:
          - atividades
        summary: Registra uma nova atividade no sistema
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - nome_atividade
                - descricao
                - peso_porcento
                - data_entrega
                - turma_id
                - professor_id
              properties:
                nome_atividade:
                  type: string
                  example: "Prova de História"
                descricao:
                  type: string
                  example: "Avaliação sobre a Revolução Francesa"
                peso_porcento:
                  type: number
                  example: 25
                data_entrega:
                  type: string
                  format: date
                  example: "2025-11-05"
                turma_id:
                  type: integer
                  example: 2
                professor_id:
                  type: integer
                  example: 5
        responses:
            201:
              description: Atividade criada com sucesso
            400:
              description: Formato de data inválido
        """
        
        base = current_app.config["GERENCIAMENTO_BASE_URL"]
        dados = request.get_json()

        try:
            turma_id = int(dados['turma_id'])
            professor_id = int(dados['professor_id'])
        except (KeyError, ValueError, TypeError):
            return jsonify({'erro': 'O ID de Turma e Professor são obrigatórios e devem ser números inteiros.'}), 400

        try:
            resp_turma = requests.get(f"{base}/turmas/{turma_id}")
            resp_professor = requests.get(f"{base}/professores/{professor_id}")
        except requests.exceptions.RequestException:
            return jsonify({'erro': 'erro de comunicação com o microsserviço Gerenciamento.'}), 502
        
        if resp_turma.status_code == 404:
            return jsonify({'erro': f'Turma com id {turma_id} não encontrada.'}), 404
        elif resp_turma.status_code != 200:
            return jsonify({'erro': f'Falha de comunicação com o microsserviço de Gerenciamento. {resp_turma.status_code}'}), 502
        
        if resp_professor.status_code == 404:
            return jsonify({'erro': f'Professor com id {professor_id} não encontrado.'}), 404
        elif resp_professor.status_code != 200:
            return jsonify({'erro': f'Falha de comunicação com o microsserviço de Gerenciamento. {resp_professor.status_code}'}), 502  

        try:
            data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido! Digite no seguinte formato: AAAA-MM-DD. Exemplo: 2025-10-25'}), 400
        
        try:
            peso_porcento = float(dados['peso_porcento'])
        except ValueError:
            return jsonify({'erro': 'O percentual do peso da nota deve ser um número decimal!'}), 400

        atv = Atividades(
            nome_atividade=dados['nome_atividade'],
            descricao=dados['descricao'],
            peso_porcento=peso_porcento,
            data_entrega=data_entrega,
            turma_id=turma_id,
            professor_id=professor_id
        )

        db.session.add(atv)
        db.session.commit()

        return jsonify({'mensagem': 'Atividade criada!', 'id': atv.id}), 201
    
    @app.route('/atividades/<int:id>', methods=['PUT'])
    def update_atividade(id):
        """
        Atualiza uma atividade existente
        ---
        tags:
            - atividades
        summary: Atualiza os dados de uma atividade cadastrada
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID da atividade que será atualizada
            example: 1
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - nome_atividade
                - descricao
                - peso_porcento
                - data_entrega
                - turma_id
                - professor_id
              properties:
                nome_atividade:
                    type: string
                    example: "Prova de Matemática - Revisão"
                descricao:
                    type: string
                    example: "Revisão de conteúdos para a avaliação final"
                peso_porcento:
                    type: number
                    example: 30
                data_entrega:
                    type: string
                    format: date
                    example: "2025-11-20"
                turma_id:
                    type: integer
                    example: 3
                professor_id:
                    type: integer
                    example: 1
        responses:
            200:
              description: Atividade atualizada com sucesso
            400:
              description: Formato de data inválido
            404:
              description: Atividade não encontrada
        """

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'erro': 'Atividade não encontrada!'}), 404
        
        dados = request.get_json()
        base = current_app.config['GERENCIAMENTO_BASE_URL']
        
        try:
            turma_id = int(dados['turma_id'])
            professor_id = int(dados['professor_id'])
        except (KeyError, ValueError, TypeError):
            return jsonify({'erro': 'O ID de Turma e Professor são obrigatórios e devem ser números inteiros.'}), 400

        try:
            resp_turma = requests.get(f"{base}/turmas/{turma_id}")
            resp_professor = requests.get(f"{base}/professores/{professor_id}")
        except requests.exceptions.RequestException:
            return jsonify({'mensagem': 'erro de comunicação com o microsserviço Gerenciamento.'}), 502
        
        if resp_turma.status_code == 404:
            return jsonify({'erro': f'Turma com id {turma_id} não encontrada.'}), 404
        elif resp_turma.status_code != 200:
            return jsonify({'erro': 'Falha de comunicação com o microsserviço de Gerenciamento.'}), 502
        
        if resp_professor.status_code == 404:
            return jsonify({'erro': f'Professor com id {professor_id} não encontrado.'}), 404
        elif resp_professor.status_code != 200:
            return jsonify({'erro': 'Falha de comunicação com o microsserviço de Gerenciamento.'}), 502  

        try:
            data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido! Digite no seguinte formato: AAAA-MM-DD. Exemplo: 2025-10-25'}), 400
        
        try:
            peso_porcento = float(dados['peso_porcento'])
        except ValueError:
            return jsonify({'erro': 'O percentual do peso da nota deve ser um número decimal!'}), 400

        atv.nome_atividade = dados['nome_atividade']
        atv.descricao = dados['descricao']
        atv.peso_porcento = peso_porcento
        atv.data_entrega = data_entrega
        atv.turma_id = turma_id
        atv.professor_id = professor_id

        db.session.commit()

        return jsonify({'mensagem': 'Atividade atualizada com sucesso!'}), 200
    
    @app.route('/atividades/<int:id>', methods=['DELETE'])
    def delete_atividade(id):
        """
        Deleta uma Atividade existente
        ---
        tags:
          - atividades
        summary: Remove uma Atividade do banco de dados
        parameters:
          - in: path
            name: id
            schema: 
              type: integer
            required: true
        responses:
          200:
            description: Atividade deletada com sucesso
          404:
            description: Atividade não encontrada
        """

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'erro': 'Nenhuma atividade encontrada!'}), 404
        
        db.session.delete(atv)
        db.session.commit()

        return jsonify({'mensagem': 'Atividade deletada com sucesso!'}), 200
    

    @app.route('/notas', methods=['GET'])
    def get_notas():
        """
        Lista todas as notas
        ---
        tags:
          - notas
        summary: Lista todas as notas cadastradas
        responses:
          200:
            description: Lista de notas
          404:
            description: Nenhuma nota encontrada.
        """

        notas = Notas.query.all()
        if not notas:
            return jsonify({'erro': 'Nenhuma nota encontrada no sistema.'}), 404
        
        return jsonify([{
            'id': nota.id,
            'nota': nota.nota,
            'aluno_id': nota.aluno_id,
            'atividade_id': nota.atividade_id
        } for nota in notas]), 200
    
    @app.route('/notas/<int:id>', methods=['GET'])
    def get_nota(id):
        """
        Obtém uma Nota pelo ID
        ---
        tags:
          - notas
        summary: Recupera uma Nota específica
        parameters:
          - in: path
            name: id
            schema: 
              type: integer
            required: true
            description: ID da Nota
        responses:
          200:
            description: Nota encontrada
          404:
            description: Nota não encontrada
        """

        nota = Notas.query.get(id)
        if not nota:
            return jsonify({'erro': 'Nenhuma nota encontrada.'}), 404
        
        return jsonify({
            'id': nota.id,
            'nota': nota.nota,
            'aluno_id': nota.aluno_id,
            'atividade_id': nota.atividade_id
        }), 200
    
    @app.route('/notas', methods=['POST'])
    def create_nota():
        """
        Cria uma nova Nota
        ---
        tags:
          - notas
        summary: Registra uma nova Nota no sistema
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - nota
                - aluno_id
                - atividade_id
            properties:
              nota:
                type: float
                example: 7.5
              aluno_id:
                type: integer
                example: 2
              atividade_id:
                type: integer
                example: 5
        responses:
            201:
              description: Nota criada com sucesso
        """

        dados = request.get_json()
        base = current_app.config['GERENCIAMENTO_BASE_URL']

        try:
            aluno_id = int(dados['aluno_id'])
            atividade_id = int(dados['atividade_id'])
        except (KeyError, TypeError, ValueError):
            return jsonify({'erro': 'O ID do aluno e da atividade são obrigatórios e deves ser um número inteiro.'}), 400
        
        try:
            resp = requests.get(f'{base}/alunos/{aluno_id}')
        except requests.exceptions.RequestException:
            return jsonify({'erro': 'Erro de comunicação com o microsserviço de Gerenciamento.'}), 502
        
        if resp.status_code == 404:
            return jsonify({'erro': f'Aluno com ID {aluno_id} não foi encontrado.'}), 404
        elif resp.status_code != 200:
            return jsonify({'erro': 'Erro de comunicação com o microsserviço de Gerenciamento.'}), 502
        
        try:
            nota = float(dados['nota'])
        except ValueError:
            return jsonify({'erro': 'Nota inválida! Digite um número decimal.'}), 400
        
        atividade = Atividades.query.get(atividade_id)
        if not atividade:
            return jsonify({'erro': f'Atividade com o ID {atividade_id} não foi encontrada.'}), 404

        nota = Notas(
            nota=nota,
            aluno_id=aluno_id,
            atividade_id=atividade.id
        )

        db.session.add(nota)
        db.session.commit()

        return jsonify({'mensagem': 'Nota cadastrada com sucesso!'}), 201
    
    @app.route('/notas/<int:id>', methods=['PUT'])
    def update_nota(id):
        """
        Atualiza uma nota existente
        ---
        tags:
          - notas
        summary: Atualiza os dados de uma nota cadastrada
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID da nota que será atualizada
            example: 1
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - nota
                - aluno_id
                - atividade_id
              properties:
                nota:
                  type: number
                  example: 7.5
                aluno_id:
                  type: integer
                  example: 3
                atividade_id:
                  type: integer
                  example: 1
        responses:
            200:
              description: Nota atualizada com sucesso
            404:
              description: Nota não encontrada
        """

        base = current_app.config['GERENCIAMENTO_BASE_URL']
        nota = Notas.query.get(id)

        if not nota:
            return jsonify({'erro': 'Nota não encontrada!'}), 404
        
        dados = request.get_json()

        try:
            aluno_id = int(dados['aluno_id'])
            atividade_id = int(dados['atividade_id'])
        except ValueError:
            return jsonify({'erro': 'O ID do aluno e da atividade são obrigatórios e devem ser um número inteiro.'}), 400
        
        try:
            resp = requests.get(f'{base}/alunos/{aluno_id}')
        except requests.exceptions.RequestException:
            return jsonify({'erro': 'Erro de comunicação com o microsserviço de Gerenciamento.'}), 502
        
        if resp.status_code == 404:
            return jsonify({'erro': f'Aluno com ID {aluno_id} não foi encontrado.'}), 404
        elif resp.status_code != 200:
            return jsonify({'erro': 'Erro de comunicação com o microsserviço de Gerenciamento.'}), 502
        
        atividade = Atividades.query.get(atividade_id)
        if not atividade_id:
            return jsonify({'erro': f'Atividade com o ID {atividade_id} não foi encontrada.'}), 404
        
        try:
            nova_nota = float(dados['nota'])
        except ValueError:
            return jsonify({'erro': 'A nota do aluno deve ser um número decimal válido.'}), 400

        nota.nota = nova_nota
        nota.aluno_id = aluno_id
        nota.atividade_id = atividade.id

        db.session.commit()

        return jsonify({'mensagem': 'Nota atualizada com sucesso!'}), 200
    
    @app.route('/notas/<int:id>', methods=['DELETE'])
    def delete_nota(id):
        """
        Deleta uma Nota existente
        ---
        tags:
          - notas
        summary: Remove uma Nota do banco de dados
        parameters:
          - in: path
            name: id
            schema:
              type: integer
            required: true
        responses:
          200:
            description: Nota deletada com sucesso
          404:
            description: Nota não encontrada
        """

        nota = Notas.query.get(id)

        if not nota:
            return jsonify({'erro': 'Nota não encontrada no sistema!'}), 404
        
        db.session.delete(nota)
        db.session.commit()

        return jsonify({'mensagem': 'Nota deletada com sucesso!'}), 200