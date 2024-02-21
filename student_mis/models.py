


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    telephone = db.Column(db.String(50), unique=True)
    gender = db.Column(db.String(50))
    role = db.Column(db.String(50))
