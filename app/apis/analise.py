from flask_restx import Namespace, Resource, fields, reqparse
from .database import analise_temperatura, analise_media_precipitacao

api = Namespace('analise', description='Api com chamadas de analise no banco')

analise_parser = reqparse.RequestParser()
analise_parser.add_argument('data_inicial', type=str, help='String formato YYYY-MM-DD',
                            required=True)
analise_parser.add_argument('data_final', type=str, help='String formato YYYY-MM-DD',
                            required=True)


@api.doc(params={'data_inicial':'String no formato YYYY-MM-DD'})
@api.doc(params={'data_final':'String no formato YYYY-MM-DD'})
@api.response(400, 'Faltando parametros da request')
class AnaliseTemperatura(Resource):
    def get(self):
        args = analise_parser.parse_args()
        if args['data_inicial'] <= args['data_final']:
            retorno = analise_temperatura(args['data_inicial'],args['data_final'])
            return retorno, 200
        else:
            api.abort(400, 'Data de inicio > Data fim')

@api.doc(params={'data_inicial':'String no formato YYYY-MM-DD'})
@api.doc(params={'data_final':'String no formato YYYY-MM-DD'})
@api.response(400, 'Faltando parametros da request')
class AnaliseMediaPrecipitacao(Resource):
    def get(self):
        args = analise_parser.parse_args()
        if args['data_inicial'] <= args['data_final']:
            retorno = analise_media_precipitacao(args['data_inicial'],args['data_final'])
            return retorno, 200
        else:
            api.abort(400, 'Data de inicio > Data fim')


api.add_resource(AnaliseTemperatura, '/api/v2/analisetemperatura', endpoint='analisetemperatura_ep')
api.add_resource(AnaliseMediaPrecipitacao, '/api/v2/analisemediaprecipitacao', endpoint='analisemediaprecipitacao_ep')
