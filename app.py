from flask import Flask, render_template
from modules.auth import auth_bp
from modules.user import user_bp
from modules.admin import admin_bp
from modules.emergency import emergency_bp   
from modules.record import record_bp
from modules.advice import advice_bp
from modules.symptomAnalyzer import symptomAnalyzer_bp

app = Flask(__name__)
app.secret_key = "secret123"

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(emergency_bp) 
app.register_blueprint(record_bp) 
app.register_blueprint(advice_bp)
app.register_blueprint(symptomAnalyzer_bp)         

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

