import os


DATABASE_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orme.db')
MIGRATIONS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db/migrations/files')

QUERY_CREATE = 1
QUERY_LIST = 2
QUERY_UPDATE = 3
QUERY_DELETE = 4
QUERY_GET = 5
