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


@views.route('/delete-repair', methods=['POST'])  # Funktion die Notizen löschen zu können vollständig von Blackbox.Ai geschrieben
def delete_repair():  
    repair = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    repairId = repair['repairId']
    repair = Repair.query.get(repairId)
    if repair:
        if repair.user_r_id == current_user.id:
            db.session.delete(repair)
            db.session.commit()

    return jsonify({}), redirect(url_for('views.repairs'))


@views.route('/repairs', methods=["GET", "POST"])
def repairs():
    return render_template("repairs.html", user=current_user)


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
            return redirect(url_for('views.repairs'))
    return render_template("database1.html", user=current_user)


@views.route('/trash', methods=["GET", "POST"])
def trash():
    tr_img1 = "https://cdn.discordapp.com/attachments/1223292817447845919/1256976184571592815/image.png?ex=6682b9cb&is=6681684b&hm=cf6f507c54766985857ab0e54bc52c170e74f8e9a8314696a356bd5701a1ba83&"
    tr_img2 = "https://cdn.discordapp.com/attachments/1223292817447845919/1256975459149676655/image.png?ex=6682b91e&is=6681679e&hm=312130e5efb32f9c0033b2b6b1273e5a0b96edc0f4b633936adc7521f746cd19&"
    if request.method == 'POST':
        plz = request.form.get('plz')
        
        if len(plz) < 5:
            flash('Postleitzahl ist ungültig (zu kurz).', category='fehler')
        elif len(plz) > 5:
            flash('Postleitzahl ist ungültig (zu lang).', category='fehler')
        else:
            if plz == "35647":
                tr_img1 = "https://media.discordapp.net/attachments/1223292817447845919/1256969668858609769/image.png?ex=6682b3ba&is=6681623a&hm=ecf7e43f515f629e25f13cd325ce43ce78f349f546cab3b559fec41025790e8f&=&format=webp&quality=lossless&width=853&height=473"
                tr_img2 = "https://media.discordapp.net/attachments/1223292817447845919/1256969809392963715/image.png?ex=6682b3db&is=6681625b&hm=f35f86a795219c30a859c5620347f5accf968ea588f76dcc8c94adb4b824ce0b&=&format=webp&quality=lossless&width=846&height=473"
            elif plz == "61250":
                tr_img1 = "https://cdn.discordapp.com/attachments/1223292817447845919/1256978715489861672/image.png?ex=6682bc27&is=66816aa7&hm=aa875c5921150b9048d3d50ed4c9e3b50a17fe8ec425fec21ee8646e2c8775b2&"
                tr_img2 = "https://cdn.discordapp.com/attachments/1223292817447845919/1256978715787792547/image.png?ex=6682bc27&is=66816aa7&hm=0d4ec880a6daf27bd146d9534ab22179f9b4a16525ff889fe27f140bca8fd80a&"
            elif plz == "61350":
                tr_img1 = "https://cdn.discordapp.com/attachments/1223292817447845919/1256979566065483869/image.png?ex=6682bcf2&is=66816b72&hm=ddda6332eb3b27f579009cdd3bb5457cffae11b51f3d654b14e53a0b424ca0f4&"
                tr_img2 = "https://cdn.discordapp.com/attachments/1223292817447845919/1256979566308884550/image.png?ex=6682bcf2&is=66816b72&hm=91c55ab6903178b9bdae1623d4873e174369cde7cb49c70b56d78746908fbc7b&"
            else:
                flash('Bitte eine gültige PLZ eingeben.', category='fehler')
            
    return render_template("trash.html", user=current_user, tr_img1=tr_img1, tr_img2=tr_img2)


@views.route('/database2', methods=["GET", "POST"])
def database2():
    if request.method == 'GET':
        suchergebnis = request.args.get("search")
        if suchergebnis:
            pass
        else:
            flash('Keine Ergebnisse für die Suchanfrage gefunden.', category='fehler')
        
    return render_template("database2.html", user=current_user, suchergebnis=suchergebnis) #wir haben leider nicht verstanden, wie man suchen kann und das auch ausgeben kann, deshalb kann man es auf der Website noch nicht anklicken
                                                                                                                                        #kann man aktivieren in base.html Zeile 41 mit: <li><a class="dropdown-item" id="database2" href="/database2">Datenbank abfragen</a></li>
