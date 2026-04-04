from flask import Blueprint, request, render_template, redirect, url_for
from database import get_db
from flask_login import login_user
from user import User
auth = Blueprint('auth', __name__)

@auth.route("/auth", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        conn = get_db()
        cursor = conn.cursor()
        adat = request.form
        name = adat['username']
        passwd = adat['password']
        cursor.execute(
            """
            SELECT  * FROM users WHERE username = ?

        """, (name,)
        )
        db_data = cursor.fetchone()
        if db_data is None:
            return render_template('login.html', error='Hibás felhasználónév vagy jelszó')
        if passwd == db_data["password"]:
            user = User(db_data['id'], db_data['username'], db_data['password'])
            login_user(user)
            return redirect(url_for('tanulok_html.index'))
        else:
            return render_template('login.html', error='Hibás felhasználónév vagy jelszó')  