import os
from dotenv import load_dotenv

load_dotenv()

__ENV = os.getenv('ENV', 'development').upper()

IS_PRODUCTION = __ENV == "PRODUCTION"
IS_LOCAL = __ENV == "LOCAL"
__DB_CRED = os.getenv('DB_CRED' if IS_PRODUCTION else "TEST_DB_CRED").split(":")
DB_HOST = __DB_CRED[0]
DB_PORT = __DB_CRED[1]
DB_USER = __DB_CRED[2]
DB_PASSWORD = __DB_CRED[3]
DB_NAME = __DB_CRED[4]

LOG_DIR = os.getenv('LOG_DIR', 'logs')