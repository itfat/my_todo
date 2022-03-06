from asyncio import Task
from cProfile import label
from inspect import stack
from flask import Flask, url_for, render_template, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PickleType
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, TaskForm
import os
from sqlalchemy.ext.mutable import MutableList


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(100))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
      return check_password_hash(self.password_hash,password)
    

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(100), nullable=False)
    labels = db.Column(MutableList.as_mutable(PickleType),
                                    default=[])
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username =form.username.data, email = form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            session['current_user'] = user.username
            session['user_available'] = True
            next = request.args.get("next")
            return redirect(next or url_for('show_task'))
        flash('Invalid email address or Password.')    
    return render_template('login.html', form=form)


@app.route("/logout")
# @login_required
def logout():
    logout_user()
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if 'user_available' in session:
        form = TaskForm()
        user = Users.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            task = Tasks(title =form.title.data, priority = form.priority.data, labels = form.labels.data, user_id=user.id)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('show_task'))
        return render_template('task.html', form=form)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/tasks')
def show_task():
    if 'user_available' in session:
        tasks = Tasks.query.all()
        user = Users.query.all()
        return render_template('tasks.html', tasks=tasks, user=user)
    flash('User is not Authenticated')
    return redirect(url_for('index'))

@app.route('/delete/<id>/<user>', methods=('GET', 'POST'))
def delete_task(id, user):
    if db.session['current_user'] == user:
        me = Tasks.query.get(id)
        db.session.edelete(me)
        db.session.commit()
        return redirect(url_for('show_task'))
    flash('You are not a valid user to delete this task')
    return redirect(url_for('show_task'))


@app.route('/update/<id>/<user>', methods=('GET', 'POST'))
def update_post(id, user):
    if session['current_user'] == user:
        me = Tasks.query.get(id)
        task = TaskForm(obj=me)
        if request.method == 'POST':
            stask = Tasks.query.get(id)
            stask.title = task.title.data
            stask.priority = task.priority.data
            db.session.commit()
            return redirect(url_for('show_task'))
        return render_template('update.html', task=task)
    flash('You are not a valid user to edit this task')
    return redirect(url_for('show_task'))

if __name__ == '__main__':
   app.run(debug = True)