from flask import Flask, render_template, jsonify, request
from database import get_db
from dotenv import load_dotenv
from tanulok_api import tanulok_api
from tanulok_html import tanulok_html


load_dotenv()

app = Flask(__name__)
app.register_blueprint(tanulok_api)
app.register_blueprint(tanulok_html)


if __name__ == "__main__":
    app.run(debug = True)