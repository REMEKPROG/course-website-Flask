#imports
from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///coursePortal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["PERMAMENT_SESSION_LIFETIME"] = timedelta(minutes=60)

database = SQLAlchemy(app)

class Klient (database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = database.Column(database.String(30), nullable=False, unique=True)
    password = database.Column(database.String(), nullable=False)
    email = database.Column(database.String(70), nullable=False, unique=True)
    age = database.Column(database.Integer, nullable=False)
    create_account_date = database.Column(database.DateTime, default=datetime.utcnow)


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
        current_client_login = checkLogin(request.form["login"])
        current_client_password = checkPassword(request.form["password"])
        current_client_password = bcrypt.generate_password_hash(current_client_password).decode("utf-8")
        current_client_email = checkEmail(request.form["email"])
        current_client_age = int(request.form["age"])

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
        current_client_login = request.form["login"]
        current_client_password = request.form["password"]
        
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

if __name__ in "__main__":
    app.run(debug=True)


#orig - zwraca surowy komunikat błedu z silnika bazy danych
#session.rollback - przywraca początkowy stan bazy bez żadnych zmian
#flash - ukazuje błąd dla użytkownika