from pathlib import Path
import pymupdf

try:
    from utility import SOURCES
except ImportError as e:
    raise SystemExit(
        f"{e}\nSetup needed: copy config.example.py -> config.py and "
        "utility.example.py -> utility.py (see README, 'How to run')."
    )
from question_splitter import run_splitter
from render_question import render_question
from db import connect, init_db, export_to_db
from topics import TOPICS, CATEGORY_DESCRIPTIONS, HIGHER_ONLY

""" Finds name of worksheet using the filename"""


def file_namer(pdf_path):
    return Path(pdf_path).stem


""" Runs important functions per worksheet."""


def run_on_page(pdf_path, document, config):
    worksheet_name = file_namer(pdf_path)
    question_list = run_splitter(document, config)
    render_question(question_list, worksheet_name, document)
    return question_list


def save_to_db():
    con = connect()
    try:
        init_db(con, TOPICS, CATEGORY_DESCRIPTIONS, HIGHER_ONLY)
        export_to_db(con, question_list, pdf)
    finally:
        con.close()


""" Loop through all worksheets in folder.
    .rglob checks every folder, subfolder
    *.pdf, * is any character.
    pdf.part = tuple of all folders """
for name, cfg in SOURCES.items():
    for pdf in Path(cfg["root"]).rglob("*.pdf"):

        """ANSWERS ARE STILL JUST PICTURES so skip them"""
        if "answers" in pdf.parts:
            continue

        else:
            document = pymupdf.open(pdf)
            question_list = run_on_page(pdf, document, cfg)
            print(f"\n{pdf}")
            for q in question_list:
                print(q)
            save_to_db()
