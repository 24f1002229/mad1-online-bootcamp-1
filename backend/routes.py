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
            return redirect(url_for("admin", email=email))
        elif user and user.role == 1:
            return redirect(url_for("user", email=email))
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
    courses = get_course()
    return render_template("admin.html", email=email, courses=courses)


def get_course(id=None):
    if id:
        return Course.query.filter_by(id=id).first()
    return Course.query.all()


@app.route("/add_course/<email>", methods=["GET","POST"])
def add_course(email):
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        description = request.form.get("description")
        newcourse = Course(id = id, name=name, description=description)
        db.session.add(newcourse)
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("add_course.html", email=email)


@app.route("/edit_course/<id>/<email>", methods = {"GET","POST"})
def edit_course(id, email):
    c = get_course(id)
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        description = request.form.get("description")
        c.id = id 
        c.name = name 
        c.description = description
        db.session.commit()
        return redirect(url_for("admin", email = email))
    return render_template("edit_course.html", email=email, course = c)

@app.route("/delete_course/<id>/<email>", methods=["GET","POST"])
def delete_course(id, email):
    dc = get_course(id)
    db.session.delete(dc)
    db.session.commit()
    return redirect(url_for("admin", email=email))


@app.route("/user/<email>")
def user(email):
    courses = get_course()
    return render_template("user.html", email=email, courses=courses)


@app.route("/add_question/<course_id>/<email>", methods=["GET", "POST"])
def add_question(course_id, email):
    if request.method == "POST":
        id =request.form.get("ques_id")
        title = request.form.get("title")
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option_key = request.form.get("correct_option")

        correct_option_mapping = {"option1" : option1 , "option2" : option2, "option3" : option3 , "option4" : option4}
        correct_option = correct_option_mapping.get(correct_option_key, "")

        new_question = Question(id = id , title=title, question_statement=question_statement, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option, course_id=course_id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("add_question.html", course_id=course_id, email=email)

@app.route("/edit_question/<id>/<email>", methods=["GET","POST"])
def edit_question(id, email):
    que = get_question(id)
    if request.method == "POST":
        title = request.form.get("title")
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")
        que.title = title
        que.question_statement = question_statement
        que.option1 = option1
        que.option2 = option2
        que.option3 = option3
        que.option4 = option4
        que.correct_option = correct_option
        db.session.commit()
        return redirect(url_for("admin", email = email))
    return render_template("edit_question.html", email = email, question = que)
    

def get_question(id):
    questions = Question.query.filter_by(id=id).first()
    return questions


@app.route("/delete_question/<id>/<email>", methods = ["GET", "POST"])
def delete_question(id, email):
    dque = get_question(id)
    db.session.delete(dque)
    db.session.commit()
    return redirect(url_for("admin", email=email))