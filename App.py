from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "abc"   # random secret key

# just users for login
users = {
    "admin": "123",
    "user": "123"
}

# movies data (dummy)
movie_list = [
    {"id": 1, "name": "Leo", "time": "10:00 AM", "cost": 200},
    {"id": 2, "name": "Jawan", "time": "01:30 PM", "cost": 250},
    {"id": 3, "name": "Pushpa 2", "time": "04:00 PM", "cost": 300},
    {"id": 4, "name": "Kalki 2898 AD", "time": "07:00 PM", "cost": 350},
    {"id": 5, "name": "Salaar", "time": "10:00 PM", "cost": 280},
]

booked = []   # store booked tickets here

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]

        if uname in users and users[uname] == pwd:
            session["login_user"] = uname
            return redirect(url_for("home"))
        else:
            return "Wrong username or password"

    return render_template("login.html")

@app.route("/home")
def home():
    if "login_user" not in session:
        return redirect("/")
    return render_template("home.html", movies=movie_list)

@app.route("/book/<int:id>", methods=["GET", "POST"])
def book(id):
    if "login_user" not in session:
        return redirect("/")

    m = None
    for i in movie_list:
        if i["id"] == id:
            m = i
            break

    if request.method == "POST":
        b = {
            "movie": m,
            "uname": request.form["name"],
            "age": request.form["age"],
            "seat": request.form["seat"]
        }
        booked.append(b)
        return redirect(url_for("confirm", index=len(booked) - 1))

    return render_template("booking.html", movie=m)

@app.route("/confirm/<int:index>")
def confirm(index):
    if "login_user" not in session:
        return redirect("/")
    mybooking = booked[index]
    return render_template("confirm.html", booking=mybooking)

@app.route("/logout")
def logout():
    session.pop("login_user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
