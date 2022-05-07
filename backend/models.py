import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash  as _hash


import database as _database


class User(_database.Base):
	__tablename__ ='users'

	id = _sql.Column(_sql.Integer,primary_key=True,index=True)
	email = _sql.Column(_sql.String(40),unique=True,index=True)
	hashed_password = _sql.Column(_sql.String(255))

	lead = _orm.relationship('Lead',back_populates="owner")


	def verify_password(self,password:str):
		return _hash.bcrypt.verify(password,self.hashed_password)


class Lead(_database.Base):
	__tablename__ ='lead'

	id = _sql.Column(_sql.Integer,primary_key=True,index=True)
	owner_id = _sql.Column(_sql.Integer,_sql.ForeignKey("users.id"))
	first_name = _sql.Column(_sql.String(20),index=True)
	last_name = _sql.Column(_sql.String(20),index=True)
	email = _sql.Column(_sql.String(255),index=True,unique=True)
	company = _sql.Column(_sql.String(20),index=True,default="")
	note = _sql.Column(_sql.Text,index=True,default="")
	date_created = _sql.Column(_sql.DateTime,index=True,default=_dt.datetime.utcnow)
	date_last_updated = _sql.Column(_sql.DateTime,index=True,default=_dt.datetime.utcnow)

	owner = _orm.relationship('User',back_populates='lead')
