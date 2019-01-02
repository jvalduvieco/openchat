import os

from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import Injector

from apps.RESTAPI.command_handlers import user_command_handlers
from apps.RESTAPI.controllers import openchat_controllers
from apps.RESTAPI.dependency_injection_modules import user, core
from apps.RESTAPI.error_handler import handle_invalid_usage
from apps.RESTAPI.tools import register_command_handlers
from domain.misc import CommandBus, EventBus


def create_openchat_app(config=None, environment=None):
    openchat = Flask(__name__)
    injector = Injector()
    openchat.config.update(config or {})
    openchat.config['ENV'] = environment
    openchat.config['TESTING'] = True if environment != 'production' else False
    openchat.config['DEBUG'] = True if environment != 'production' else False
    CORS(openchat, resources={r"/*": {"origins": "*"}})
    openchat.register_blueprint(openchat_controllers)
    FlaskInjector(app=openchat, injector=injector, modules=[core, user])
    register_command_handlers(injector, injector.get(CommandBus), injector.get(EventBus),
                              modules=[user_command_handlers])
    openchat.register_error_handler(ValueError, handle_invalid_usage)
    return openchat


if __name__ == "__main__":
    config = {
        'SERVER_NAME': "%s:%s" % (os.environ.get('LISTEN', 'localhost'), os.environ.get('PORT', 8080)),
    }
    app = create_openchat_app(config=config, environment=os.environ.get('ENV', 'development'))
    app.run()
