import os

class DevelopmentConfig:
    DATABASE_URL = os.environ['POSTGRESQLCONNSTR']
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'allow'
    SCHEME = 'http'

class DevelopmentConfigDocker:
    DATABASE_URL = os.environ['POSTGRESQLCONNSTR']
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'allow'
    SCHEME = 'http'

class ProductionConfig:
    DATABASE_URL = os.environ['POSTGRESQLCONNSTR']
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'require'
    SCHEME = 'https'

config = {
    'development' : DevelopmentConfig,
    'development-docker' : DevelopmentConfigDocker,
    'production' : ProductionConfig,
}