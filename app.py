import os
from flask import Flask, request
from flask_cors import CORS
from sqlalchemy.engine import URL
from api.loghandler.logger import Logger
from api.loghandler.formatted import FormattedLogHandler
from api.service.config import config, set_config_path
from api.controller.usercontroller import users
from api.controller.charactercontroller import characters
from api.model import db
from api.model.user import User
from api.service.dbservice import RoleService


# Setup logger
Logger.config_set_handler(FormattedLogHandler().set_color_dates(True))

# Create app
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Register routes

app.register_blueprint(users)
app.register_blueprint(characters)

# Register db
set_config_path(os.path.dirname(os.path.realpath(__file__)))


dburl = os.getenv('DATABASE_URL')
if dburl is not None:
  app.config['SQLALCHEMY_DATABASE_URI'] = dburl
else:
  cfg = config()
  uri = URL.create(cfg['drivername'],
                  cfg['username'],
                  cfg['password'],
                  cfg['host'],
                  cfg['port'],
                  cfg['database'])
  app.config['SQLALCHEMY_DATABASE_URI'] = uri

db.init_app(app)

# Logging middleware

@app.before_request
def before_request():
    Logger.debug(f"Request: {request.method} {request.path}")

@app.after_request
def after_request(response):
    Logger.debug(f"Response: {response.status_code}")
    return response


with app.app_context():
    db.create_all()
    db.session.commit()
    RoleService.initRoles()

