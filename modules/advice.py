from flask import Blueprint, render_template, session, redirect
from config import get_db_connection

advice_bp = Blueprint("advice", __name__, url_prefix="/advice")


@advice_bp.route("/")
def advice():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

   
    cursor.execute("""
        SELECT symptom_id, symptom_name
        FROM symptom
        WHERE user_id = %s
        ORDER BY symptom_id DESC
        LIMIT 1
    """, (session["user_id"],))

    symptom = cursor.fetchone()

    if not symptom:
        cursor.close()
        conn.close()
        return render_template("advice.html", advice=None)

    
    cursor.execute("""
        SELECT *
        FROM advice
        WHERE LOWER(symptom_name) = LOWER(%s)
        LIMIT 1
    """, (symptom["symptom_name"],))

    advice = cursor.fetchone()

   
    if advice:
        cursor.execute("""
            INSERT INTO record (user_id, symptom_id, advice_id, date)
            VALUES (%s, %s, %s, CURDATE())
        """, (
            session["user_id"],
            symptom["symptom_id"],
            advice["advice_id"]
        ))
        conn.commit()

    cursor.close()
    conn.close()

    return render_template("advice.html", advice=advice)