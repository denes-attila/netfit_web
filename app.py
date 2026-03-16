from flask import Flask, render_template, jsonify, request
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    meresek = ["suly", "magassag", "testzsir", "tavolugrás", "ingafutas",
           "fekvotamasz", "hajlekonysag", "szoritoeró", "torzsemeles"]
    return render_template("index.html", meresek = meresek)

def get_db():
    db_path = os.getenv("DATABASE_URL")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/tanulok")
def tanulok():
    conn = get_db()
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
    conn = get_db()
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
    conn = get_db()
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
    conn = get_db()
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

@app.route('/api/tanulok', methods = ['GET', 'POST'])
def tanulok_api():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        adat = request.get_json()
        nev = adat["nev"]
        nem = adat["nem"]
        kor = adat["kor"]
        sportolo = adat["sportolo"]
        datum = adat["datum"]
        suly = adat["suly"]
        magassag = adat["magassag"]
        testzsir = adat["testzsir"]
        tavolugrás = adat["tavolugrás"]
        ingafutas = adat["ingafutas"]
        fekvotamasz = adat["fekvotamasz"]
        hajlekonysag = adat["hajlekonysag"]
        szoritoeró = adat["szoritoeró"]
        torzsemeles = adat["torzsemeles"]
        cursor.execute(
            """
            INSERT INTO meresek (nev, nem, kor, sportolo, datum, suly, magassag, testzsir, tavolugrás, ingafutas, fekvotamasz,
            hajlekonysag, szoritoeró, torzsemeles)     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (nev, nem, kor, sportolo, datum, suly, magassag, testzsir, tavolugrás, ingafutas, fekvotamasz,
            hajlekonysag, szoritoeró, torzsemeles,)
        )
        conn.commit()
        conn.close()
        
        return jsonify({"uzenet": "Tanuló sikeresen hozzáadva"}), 201
    else:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT nev
        FROM meresek
        """)
        nevek = [dict(sor) for sor in cursor.fetchall()]
        conn.close()
        nevek = jsonify(nevek)
        return(nevek)

@app.route('/api/tanulo/<nev>', methods = ['GET', 'DELETE', 'PATCH', 'PUT'])
def tanulo_api(nev):

    if request.method == 'DELETE':
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT nev FROM meresek WHERE nev = ?
        """, (nev,)
        )
        adat = cursor.fetchall()
        if not adat:
            return jsonify("Nincs ilyen gyerek"), 404
        else:
            cursor.execute(
                """
                DELETE FROM meresek WHERE nev = ?
            """, (nev,)
            )
            
            conn.commit()
            conn.close()
            return jsonify({"uzenet": "Sikeresen törölve"}), 200
    elif  request.method == 'PATCH':
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT nev
        FROM meresek
        WHERE nev = ?

        """, (nev,))
        keresett_nev = cursor.fetchall()
        if not keresett_nev:
            return jsonify("Nincs ilyen tanuló "), 404
        else:
            adat = request.get_json()
            mezok = ", ".join([f"{k} = ?" for k in adat.keys()])
            ertekek = list(adat.values())
            ertekek.append(nev)
            cursor.execute(
            f"UPDATE meresek SET {mezok} WHERE nev = ?",
                ertekek
            )
            conn.commit()
            conn.close()
            return jsonify("Sikeres módosítás"), 200
    elif request.method == 'PUT':
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT nev FROM meresek WHERE nev = ?
            """, (nev,)
        )
        keresett_nev = cursor.fetchall()
        if not keresett_nev:
            return jsonify("Nincs ilyen nevű gyerek"), 404
        else:
            adat = request.get_json()
            adat_nev = adat["nev"]
            nem = adat["nem"]
            kor = adat["kor"]
            sportolo = adat["sportolo"]
            datum = adat["datum"]
            suly = adat["suly"]
            magassag = adat["magassag"]
            testzsir = adat["testzsir"]
            tavolugrás = adat["tavolugrás"]
            ingafutas = adat["ingafutas"]
            fekvotamasz = adat["fekvotamasz"]
            hajlekonysag = adat["hajlekonysag"]
            szoritoeró = adat["szoritoeró"]
            torzsemeles = adat["torzsemeles"]
            cursor.execute(
                """
                UPDATE meresek SET nev = ?, nem=?, kor = ?, sportolo = ?, datum = ?, suly = ?, magassag = ?,
                testzsir =?, tavolugrás=?, ingafutas=?, fekvotamasz =?, hajlekonysag = ?, szoritoeró= ?, torzsemeles=?
                WHERE nev = ?
                """, (adat_nev, nem, kor, sportolo, datum, suly, magassag, testzsir, tavolugrás, ingafutas, fekvotamasz,
                hajlekonysag, szoritoeró, torzsemeles, nev,)
            )
            conn.commit()
            conn.close()
            return jsonify("Row succesfull updated"), 200
    else:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT *
        FROM meresek
        WHERE nev = ?

        """, (nev,))


        tanulo_adatok = [dict(sor) for sor in cursor.fetchall()]
        if not tanulo_adatok:
            return jsonify("Nincs ilyen nevű gyerek"), 404
        else:
            tanulo_adatok = jsonify(tanulo_adatok)
            return(tanulo_adatok)

@app.route("/api/atlag/<meres>", methods=['POST'] )
def meres_atlag_api(meres):
    conn = get_db()
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