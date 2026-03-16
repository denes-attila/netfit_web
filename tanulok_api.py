from flask import jsonify, request
from database import get_db
from flask import Blueprint

tanulok_api = Blueprint('tanulok_api', __name__)

@tanulok_api.route('/api/tanulok', methods = ['GET', 'POST'])
def tanulok_list_api():
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

@tanulok_api.route('/api/tanulo/<nev>', methods = ['GET', 'DELETE', 'PATCH', 'PUT'])
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

@tanulok_api.route("/api/atlag/<meres>", methods=['POST'] )
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