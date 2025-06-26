from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Medical Chat App!"

@app.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        symptoms = request.form['symptoms']
        print(f"New patient: {name}, Age: {age}, Symptoms: {symptoms}")
        return f"Patient {name} registered successfully!"
    return render_template('register_patient.html')

@app.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        print(f"New doctor: {name}, Specialty: {specialty}")
        return f"Doctor {name} registered successfully!"
    return render_template('register_doctor.html')

if __name__ == '__main__':
    app.run(debug=True)
