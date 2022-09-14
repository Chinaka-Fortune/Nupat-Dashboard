import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Course, Instructor, Student, setup_db

from dotenv import load_dotenv
load_dotenv()

class NupatTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.database_name = os.getenv("TEST_DB_NAME")
        self.database_path = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_course = {"course": "What is your hobby?", "answer": "Football", "category": 6, "difficulty": 1}
        self.new_student = {"student": "What is your hobby?", "answer": "Football", "category": 6, "difficulty": 1}
        self.new_instructor = {"instructor": "What is your hobby?", "answer": "Football", "category": 6, "difficulty": 1}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Two tests for each route, each test for successful operation and for expected errors.
    """
    def test_get_paginated_students(self):
        res = self.client().get("/students")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_students"])
        self.assertTrue(len(data["students"]))
    
    def test_404_sent_requesting_beyond_valid_page_get_students(self):
        res = self.client().get("/students/1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_create_new_student(self):
        res = self.client().post("/students", json=self.new_student)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_students"])
        self.assertTrue(len(data["students"]))
    
    def test_422_student_creation_fails(self):
        res = self.client().post("/students", json={
            'javaScript': "one"
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_delete_students(self):
        res = self.client().delete("/students/7")
        data = json.loads(res.data)
        
        student = Student.query.filter(Student.id == 7).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 7)
        self.assertTrue(data["total_students"])
        self.assertTrue(len(data["students"]))
        self.assertEqual(student, None)
    
    def test_422_student_does_not_exist(self):
        res = self.client().delete("/students/1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_get_paginated_courses(self):
        res = self.client().get("/courses")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_courses"])
        self.assertTrue(len(data["courses"]))
    
    def test_404_sent_requesting_beyond_valid_page_get_courses(self):
        res = self.client().get("/courses/1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_delete_course(self):
        res = self.client().delete("/courses/7")
        data = json.loads(res.data)
        
        course = Course.query.filter(Course.id == 7).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 7)
        self.assertTrue(data["total_courses"])
        self.assertTrue(len(data["courses"]))
        self.assertEqual(course, None)
        
    def test_422_course_does_not_exist(self):
        res = self.client().delete("/courses/1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_create_new_course(self):
        res = self.client().post("/courses", json=self.new_course)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_courses"])
        self.assertTrue(len(data["courses"]))
    
    def test_422_course_creation_fails(self):
        res = self.client().post("/courses", json={
            'javaScript': "one"
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_get_paginated_instructors(self):
        res = self.client().get("/instructors")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_instructors"])
        self.assertTrue(len(data["instructors"]))
    
    def test_404_sent_requesting_beyond_valid_page_get_instructors(self):
        res = self.client().get("/instructors/1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_delete_instructor(self):
        res = self.client().delete("/instructors/7")
        data = json.loads(res.data)
        
        instructor = Instructor.query.filter(Instructor.id == 7).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 7)
        self.assertTrue(data["total_instructors"])
        self.assertTrue(len(data["instructors"]))
        self.assertEqual(instructor, None)
    
    def test_422_instructor_does_not_exist(self):
        res = self.client().delete("/instructors/1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_create_new_instructor(self):
        res = self.client().post("/instructors", json=self.new_instructor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_instructors"])
        self.assertTrue(len(data["instructors"]))
    
    def test_422_instructor_creation_fails(self):
        res = self.client().post("/instructors", json={
            'javaScript': "one"
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_get_course_search_results(self):
        res = self.client().post("/courses/search", json={"search": "jav"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["courses"])
        self.assertTrue(data["current_courses"])
        self.assertTrue(len(data["courses"]))
    
    def test_get_course_search_no_results(self):
        res = self.client().post("/courses/search/10")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["message"]), "resourse not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()