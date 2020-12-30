from requests import post, get

class ApiIntegracao(object):
    def __init__(self, id_cliente):
        self.base = 'http://apiadvisor.climatempo.com.br/api/v1'
        self.params = f'/forecast/locale/{id_cliente}/days/15?token={self.get_token()}'
        self.url = self.base+self.params

    def get_token(self):
        return open('./keys','r').read()

    def executa_url(self, method: str, data=None):
        if method.upper() == 'GET':
            return get(self.url)
        elif method.upper() == 'POST':
            return post(self.url, data=data)
        else:
            return "Metodo nao implementado"