from flask import Flask, render_template, request, redirect, url_for

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

EMAIL = "admin@gmail.com"
PASSWORD = "admin123"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/authenticate", methods=["POST"])
def authenticate():

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if email == EMAIL and password == PASSWORD:
        return redirect(url_for("home"))

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )
@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return "Passwords do not match"

    # Database code will be added later

    return redirect(url_for("login_page"))

@app.route("/product")
def product():
    return render_template("product-details.html")

@app.route("/testdb")
def test():

    try:

        db.session.execute(db.text("SELECT 1"))

        return "Database Connected Successfully"

    except Exception as e:

        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)