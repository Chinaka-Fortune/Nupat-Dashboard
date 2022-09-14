import os
import psycopg2
from flask import Flask, request, session, abort, jsonify, render_template, redirect, flash, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from dotenv import load_dotenv
load_dotenv()

from models import setup_db, Student, User, Course, Instructor, Admin, Sponsor
from auth.auth import AuthError, requires_auth

def get_db_connection():
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    database_path = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    
    conn = psycopg2.connect(database_path)
    
    return conn

STUDENTS_PER_PAGE = 10

def paginage_students(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * STUDENTS_PER_PAGE
    end = start + STUDENTS_PER_PAGE
    
    students = [student.format() for student in selection]
    current_students = students[start:end]
    
    return current_students

def create_app(test_cobfig=None):
    # create and configure the app
    app = Flask(__name__)
    
    #Set up CORS. Allow '*' for origins.
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    
    #The afterr_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, PATCH, POST, DELETE, OPTIONS"
        )
        return response
    
    """
    Login in
    """
    @app.route('/login', methods=["GET", "POST"])
    def login():
        body = request.get_json()
        
        new_email = body.get("email", None)
        new_username = body.get("username", None)
        new_password = body.get("password", None)
        new_role = body.get("role", None)
        
        search = body.get("search", None)
        
        try:
            if search is None:
                abort(403)
            
            if new_email != User.email or new_username != User.username or new_password != User.password or new_role != User.role:
                abort(403)
                
            if search:
                selection = User.query.order_by(User.id).filter(User.role.ilike("%{}%".format(search)))
                current_user = paginage_students(request, selection)
                
                # users = User(email=new_email, username=new_username, password=new_password, role=new_role)
                
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(selection)
                
                user = cur.fetchall()
                
                cur.close()
                conn.close()
                
                if user:
                    session['loggedin'] = True
                    session['new_email'] = User('new_email')
                    session['new_username'] = User('new_username')
                    session['new_password'] = User('new_password')
                    session['new_role'] = User('new_role')
                
                return jsonify(
                    {
                        "success": True,
                        "user": current_user,
                        "total_users": len(selection.all()),
                    }
                )
            else:
                abort(403)
                
        except Exception as e:
            print(e)
            abort(403)
    
    """
    Students
    """
    @app.route("/students")
    @requires_auth("get:students")
    def get_students():
        selection = Student.query.order_by(Student.id).all()
        current_students = paginage_students(request, selection)
        
        if len(current_students) == 0:
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "students": current_students,
                "total_students": len(Student.query.all())
            }
        )
    
    @app.route("/students", methods=["POST"])
    @requires_auth("post:students")
    def create_students(payload):
        body = request.get_json()
        
        new_date_of_birth = body.get("date_of_birth", None)
        new_program_start_date = body.get("program_start_date", None)
        new_program_end_date = body.get("program_end_date", None)
        new_accommodation = body.get("accommodation", None)
        new_amount_paid = body.get("amount_paid", None)
        new_gender = body.get("gender", None)
        new_student_program = body.get("student_program", None)
        new_marital_status = body.get("marital_status", None)
        new_health_condition = body.get("health_condition", None)
        new_disability = body.get("disability", None)
        new_profile_picture = body.get("profile_picture", None)
        
        search = body.get("search", None)
        
        try:
            if search:
                selection = Student.query.order_by(Student.id).filter(Student.student_program.ilike("%{}%".format(search)))
                current_students = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "students": current_students,
                        "total_students": len(selection.all()),
                    }
                )
                
            else:
                students = Student(date_of_birth=new_date_of_birth, program_start_date=new_program_start_date, program_end_date=new_program_end_date, accommodation=new_accommodation, amount_paid=new_amount_paid, gender=new_gender, student_program=new_student_program, marital_status=new_marital_status, health_condition=new_health_condition, disability=new_disability, profile_picture=new_profile_picture)
                
                students.insert()
                
                selection = Student.query.order_by(Student.id).all()
                current_students = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "updated": students.id,
                        "students": current_students,
                        "total_students": len(Student.query.all())
                    }
                )
                
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/students/<int:student_id>/edit", methods=["PATCH"])
    @requires_auth("patch:students")
    def edit_student_submission(payload, student_id):
        body = request.get_json()
        
        new_date_of_birth = body.get("date_of_birth", None)
        new_program_start_date = body.get("program_start_date", None)
        new_program_end_date = body.get("program_end_date", None)
        new_accommodation = body.get("accommodation", None)
        new_amount_paid = body.get("amount_paid", None)
        new_gender = body.get("gender", None)
        new_student_program = body.get("student_program", None)
        new_marital_status = body.get("marital_status", None)
        new_health_condition = body.get("health_condition", None)
        new_disability = body.get("disability", None)
        new_profile_picture = body.get("profile_picture", None)
        
        search = body.get("search", None)
        
        try:
            if search:
                selection = Student.query.order_by(Student.id).filter(Student.student_program.ilike("%{}%".format(search)))
                current_students = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "students": current_students,
                        "total_students": len(selection.all()),
                    }
                )
                
            else:
            
                students = Student(date_of_birth=new_date_of_birth, program_start_date=new_program_start_date, program_end_date=new_program_end_date, accommodation=new_accommodation, amount_paid=new_amount_paid, gender=new_gender, student_program=new_student_program, marital_status=new_marital_status, health_condition=new_health_condition, disability=new_disability, profile_picture=new_profile_picture)
                
                students.update()
                
                selection = Student.query.order_by(Student.id).all()
                current_students = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "updated": students.id,
                        "students": current_students,
                        "total_students": len(Student.query.all())
                    }
                )
        except Exception as e:
            print(e)
            abort(422)
    
    @app.route("/students/<int:student_id>", methods=["DELETE"])
    @requires_auth("delete:students")
    def delete_student(student_id):
        try:
            student = Student.query.filter(Student.id == student_id).one_or_none()
            
            if student is None:
                abort(404)
                
            student.delete()
            
            selection = Student.query.order_by(Student.id).all()
            current_students = paginage_students(request, selection)
            
            return jsonify(
                {
                    "success": True,
                    "deleted": student_id,
                    "students": current_students,
                    "total_students": len(Student.query.all())
                }
            )
            
        except Exception as e:
            print(e)
            abort(422)
    
    
    """
    Courses
    """
    @app.route("/courses", methods=["POST"])
    @requires_auth("post:courses")
    def create_course():
        body = request.get_json()
        
        new_course_title = body.get("course_title", None)
        new_course_description = body.get("course_description", None)
        new_course_instructor = body.get("course_instructor", None)
        new_course_outline = body.get("course_outline", None)
        new_course_material = body.get("course_material", None)
        new_registered_students = body.get("registered_students", None)
        new_course_start_date = body.get("course_start_date", None)
        new_course_end_date = body.get("course_end_date", None)
        new_course_project = body.get("course_project", None)
        new_course_assignment = body.get("course_assignment", None)
        
        search = body.get("search", None)
        
        try:
            if search:
                selection = Course.query.order_by(Course.id).filter(Course.course_title.ilike("%{}%".format(search)))
                current_courses = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": current_courses,
                        "total_courses": len(selection.all())
                    }
                )
                
            else:
                courses = Course(course_title=new_course_title, course_description=new_course_description, course_instructor=new_course_instructor, course_outline=new_course_outline, course_material=new_course_material, registered_students=new_registered_students, course_start_date=new_course_start_date, course_end_date=new_course_end_date, course_project=new_course_project, course_assignment=new_course_assignment)
                
                courses.insert()
                
                selection = Course.query.order_by(Course.id).all()
                current_courses = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": current_courses,
                        "total_courses": len(Course.query.all())
                    }
                )
                
        except Exception as e:
            print(e)
            abort(422)
            
            #Testing with postman
            # curl http://127.0.0.1:5000/courses?page=1 -X POST -H "Content-Type: application/json" -d '{"course_title":"Neverwhere", "course_instructor":"Neil Gaiman", "course_outline":"Machine Learning", "registered_students":"Chidimma", "course_start_date":"12 02 2022", "course_end_date":"22 02 2022", "course_project":"This is your first project.", "course_assignment":"This is your first assignment."}'
    
    @app.route("/courses")
    @requires_auth()
    def retrieve_courses():
        selection = Course.query.order_by(Course.id).all()
        current_courses = paginage_students(request, selection)
        
        if len(current_courses) == 0:
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "courses": current_courses,
                "total_courses": len(Course.query.all())
            }
        )
    
    @app.route("/courses/<int:course_id>", methods=["DELETE"])
    def delete_course(course_id):
        try:
            course = Course.query.filter(Course.id == course_id).one_or_none()
            
            if course is None:
                abort(404)
                
            course.delete()
            
            selection = Course.query.order_by(Course.id).all()
            current_courses = paginage_students(request, selection)
            
            return jsonify(
                {
                    "success": True,
                    "deleted": course_id,
                    "courses": current_courses,
                    "total_courses": len(Course.query.all())
                }
            )
            
        except Exception as e:
            print(e)
            abort(422)
        
    @app.route("/courses/<int:course_id>/edit", methods=["POST"])
    def edit_courses(course_id):
        body = request.get_json()
        
        new_course_title = body.get("course_title", None)
        new_course_description = body.get("course_description", None)
        new_course_instructor = body.get("course_instructor", None)
        new_course_outline = body.get("course_outline", None)
        new_registered_students = body.get("registered_students", None)
        new_course_start_date = body.get("course_start_date", None)
        new_course_end_date = body.get("course_end_date", None)
        new_course_project = body.get("course_project", None)
        new_course_assignment = body.get("course_assignment", None)
        
        search = body.get("search", None)
        
        try:
            if search:
                selection = Student.query.order_by(Student.id).filter(Student.course_title.ilike("%{}%".format(search)))
                current_courses = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "courses": current_courses,
                        "total_courses": len(selection.all()),
                    }
                )
                
            else:
            
                courses = Course(course_title=new_course_title, course_description=new_course_description, course_instructor=new_course_instructor, course_outline=new_course_outline, registered_students=new_registered_students, course_start_date=new_course_start_date, course_end_date=new_course_end_date, course_project=new_course_project, course_assignment=new_course_assignment)
                
                courses.update()
                
                selection = Course.query.order_by(Course.id).all()
                current_courses = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "updated": courses.id,
                        "courses": current_courses,
                        "total_courses": len(Course.query.all())
                    }
                )
                
        except Exception as e:
            print(e)
            abort(422)
            
    """
    Instructor
    """
    @app.route("/instructos")
    def retrieve_instructos():
        selection = Instructor.query.order_by(Instructor.id).all()
        current_instructors = paginage_students(request, selection)
        
        if len(current_instructors) == 0:
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "instructors": current_instructors,
                "total_instructors": len(Instructor.query.all())
            }
        )
    
    @app.route("/instructors", methods=["POST"])
    def create_instructors():
        body = request.get_json()
        
        new_instructor_course = body.get("instructor_course", None)
        new_weekly_project = body.get("weekly_project", None)
        new_project_grade = body.get("project_grade", None)
        
        search = body.get("search", None)
        
        try:
            if search:
                selection = Instructor.query.order_by(Instructor.id).filter(Instructor.instructor_course.ilike("%{}%".format(search)))
                current_instructors = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": current_instructors,
                        "total_instructors": len(selection.all())
                    }
                )
                
            else:
                instructors = Instructor(instructor_course=new_instructor_course, weekly_project=new_weekly_project, project_grade=new_project_grade)
                
                instructors.insert()
                
                selection = Instructor.query.order_by(Instructor.id).all()
                current_instructors = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": current_instructors,
                        "total_instructors": len(Instructor.query.all())
                    }
                )
                
        except Exception as e:
            print(e)
            abort(422)
    
    @app.route("/instructors/<int:instructor_id>/edit", methods=["POST"])
    def edit_instructor(instructor_id):
        body = request.get_json()
        
        new_instructor_course = body.get("instructor_course", None)
        new_weekly_project = body.get("weekly_project", None)
        new_project_grade = body.get("project_grade", None)
        
        search = body.get("search", None)
        
        try:
            if search:
                selection = Instructor.query.order_by(Instructor.id).filter(Instructor.instructor_course.ilike("%{}%".format(search)))
                current_instructors = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": current_instructors,
                        "total_instructors": len(selection.all())
                    }
                )
                
            else:
                instructors = Instructor(instructor_course=new_instructor_course, weekly_project=new_weekly_project, project_grade=new_project_grade)
                
                instructors.update()
                
                selection = Instructor.query.order_by(Instructor.id).all()
                current_instructors = paginage_students(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": current_instructors,
                        "total_instructors": len(Instructor.query.all())
                    }
                )
                
        except Exception as e:
            print(e)
            abort(422)
            
    @app.route("/instructors/<int:instructor_id>", methods=["DELETE"])
    def delete_instructor(instructor_id):
        try:
            instructor = Instructor.query.filter(Instructor.id == instructor_id).one_or_none()
            
            if instructor is None:
                abort(404)
                
            instructor.delete()
            
            selection = Instructor.query.order_by(Instructor.id).all()
            current_instructors = paginage_students(request, selection)
            
            return jsonify(
                {
                    "success": True,
                    "deleted": instructor_id,
                    "instructors": current_instructors,
                    "total_instructors": len(Instructor.query.all())
                }
            )
            
        except Exception as e:
            print(e)
            abort(422)
        
            
    """
    Here are the error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
        
    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
            405,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}), 400
        )
        
    @app.errorhandler(500)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "server error"}), 500
        )
    
    return app