import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from os.path import isdir, join
# from wave.base import app_context

db_folder = join(os.getenv('USERPROFILE'), 'wave-data', 'db')
if not isdir(db_folder):
    os.mkdir(db_folder)

SQLALCHEMY_DATABASE_URL = "sqlite:///" + join(db_folder, 'database.db')
engine = _sql.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# conn = sqlite.connect('database.db')
# c = conn.cursor()
# c.execute("PRAGMA key='youWillNeverKnowTheSecret01|*8'")
# c.execute("PRAGMA cipher_compatibility = 3")
# conn.commit()
# c.close()
print("does this file run every time i just save or make a change")
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = _declarative.declarative_base()