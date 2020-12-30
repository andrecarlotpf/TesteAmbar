from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse, fields
import requests
import database as db
import os.path
app = Flask(__name__)
api = Api(app)


class ApiIntegracao(object):
    def __init__(self, id_cliente):
        self.base = 'http://apiadvisor.climatempo.com.br/api/v1'
        self.params = f'/forecast/locale/{id_cliente}/days/15?token={self.get_token()}'
        self.url = self.base+self.params

    def get_token(self):
        return open('./keys','r').read()

    def executa_url(self, method: str, data=None):
        if method.upper() == 'GET':
            return requests.get(self.url)
        elif method.upper() == 'POST':
            return requests.post(self.url, data=data)
        else:
            return "Metodo nao implementado"


analise_parser = reqparse.RequestParser()
analise_parser.add_argument('data_inicial', type=str, help='String formato YYYY-MM-DD',
required=True)
analise_parser.add_argument('data_final', type=str, help='String formato YYYY-MM-DD',
required=True)

analise_model_response = api.model('AnaliseResponse',{
        'cidade':fields.String,
        'temperatura_max': fields.Integer,
        'precipitacao_avg': fields.Float
})
@api.doc(params={'data_inicial':'String no formato YYYY-MM-DD'})
@api.doc(params={'data_final':'String no formato YYYY-MM-DD'})
class Analise(Resource):
    @api.marshal_with(analise_model_response)
    def get(self):
        args = analise_parser.parse_args()
        retorno = db.analise(args['data_inicial'],args['data_final'])
        return retorno, 200



cidadesync_parser = reqparse.RequestParser()
cidadesync_parser.add_argument('id_cidade', type=int, help='Id da cidade para sincronizar',
required=True)

cidadesync_model_request = api.model('CidadeSyncRequest',{
        'id_cidade': fields.Integer
})

@api.doc(params={'id_cidade':'Id da cidade a sincronizar'})
class CidadeSync(Resource):
    @api.marshal_with(cidadesync_model_request)
    def post(self):
        args = cidadesync_parser.parse_args()
        
        if args['id_cidade']:
            api_integracao = ApiIntegracao(args['id_cidade'])
            response = api_integracao.executa_url(method='GET')
            
            if db.insert_into_db(response.json()):
                return 200
        else:
            return "Erro"


api.add_resource(CidadeSync, '/api/v2/cidade', endpoint='cidade_ep')
api.add_resource(Analise, '/api/v2/analise', endpoint='analise_ep')

if __name__ == '__main__':
    if os.path.isfile('./database/webservice.db'):
        pass
    else:
        db.create_database()
    app.run(debug=True)