from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ✅ Pehle db ko define karein

class User(db.Model):
    __tablename__ = 'user'  # Ensure table name is set

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    saved_passwords = db.relationship('SavedPassword', backref='user', lazy=True)

class SavedPassword(db.Model):
    __tablename__ = 'saved_password'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
