from flask import Flask
from flask_restx import Resource, Api, reqparse, fields
import database as db

app = Flask(__name__)
api = Api(app)


#api.add_resource(CidadeSync, '/api/v2/cidade', endpoint='cidade_ep')


parser = reqparse.RequestParser()
parser.add_argument('id_cidade', type=int, help='Id da cidade para sincronizar',
required=True)

analise_parser = reqparse.RequestParser()
analise_parser.add_argument('data_inicial', type=str, help='String formato YYYY-MM-DD',
required=True)
analise_parser.add_argument('data_final', type=str, help='String formato YYYY-MM-DD',
required=True)

analise = api.model('Analise',{
        'cidade':fields.String,
        'temperatura_max': fields.Integer,
        'precipitacao_avg': fields.Float
})


@api.route('/api/v2/analise', endpoint='analise_ep')
@api.doc(params={'data_inicial':'String no formato YYYY-MM-DD'})
@api.doc(params={'data_final':'String no formato YYYY-MM-DD'})
class Analise(Resource):
    @api.marshal_with(analise)
    def post(self):
        args = analise_parser.parse_args()
        retorno = db.analise(args['data_inicial'],args['data_final'])
        return retorno, 200


@api.route('/api/v2/cidade', endpoint='cidade_ep')
class CidadeSync(Resource):

    def get(self):
        return {'Get':'Ok'}, 201

    def post(self):
        args = parser.parse_args()
        return {1:args['id_cidade']}



if __name__ == '__main__':
    app.run(debug=True)