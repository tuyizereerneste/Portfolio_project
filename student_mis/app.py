from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'student_mis_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://*****:******@localhost/student_mis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150))
    password = db.Column(db.String(1024), nullable=False)  # Increase length for hashed password
    address = db.Column(db.String(100))
    telephone = db.Column(db.String(50), unique=True)
    gender = db.Column(db.String(50))
    role = db.Column(db.String(50))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150))
    address = db.Column(db.String(255), nullable=False)  # Increase length for hashed password
    gender = db.Column(db.String(100))
    classroom = db.Column(db.String(50))
    father_name = db.Column(db.String(150))
    father_email = db.Column(db.String(150))
    father_telephone = db.Column(db.String(150))
    father_address = db.Column(db.String(150))
    mother_name = db.Column(db.String(150))
    mother_email = db.Column(db.String(150))
    mother_telephone = db.Column(db.String(150))
    mother_address = db.Column(db.String(150))
    comment = db.Column(db.String(1000))
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Authentication successful
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed
            return render_template('login.html')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    response = make_response(redirect(url_for('login')))
    # Add cache control headers to prevent caching of the dashboard page
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/sign_up')
def sign_up():
    return render_template('user_form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    telephone = request.form.get('telephone')
    gender = request.form.get('gender')
    role = request.form.get('role')

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)

    # Save data to the database
    new_user = User(firstname=firstname, lastname=lastname, email=email,
                    password=hashed_password, address=address, telephone=telephone, gender=gender, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('dashboard'))

    # PROCESS STUDENT REGISTRATION
@app.route('/student_form')
def student_form():
    return render_template('student_form.html')


@app.route('/process_student', methods=['POST'])
def process_student():
    firstname = request.form.get('first-name')
    lastname = request.form.get('last-name')
    email = request.form.get('email')
    address = request.form.get('address')
    gender = request.form.get('gender')
    classroom = request.form.get('classroom')
    father_name = request.form.get('father-name')
    father_email = request.form.get('father-email')
    father_telephone = request.form.get('telephone1')
    father_address = request.form.get('address1')
    mother_name = request.form.get('mother-name')
    mother_email = request.form.get('mother-email')
    mother_telephone = request.form.get('telephone2')
    mother_address = request.form.get('address2')
    comment = request.form.get('comment')

    new_student = Student(firstname=firstname, lastname=lastname, email=email, address=address, gender=gender, classroom=classroom,
                          father_name=father_name, father_email=father_email, father_telephone=father_telephone, father_address=father_address,
                          mother_name=mother_name, mother_email=mother_email, mother_telephone=mother_telephone, mother_address=mother_address,
                          comment=comment)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/search_form')
def search_form():
    return render_template('search_form.html')


@app.route('/search')
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = Student.query.filter(Student.firstname.ilike(f'%{q}%') | Student.lastname.ilike(f'%{q}%') | Student.classroom.ilike(f'%{q}%')) \
        .limit(20).all()
    else:
        results =[]
        
    return render_template('search_results.html', results=results)

@app.route('/student_details/<int:id>')
def student_details(id):
    student = Student.query.get(id)
    if student:
        return render_template('student_details.html', student=student)
    else:
        # Handle the case where the student with the given ID doesn't exist
        # Redirect to an error page or display an error message
        return redirect(url_for('search_form'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
