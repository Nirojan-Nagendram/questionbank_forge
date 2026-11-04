from pathlib import Path
import pymupdf

try:
    from utility import SOURCES
except ImportError as e:
    raise SystemExit(
        f"{e}\nSetup needed: copy utility.example.py -> utility.py "
        "(see README, 'How to run')."
    )
from question_splitter import run_splitter
from render_question import render_question
from db import connect, init_db, export_to_db
from topics import TOPICS, CATEGORY_DESCRIPTIONS, HIGHER_ONLY

from validate import validate_on_sheet

""" Finds name of worksheet using the filename"""


def file_namer(pdf_path):
    return Path(pdf_path).stem


""" Runs important functions per worksheet."""


def run_on_page(pdf_path, document, config):
    worksheet_name = file_namer(pdf_path)
    question_list = run_splitter(document, config)
    render_question(question_list, worksheet_name, document)
    # print(f"\n {question_list[0]}\n")
    report = validate_on_sheet(worksheet_name, document, config, question_list)
    return question_list, report


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
reports = []
for name, cfg in SOURCES.items():
    for pdf in Path(cfg["root"]).rglob("*.pdf"):

        """ANSWERS ARE STILL JUST PICTURES so skip them"""
        if "answers" in pdf.parts or not cfg["enabled"]:
            continue

        else:
            document = pymupdf.open(pdf)
            print(f"\n{pdf}")
            question_list, current_report = run_on_page(pdf, document, cfg)
            reports.append(current_report)
            for q in question_list:
                # print(q)pdf_p
                pass
            save_to_db()
