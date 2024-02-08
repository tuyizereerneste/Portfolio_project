from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Test4</h1>"

@views.route('/login')
def login():
    return "<p>Login</p>"

@views.route('/logout')
def logout():
    return "<p>Logout</p>"

@views.route('/sign-up')
def sign_up():
    return "<p>SignUp</p>"