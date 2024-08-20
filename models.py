from db_init import db  # Import db from the new module
from sqlalchemy import Column, Integer, String, LargeBinary, JSON, Text, ForeignKey

class User(db.Model):
    __tablename__ = 'users'
    username = Column(String(50), primary_key=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    images = db.relationship('Plant', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Plant(db.Model):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    plant_info = Column(JSON, nullable=False)
    plant_uses = Column(Text, nullable=False)
    username = Column(String(50), ForeignKey('users.username'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(Text, nullable=False)
    rate = Column(Integer, nullable=False)
    username = Column(String(50), ForeignKey('users.username'), nullable=False)
