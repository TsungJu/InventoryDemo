
class DevelopmentConfig:
    DATABASE_URL = 'postgres://qdmzygkpespeaf:33c15fbd604ee23e55421bb0dae653b769e3b1222765f51ce018690bb56b3539@localhost:5432/d87gbe1ta420fb'
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'allow'
    SCHEME = 'http'

class DevelopmentConfigDocker:
    DATABASE_URL = 'postgres://qdmzygkpespeaf:33c15fbd604ee23e55421bb0dae653b769e3b1222765f51ce018690bb56b3539@postgres-dev:5432/d87gbe1ta420fb'
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'allow'
    SCHEME = 'http'

class ProductionConfig:
    DATABASE_URL = 'postgres://qdmzygkpespeaf:33c15fbd604ee23e55421bb0dae653b769e3b1222765f51ce018690bb56b3539@ec2-18-213-133-45.compute-1.amazonaws.com:5432/d87gbe1ta420fb'
    SECRET_KEY = 'eb6ecd808fcc342793df99a753ed7292'
    SSL_MODE = 'require'
    SCHEME = 'https'

config = {
    'development' : DevelopmentConfig,
    'development_docker' : DevelopmentConfigDocker,
    'production' : ProductionConfig,
}