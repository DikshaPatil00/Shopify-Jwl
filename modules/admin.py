from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect("/admin/login")

    return render_template("admin_dashboard.html")

@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM admins WHERE email=%s AND password=%s",
            (email, password)
        )
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            session["admin_id"] = admin["admin_id"]
            return redirect("/admin/dashboard")
        else:
            return render_template("admin_login.html", error="Invalid admin credentials")

    return render_template("admin_login.html")  

@admin_bp.route("/users")
def view_users():
    if "admin_id" not in session:
        return redirect("/admin/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id, name, age, gender, email FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("viewUsers.html", users=users)

@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    if "admin_id" not in session:
        return redirect("/admin/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
       
        cursor.execute("DELETE FROM record WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM emergency WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM symptom WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Delete error:", e)

    finally:
        cursor.close()
        conn.close()

    return redirect("/admin/users")

@admin_bp.route("/records")
def view_records():
    if "admin_id" not in session:
        return redirect("/admin/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            u.user_id,
            u.name,
            s.symptom_name,
            s.temperature,
            s.severity,
            a.remedy,
            a.medicine,
            a.diet,
            r.date
        FROM record r
        JOIN users u ON r.user_id = u.user_id
        JOIN symptom s ON r.symptom_id = s.symptom_id
        JOIN advice a ON r.advice_id = a.advice_id
        ORDER BY r.date DESC
    """)

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("viewUserRecords.html", records=records)



@admin_bp.route("/emergency-cases")
def emergency_cases():
    if "admin_id" not in session:
        return redirect("/admin/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    
    cursor.execute("""
        SELECT 
            e.emergency_id,
            u.name AS user_name,
            u.email,
            e.symptom_names,
            e.emergency_message,
            e.emergency_level
        FROM emergency e
        JOIN users u ON e.user_id = u.user_id
        ORDER BY e.emergency_id DESC
    """)

    emergencies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("viewUserEmergency.html", emergencies=emergencies)

@admin_bp.route("/logout")
def admin_logout():
    session.clear()
    return redirect("/")      