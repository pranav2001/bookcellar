from bookcellar_pkg import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # fname = db.Column(db.String(20), unique=True, nullable=False)
    # lname = db.Column(db.String(20), nullable=False)
    username=db.Column(db.String(15),unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), unique=True, nullable=False)
    address = db.Column(db.Text, unique=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.Integer)
    def __repr__(self):
        return f"User '{self.user_id}','{self.fname}', '{self.email}'"

class Book(db.Model,UserMixin):
    book_id=db.Column(db.Integer,primary_key=True)
    book_title=db.Column(db.String(15),unique=True,nullable=False)
    description=db.Column(db.Text, unique=True)
    book_img=db.Column(db.String(20),nullable=False)
    category=db.Column(db.String(20),nullable=False)
    author=db.Column(db.String(120),unique=False, nullable=False)
    price=db.Column(db.Integer,nullable=False)

class Cart(db.Model):
    order_id=db.Column(db.Integer,primary_key=True)
    book_id=db.Column(db.Integer,nullable=False)
    title=db.Column(db.String(15),nullable=False)
    author=db.Column(db.String(15),nullable=False)
    image=db.Column(db.String(15),nullable=False)
    price=db.Column(db.Integer,nullable=False)