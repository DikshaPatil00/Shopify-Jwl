from flask import Blueprint, render_template, request, session, redirect, url_for
from config import get_db_connection
from modules.emergency import is_emergency

symptomAnalyzer_bp = Blueprint("symptom", __name__, url_prefix="/user")


@symptomAnalyzer_bp.route("/symptoms", methods=["GET", "POST"])
def symptoms():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        user_id = session["user_id"]

        
        selected_symptoms = request.form.getlist("symptoms")
        other_symptoms = request.form.get("other_symptoms")  
        temperature = float(request.form["temperature"])
        duration = request.form["duration"]
        severity = request.form["severity"]

        
        all_symptoms = selected_symptoms.copy()

        if other_symptoms:
            extra = [s.strip() for s in other_symptoms.split(",") if s.strip()]
            all_symptoms.extend(extra)

        
        conn = get_db_connection()
        cursor = conn.cursor()

        for s in all_symptoms:
            cursor.execute("""
                INSERT INTO symptom
                (user_id, symptom_name, duration, severity, temperature)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, s, duration, severity, temperature))

        conn.commit()

        
        emergency, level, reason = is_emergency(all_symptoms, temperature, severity)

        if emergency:
            session["emergency_level"] = level
            session["emergency_reason"] = reason

            cursor.execute("""
                INSERT INTO emergency
                (user_id, symptom_names, emergency_message, emergency_level)
                VALUES (%s, %s, %s, %s)
            """, (
                user_id,
                ", ".join(all_symptoms),
                reason,
                level
            ))    

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for("emergency.emergency"))

        cursor.close()
        conn.close()

        return redirect(url_for("advice.advice"))

    return render_template("symptoms.html")