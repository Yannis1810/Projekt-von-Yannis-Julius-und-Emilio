# Authentifizierung des Users (Registrieren, Anmeldung, Abmeldung)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # das gleiche, wie from .__init__ import db
from flask_login import login_user, login_required, logout_user, current_user

#'fehler' und 'erfolg' Nachrichten in base.html Zeile 46 ff.

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST']) # Anmeldung eines Users
def login():
    if request.method == 'POST': # wird in login.html auf 'Post' eingestellt
        email = request.form.get('email') # angaben werden aus dem Formular ausgelesen
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # .first() ist hier eig unnötig, weil Email ein unique PK ist und somit sowieso nur 1 Ergebnis max. erscheinen sollte und dies dann nur zeigen würde, dasss die email bereits existiert
        if user: # wenn es den User schon gibt ...
            if user.password == password: # Passwort wird überprüft
                flash('Erfolgreich angemeldet!', category='erfolg') # Nachricht die dabei angezeigt bzw eingeblendet wird
                login_user(user, remember=True)
                return redirect(url_for('views.home')) # User wird zur Startseite weitergeleitet
            else:
                flash('Falsches Passwort, versuche es erneut.', category='fehler')
        else:
            flash('Email existiert nicht, versuche es erneut oder registriere dich.', category='fehler') # wenn die Email des Users noch nicht registriert wurde

    return render_template("login.html", user=current_user) # passendes Template wird angezeigt


@auth.route('/logout')
@login_required
def logout():
    logout_user() # Funktion von flask_login --> User wird ausgeloggt und weitergeleitet zur Anmeldung bzw. zum Registrieren
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # .first() ist hier eig unnötig, weil Email ein unique PK ist und somit sowieso nur 1 Ergebnis max. erscheinen sollte und dies dann nur zeigen würde, dasss die email bereits existiert
        if user:
            flash('Email existiert bereits.', category='fehler')
        elif len(email) < 4: # hier werden einige Bedingungen für das Erstellen eines Accounts überprüft
            flash('Email muss mehr als 3 Zeichen lang sein.', category='fehler') 
        elif len(first_name) < 2:
            flash('Vorname muss mehr als 1 Zeichen lang sein.', category='fehler')
        elif password1 != password2:
            flash('Passwörter stimmen nicht überein.', category='fehler')
        elif len(password1) < 6:
            flash('Passwort muss mindestens 6 Zeichen lang sein.', category='fehler')
        else:
            new_user = User(email=email, first_name=first_name, password=password1) # Passwort könnte man noch verschlüsseln, damit es nicht in der Datenbank auftaucht
            db.session.add(new_user)
            db.session.commit() # neuer User wird zur Datenbank hinzugefügt
            login_user(new_user, remember=True)
            flash('Erfolgreich registriert!', category='erfolg')
            return redirect(url_for('views.home')) # User wird zur Startseite weitergeleitet

    return render_template("sign_up.html", user=current_user)

@auth.route('/account', methods=["GET", "POST"])
@login_required
def account():
    if request.method == 'POST': # wird in login.html auf 'Post' eingestellt
        logout_user()
        email = request.form.get('email') # angaben werden aus dem Formular ausgelesen
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # .first() ist hier eig unnötig, weil Email ein unique PK ist und somit sowieso nur 1 Ergebnis max. erscheinen sollte und dies dann nur zeigen würde, dasss die email bereits existiert
        print(email,password,user)
        if user: # wenn es den User mit der Email Adresse schon gibt ...
            if user.password == password: # Passwort wird überprüft
                flash('Erfolgreich angemeldet!', category='erfolg') # Nachricht die dabei angezeigt bzw eingeblendet wird
                login_user(user, remember=True)
                return redirect(url_for('views.home')) # User wird zur Startseite weitergeleitet
            else:
                flash('Falsches Passwort, versuche es erneut.', category='fehler')
                return redirect(url_for('auth.login'))
        else:
            flash('Email existiert nicht, versuche es erneut oder registriere dich.', category='fehler') # wenn die Email des Users noch nicht registriert wurde

    return render_template("account.html", user=current_user)
