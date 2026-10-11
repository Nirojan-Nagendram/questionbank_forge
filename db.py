import sqlite3
import json

""" talks to database"""


def connect(db_path="questions.db"):
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL;")  # lets readers and a writer can overlap
    return con


# Add later, marks, answers image path, ai_topics, ai_difficulty.
def create_tables(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY,
            source_pdf  TEXT NOT NULL,  
            number      TEXT NOT NULL,
            regions     TEXT NOT NULL,
            image_path  TEXT,
            source      TEXT,
            subject     TEXT,
            board       TEXT,
            level       TEXT,
            topic       TEXT,       
            UNIQUE (source_pdf, number)
        )
    """)
    con.commit()


# source path is OG pdf path
def save_question(con, source_pdf, question):
    con.execute(
        "INSERT INTO questions (source_pdf, number, regions, image_path)VALUES (?, ?, ?, ?)",
        (str(source_pdf), question.number, json.dumps(question.regions), question.path),
    )


def export_to_db(questions, pdf_path):
    con = connect()
    con.execute("DROP TABLE IF EXISTS questions")
    create_tables(con)
    for q in questions:
        with con:
            save_question(con, pdf_path, q)
            con.commit()
    con.close()


if __name__ == "__main__":
    pass
