from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from ERICA import KInit, log

DB_URI = postgres://dnldonok:TJjru0b0Vm86ApLkQsprkb0ETKFRjdXI@tyke.db.elephantsql.com/dnldonok


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8", echo=KInit.DEBUG)
    log.info("[PostgreSQL] Connecting to database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION: scoped_session = start()
except Exception as e:
    log.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
log.info("[PostgreSQL] Connection successful, session started.")
