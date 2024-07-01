from website import create_app # create_app() wird von __init__.py importiert

app = create_app()

if __name__ == '__main__': # hier wird die App nur gestartet, wenn sie __main__ heißt, was autom. passiert durch den Import
    app.run(debug=True) # damit man nicht immer neu starten muss, sondern die Änderungen mit dem Speichern direkt geladen werden