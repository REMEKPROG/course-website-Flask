#imports
from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import re

from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError
)


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "ChristopherMango67"

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://kit.fontawesome.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://ka-f.fontawesome.com; "
        "font-src 'self' https://fonts.gstatic.com https://ka-f.fontawesome.com; "
        "connect-src 'self' https://ka-f.fontawesome.com; "
        "img-src 'self' data:; "
    )
    return response


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///coursePortal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

database = SQLAlchemy(app)

class Klient (database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = database.Column(database.String(30), nullable=False, unique=True)
    password = database.Column(database.String(), nullable=False)
    email = database.Column(database.String(70), nullable=False, unique=True)
    age = database.Column(database.Integer, nullable=False)
    create_account_date = database.Column(database.DateTime, default=datetime.utcnow)

    client_courses = database.relationship(
        "Course",
        back_populates="client_course",
        cascade="all, delete-orphan"
    )

class Course (database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey(Klient.id))
    language = database.Column(database.String(50))
    image_path = database.Column(database.String(300), nullable=True)
    title = database.Column(database.String(50), nullable=False)
    shorter_description = database.Column(database.String(100))
    description = database.Column(database.String(200), nullable=False)
    rating = database.Column(database.Integer, database.CheckConstraint("rating BETWEEN 0 AND 6"), default=0)
    create_course_date = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)

    client_course = database.relationship("Klient", back_populates="client_courses")

    lessons = database.relationship( #definiuje relacje z lessons
        'Lesson',              
        back_populates='course', #nazwa relacji a nie kolumny klucza obcego  
        cascade="all, delete-orphan"
    )   


class Lesson(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    course_id  = database.Column(database.Integer, database.ForeignKey(Course.id))
    course_content = database.Column(database.Text, nullable=False)
    video_url = database.Column(database.String(500), nullable=True)

    course = database.relationship("Course", back_populates="lessons")

with app.app_context():
    database.create_all()



def checkLogin(login):
    regex = r"^[0-9A-Za-z]{4,16}$"
    if re.fullmatch(regex, login):
        return login
    else:
        print(f"Login {login} is not valid")

def checkPassword(password):
    regex = r'[A-Za-z0-9@!#$%^&+=]{8,}'
    if re.fullmatch(regex, password):
        return password
    else:
        print(f"Password {password} is valid")

def checkEmail(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.fullmatch(regex, email):
        print("No i dobra coś sobie dodałem")
        return email
    else:
        print(f"Email {email} is not valid")

@app.route("/")
def index():    
    idUser = session.get("userId")
    currentUser = Klient.query.filter_by(id=idUser).first()
    return render_template("index.html", user=currentUser)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        current_client_login = checkLogin(request.form["login"]).strip()
        current_client_password = checkPassword(request.form["password"]).strip()
        current_client_password = bcrypt.generate_password_hash(current_client_password).decode("utf-8")
        current_client_email = checkEmail(request.form["email"]).strip()
        current_client_age = int(request.form["age"].strip())

        new_client = Klient(
            login = current_client_login,
            password = current_client_password,
            email = current_client_email,
            age = current_client_age,
        )
        try:
            database.session.add(new_client)
            database.session.commit()
            
            session.clear()
            session["userId"] = new_client.id
            session["userLogin"] = current_client_login

            flash(f"Witaj {current_client_login}!", "success")
            return redirect("/")
        except IntegrityError as e:
            database.session.rollback()
            error = str(e.args)

            if "login" in error:
                flash("Ten login jest zajęty. Spróbuj ponownie", "error")
            elif "email" in error:
                flash("Ten adres e-mail jest zajęty. Spróbuj ponownie", "error")
            else:
                flash("Wystąpił błąd podczas rejestracji. Spróbuj ponownie", "error")
            
            return redirect("/register")
    else:
        return render_template("register.html", user=None)
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        current_client_login = request.form["login"].strip()
        current_client_password = request.form["password"].strip()
        
        client = Klient.query.filter_by(login=current_client_login).first()
        if client:
            client_Password = bcrypt.check_password_hash(client.password, current_client_password)
            if client_Password:
                session.clear()

                session["userId"] = client.id
                session["userLogin"] = client.login
                flash(f"Witaj z powrotem {client.login}!", "success")
                return redirect("/")
            else:
                flash("nieprawidłowe hasło!", "error")
                return redirect("/login")
        else:
            flash("Nieprawidłowy login!", "error")
            return redirect("/login")
    else:
        return render_template("login.html", user=session.get("userId"))
    

@app.route("/logout")
def logout():
    session.clear()
    flash("Pomyślnie wylogowano!", "success")
    return redirect("/login")

@app.route("/clientData")
def checkUserData():
    clientData = Klient.query.get_or_404(session.get("userId"))
    return render_template("clientData.html", user=clientData)

@app.route("/coursesPage", methods=["POST", "GET"])
def coursesSite():
    idUser = session.get("userId")
    if idUser == None:
        return redirect("/login")
    else:
        currentUser = Klient.query.filter_by(id=idUser).first()
        languages = [c.language for c in Course.query.with_entities(Course.language).all()]
        courseData = Course.query.options(joinedload(Course.client_course))

        if request.method == "POST":
            query = Course.query

            languageChoiced = request.form["language"]
            print(languageChoiced)

            if not languageChoiced == "all":
                query = query.filter_by(language=languageChoiced)

            ratingChoiced = request.form["rating"]

            if ratingChoiced == "lowest":
                query = query.order_by(Course.rating.asc())
            elif ratingChoiced == "highest":
                query = query.order_by(Course.rating.desc())
            else:
                query = query

            print(ratingChoiced)
            dateUploadChoiced = request.form["date"]
            print(dateUploadChoiced)

            if dateUploadChoiced == "earliest":
                query = query.order_by(Course.create_course_date.desc())
            elif dateUploadChoiced == "oldest":
                query = query.order_by(Course.create_course_date.asc())
            else:
                query = query

            print(query)
            courseData = query.all()

        return render_template("courses.html", user=currentUser, courses=courseData, languages=languages)

@app.route("/createCourseHeader")
def courseHeader():
    idUser = session.get("userId")
    if idUser == None:
        return redirect("/login")
    else:
        userData = Klient.query.get_or_404(idUser)
        return render_template("createCourseHeader.html", user=userData)

if __name__ in "__main__":
    app.run(debug=True)


#orig - zwraca surowy komunikat błedu z silnika bazy danych
#session.rollback - przywraca początkowy stan bazy bez żadnych zmian
#flash - ukazuje błąd dla użytkownika