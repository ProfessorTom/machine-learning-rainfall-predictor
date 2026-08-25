from dotenv import load_dotenv
from flask import Flask

import db
import os

DEBUG = True

load_dotenv()
app = Flask(__name__)
# db.init_db()


@app.route("/")
def home():
    db_status = db.get_db_status()
    return f"""
        <h1>Rainfall Predictor</h1>
        <p>{db_status}</p>
    """


def print_db_variables_debug():
    print("\n")
    print(f"CACHE_DB_NAME from env: {os.getenv("CACHE_DB_NAME")}")
    print(f"CACHE_DB_DIR from env: {os.getenv("CACHE_DB_DIR")}")

    print("\n")
    print(f"db.CACHE_DB_DIR: {db.CACHE_DB_DIR}")
    print(f"db.CACHE_DB_NAME: {db.CACHE_DB_NAME}")
    print(f"db.CACHE_DB_PATH: {db.CACHE_DB_PATH}")


if __name__ == "__main__":

    if DEBUG:
        print_db_variables_debug()

    app.run(debug=DEBUG, use_reloader=False)
