# Provident Fund System (Web-Based)

A web-based multi-user Provident Fund management system with:
- Monthly contribution tracking
- Loan eligibility and issuance
- Final settlement reports
- SQLite storage
- Currency support for **BDT** and **USD**

## 🛠 Features
- Multi-user accounts
- Employer/Employee contributions (12%)
- Loan eligibility (up to 60% of PF balance)
- Final settlement API
- Flask + SQLite backend

## 📦 Tech Stack
- Python 3.8+
- Flask
- SQLAlchemy
- SQLite

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/your-username/provident_fund_system.git
cd provident_fund_system

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Access: `http://127.0.0.1:5000`

## 🧪 API Endpoints

| Method | Endpoint               | Description               |
|--------|------------------------|---------------------------|
| POST   | /create_user           | Create new user           |
| POST   | /contribute/<user_id>  | Add monthly contribution  |
| POST   | /loan/<user_id>        | Request a loan            |
| GET    | /settlement/<user_id>  | View final settlement     |

## 🧾 License
MIT License
