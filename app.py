from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pf_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.Date, default=datetime.utcnow)
    salary = db.Column(db.Float, nullable=False)
    pf_balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='BDT')

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, default=0.07)
    repayment_years = db.Column(db.Integer, default=5)
    date_taken = db.Column(db.Date, default=datetime.utcnow)

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    user = User(
        name=data["name"],
        salary=data["salary"],
        currency=data.get("currency", "BDT")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "User created", "user_id": user.id})

@app.route("/contribute/<int:user_id>", methods=["POST"])
def contribute(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    contribution = user.salary * 0.12 * 2
    user.pf_balance += contribution
    db.session.commit()
    return jsonify({"status": "Contribution added", "balance": user.pf_balance})

@app.route("/loan/<int:user_id>", methods=["POST"])
def take_loan(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    amount = request.json["amount"]
    max_loan = user.pf_balance * 0.6
    if amount > max_loan:
        return jsonify({"error": "Exceeds loan eligibility"}), 400
    loan = Loan(user_id=user.id, amount=amount)
    user.pf_balance -= amount
    db.session.add(loan)
    db.session.commit()
    return jsonify({"status": "Loan granted", "loan_id": loan.id})

@app.route("/settlement/<int:user_id>")
def settlement(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    loans = Loan.query.filter_by(user_id=user.id).all()
    loan_summary = [{"amount": l.amount, "interest": l.interest_rate} for l in loans]
    return jsonify({
        "user": user.name,
        "balance": user.pf_balance,
        "currency": user.currency,
        "loans": loan_summary
    })

if __name__ == "__main__":
    app.run(debug=True)
