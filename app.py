from flask import Flask
from extensions import db
from models.user import User

app = Flask(__name__)

# MySQL configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Patil@localhost/real_estate_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with Flask
db.init_app(app)


@app.route("/")
def home():
    return "Real Estate Management System"


@app.route("/test-db")
def test_db():
    try:
        db.engine.connect()
        return "MySQL Connected Successfully!"
    except Exception as e:
        return f"Database Connection Failed: {e}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)