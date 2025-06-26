from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config DB
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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
        #print(f"New patient: {name}, Age: {age}, Symptoms: {symptoms}")
        new_patient = Patient(name=name, age=age, symptoms=symptoms)
        db.session.add(new_patient)
        db.session.commit()
        return f"Patient {name} registered successfully!"
    return render_template('register_patient.html')

@app.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']  # ← اینو اضافه کن
        specialty = request.form['specialty']
        #print(f"New doctor: {name}, Specialty: {specialty}")
        new_doctor = Doctor(name=name, email=email,specialty=specialty)
        db.session.add(new_doctor)
        db.session.commit()
        return f"Doctor {name} registered successfully!"
    return render_template('register_doctor.html')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    symptoms = db.Column(db.String(300))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))  # ← اضافه کن    
    specialty = db.Column(db.String(100))


if __name__ == '__main__':
    app.run(debug=True)
