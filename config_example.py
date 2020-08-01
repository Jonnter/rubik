import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config():
    # MySQL setting like:
    DB_ENGINE = 'mysql'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'rubik'
    DB_PASSWORD = '123456'
    DB_NAME = 'rubik'
    DB_OPTIONS = {
        "unix_socket": "/var/run/mysqld/mysqld.sock",
    }

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    HTTP_BIND_HOST = '0.0.0.0'
    HTTP_LISTEN_PORT = 8080

    # Development env open this, when error occur display the full process track, Production disable it
    DEBUG = True

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    LOG_LEVEL = 'DEBUG'
    LOG_DIR = os.path.join(BASE_DIR, 'logs')

    # Use Redis as broker for celery and web socket
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''
    BROKER_URL = 'redis://%(password)s%(host)s:%(port)s/15' % {
        'password': REDIS_PASSWORD,
        'host': REDIS_HOST,
        'port': REDIS_PORT,
    }

    # vpn file path
    OPENVPN_FILE = '/etc/openvpn/psw-file'

    # Email config
    EMAIL_HOST = 'smtp.163.com'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = '****'
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = False
    EMAIL_SUBJECT_PREFIX = '[rubik]'

config = Config()


