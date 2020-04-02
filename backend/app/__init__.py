from flask import Flask
from .config import DevConfig
from flask_mongoalchemy import MongoAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['MONGOALCHEMY_DATABASE'] = DevConfig.MONGO_URI
db = MongoAlchemy(app)

from .models import PlanningResult, Emergency
from . import routes
migrate = Migrate(app, db)