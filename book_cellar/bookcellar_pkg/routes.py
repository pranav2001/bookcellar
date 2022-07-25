import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request
from wtforms.validators import Email
from bookcellar_pkg.forms import RegistrationForm,LoginForm,UpdateAccountForm, bookform
from flask_login import LoginManager,login_user, current_user, logout_user,login_required
from bookcellar_pkg import app,db,bcrypt
from bookcellar_pkg.models import User,Book,Cart




@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
    Educational = Book.query.filter_by(category='Educational')
    Fiction = Book.query.filter_by(category='Fiction')
    Biography = Book.query.filter_by(category='Biography')
    Cooking = Book.query.filter_by(category='Cooking')
    return render_template('home.html',Educational=Educational,Fiction=Fiction,Biography=Biography,Cooking=Cooking)


@app.route('/register',methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newuser=User(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(newuser)
        db.session.commit()
        flash(f'Account created for {form.username.data}! ','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form_html=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash('You have logged in successfully','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful.Please check email and password','warning')
    return render_template('login.html',title='Login',form_html=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
    op_size=(150,150)
    img=Image.open(form_picture)
    img.thumbnail(op_size)
    img.save(picture_path)
    
    return picture_fn


def save_book(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path=os.path.join(app.root_path,'static/book_pics',picture_fn)
    op_size=(150,150)
    img=Image.open(form_picture)
    img.thumbnail(op_size)
    img.save(picture_path)
    
    return picture_fn

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.dp.data:
            picture=save_book(form.dp.data)
            current_user.img_file=picture
            db.session.commit()

        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.address=form.address.data
        current_user.city=form.city.data
        current_user.state=form.state.data
        current_user.zip_code=form.zip_code.data
        db.session.commit()
        flash('Account details updated successfully!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        form.address.data=current_user.address
        form.city.data=current_user.city
        form.state.data=current_user.state
        form.zip_code.data=current_user.zip_code
    image_file=url_for('static',filename='profile_pics/'+ current_user.img_file)
    return render_template('account.html',title='Account',dp=image_file,form_html=form)


@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
    form=bookform()
    if form.validate_on_submit():
        book=Book(book_title=form.book_title.data,description=form.description.data,category=form.category.data,author=form.author.data,price=form.price.data)
        if form.book_img.data:
            picture=save_book(form.book_img.data)
            book.book_img=picture
        
        db.session.add(book)
        db.session.commit()
        flash('Item successfully added!', 'success')
        # img_file=url_for('static',filename='book_pics/'+ book.book_img)
    return render_template('admin.html',form_html=form)




@app.route('/home/Educational')
def educational():
    Educational = Book.query.filter_by(category='Educational')

    return render_template('educational.html', Educational=Educational)


@app.route('/home/Fiction')
def fiction():
    Fiction = Book.query.filter_by(category='Fiction')

    return render_template('fiction.html', Fiction=Fiction)


@app.route('/home/Biography')
def biography():
    Biography = Book.query.filter_by(category='Biography')

    return render_template('biography.html', Biography=Biography)

@app.route('/home/Cooking')
def cooking():
    Cooking = Book.query.filter_by(category='Cooking')

    return render_template('cooking.html',  Cooking= Cooking)


@app.route('/cart/<int:book_id>',methods=['GET','POST'])
def add_to_cart(book_id):
    items = Book.query.filter_by(book_id=book_id).all()
    for item in items:
        cart_item=Cart(book_id=book_id,title=item.book_title,author=item.author,image=item.book_img,price=item.price)
    db.session.add(cart_item)
    db.session.commit()
    flash('Product Added to Cart Successfully!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/') 
def cart():
    products = Cart.query.all()
    price = []
    for product in products:
        price.append(product.price)
    cart_total = sum(price)
    cart_len = len(products)
    return render_template('cart.html', products=products, cart_len=cart_len,cart_total=cart_total)

@app.route('/cart/clear_cart',methods=['GET','POST'])
def clear_cart():
    db.session.query(Cart).delete()
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/checkout/final')
def final():
    items = Cart.query.all()
    db.session.query(Cart).delete()
    db.session.commit()
    return render_template('order.html',items=items)

