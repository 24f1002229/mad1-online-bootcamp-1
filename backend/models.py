from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    chapters = db.relationship("Chapter", backref="course", cascade="all,delete", lazy=True)


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    no_of_question = db.Column(db.Integer, default = 0)
    description = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all,delete", lazy=True)
                            

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    remarks = db.Column(db.String)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    scores = db.relationship("Scores", backref="quiz", cascade="all,delete", lazy=True)
    questions = db.relationship("Question", backref='quiz', cascade='all,delete', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    question_statement = db.Column(db.String)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.String, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp_of_attempt = db.Column(db.Time)
    total_scored = db.Column(db.Integer, default = 00)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, default=1)
    scores = db.relationship("Scores", backref="user", cascade="all,delete", lazy=True)