from flask import Flask
from apis import api
import os.path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/webservice2.db'
api.init_app(app)


if os.path.isfile('./database/webservice2.db'):
    pass
else:
    pass
app.run(debug=True)