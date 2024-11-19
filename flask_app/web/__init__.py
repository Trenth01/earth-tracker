from flask import Flask
from flask_restful import Api
from .db_admin import *
from .db_controller import *

API = "api"
DB_RESOURCES = f'/{API}/postgresql'


class LocalConfig:
    DEBUG = True
    HOST = 'localhost'
    PORT = '5000'


def init_routes(api: Api) -> None:
    api.add_resource(DatabaseHealthResource, f'{DB_RESOURCES}/health', f'{DB_RESOURCES}')
    api.add_resource(DatabaseGuestsResource, f'{DB_RESOURCES}/guests')
    api.add_resource(DatabaseGuestIdResource, f'{DB_RESOURCES}/guests/<int:guest_id>')
    api.add_resource(DatabaseInitResource, f'{DB_RESOURCES}/init')
    api.add_resource(DatabaseFlushRestartResource, f'{DB_RESOURCES}/flush-restart')


def init_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config.from_object(LocalConfig())

    api = Api(app)

    init_routes(api)

    return app
