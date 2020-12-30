from flask_restx import Namespace, Resource, fields, reqparse
from .api_integracao import ApiIntegracao

api = Namespace('cidadesync', description='Operacoes de sincronizacao')

cidadesync_model_request = api.model('CidadeSyncRequest',{
        'id_cidade' : fields.Integer(required=True, 
                                    description='Id da cidade que sera sincronizado')
})

cidadesync_parser = reqparse.RequestParser()
cidadesync_parser.add_argument('id_cidade', type=int, help='Id da cidade para sincronizar',
required=True)

@api.doc(params={'id_cidade':'Id da cidade a sincronizar'})
class CidadeSync(Resource):

    @api.expect(cidadesync_model_request)
    @api.response(404,'Cidade nao encontrada')
    def post(self):
        args = cidadesync_parser.parse_args()
        
        if args['id_cidade']:
            api_integracao = ApiIntegracao(args['id_cidade'])
            response = api_integracao.executa_url(method='GET')
            
            return response.json()
            
        else:
            return "Erro"

api.add_resource(CidadeSync, '/api/v2/cidadesync', endpoint='cidade_ep')