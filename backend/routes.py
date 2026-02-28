from flask import Flask, render_template, redirect, url_for, request, session
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
        
    return render_template("Login.html", msg="")

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

@app.route("/add_question/<course_id>/<email>", methods=["GET","POST"])
def add_question(course_id, email):
    if request.method == "POST":
        id = request.form.get("ques_id")
        title = request.form.get("title")
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option_key = request.form.get("correct_option")
        correct_option_mapping = {"option1" : option1 , "option2" : option2 , "option3" : option3 , "option4" : option4}
        correct_option = correct_option_mapping.get(correct_option_key, "")
        new_question = Question(id=id,title=title,question_statement=question_statement,option1=option1,option2=option2,option3=option3,option4=option4,correct_option=correct_option, course_id=course_id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template('add_question.html', course_id=course_id,email=email)


@app.route("/edit_question/<id>/<email>", methods=["GET","POST"])
def edit_question(id, email):
    ques = get_question(id)
    if request.method == "POST":
        title = request.form.get("title")
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")  
        ques.title = title
        ques.question_statement = question_statement
        ques.option1 = option1
        ques.option2 = option2
        ques.option3 = option3
        ques.option4 = option4
        ques.correct_option = correct_option
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("edit_question.html", email=email, question = ques)     


def get_question(id):
    questions = Question.query.filter_by(id=id).first()
    return questions

@app.route("/delete_question/<id>/<email>", methods=["GET","POST"])
def delete_question(id, email):
    dc = get_question(id)
    db.session.delete(dc)
    db.session.commit()
    return redirect(url_for("admin", email=email))

@app.route("/start_test/<course_id>/<email>", methods=["GET","POST"])
def start_test(course_id,email):
    questions = Question.query.filter_by(course_id=course_id).all()
    total_questions = len(questions)

    if request.args.get("restart") or "current_question" not in session or session.get("course_id") != course_id:
        session["current_question"] = 0
        session["score"] = 0
        session["course_id"] = course_id

    if total_questions == 0:
        return "No Questions are Available"
    
    if session["current_question"] >= total_questions:
        return redirect(url_for("test_result", course_id=course_id, email=email))
    
    current_question = questions[session["current_question"]]

    if request.method == "POST":
        selected_option = request.form.get("option")
        correct_option = current_question.correct_option

        if selected_option and selected_option.strip().lower() == correct_option.strip().lower():
            session["score"] +=1 

        session["current_question"] +=1
        session.modified = True

        return redirect(url_for("start_test", course_id=course_id, email=email))
    return render_template("start_test.html", email=email, question = current_question, current_question=session["current_question"] +1 , total_questions=total_questions, course_id=course_id)

@app.route("/test_result/<course_id>/<email>")
def test_result(course_id, email):
    user = User.query.filter_by(email=email).first()
    total = session.get("score" , 0)
    total_questions = Question.query.filter_by(course_id=course_id).count()

    existing = Scores.query.filter_by(user_id = user.id, course_id=course_id).first()

    if existing:
        existing.total_scored = total
    else:
        db.session.add(Scores(user_id = user.id, course_id=course_id, total_scored = total))
        db.session.commit()

    return render_template("result.html", course_id=course_id, email=email, total_scored = total, total_questions=total_questions)


@app.route("/search/<email>", methods=["GET","POST"])
def search_txt(email):
    if request.method == "POST":
        search_txt = request.form.get("search")
        by_user = search_by_user(search_txt)
        by_course = search_by_courses(search_txt)
        return render_template("search.html", email=email, users=by_user, courses=by_course)


def search_by_user(search_txt):
    users = User.query.filter(User.email.ilike(f"%{search_txt}%")).all()
    return users

def search_by_courses(search_txt):
    courses = Course.query.filter(Course.name.ilike(f"%{search_txt}%")).all()
    return courses
