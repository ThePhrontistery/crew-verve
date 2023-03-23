from typing import Self
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
   db.init_app(app)
   return db

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(255), nullable=False, unique=True)
    email_user = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    projects = db.relationship('Project', secondary='user_project', back_populates='users')

    def set_password(self, password):
        # Generate a random salt
        salt = bcrypt.gensalt()

        # Hash the password using the salt and the bcrypt algorithm
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Store the salt and the hashed password in the database
        self.password_salt = salt.decode('utf-8')
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password):
        # Hash the password using the stored salt and the bcrypt algorithm
        password_hash = bcrypt.hashpw(password.encode('utf-8'), self.password_salt.encode('utf-8'))

        # Compare the hashed password to the stored password hash
        return password_hash == self.password_hash.encode('utf-8')
    
    
class Project(db.Model):
    id_project = db.Column(db.Integer, primary_key=True)
    name_project = db.Column(db.String(255), nullable=False)
    # para hacer 1-n entre proyecto y encuesta
    surveys = db.relationship('Survey', backref='project')
    #surveys = db.relationship('Survey', back_populates='projects')
    users = db.relationship('User', secondary='user_project', back_populates='projects')

class Survey(db.Model):
    id_survey = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    name_survey = db.Column(db.String(255), nullable=False)
    #description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=False)
    mood = db.Column(db.Integer, nullable=False)
    rating =  db.Column(db.Integer, nullable=False)
    participation = db.Column(db.Integer, nullable=False)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id_project')) 
    answers = db.relationship('Survey_answer', backref='survey')
    tickets = db.relationship('Survey_ticket', backref='survey')

class Survey_answer(db.Model):
    id_survey_answer = db.Column(db.Integer, primary_key=True)
    id_survey = db.Column(db.Integer, db.ForeignKey('survey.id_survey'))
    answers = db.Column(db.String(255), nullable=False)

class Survey_ticket(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id_survey'), primary_key=True)
    completed = db.Column(db.Boolean, default=False)


user_project = db.Table('user_project',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id_user'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id_project'), primary_key=True)
)

class Stats:
    projects = Project
    surveys = Survey
    selected_project: int
    selected_survey: int
    survey_has_answers: int
    
