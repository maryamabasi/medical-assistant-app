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


@app.route('/chat/patient', methods=['GET', 'POST'])
def chat_patient():
    if request.method == 'POST':
        message = request.form['message']
        new_message = Conversation(patient_id=session.get('user_id'), message=message, sender='patient')
        db.session.add(new_message)

        # پاسخ ساده بات:
        reply = Conversation(patient_id=session.get('user_id'), message="Thank you, we will contact your doctor.", sender='bot')
        db.session.add(reply)
        db.session.commit()
        
        return redirect(url_for('chat_patient'))

    conversations = Conversation.query.filter_by(patient_id=session.get('user_id')).all()
    return render_template('chat_patient.html', conversations=conversations)

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        patient_id = session.get('user_id')
        doctor_id = request.form['doctor_id']
        text = request.form['text']
        
        new_msg = Message(patient_id=patient_id, doctor_id=doctor_id, text=text)
        db.session.add(new_msg)
        db.session.commit()
        return "Message sent successfully"
    
    doctors = Doctor.query.all()
    return render_template('send_message.html', doctors=doctors)


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

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    message = db.Column(db.Text)
    sender = db.Column(db.String(10))  # 'patient' یا 'bot'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    text = db.Column(db.String(500))


if __name__ == '__main__':
    app.run(debug=True)
