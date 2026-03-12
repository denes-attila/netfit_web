from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    meresek = ["suly", "magassag", "testzsir", "tavolugrás", "ingafutas",
           "fekvotamasz", "hajlekonysag", "szoritoeró", "torzsemeles"]
    return render_template("index.html", meresek = meresek)



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
    elso = [ sor for sor in tanulo_adatok if sor["datum"] == '2025-03-01']
    masodik = [ sor for sor in tanulo_adatok if sor["datum"] == '2026-03-01']
    conn.close()
    return render_template("tanulo.html", elso = elso, masodik = masodik) 

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


def osszes_atlag(meres):
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
    return render_template("meres.html", meres_atlagok = meres_atlagok, meresek = meresek)

@app.route('/api/tanulok')
def tanulok_api():
    conn = sqlite3.connect("../netfit_proc/netfit.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT nev
    FROM meresek
    """)
    nevek = [dict(sor) for sor in cursor.fetchall()]
    conn.close()
    nevek = jsonify(nevek)
    return(nevek)

@app.route('/api/tanulo/<nev>')
def tanulo_api(nev):
    conn = sqlite3.connect("../netfit_proc/netfit.db")
    conn.row_factory =sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM meresek
    WHERE nev = ?

    """, (nev,))

    tanulo_adatok = [dict(sor) for sor in cursor.fetchall()]
    tanulo_adatok = jsonify(tanulo_adatok)
    return(tanulo_adatok)

@app.route("/api/atlag/<meres>", methods=['POST'] )
def meres_atlag_api(meres):
    conn = sqlite3.connect('../netfit_proc/netfit.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    meresek = ["suly", "magassag", "testzsir", "tavolugrás", "ingafutas",
           "fekvotamasz", "hajlekonysag", "szoritoeró", "torzsemeles"]
    adat = request.get_json()
    nem = adat["nem"]

    if meres not in meresek:
        return "Érvénytelen mérés!", 400
    cursor.execute(f"""
    SELECT nem, AVG({meres}) as atlag
    FROM meresek
    WHERE nem = ?
    
    """, (nem,))

    meres_atlagok = [dict(sor) for sor in cursor.fetchall()]
    conn.close()
    return jsonify(meres_atlagok)

if __name__ == "__main__":
    app.run(debug = True)