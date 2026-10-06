import os
import socket

from flask import Flask

app = Flask(__name__)

# Set by compose.yaml. Without it the app runs with no database.
DATABASE_URL = os.environ.get("DATABASE_URL")


def count_visit():
    import psycopg

    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS visits "
            "(id serial PRIMARY KEY, at timestamptz DEFAULT now())"
        )
        conn.execute("INSERT INTO visits DEFAULT VALUES")
        return conn.execute("SELECT count(*) FROM visits").fetchone()[0]


@app.get("/")
def home():
    greeting = os.environ.get("GREETING", "Hello")
    lines = [f"{greeting} from container {socket.gethostname()}!"]
    if DATABASE_URL:
        lines.append(f"Visits so far: {count_visit()}")
    return "\n".join(lines) + "\n"


@app.get("/health")
def health():
    return "ok\n"
