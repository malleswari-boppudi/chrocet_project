from flask import Flask, render_template, request

app = Flask(__name__)

EMAIL = "admin@gmail.com"
PASSWORD = "admin123"


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    if email == "malli@gmail.com" and password == "Malli123":
        return render_template("index.html")

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)