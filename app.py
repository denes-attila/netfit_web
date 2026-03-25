from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from tanulok_api import tanulok_api
from tanulok_html import tanulok_html
from flask_login import LoginManager
from user import User
from database import get_db



load_dotenv(override=False)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM users WHERE id = ?
        """, (id,)
    )
    adat = cursor.fetchone()
    name = adat["username"]
    passwd = adat["password"]
    user = User(id, name, passwd)
    return user

app.register_blueprint(tanulok_api)
app.register_blueprint(tanulok_html)


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')