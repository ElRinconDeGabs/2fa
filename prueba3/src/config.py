class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'Gabs'
    MYSQL_PASSWORD = 'Wq)Ywlv1v)ksdB5f'
    MYSQL_DB = 'gabs'
    
config = {
    'development': DevelopmentConfig
}
