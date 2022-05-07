import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm


DATABASE_URL = 'mysql://Aaron:1DjAg/Qc2mObJ2SX@localhost/fastapi'

engine = _sql.create_engine(DATABASE_URL) #connect_args={"check_same_thread":False} --> if using sqlite database

SessionLocal = _orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = _declarative.declarative_base()
