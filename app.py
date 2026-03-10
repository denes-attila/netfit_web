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

@app.route("/atlagok")
def atlagok():
    conn = sqlite3.connect("../netfit_proc/netfit.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT nem, AVG(fekvotamasz)
    FROM meresek
    GROUP BY nem
    """)
    fekvotamasz_atlagok  = [dict(sor) for sor in cursor.fetchall()]
    conn.close()

    return render_template("atlagok.html", fekvotamasz_atlagok = fekvotamasz_atlagok)

@app.route("/atlagok/<meres>")


def ossze_atlag(meres):
    conn = sqlite3.connect("../netfit_proc/netfit.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    meresek = ["suly", "magassag", "testzsir", "tavolugrás", "ingafutas",
           "fekvotamasz", "hajlekonysag", "szoritoeró", "torzsemeles"]
    

    if meres not in meresek:
        return "Érvénytelen mérés!", 400
    query = (f"""
    SELECT nem, AVG({meres}) as atlag
    FROM meresek
    WHERE datum = '2025-03-01'
    GROUP BY nem
    """)
    print(query)


    cursor.execute(query)

    meres_atlagok = [dict(sor) for sor in cursor.fetchall()]
    conn.close()
    return render_template("meres.html", meres_atlagok = meres_atlagok)


if __name__ == "__main__":
    app.run(debug = True)