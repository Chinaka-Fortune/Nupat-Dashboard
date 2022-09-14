import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

import datetime

from dotenv import load_dotenv
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
database_path = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
User
"""
class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    other_names = Column(String)
    role = Column(String)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = Column(String(60), unique=True, nullable=True)
    default_password = Column(String(300), unique=True)
    actual_password = Column(String(300), unique=True, nullable=False)
    phone_number = Column(Integer)
    address = Column(String)
    students = db.relationship("Student", backref="author", lazy=True)
    sponsors = db.relationship("Sponsor", backref="author", lazy=True)
    courses = db.relationship("Course", backref="author", lazy=True)
    instructors = db.relationship("Instructor", backref="author", lazy=True)
    admins = db.relationship("Admin", backref="author", lazy=True)
    
    def __init__(self,  first_name, last_name, other_names, role, email, username, default_password, actual_password, phone_number, address):
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.role = role
        self.email = email
        self.username = username
        self.default_password = default_password
        self.actual_password = actual_password
        self.phone_number = phone_number
        self.address = address
        


    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'other_names': self.other_names,
            'role': self.role,
            'email': self.email,
            'username': self.username,
            'default_password': self.default_password,
            'actual_password': self.actual_password,
            'phone_number': self.phone_number,
            'address': self.address
        }

"""
Student

"""
class Student(db.Model):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    date_of_birth = Column(db.DateTime)
    program_start_date = Column(db.DateTime, nullable=False, default = datetime.datetime.utcnow())
    program_end_date = Column(db.DateTime, nullable=False, default = datetime.datetime.utcnow())
    accommodation = Column(db.Boolean)
    amount_paid = Column(Integer())
    gender = Column(String)
    student_program = Column(String)
    marital_status = Column(String)
    health_condition = Column(String)
    disability = Column(String)
    profile_picture = Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    sponsors = db.relationship("Sponsor", backref="author", lazy=True)
    admins = db.relationship("Admin", backref="author", lazy=True)
    
    def __init__(self, user_id, course_id, date_of_birth, program_start_date, program_end_date, accommodation, amount_paid, gender, student_program, marital_status, health_condition, disability, profile_picture):
        self.user_id = user_id
        self.course_id = course_id
        self.date_of_birth = date_of_birth
        self.program_start_date = program_start_date
        self.program_end_date = program_end_date
        self.accommodation = accommodation
        self.amount_paid = amount_paid
        self.gender = gender
        self.student_program = student_program
        self.marital_status = marital_status
        self.health_condition = health_condition
        self.disability = disability
        self.profile_picture = profile_picture
        
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'date_of_birth': self.date_of_birth,
            'program_start_date': self.program_start_date,
            'program_end_date': self.program_end_date,
            'accommodation': self.accommodation,
            'amount_paid': self.amount_paid,
            'gender': self.gender,
            'student_program': self.student_program,
            'marital_status': self.marital_status,
            'health_condition': self.health_condition,
            'disability': self.disability,
            'profile_picture': self.profile_picture
        }
        
        
"""
Sponsor

"""
class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    
    id = Column(Integer, primary_key=True)
    state_of_origin = Column(String)
    lga_of_origin = Column(String)
    home_address = Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    admins = db.relationship("Admin", backref="author", lazy=True)

    def __init__(self, user_id, student_id, state_of_origin, lga_of_origin, home_address):
        self.user_id = user_id
        self.student_id = student_id
        self.state_of_origin = state_of_origin
        self.lga_of_origin = lga_of_origin
        self.home_address = home_address

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'state_of_origin': self.state_of_origin,
            'lga_of_origin': self.lga_of_origin,
            'home_address': self.home_address
        }
    
"""
Course

"""
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    course_title = Column(String)
    course_description = Column(String)
    course_instructor = Column(String)
    course_outline = Column(String)
    course_material = Column(String)
    registered_students = Column(String)
    course_start_date = Column(db.DateTime)
    course_end_date = Column(db.DateTime)
    course_project = Column(String)
    course_assignment = Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    admins = db.relationship("Admin", backref="author", lazy=True)
    students = db.relationship("Student", backref="author", lazy=True)
    instructors = db.relationship("Instructor", backref="author", lazy=True)
    
    def __init__(self, user_id, course_title, course_description, course_instructor, course_outline, course_material, registered_students, course_start_date, course_end_date, course_project, course_assignment):
        self.user_id = user_id
        self.course_title = course_title
        self.course_description = course_description
        self.course_instructor = course_instructor
        self.course_outline = course_outline
        self.course_material = course_material
        self.registered_students = registered_students
        self.course_start_date = course_start_date
        self.course_end_date = course_end_date
        self.course_project = course_project
        self.course_assignment = course_assignment
        
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_title': self.course_title,
            'course_description': self.course_description,
            'course_instructor': self.course_instructor,
            'course_outline': self.course_outline,
            'course_material': self.course_material,
            'registered_students': self.registered_students,
            'course_start_date': self.course_start_date,
            'course_end_date': self.course_end_date,
            'course_project': self.course_project,
            'course_assignment': self.course_assignment
        }
    
"""
Instructor

"""
class Instructor(db.Model):
    __tablename__ = 'instructors'
    
    id = Column(Integer, primary_key=True)
    instructor_course = Column(String)
    weekly_project = Column(String)
    project_grade = Column(String)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    admins = db.relationship("Admin", backref="author", lazy=True)
    
    def __init__(self, user_id, student_id, course_id, instructor_course, weekly_project, project_grade):
        self.instructor_course = instructor_course
        self.weekly_project = weekly_project
        self.project_grade = project_grade
        self.user_id = user_id
        self.student_id = student_id
        self.course_id = course_id
    
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'instructor_course': self.instructor_course,
            'weekly_project': self.weekly_project,
            'project_grade': self.project_grade
        }

"""
Admin
"""
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True)
    admin_password = Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey("instructors.id"), nullable=False)
    
    def __init__(self, user_id, course_id, student_id, instructor_id):
        self.user_id = user_id
        self.course_id = course_id
        self.student_id = student_id
        self.instructor_id = instructor_id
        
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'instructor_id': self.instructor_id
        }