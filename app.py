import logging
import flask
import flask_login
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import sessionmaker

app = flask.Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 연결 
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

# 로그인 매니저 초기화
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'users'
    UserID = Column(Integer, primary_key=True)
    ID = Column(String(11))
    Username = Column(String(255))
    Password = Column(String(255))
    Email = Column(String(255))
    Phone = Column(String(20))
    DateOfBirth = Column(Date)
    DateJoined = Column(DateTime)
    LastLogin = Column(DateTime)
    Status = Column(Enum('active', 'inactive', name='user_status'))

    def __init__(self, id, password):
        self.ID = id
        self.Password = password
    
    def get_id(self):
        return self.ID  # 사용자의 ID를 반환하는 메서드

@login_manager.user_loader
def load_user(id):
    session = Session()
    user = session.query(User).filter_by(ID=id).first()
    session.close()
    return user

@app.route('/')
def home():
    if flask_login.current_user.is_authenticated:
        return flask.render_template('main.html')
    else:
        return flask.redirect(flask.url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        id = flask.request.form.get("id")
        password = flask.request.form.get("password")

        user = User.query.filter_by(ID=id).first()

        if user and user.Password == password:
            flask_login.login_user(user)
            return flask.redirect(flask.url_for("main"))
        else:
            flask.flash('Login failed. Please check your username and password.', 'error')
            return flask.redirect(flask.url_for('login'))

    return flask.render_template('login.html')

@app.route('/join')
def join_us():
    return flask.render_template('join.html') 

@app.route("/main")
@flask_login.login_required
def main():
    return flask.render_template('main.html')

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])