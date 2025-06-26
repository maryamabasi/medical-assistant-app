from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # برای flash و session

# Config DB
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =================== MODELS ===================

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    symptoms = db.Column(db.String(300))
    messages = db.relationship('PatientMessage', backref='patient', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialty = db.Column(db.String(100))
    email = db.Column(db.String(120))

class PatientMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# =================== ROUTES ===================

@app.route('/')
def home():
    return "Welcome to the Medical Chat App!"

@app.route('/dashboard/patient')
def dashboard_patient():
    return "Welcome to Patient Dashboard"

@app.route('/dashboard/doctor')
def dashboard_doctor():
    return "Welcome to Doctor Dashboard"

# بیمار
@app.route('/login/patient', methods=['GET', 'POST'])
def login_patient():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        patient = Patient.query.filter_by(email=email, password=password).first()
        if patient:
            session['user_type'] = 'patient'
            session['user_id'] = patient.id
            return redirect(url_for('dashboard_patient'))
        else:
            flash('Invalid email or password')
    return render_template('login_patient.html')

# دکتر
@app.route('/login/doctor', methods=['GET', 'POST'])
def login_doctor():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        doctor = Doctor.query.filter_by(email=email, password=password).first()
        if doctor:
            session['user_type'] = 'doctor'
            session['user_id'] = doctor.id
            return redirect(url_for('dashboard_doctor'))
        else:
            flash('Invalid email or password')
    return render_template('login_doctor.html')

@app.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        symptoms = request.form['symptoms']
        new_patient = Patient(name=name, age=age, symptoms=symptoms)
        db.session.add(new_patient)
        db.session.commit()
        return f"Patient {name} registered successfully!"
    return render_template('register_patient.html')

@app.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        email = request.form['email']
        new_doctor = Doctor(name=name, specialty=specialty, email=email)
        db.session.add(new_doctor)
        db.session.commit()
        return f"Doctor {name} registered successfully!"
    return render_template('register_doctor.html')

# بیمار - ارسال پیام
@app.route('/chat/patient', methods=['GET', 'POST'])
def chat_patient():
    if request.method == 'POST':
        message = request.form['message']
        patient_id = session.get('user_id')

        if patient_id:
            new_message = PatientMessage(patient_id=patient_id, message=message)
            db.session.add(new_message)
            db.session.commit()
            flash("Your message was sent!")
            return redirect(url_for('chat_patient'))
        else:
            flash("Please login first.")
            return redirect(url_for('login_patient'))

    return render_template('chat_patient.html')

@app.route('/chat/doctor', methods=['GET', 'POST'])
def chat_doctor():
    messages = [
        {"sender": "Patient", "message": "I have a headache."},
        {"sender": "Doctor", "message": "How long have you had it?"}
    ]
    if request.method == 'POST':
        new_message = request.form['message']
        messages.append({"sender": "Doctor", "message": new_message})
    return render_template('chat_doctor.html', messages=messages)

# =================== MAIN ===================

if __name__ == '__main__':
    app.run(debug=True)
