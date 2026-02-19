from flask import Flask, render_template, redirect, url_for, request
from .models import *
from app import app 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email , password = password).first()
        if user and user.role == 0:
            return redirect(url_for("admin", email = email))
        elif user and user.role == 1:
            return redirect(url_for("user", email= email))
        else:
            return render_template("Login.html", msg = "Invalid user")
        
    return render_template("Login.html")

@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email , password = password).first()
        if user:
            return render_template("Register.html", msg= "User already exists !!")
        newuser = User(email = email, password = password)
        db.session.add(newuser)
        db.session.commit()
        return render_template("Login.html", msg = "You can login and continue")
    return render_template("Register.html")


@app.route("/admin/<email>")
def admin(email):
    courses = get_courses()
    return render_template("admin.html", email=email, courses=courses)


def get_courses(id=None):
    if id:
        return Course.query.filter_by(id=id).first()
    return Course.query.all()


@app.route("/user/<email>")
def user(email):
    courses = get_courses()
    return render_template("User.html", email=email, courses=courses)


@app.route("/add_course/<email>", methods=["GET", "POST"])
def add_course(email):
    if request.method=="POST":
        id = request.form.get("id")
        name = request.form.get("name")
        description = request.form.get("description")
        newcourse = Course (id = id, name = name, description=description)
        db.session.add(newcourse)
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("add_course.html", email=email)
    

@app.route("/edit_course/<id>/<email>", methods=['GET', 'POST'])
def edit_course(id, email):
    c = get_courses(id)
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        description = request.form.get("description")
        c.id = id
        c.name = name
        c.description = description
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("edit_course.html", email=email, course = c)

@app.route("/delete_course/<id>/<email>", methods=["GET","POST"])
def delete_course(id,email):
    dc = get_courses(id)
    db.session.delete(dc)
    db.session.commit()
    return redirect(url_for("admin", email=email))