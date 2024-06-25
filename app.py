import flask
import flask_login
from config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

users = {"user": User("user", "1234")}


@login_manager.user_loader
def user_loader(id):
    return users.get(id)

@app.route('/')
def home():
    if flask_login.current_user.is_authenticated:
        return flask.render_template('main.html')
    else:
        return flask.redirect(flask.url_for('get_login'))

@app.get("/login")
def get_login():
    return flask.render_template('login.html')

@app.post("/login")
def post_login():
    user = users.get(flask.request.form["id"])

    if user is None or user.password != flask.request.form["password"]:
        return flask.redirect(flask.url_for("login"))

    flask_login.login_user(user)
    return flask.redirect(flask.url_for("protected"))

@app.route("/main")
@flask_login.login_required
def protected():
    return flask.render_template('main.html')

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"