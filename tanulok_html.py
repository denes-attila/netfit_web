from flask import Blueprint, render_template, request
from database import get_db
from flask_login import login_required

tanulok_html = Blueprint('tanulok_html', __name__)

@tanulok_html.route("/")
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
    elso = [ sor for sor in tanulo_adatok if sor["datum"] == '2025-03-01']
    masodik = [ sor for sor in tanulo_adatok if sor["datum"] == '2026-03-01']
    conn.close()
    return render_template("tanulo.html", elso = elso, masodik = masodik) 

@tanulok_html.route("/osszehasonlitas")
@login_required
def osszehasonlitas():
    nev1 = request.args.get('nev1', '')
    nev2 = request.args.get('nev2', '')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * 
        FROM meresek
        WHERE nev = %s AND datum = '2025-03-01'
    """, (nev1,))
    tanulo1 = cursor.fetchone()
    cursor.execute("""
        SELECT * 
        FROM meresek
        WHERE nev = %s AND datum = '2025-03-01'
    """, (nev2,))
    tanulo2 = cursor.fetchone()
    conn.close()

    return render_template('osszehasonlitas.html', tanulo1 = tanulo1, tanulo2 = tanulo2)

@tanulok_html.route("/atlagok")
@login_required
def atlagok():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT nem, AVG(fekvotamasz) as atlag
    FROM meresek
    GROUP BY nem
    """)
    fekvotamasz_atlagok  = [dict(sor) for sor in cursor.fetchall()]
    conn.close()

    return render_template("atlagok.html", fekvotamasz_atlagok = fekvotamasz_atlagok)


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