from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection
from mysql.connector import Error

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO users (name, age, gender, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, age, gender, email, password))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect("/login")

        except Error as e:
            if "Duplicate entry" in str(e):
                return render_template("user_exist.html")
            return str(e)

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["user_id"]
            return redirect("/user/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")