import sqlite3
import json

""" talks to database"""


def connect(db_path="questions.db"):
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL;")  # lets readers and a writer can overlap
    con.execute("PRAGMA foreign_keys = ON;")
    return con


def create_topics(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS  topics (
            id        INTEGER PRIMARY KEY,
            name      TEXT NOT NULL,
            higher_only INTEGER NOT NULL DEFAULT 0,
            parent_id INTEGER REFERENCES topics(id),
            description TEXT,
            UNIQUE (parent_id, name)
        )""")
    con.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_topics_top_level
        ON topics(name) WHERE parent_id IS NULL
    """)
    con.commit()


def create_question_topics(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS question_topics (
        question_id INTEGER NOT NULL REFERENCES questions(id),
        topic_id    INTEGER NOT NULL REFERENCES topics(id),
        is_primary  INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (question_id, topic_id)
        )
    """)
    con.commit()


# Add later, marks, answers image path, ai_topics, ai_difficulty.
def create_path_table(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY,
            idx         INTEGER NOT NULL,
            source_pdf  TEXT NOT NULL,  
            number      TEXT NOT NULL,
            regions     TEXT NOT NULL,
            image_path  TEXT,
            source      TEXT,
            subject     TEXT,
            board       TEXT,
            level       TEXT,     
            UNIQUE (source_pdf, idx)
        )
    """)
    con.commit()


def create_tables(con):
    create_path_table(con)
    create_topics(con)
    create_question_topics(con)


def reset_tables(con):
    with con:
        con.executescript("""   DROP TABLE IF EXISTS question_topics;
                                    DROP TABLE IF EXISTS questions;
                                    DROP TABLE IF EXISTS topics;""")


def add_topic(con, name, higher_only=0, parent_id=None, description=None):
    current = con.execute(
        "INSERT INTO topics (name,higher_only, parent_id, description)VALUES (?,?,?, ?)",
        (name, higher_only, parent_id, description),
    )
    return current.lastrowid  # returns id


# source path is OG pdf path
def save_question(con, idx, source_pdf, question):
    con.execute(
        "INSERT INTO questions (idx, source_pdf, number, regions, image_path)VALUES (?, ?, ?, ?, ?)",
        (
            idx,
            str(source_pdf),
            question.number,
            json.dumps(question.regions),
            question.path,
        ),
    )


def link_question_topic(con, question_id, topic_id, is_primary):
    con.execute(
        "INSERT INTO question_topics (question_id, topic_id, is_primary)VALUES (?, ?, ?)",
        (question_id, topic_id, is_primary),
    )


def seed_topic(con, topics, category_descriptions, higher_only):
    all_names = {sub["name"] for subs in topics.values() for sub in subs}
    missing = higher_only - all_names
    assert not missing, missing
    with con:
        for category, subtopics in topics.items():
            parent_id = add_topic(
                con, category, description=category_descriptions[category]
            )
            for sub in subtopics:
                add_topic(
                    con,
                    sub["name"],
                    int(sub["name"] in higher_only),
                    parent_id,
                    sub["description"],
                )


def init_db(con, topics, category_descriptions, higher_only):
    reset_tables(con)
    create_tables(con)
    seed_topic(con, topics, category_descriptions, higher_only)


def export_to_db(con, questions, pdf_path):
    with con:
        for q in questions:
            save_question(con, q.idx, pdf_path, q)
            con.commit()


if __name__ == "__main__":
    pass
