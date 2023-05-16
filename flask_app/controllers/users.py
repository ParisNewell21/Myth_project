from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_app.models.user import User
from flask_app.models.creature import Creature
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login')
def mainpage():
    return render_template('login.html')


@app.route('/register', methods =['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    save = User.save(data)
    session['user_id'] = save

    return redirect('/profile')


@app.route('/login', methods =['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/profile')
def Profile_page():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    return render_template("profile.html",user=user)
