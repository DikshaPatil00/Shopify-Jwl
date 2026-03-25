from flask import Blueprint, render_template, session, redirect
from config import get_db_connection

record_bp = Blueprint("record", __name__, url_prefix="/record")

@record_bp.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.date,
            s.symptom_name,
            a.remedy,
            a.medicine,
            a.diet,
            a.water_intake,
            r.emergency_id
        FROM record r
        JOIN symptom s ON r.symptom_id = s.symptom_id
        LEFT JOIN advice a ON r.advice_id = a.advice_id
        WHERE r.user_id = %s
        ORDER BY r.date DESC
    """, (session["user_id"],))

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("records.html", records=records)