from flask import Flask
from .config.config import config
#import psycopg2

config_name = 'production'
app = Flask(__name__)
app.config.from_object(config[config_name])

#conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
#cursor = conn.cursor()