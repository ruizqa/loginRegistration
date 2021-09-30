from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
#import datetime to change date format


@app.route("/")
def form():
    return render_template("create.html")


@app.route('/register', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not User.validate_user(request.form):
        # we redirect to the template with the form.
            return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    
    data = {
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    
    # We pass the data dictionary into the save method from the User class.
    User.save(data)
    # Don't forget to redirect after saving to the database.
    session['email'] = data['email']
    return redirect('/homepage')            

@app.route('/login', methods=["POST"])
def login_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not User.validate_login(request.form):
        # we redirect to the template with the form.
            return redirect('/')

    data = {
        "email" : request.form["email"],
        "password" : request.form["pw"]
    }

    user= User.login(data)
    
    if not user:
        return redirect('/')
    elif not bcrypt.check_password_hash(user.password, data['password']):
        flash("The password is incorrect", "login")
        return redirect('/')
    session['email'] = data['email']
    # Don't forget to redirect after saving to the database.
    return redirect('/homepage')  


@app.route("/homepage")
def read():
    # call the get all classmethod to get all users
    
    if not 'email' in session:
        flash("Please login to access the home page", "login")
        return redirect("/")
    
    data={
        'email': session['email']
    }

    user= User.get_user_info(data)
    return render_template("read.html", user=user)

@app.route("/logout")
def clearsession():
    session.clear()
    return redirect('/')