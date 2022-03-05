from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///todo.sqlite3'


db = SQLAlchemy(app)
class users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('tasks', backref='user', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.username

class tasks(db.Model):
    id = id = db.Column('task_id', db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(100), nullable=False)
    labels = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)