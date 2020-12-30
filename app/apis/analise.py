from flask_restx import Namespace, Resource, fields, reqparse

api = Namespace('analise', description='Api com chamadas de analise no banco')

analise_parser = reqparse.RequestParser()
analise_parser.add_argument('data_inicial', type=str, help='String formato YYYY-MM-DD',
                            required=True)
analise_parser.add_argument('data_final', type=str, help='String formato YYYY-MM-DD',
                            required=True)

analise_model_request = api.model('AnaliseRequest',{
            'data_inicial':fields.String(required=True, description='Data inicio da analise'),
            'data_final':fields.String(required=True, description='Data fim da analise'),
})

analise_model_response = api.model('AnaliseResponse',{
        'cidade':fields.String,
        'temperatura_max': fields.Integer,
        'precipitacao_avg': fields.Float
})

@api.doc(params={'data_inicial':'String no formato YYYY-MM-DD'})
@api.doc(params={'data_final':'String no formato YYYY-MM-DD'})
class Analise(Resource):
    @api.doc('Cidade mais quente')
    @api.expect(analise_model_request)
    @api.marshal_with(analise_model_response)
    def get(self):
        args = analise_parser.parse_args()
        #retorno = db.analise(args['data_inicial'],args['data_final'])
        return 200

api.add_resource(Analise, '/api/v2/cidadesync', endpoint='analise_ep')
