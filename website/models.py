from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#This code defines class named Note that represents a table in the database
class Note(db.Model): #extends from Model
    #Defines a column named id that is of type Integer and serves as the primary key for the Note table.
    id = db.Column(db.Integer, primary_key=True)
    #Creates a column named data that stores string values with a maximum length of 10000 characters.
    data = db.Column(db.String(10000))
    #Creates a column named date that stores date and time information. Timezone information by default.
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #establishes a foreign key relationship with the id column in the user table.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #holds Integer values and establishes a foreign key relationship with the id column in the student table
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))


class User(db.Model, UserMixin):
    # serves as the primary key for the User table.
    id = db.Column(db.Integer, primary_key=True)
    #Email type of String, unique=True constrains each email in this column must be unique 
    email = db.Column(db.String(150), unique=True)
    #Password
    password = db.Column(db.String(150))
    #First name
    first_name = db.Column(db.String(150))
    #a user can have multiple notes
    notes = db.relationship('Note')
    #multiple students
    students = db.relationship('Student')
    #list of lessons
    lessons = db.relationship('Lesson')

class Student(db.Model):
    #Defines a column named id that serves as the primary key for the table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    #exam mark with a type of int
    exam = db.Column(db.Integer)
    #mark
    mark = db.Column(db.String(150))
    #Establishes a foreign key relationship with the id column in the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #foreign key relationship with the id column in the Lesson table
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    #additional notes
    notes = db.relationship('Note')
    
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Creates a column named ls_name 
    ls_name = db.Column(db.String(150))
    #Defines a column named ls_description to store string values (Max 150 characters)
    ls_description = db.Column(db.String(150))
    #Specific user associated with this lesson.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #multiple associated students.
    students = db.relationship('Student')
    

