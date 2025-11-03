from flask import current_app
from flask_restx import Namespace, Resource, fields
from .__init__ import db
from .models import Reserva
from .schemas import reserva_schema, reservas_schema
import requests


GERENCIAMENTO_URL = current_app.config.get('GERENCIAMENTO_SERVICE_URL')

reserva_ns = Namespace('reservas', description='Operações CRUD de Reservas de Salas')

reserva_model = reserva_ns.model('Reserva', {
    'num_sala': fields.String(required=True),
    'lab': fields.Boolean(default=False),
    'data': fields.Date(required=True, example='YYYY-MM-DD'),
    'turma_id': fields.Integer(required=True, description='ID da Turma para vincular a reserva')
})

@reserva_ns.route('/')
class ReservaList(Resource):
    def get(self):
        reservas = Reserva.query.all()
        return reservas_schema.dump(reservas), 200

    @reserva_ns.expect(reserva_model, validate=True)
    def post(self):
        data = reserva_ns.payload
        turma_id = data['turma_id']

        try:
            
            response = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}")
            
            if response.status_code == 404:
                return {'message': f"Turma com ID {turma_id} não encontrada no Gerenciamento-Service."}, 404
            if response.status_code != 200:
                
                return {'message': f"Erro ao comunicar com o Gerenciamento-Service. Status: {response.status_code}"}, 503

        except requests.exceptions.ConnectionError:
            return {'message': "Falha na conexão com o Gerenciamento-Service."}, 503

        try:
            nova_reserva = Reserva(**reserva_schema.load(data))
            db.session.add(nova_reserva)
            db.session.commit()
            return reserva_schema.dump(nova_reserva), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

@reserva_ns.route('/<int:id>')
@reserva_ns.param('id', 'ID da Reserva')
class ReservaResource(Resource):
    def get(self, id):
        reserva = Reserva.query.get_or_404(id)
        return reserva_schema.dump(reserva), 200
        
    def delete(self, id):
        reserva = Reserva.query.get_or_404(id)
        db.session.delete(reserva)
        db.session.commit()
        return '', 204
    
    @reserva_ns.expect(reserva_model, validate=False)
    def put(self, id):
        reserva = Reserva.query.get_or_404(id)
        try:
            data = reserva_schema.load(reserva_ns.payload, partial=True)
            for key, value in data.items():
                setattr(reserva, key, value)
            db.session.commit()
            return reserva_schema.dump(reserva), 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

