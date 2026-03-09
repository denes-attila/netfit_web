from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/tanulok")
def tanulok():
    conn = sqlite3.connect("../netfit_proc/netfit.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT nev
        FROM meresek
    """)

    sorok = cursor.fetchall()
    conn.close()

    nevek = [sor[0] for sor in sorok]

    return render_template("tanulok.html", nevek = nevek)


@app.route("/tanulo/<nev>")
def tanulo(nev):
    conn = sqlite3.connect("../netfit_proc/netfit.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * 
        FROM meresek
        WHERE nev = ?
        
    """, (nev,))

    tanulo_adatok = [dict(sor) for sor in cursor.fetchall()]
    conn.close()
    return render_template("tanulo.html", tanulo_adatok = tanulo_adatok)

if __name__ == "__main__":
    app.run(debug = True)