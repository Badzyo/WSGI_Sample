from ..config import config
from . import postgres


DB_MANAGERS_MAP = {
    'postgres': postgres.PGManager
}

db = DB_MANAGERS_MAP[config.server.db]()
