from flask import request, jsonify
from Model.professor_model import Professor
from Model.aluno_model import Aluno
from Model.turma_model import Turma
from Model.database import db
from datetime import datetime

def setup_routes(app):

   

    @app.route('/professores', methods=['GET'])
    def list_professores():
        """
        Lista os professores
        ---
        tags:
          - Professores
        summary: Lista todos os professores
        responses:
          200:
            description: Lista de professores
        """
        professores = Professor.query.all()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'materia': p.materia,
            'observacoes': p.observacoes
        } for p in professores])

    @app.route('/professores/<int:id>', methods=['GET'])
    def get_professor(id):
        """
        Obtém um Professor pelo ID
        ---
        tags:
          - professor
        summary: Recupera um professor específico
        parameters:
          - in: path
            name: id
            schema:
              type: integer
            required: true
            description: ID da professor
        responses:
          200:
            description: Professor encontrado
          404:
            description: Professor não encontrado
        """

        prof = Professor.query.get(id)
        if not prof:
            return jsonify({'erro': 'Professor não encontrado.'}), 404
        
        return jsonify({
            'id': prof.id,
            'nome': prof.nome,
            'idade': prof.idade,
            'materia': prof.materia,
            'observacoes': prof.observacoes
            }), 200
    
    @app.route('/professores', methods=['POST'])
    def create_professor():
        """
        Cria um novo professor
        ---
        tags:
          - Professores
        summary: Cria um novo professor
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  nome: { type: string }
                  idade: { type: integer }
                  materia: { type: string }
                  observacoes: { type: string }
        responses:
          201:
            description: Professor criado com sucesso
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        professor = Professor(
            nome=data['nome'],
            idade=int(data['idade']),
            materia=data['materia'],
            observacoes=data.get('observacoes', '')
        )
        db.session.add(professor)
        db.session.commit()
        return jsonify({'message': 'Professor criado', 'id': professor.id}), 201

    @app.route('/professores/<int:id>', methods=['PUT'])
    def update_professor(id):
        """
        Atualiza um professor existente
        ---
        tags:
          - Professores
        summary: Atualiza um professor existente
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
            description: ID do professor
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  nome: { type: string }
                  idade: { type: integer }
                  materia: { type: string }
                  observacoes: { type: string }
        responses:
          200:
            description: Professor atualizado
          404:
            description: Professor não encontrado
        """
        professor = Professor.query.get_or_404(id)
        data = request.get_json()
        professor.nome = data['nome']
        professor.idade = int(data['idade'])
        professor.materia = data['materia']
        professor.observacoes = data.get('observacoes', '')
        db.session.commit()
        return jsonify({'message': 'Professor atualizado'})

    @app.route('/professores/<int:id>', methods=['DELETE'])
    def delete_professor(id):
        """
        Deleta um professor existente
        ---
        tags:
          - Professores
        summary: Deleta um professor existente
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
            description: ID do professor
        responses:
          200:
            description: Professor deletado
          404:
            description: Professor não encontrado
        """
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'message': 'Professor deletado'})


    # ------------------ CRUD Turmas ------------------

    @app.route('/turmas', methods=['GET'])
    def list_turmas():
        """
        Lista todas as turmas
        ---
        tags:
          - Turmas
        summary: Lista todas as turmas
        responses:
          200:
            description: Lista de turmas
        """
        turmas = Turma.query.all()
        return jsonify([{
            'id': t.id,
            'descricao': t.descricao,
            'professor_id': t.professor_id,
            'ativo': t.ativo
        } for t in turmas])
    
    @app.route('/turmas/<int:id>', methods=['GET'])
    def get_turma(id):
      """
      Busca uma turma pelo ID
      ---
      tags:
        - Turmas
      summary: Obtém uma turma específica pelo ID
      parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: ID da turma
      responses:
        200:
          description: Detalhes da turma
        404:
          description: Turma não encontrada
      """
      turma = Turma.query.get(id)
      if not turma:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

      return jsonify({
          'id': turma.id,
          'descricao': turma.descricao,
          'professor_id': turma.professor_id,
          'ativo': turma.ativo
      }), 200


    @app.route('/turmas', methods=['POST'])
    def create_turma():
        """
        Cria uma nova turma
        ---
        tags:
          - Turmas
        summary: Cria uma nova turma
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  descricao: { type: string }
                  professor_id: { type: integer }
                  ativo: { type: boolean }
        responses:
          201:
            description: Turma criada
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        turma = Turma(
            descricao=data['descricao'],
            professor_id=int(data['professor_id']),
            ativo=data.get('ativo', True)
        )
        db.session.add(turma)
        db.session.commit()
        return jsonify({'message': 'Turma criada', 'id': turma.id}), 201

    @app.route('/turmas/<int:id>', methods=['PUT'])
    def update_turma(id):
        """
        Atualiza uma turma existente
        ---
        tags:
          - Turmas
        summary: Atualiza uma turma existente
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
                  descricao: { type: string }
                  professor_id: { type: integer }
                  ativo: { type: boolean }
        responses:
          200:
            description: Turma atualizada
          404:
            description: Turma não encontrada
        """
        turma = Turma.query.get_or_404(id)
        data = request.get_json()
        turma.descricao = data['descricao']
        turma.professor_id = int(data['professor_id'])
        turma.ativo = data.get('ativo', True)
        db.session.commit()
        return jsonify({'message': 'Turma atualizada'})

    @app.route('/turmas/<int:id>', methods=['DELETE'])
    def delete_turma(id):
        """
        Deleta uma turma existente
        ---
        tags:
          - Turmas
        summary: Deleta uma turma existente
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        responses:
          200:
            description: Turma deletada
          404:
            description: Turma não encontrada
        """
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma deletada'})


   

    @app.route('/alunos', methods=['GET'])
    def list_alunos():
        """
        Lista todos os alunos
        ---
        tags:
          - Alunos
        summary: Lista todos os alunos
        responses:
          200:
            description: Lista de alunos
        """
        alunos = Aluno.query.all()
        return jsonify([{
            'id': a.id,
            'nome': a.nome,
            'idade': a.idade,
            'turma_id': a.turma_id,
            'data_nascimento': a.data_nascimento.isoformat(),
            'nota_primeiro_semestre': a.nota_primeiro_semestre,
            'nota_segundo_semestre': a.nota_segundo_semestre,
            'media_final': a.media_final
        } for a in alunos])

    @app.route('/alunos/<int:id>', methods=['GET'])
    def get_aluno(id):
        
        
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'erro': 'Aluno não encontrado!'}), 404
        
        return jsonify({
            'id': aluno.id,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'turma_id': aluno.turma_id,
            'data_nascimento': aluno.data_nascimento.isoformat(),
            'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
            'nota_segundo_semestre': aluno.nota_segundo_semestre,
            'media_final': aluno.media_final
        })

    @app.route('/alunos', methods=['POST'])
    def create_aluno():
        """
        Cria um novo aluno
        ---
        tags:
          - Alunos
        summary: Cria um novo aluno
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  nome: { type: string }
                  idade: { type: integer }
                  turma_id: { type: integer }
                  data_nascimento: { type: string, format: date }
                  nota_primeiro_semestre: { type: number }
                  nota_segundo_semestre: { type: number }
                  media_final: { type: number }
        responses:
          201:
            description: Aluno criado
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        aluno = Aluno(
            nome=data['nome'],
            idade=int(data['idade']),
            turma_id=int(data['turma_id']),
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            nota_primeiro_semestre=float(data['nota_primeiro_semestre']),
            nota_segundo_semestre=float(data['nota_segundo_semestre']),
            media_final=float(data['media_final'])
        )
        db.session.add(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno criado', 'id': aluno.id}), 201

    @app.route('/alunos/<int:id>', methods=['PUT'])
    def update_aluno(id):
        """
        Atualiza um aluno existente
        ---
        tags:
          - Alunos
        summary: Atualiza um aluno existente
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
                  nome: { type: string }
                  idade: { type: integer }
                  turma_id: { type: integer }
                  data_nascimento: { type: string, format: date }
                  nota_primeiro_semestre: { type: number }
                  nota_segundo_semestre: { type: number }
                  media_final: { type: number }
        responses:
          200:
            description: Aluno atualizado
          404:
            description: Aluno não encontrado
        """
        aluno = Aluno.query.get_or_404(id)
        data = request.get_json()
        aluno.nome = data['nome']
        aluno.idade = int(data['idade'])
        aluno.turma_id = int(data['turma_id'])
        aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        aluno.nota_primeiro_semestre = float(data['nota_primeiro_semestre'])
        aluno.nota_segundo_semestre = float(data['nota_segundo_semestre'])
        aluno.media_final = float(data['media_final'])
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado'})

    @app.route('/alunos/<int:id>', methods=['DELETE'])
    def delete_aluno(id):
        """
        Deleta um aluno existente
        ---
        tags:
          - Alunos
        summary: Deleta um aluno existente
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        responses:
          200:
            description: Aluno deletado
          404:
            description: Aluno não encontrado
        """
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno deletado'})