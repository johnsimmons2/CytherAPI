import os
from dotenv import load_dotenv
from flask import Flask, request
from flask.wrappers import Request, Response
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_socketio import SocketIO
from sqlalchemy.engine import URL
from api.controller import campaigncontroller
from api.loghandler.logger import Logger
from api.loghandler.formatted import FormattedLogHandler
from api.service.config import config, set_config_path
from api.controller.usercontroller import users
from api.controller.charactercontroller import characters
from api.controller.racecontroller import race
from api.controller.featcontroller import feats
from api.controller.classcontroller import classes
from api.controller.skillscontroller import skills
from api.controller.spellcontroller import spells
from api.controller.authcontroller import auth
from api.controller.socketcontroller import wsocket
from api.controller.campaigncontroller import campaigns
from api.controller.ext_contentcontroller import ext_content
from api.controller.notecontroller import notes
from api.model.user import User, UserRole, UserRequest, UserCharacters
from api.model.note import Note, Tag, NoteSharedUsers, NoteTags, TagSharedUsers
from api.service.dbservice import RoleService, UserService
from api.service.repo.skillservice import SkillService
from api.service.repo.statsheetservice import StatsheetService
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

app.register_blueprint(users, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(characters, url_prefix='/api')
app.register_blueprint(campaigns, url_prefix='/api')
app.register_blueprint(race, url_prefix='/api')
app.register_blueprint(feats, url_prefix='/api')
app.register_blueprint(classes, url_prefix='/api')
app.register_blueprint(skills, url_prefix='/api')
app.register_blueprint(spells, url_prefix='/api')
app.register_blueprint(wsocket, url_prefix='/api')
app.register_blueprint(notes, url_prefix='/api')

monkey.patch_all()

# Register external content
app.register_blueprint(ext_content, url_prefix='/api')

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
envPort = os.getenv('PORT')
apiVersion = os.getenv('API_VERSION')

Logger.debug("API Version: " + str(apiVersion))

if envPort is None:
  envPort = 5000

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
    db.session.commit()
    RoleService.initRoles()
    UserService.initUsers()
    SkillService.initBaseSkills()
    StatsheetService.initSavingThrows()

if __name__ == "__main__":
    Logger.debug("Starting Cyther-API on port " + str(envPort))

    if os.getenv('ENVIRONMENT') != 'production':
        Logger.warn("Cyther-API is running on [" + str(os.getenv('ENVIRONMENT')) + "]")
    
    # socketio.run(app, host='0.0.0.0', port=envPort)
    http_server = WSGIServer(('0.0.0.0', envPort), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
