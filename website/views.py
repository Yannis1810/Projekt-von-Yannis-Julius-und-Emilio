# Views des Users (was kann er sich angucken bzw. sehen)
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Repair
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/notes1', methods=['GET', 'POST'])
@login_required
def notes1():
    if request.method == 'POST': 
        note = request.form.get('note') # Eintrag wird aus der HTML-Datei genommen

        if len(note) < 1:
            flash('Notiz ist zu kurz!', category='fehler') 
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # Notiz wird zur Datenbank hinzugefügt
            db.session.commit()
            flash('Notiz wurde hinzugefügt!', category='erfolg')
            
    return render_template("notes.html", user=current_user)


@views.route('/delete-note', methods=['POST'])  # Funktion die Notizen löschen zu können vollständig von Blackbox.Ai geschrieben
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({}), redirect(url_for('views.notes1'))


@views.route('/database1', methods=["GET", "POST"]) # für Datenbankeinträge in die Repair Tabelle der Datenbank
def database1():
    if request.method == 'POST':
        r_object = request.form.get('r_object')
        location = request.form.get('location')
        tool = request.form.get('tool')
        next_maintenance = request.form.get('next_maintenance')
        r_note = request.form.get('r_note')

        if len(r_object) < 2:
            flash('Bezeichnung des Objekts muss mehr als 1 Zeichen lang sein.', category='fehler')
        elif len(location) < 2:
            flash('Standort des Objekts muss genauer angegeben werden.', category='fehler')
        elif len(tool) < 3:
            flash('Genutztes Werkzeug muss mehr als 2 Zeichen lang sein.', category='fehler')
        elif len(next_maintenance) < 3:
            flash('Der angegebene Zeitraum muss mehr als 2 Zeichen lang sein.', category='fehler')
        elif len(r_note) < 1:
            flash('Wartungsprotokoll kann nicht ohne zusätzliche Notiz gespeichert werden.', category='fehler')
        else:
            new_repair = Repair(r_object=r_object, location=location, tool=tool, next_maintenance=next_maintenance, r_note=r_note, user_r_id=current_user.id)
            db.session.add(new_repair)
            db.session.commit()
            flash('Wartungsprotokoll erfolgreich hinzugefügt!', category='erfolg')
            return redirect(url_for('views.home'))
    return render_template("database1.html", user=current_user)


@views.route('/database2', methods=["GET", "POST"])
def database2():
    if request.method == 'GET':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        
    return render_template("database2.html", user=current_user)