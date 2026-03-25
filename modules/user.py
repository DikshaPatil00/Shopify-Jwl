from flask import Blueprint, render_template, request, session, redirect
 

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("user_dashboard.html")


