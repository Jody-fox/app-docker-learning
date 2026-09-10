from flask import Flask, request, redirect
import os
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "dockerdb"),
        user=os.getenv("DB_USER", "dockeruser"),
        password=os.getenv("DB_PASSWORD", "dockerpass"),
    )


@app.route("/", methods=["GET", "POST"])
def home():
    messaggio = ""

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persone (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL
        )
    """)

    if request.method == "POST":

        azione = request.form.get("azione")

        if azione == "inserisci":
            nome = request.form.get("nome_inserisci", "").strip()

            if nome:
                cur.execute(
                    "INSERT INTO persone (nome) VALUES (%s)",
                    (nome,)
                )
                conn.commit()

            cur.close()
            conn.close()

            return redirect("/")

        elif azione == "cerca":
            nome = request.form.get("nome_cerca", "").strip()

            if nome:
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM persone
                    WHERE LOWER(nome) = LOWER(%s)
                    """,
                    (nome,)
                )

                quanti = cur.fetchone()[0]

                if quanti == 0:
                    messaggio = f"Non ci sono persone registrate con il nome {nome}."
                elif quanti == 1:
                    messaggio = f"C'è 1 persona registrata con il nome {nome}."
                else:
                    messaggio = f"Ci sono {quanti} persone registrate con il nome {nome}."

    conn.commit()
    cur.close()
    conn.close()

    return f"""
    <h1>Docker Learning App</h1>

    <p>Connessione a PostgreSQL riuscita.</p>

    <h2>Inserisci il tuo nome</h2>

    <form method="POST">
        <input
            type="text"
            name="nome_inserisci"
            placeholder="Inserisci il tuo nome"
            required
        >

        <button
            type="submit"
            name="azione"
            value="inserisci"
        >
            Salva
        </button>
    </form>

    <hr>

    <h2>Cerca persone con il tuo nome</h2>

    <form method="POST">
        <input
            type="text"
            name="nome_cerca"
            placeholder="Nome da cercare"
            required
        >

        <button
            type="submit"
            name="azione"
            value="cerca"
        >
            Cerca
        </button>
    </form>

    <h3>{messaggio}</h3>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)