from flask import Blueprint, render_template
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


@tanulok_html.route("/tanulo/<nev>")
@login_required
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

@tanulok_html.route("/atlagok")
@login_required
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