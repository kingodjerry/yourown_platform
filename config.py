class Config:
    user = "root"
    password = "1234"
    host = "127.0.0.1"
    port = "3309"
    database = "platform"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'smartplatform'