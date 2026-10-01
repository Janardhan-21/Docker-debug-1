from flask import Flask
import os
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "database"),
        database=os.getenv("DB_NAME", "debugdb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "correctpassword"),
        port=os.getenv("DB_PORT", "5432")
    )


@app.route("/")
def home():
    try:
        conn = get_db_connection()

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return f"""
        <html>
            <head>
                <title>Docker Debug Lab</title>
            </head>
            <body>
                <h1>Application is working!</h1>
                <p><strong>Database:</strong> {result[0]}</p>
                <p><strong>Status:</strong> Connected successfully</p>
            </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h1>Database connection failed</h1>
        <p>{e}</p>
        """, 500


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )