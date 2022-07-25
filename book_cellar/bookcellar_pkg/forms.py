from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,IntegerField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp,ValidationError
from bookcellar_pkg.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=15),Regexp(r'^[^\s]+$')])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8),Regexp(r'^[^\s]+$')])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is already taken!Use a different one")

    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is already taken!Use a different one")

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8),Regexp(r'^[^\s]+$')])
    remember=BooleanField('Remember me')
    submit=SubmitField('Sign in')




class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=15),Regexp(r'^[^\s]+$')])
    email=StringField('Email',validators=[DataRequired(),Email()])
    dp=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    address = TextAreaField('Add Full Address' )
    city = StringField('City')
    state = SelectField('Choose Your State', choices = [("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry")])
    zip_code = IntegerField('Zip-Code')
    submit = SubmitField('Submit')

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username is already taken!Use a different one")

    
    def validate_email(self,email):
        if email.data!= current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The email is already taken!Use a different one")
        
    
class bookform(FlaskForm):
    book_title=StringField('Title',validators=[DataRequired()])
    description=StringField('description',validators=[DataRequired()])
    category = SelectField('Category', choices = [("Educational","Educational"),("Fiction","Fiction"),("Biography","Biography"),("Cooking","Cooking")])
    book_img=FileField('Book Image',validators=[FileAllowed(['jpg','png','jpeg'])])
    author=StringField('author',validators=[DataRequired()])
    price=IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')
