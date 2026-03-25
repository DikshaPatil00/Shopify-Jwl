from flask import Blueprint, render_template, session, redirect

emergency_bp = Blueprint("emergency", __name__, url_prefix="/user")


def is_emergency(symptoms, temperature, severity):
    critical_symptoms = [
        "chest pain",
        "breathlessness",
        "unconsciousness",
        "severe bleeding"
    ]

    reasons = []
    level = "Low"

    
    for s in symptoms:
        if s.lower() in critical_symptoms:
            reasons.append(f"Critical symptom detected: {s}")
            level = "High"

   
    if temperature >= 39:
        reasons.append("Very high temperature")
        level = "High"

    
    if severity.lower() == "high":
        reasons.append("High severity selected")
        level = "High"

    if reasons:
        return True, level, ", ".join(reasons)

    return False, None, None


@emergency_bp.route("/emergency")
def emergency():
    if "user_id" not in session:
        return redirect("/user/dashboard")

    reason = session.get("emergency_reason")
    return render_template("emergency.html", reason=reason)