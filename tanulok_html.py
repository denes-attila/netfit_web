from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db
from flask_login import login_required

tanulok_html = Blueprint('tanulok_html', __name__)

@tanulok_html.route("/")
@login_required
def index():
    meresek = ["suly", "magassag", "testzsir", "tavolugrás", "ingafutas",
           "fekvotamasz", "hajlekonysag", "szoritoeró", "torzsemeles"]
    return render_template("index.html", meresek = meresek)


@tanulok_html.route("/tanulok")
@login_required
def tanulok():
    hasonlit = request.args.get('hasonlit', '')
    kereses = request.args.get('kereses', '')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT nev
        FROM meresek WHERE nev LIKE %s
    """, (f'%{kereses}%',))

    sorok = cursor.fetchall()
    conn.close()

    nevek = [sor["nev"] for sor in sorok]

    return render_template("tanulok.html", nevek = nevek, kereses = kereses, hasonlit = hasonlit)


@tanulok_html.route("/tanulo/<nev>")
@login_required
def tanulo(nev):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * 
        FROM meresek
        WHERE nev = %s
        
    """, (nev,))

    tanulo_adatok = [dict(sor) for sor in cursor.fetchall()]
    conn.close()
    return render_template("tanulo.html", adatok = tanulo_adatok) 

@tanulok_html.route("/osszehasonlitas")
@login_required
def osszehasonlitas():
    nev1 = request.args.get('nev1', '')
    nev2 = request.args.get('nev2', '')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM meresek
        WHERE nev = %s
        ORDER BY datum ASC
        LIMIT 1
        """, (nev1,))
    tanulo1 = cursor.fetchone()
    cursor.execute("""
        SELECT * FROM meresek
        WHERE nev = %s
        ORDER BY datum ASC
        LIMIT 1
        """, (nev2,))
    tanulo2 = cursor.fetchone()
    conn.close()

    return render_template('osszehasonlitas.html', tanulo1 = tanulo1, tanulo2 = tanulo2)


@tanulok_html.route("/atlagok/<meres>")
@login_required
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

@tanulok_html.route("/uj_tanulo", methods = ['GET', 'POST'])
@login_required
def uj_tanulo():
    if request.method == 'GET':
        return render_template('uj_tanulo.html')
    elif request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        adat = request.form
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
            hajlekonysag, szoritoeró, torzsemeles)     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (nev, nem, kor, sportolo, datum, suly, magassag, testzsir, tavolugrás, ingafutas, fekvotamasz,
            hajlekonysag, szoritoeró, torzsemeles,)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('tanulok_html.tanulok'))