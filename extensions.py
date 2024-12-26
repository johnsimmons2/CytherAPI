
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from api.loghandler.formatted import FormattedLogHandler
from api.loghandler.logger import Logger


ORIGINS = ["https://cyther.online", "http://127.0.0.1", "http://localhost:8100"]

Logger.config_set_handler(FormattedLogHandler().set_color_dates(True))

cors = CORS(resources={r"/*": {"origins": ORIGINS}}, supports_credentials=True)
db =  SQLAlchemy()
socketio = SocketIO(cors_allowed_origins=ORIGINS)
mail = Mail()