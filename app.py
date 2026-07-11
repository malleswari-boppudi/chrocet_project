from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)