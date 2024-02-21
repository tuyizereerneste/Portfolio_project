from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', boolean=True)

@views.route('/logout')
def logout():
    return "<p>Logout</p>"

@views.route('/sign-up', methods=['POST'])
def sign_up():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    telephone = request.form.get('telephone')
    gender = request.form.get('gender')
    role = request.form.get('role')

    # Save data to the database

    new_user = User(firstname=firstname, lastname=lastname, email=email,
                    password=password, address=address, telephone=telephone, gender=gender, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('master_page'))