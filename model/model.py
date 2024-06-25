from flask import Flask, jsonify
from sqlalchemy import create_engine, text

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    
    database = create_engine(app.config['db_url'], encoding='utf-8', max_overflow=0)
    app.database = database
    
    @app.route('/example/<string:user_name>', methods=['GET'])
    def get_email(user_name):
        params = {'name': user_name}
        row = app.database.execute(text("""
            SELECT * 
            FROM users 
            WHERE name = :name
        """), params).fetchone()
        return jsonify({'email': row['email']})
    
    return app