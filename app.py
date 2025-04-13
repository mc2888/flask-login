from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "supersegreto"  # Cambialo in produzione!

# Account demo (username: admin, password: password)
USERS = {
    "admin": "password"
}

@app.route("/")
def index():
    if "username" in session:
        return f"Benvenuto, {session['username']}! <a href='/logout'>Logout</a>"
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Credenziali non valide.")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
