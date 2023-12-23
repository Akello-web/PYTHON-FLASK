from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Student
from .models import Note
from .models import Lesson
from . import db
import json
import requests

views = Blueprint('views', __name__)

#login
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

#all about notes: 
@views.route('/add-note', methods=['POST'])
def add_note():
    if request.method == 'POST': 
        note = request.form.get('comment')
        studId = request.form.get('sid')
        student=Student.query.get(studId)

        if len(note) < 1:
            flash('Comment is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id, student_id=studId)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("student_details.html", user=current_user, student=student)

#deleting notes
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
#jsonify() is a Flask function that converts Python dictionaries into JSON-formatted data, making it suitable for sending JSON responses in Flask routes.
    return jsonify({})

#add student
@views.route('/add-student', methods=['GET', 'POST'])
def addstudent():
    if request.method == 'POST':
        name  = request.form.get('name')
        surname  = request.form.get('surname')
        exam = request.form.get('exam')
        lesson_id = request.form.get('st_lesson')
        if int(exam)>=0 and int(exam) <=100: 
            #marks
            if int(exam) < 50:
                mark = 'F'
            elif int(exam) < 60:
                mark = 'D'
            elif int(exam) < 75:
                mark = 'C'
            elif int(exam) < 90:
                mark = 'B'
            elif int(exam) < 100:
                mark = 'A'
                
            new_student = Student(first_name=name, last_name=surname, exam=exam, lesson_id=lesson_id, mark=mark, user_id=current_user.id)
            db.session.add(new_student)
            db.session.commit()
            flash('Student added!', category='success')
        else:
            flash('Wrong exam points!', category='error')
        
            
    return render_template("addStudent.html", user=current_user)

#appears to handle both GET and POST requests to a route that includes a student ID as a parameter
@views.route('/student/<int:student_id>', methods=['GET', 'POST'])
#The function takes the student_id as a parameter.
def student_details(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        name  = request.form.get('name')
        surname  = request.form.get('surname')
        exam = request.form.get('exam')
        if int(exam)>=0 and int(exam) <=100: 
            if int(exam) < 50:
                mark = 'F'
            elif int(exam) < 60:
                mark = 'D'
            elif int(exam) < 75:
                mark = 'C'
            elif int(exam) < 90:
                mark = 'B'
            elif int(exam) < 100:
                mark = 'A'
                
            student.first_name = name
            student.last_name = surname
            student.exam = exam
            student.mark = mark
            
            db.session.commit()
            flash('Student updated!', category='success')
        else:
            flash('Wrong exam points!', category='error')
    
    
    return render_template('student_details.html',user=current_user, student=student)

#this method is to delete a student from database
@views.route('/delete-student', methods=['POST'])
def delete_student():  
    student = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    studId = student['studId']
    student = Student.query.get(studId)
    if student:
        if student.user_id == current_user.id:
            db.session.delete(student)
            db.session.commit()

    return jsonify({})

@views.route('/profile-page')
def profile_page():  
    return render_template('profile.html',user=current_user)
#This decorator specifies that this function handles both GET and POST requests to the /lessons-page route.
@views.route('/lessons-page', methods=['GET', 'POST'])
def lessons_page():  
    #his conditional statement checks if the request method is POST.
    if request.method == 'POST':
        #nside the POST block:
        name  = request.form.get('name')
        description  = request.form.get('description')
        if len(name) > 1: 
            new_lesson = Lesson(ls_name=name, ls_description=description, user_id=current_user.id)
            db.session.add(new_lesson)
            db.session.commit()
            flash('Lesson added!', category='success')
        else:
            flash('Wrong name length!', category='error')
            
    return render_template('lessons.html',user=current_user)


@views.route('/api-page', methods=['GET', 'POST'])
def api_page():     
    #Defines the URL of an external API (Exchange Rate API in this case).        
    api_url = "https://v6.exchangerate-api.com/v6/c9d48243dcc1bbe061817d0f/latest/USD"
    response = requests.get(api_url)
    if response.status_code == 200:  # If the request was successful
        data = response.json()  # Extract JSON data
    else:
        print("Failed to fetch data from the API")
        print("Status code:", response.status_code) 
                
    return render_template('apis.html',user=current_user, data=data)