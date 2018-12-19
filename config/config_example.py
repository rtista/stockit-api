class Config:
    '''
    Configuration class to hold all configurations for the API.
    '''
    # Application name
    APP_NAME = 'Inventory API'

    # Debugging Mode
    DEBUG = True


class DevelopmentConfig(Config):
    '''
    Configuration for the development environment.
    '''
    # Debugging Mode
    DEBUG = True

    # Server listening config
    SERVER = {
        'url': '0.0.0.0',
        'port': 8000
    }

    # ActiveMQ connection configuration
    MYSQL = {
        'engine': 'mysql+mysqldb',
        'username': 'inventory_user',
        'password': 'inventory_pass',
        'host': '127.0.0.1',
        'port': 3306,
        'dbname': 'inventory_app'
    }
    
    # Token lifetime is 3 hours
    TOKEN_LIFE = 10800


class StagingConfig(Config):
    '''
    Configuration for the staging environment.
    '''
    # Debugging Mode
    DEBUG = True
    
    # Token lifetime is 2 hours
    TOKEN_LIFE = 7200


class ProductionConfig(Config):
    '''
    Configuration for the production environment.
    '''
    # Debugging Mode
    DEBUG = False
    
    # Token lifetime is 1 hour
    TOKEN_LIFE = 3600
