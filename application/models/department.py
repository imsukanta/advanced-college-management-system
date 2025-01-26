from application import db
from sqlalchemy import Column,Integer,String
class Department(db.Model):
    __tablename__='department'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))