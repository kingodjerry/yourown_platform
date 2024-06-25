db = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 3309,
    'database': 'platform'
}

# MySQL 연결 문자열 생성
db_url = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"

class Config:
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'smartplatform'