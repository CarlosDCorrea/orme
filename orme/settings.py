import os


DATABASE_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orme.db')
MIGRATIONS_BASE_PATH = os.path.abspath(os.path.dirname(__file__))

APPS = [
    'expense',
    'debt'
]
