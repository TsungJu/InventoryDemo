import os

class DevelopmentConfig:
    DATABASE_URL = os.environ['POSTGRESQLCONNSTR']
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'allow'
    SCHEME = 'http'
    API_SERVER = 'http://127.0.0.1:5000'

class DevelopmentConfigDocker:
    DATABASE_URL = os.environ['POSTGRESQLCONNSTR']
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'allow'
    SCHEME = 'http'
    API_SERVER = 'http://127.0.0.1:5000'

class ProductionConfig:
    DATABASE_URL = os.environ['POSTGRESQLCONNSTR']
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'require'
    SCHEME = 'https'
    API_SERVER = 'https://data-analyze-ml-toolset-backend.azurewebsites.net'

config = {
    'development' : DevelopmentConfig,
    'development-docker' : DevelopmentConfigDocker,
    'production' : ProductionConfig,
}