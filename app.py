import os
from dotenv import load_dotenv
from flask import Flask, request
from flask.wrappers import Response
from sqlalchemy.engine import URL
from api.loghandler.logger import Logger
from api.service.config import config, set_config_path
from api.controller.usercontroller import users as users_blueprint
from api.controller.charactercontroller import characters as characters_blueprint
from api.controller.racecontroller import race as race_blueprint
from api.controller.featcontroller import feats as feats_blueprint
from api.controller.classcontroller import classes as classes_blueprint
from api.controller.skillscontroller import skills as skills_blueprint
from api.controller.spellcontroller import spells as spells_blueprint
from api.controller.authcontroller import auth as auth_blueprint
from api.controller.socketcontroller import wsocket as wsocket_blueprint
from api.controller.campaigncontroller import campaigns as campaigns_blueprint
from api.controller.ext_contentcontroller import ext_content as ext_content_blueprint
from api.controller.itemscontroller import items as items_blueprint
from api.controller.notecontroller import notes as notes_blueprint
from api.service.dbservice import RoleService, UserService
from api.service.repo.abilityservice import AbilityService
from api.service.repo.conditionsservice import ConditionsService
from api.service.repo.damagetypesservice import DamageTypeService
from api.service.repo.featservice import FeatService
from api.service.repo.languageservice import LanguageService
from api.service.repo.noteservice import NoteService
from api.service.repo.skillservice import SkillService
from api.service.repo.statsheetservice import StatsheetService
from api.model import *
from extensions import db, cors, socketio, mail
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

# app.py
load_dotenv()
# Setup logger

# Create app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Register routes

app.register_blueprint(users_blueprint, url_prefix='/api')
app.register_blueprint(characters_blueprint, url_prefix='/api')
app.register_blueprint(race_blueprint, url_prefix='/api')
app.register_blueprint(feats_blueprint, url_prefix='/api')
app.register_blueprint(classes_blueprint, url_prefix='/api')
app.register_blueprint(skills_blueprint, url_prefix='/api')
app.register_blueprint(spells_blueprint, url_prefix='/api')
app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(wsocket_blueprint, url_prefix='/api')
app.register_blueprint(campaigns_blueprint, url_prefix='/api')
app.register_blueprint(ext_content_blueprint, url_prefix='/api')
app.register_blueprint(items_blueprint, url_prefix='/api')
app.register_blueprint(notes_blueprint, url_prefix='/api')

monkey.patch_all()

# Register external content

# Register mailtrap client
app.config['MAIL_SERVER'] = 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = os.getenv('MAILTRAP_TOKEN')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('ADMIN_EMAIL')

set_config_path(os.path.dirname(os.path.realpath(__file__)))

dburl = os.getenv('DATABASE_URL')
envPort = int(os.getenv('PORT', 5000))
apiVersion = os.getenv('API_VERSION')

Logger.debug("API Version: " + str(apiVersion))
Logger.debug("Environment Port: " + str(envPort))

if dburl is not None:

  dburl = dburl.replace("postgres://", "postgresql://", 1)
  Logger.debug("Using database URL: " + str(dburl))


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
  Logger.debug("Using local database URL: " + str(uri))
  
mail.init_app(app)
Logger.debug("Mailtrap: " + str(os.getenv('ADMIN_EMAIL')) + " " + str(os.getenv('MAILTRAP_TOKEN')))
socketio.init_app(app)
Logger.debug("SocketIO configured")
cors.init_app(app)
Logger.debug("CORS Configured")
db.init_app(app)
Logger.debug("Database configured")


# Logging middleware
@app.before_request
def before_request():
    Logger.debug(f"Request: {request.method} {request.path}")

@app.after_request
def after_request(response: Response):
    if 200 <= response.status_code < 300:
      Logger.debug(f"Response: {response.status_code}")
    else:
      Logger.error(f"Response: {response.status_code}\t{response.response}")
    return response


with app.app_context():
    RoleService.initRoles()
    UserService.initUsers()
    AbilityService.init_default_abilities()
    DamageTypeService.init_default_damage_types()
    SkillService.init_default_skills()
    ConditionsService.init_default_conditions()
    LanguageService.init_default_languages()
    NoteService.init_default_tags()
    db.session.commit()
    
if __name__ == "__main__":
    Logger.debug("Starting Cyther-API on port " + str(envPort))

    if os.getenv('ENVIRONMENT') != 'production':
        Logger.warn("Cyther-API is running on [" + str(os.getenv('ENVIRONMENT')) + "]")
    
    # socketio.run(app, host='0.0.0.0', port=envPort)
    http_server = WSGIServer(('0.0.0.0', envPort), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
