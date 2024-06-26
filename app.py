import flask
import flask_login
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import sessionmaker
import datetime
import bcrypt
from flask_oauthlib.client import OAuth

app = flask.Flask(__name__)
app.config.from_object(Config)

#구글 로그인
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_OAUTH2_CLIENT_ID'),
    consumer_secret=app.config.get('GOOGLE_OAUTH2_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

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

    def get_id(self):
        return self.ID

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

        if user:
            # 데이터베이스에 저장된 해시된 비밀번호와 입력된 비밀번호 비교
            if bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
                flask_login.login_user(user)
                return flask.redirect(flask.url_for("main"))
            else:
                flask.flash('Login failed. Please check your username and password.', 'error')
                return flask.redirect(flask.url_for('login'))
        else:
            flask.flash('Login failed. Please check your username and password.', 'error')
            return flask.redirect(flask.url_for('login'))

    return flask.render_template('login.html')

@app.route("/google/login")
def google_login():
    return google.authorize(callback=flask.url_for('google_callback', _external=True))

@app.route('/google/callback')
@google.authorized_handler
def google_callback(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            flask.request.args['error_reason'],
            flask.request.args['error_description']
        )
    flask.session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    # Example of how to access user information from Google:
    # email = user_info.data['email']
    # name = user_info.data['name']
    # Implement logic to check if the user exists and login/register as needed
    return flask.redirect(flask.url_for('main'))

@google.tokengetter
def get_google_oauth_token():
    return flask.session.get('google_token')

@app.route('/register', methods=['POST'])
def register():
    name = flask.request.form.get('name')
    join_id = flask.request.form.get('join_id')
    join_pwd = flask.request.form.get('join_pwd')
    birth = flask.request.form.get('birth')
    phone = flask.request.form.get('phone')
    email = flask.request.form.get('email')

    # 비밀번호 암호화
    hashed_pwd = bcrypt.hashpw(join_pwd.encode('utf-8'), bcrypt.gensalt())

    # 데이터베이스 저장
    new_user = User(
        ID=join_id,
        Username=name,
        Password=hashed_pwd,
        Email=email,
        Phone=phone,
        DateOfBirth=birth,
        DateJoined= datetime.datetime.now(),
        Status='active'
    )

    session = Session()
    session.add(new_user)
    session.commit()
    session.close()

    flask.flash('Account created successfully!', 'success')
    return flask.redirect(flask.url_for('login'))

@app.route('/get_terms_of_use')
def get_terms_of_use():
    with open('TermsofUse/TermsofUse.txt', 'r', encoding='utf-8') as file:
        terms_of_use = file.read()
    return terms_of_use

@app.route('/get_personal_information')
def get_personal_information():
    with open('TermsofUse/PersonalInformation.txt', 'r', encoding='utf-8') as file:
        personal_information = file.read()
    return personal_information


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"



@app.route("/main")
@flask_login.login_required
def main():
    return flask.render_template('main.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])