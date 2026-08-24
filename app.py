from flask import Flask
from extensions import db
from models.user import User
from models.property import Property, PropertyImage
from routes.auth import auth
from flask_login import LoginManager
from routes.property import property_bp
from flask import Flask, render_template

app = Flask(__name__)

app.config["SECRET_KEY"] = "your-secret-key"

# MySQL configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Patil@localhost/real_estate_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# database 
db.init_app(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authentication routes
app.register_blueprint(auth)
app.register_blueprint(property_bp)



@app.route("/")
def home():
    # return "Real Estate Management System"
    return render_template("index.html")


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