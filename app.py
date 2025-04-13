from flask import Flask, render_template, request, redirect, url_for, flash, session
import random

app = Flask(__name__)
app.secret_key = "supersegreto"  # Cambialo in produzione!

# Account demo (username: admin, password: password)
USERS = {
    "admin": "password"
}

# Domande per il gioco (ramificazioni)
game_questions = [
    {
        "image": "event1.png",  # Puoi cambiare il nome dell'immagine
        "question": "Vuoi entrare nella caverna?",
        "choices": ["Sì", "No"],
        "next": [1, 2]  # Indice delle prossime domande in base alla scelta
    },
    {
        "image": "event2.jpg",
        "question": "Affronti il drago?",
        "choices": ["Sì", "No"],
        "next": [3, 4]
    },
    {
        "image": "event3.png",
        "question": "Sei pronto per combattere?",
        "choices": ["Sì", "No"],
        "next": [5, 6]
    },
    # Puoi continuare a definire altre ramificazioni...
]

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("game"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("game"))
        else:
            flash("Credenziali non valide.")
    
    return render_template("login.html")

@app.route("/guest")
def guest():
    session["guest"] = True
    return redirect(url_for("game"))

@app.route("/game")
def game():
    # Impostiamo una sessione per seguire la ramificazione
    if "guest" not in session:
        return redirect(url_for("login"))
    
    # Ramificazione, partiamo dalla prima domanda
    current_question = 0
    return render_template("game.html", question=game_questions[current_question], path="")

@app.route("/choose/<int:choice>")
def choose(choice):
    # Ottieni la prossima domanda in base alla scelta
    current_question = int(request.args.get("current", 0))
    next_question = game_questions[current_question]["next"][choice]
    
    path = session.get('path', '') + f' -> {game_questions[current_question]["choices"][choice]}'
    session['path'] = path

    # Se non ci sono altre domande, termina
    if next_question >= len(game_questions):
        return redirect(url_for("game_over"))

    return render_template("game.html", question=game_questions[next_question], path=path)

@app.route("/game_over")
def game_over():
    return render_template("game_over.html", path=session.get('path', ''))

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("guest", None)
    session.pop("path", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
