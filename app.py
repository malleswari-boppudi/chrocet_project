from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {
    "admin@gmail.com": "admin123"
}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    if email in users and users[email] == password:
        return redirect(url_for("dashboard"))

    return "Invalid Email or Password"

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)