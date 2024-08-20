from app import db

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    images = db.relationship('Plant', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    plant_info = db.Column(db.JSON, nullable=False)
    plant_uses = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)
