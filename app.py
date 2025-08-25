from flask import Flask, request, redirect, render_template, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # any random strong string
# Database connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "login_db"
}

@app.route("/", methods=["GET", "POST"])
def login():
    message = "Please Login"
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to check user
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, password))
        result = cursor.fetchone()

        if result:
            message = f"✅ Login successful. Welcome {user}!"
            session["user"] = user
            # Example redirect:
            return redirect(url_for("dashboard"))
        else:
            message = "❌ Invalid username or password."

        cursor.close()
        conn.close()

    # render HTML from templates folder
    return render_template("login.html", message=message)

@app.route("/profile")
def profile():
    # ✅ User must be logged in (session must exist)
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", user=session["user"])

@app.route("/dashboard")
def dashboard():
    # ✅ User must be logged in (session must exist)
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    # clear session
    session.pop("user", None)
    return redirect(url_for("login")) #fixed

#add no-cache headers:
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True)


