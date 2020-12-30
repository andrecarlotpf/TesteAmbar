from flask_restx import Api

from .analise import api as analise_api
from .cidade_sync import api as cidade_sync_api



api = Api(
    title='Api Projeto Ambar',
    version='2.0'
    )

api.add_namespace(analise_api)
api.add_namespace(cidade_sync_api)