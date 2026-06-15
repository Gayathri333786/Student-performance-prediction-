from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import joblib
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load ML Model
model = joblib.load('model.pkl')

# Database Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    attendance = db.Column(db.Float)
    study_hours = db.Column(db.Float)
    assignment = db.Column(db.Float)
    internal_marks = db.Column(db.Float)
    predicted_marks = db.Column(db.Float)

# Create DB
with app.app_context():
    db.create_all()

# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():

    prediction = None

    if request.method == 'POST':

        name = request.form['name']
        attendance = float(request.form['attendance'])
        study_hours = float(request.form['study_hours'])
        assignment = float(request.form['assignment'])
        internal_marks = float(request.form['internal_marks'])

        result = model.predict([[
            attendance,
            study_hours,
            assignment,
            internal_marks
        ]])

        prediction = round(result[0], 2)

        student = Student(
            name=name,
            attendance=attendance,
            study_hours=study_hours,
            assignment=assignment,
            internal_marks=internal_marks,
            predicted_marks=prediction
        )

        db.session.add(student)
        db.session.commit()

        return render_template(
            'index.html',
            prediction=prediction,
            name=name
        )

    return render_template('index.html')

# Dashboard
@app.route('/dashboard')
def dashboard():

    students = Student.query.all()

    total_students = len(students)

    if total_students > 0:
        average_marks = round(
            sum(s.predicted_marks for s in students)
            / total_students,
            2
        )
    else:
        average_marks = 0

    return render_template(
        'dashboard.html',
        total_students=total_students,
        average_marks=average_marks
    )

# History Page
@app.route('/history')
def history():

    students = Student.query.order_by(
        Student.id.desc()
    ).all()

    return render_template(
        'history.html',
        students=students
    )

if __name__ == '__main__':
    app.run(debug=True)
