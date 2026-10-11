from pathlib import Path
import pymupdf

try:
    from utility import root
except ImportError as e:
    raise SystemExit(
        f"{e}\nSetup needed: copy config.example.py -> config.py and "
        "utility.example.py -> utility.py (see README, 'How to run')."
    )
from question_splitter import run_splitter
from render_question import render_question
from db import export_to_db

""" Finds name of worksheet using the filename"""


def file_namer(pdf_path):
    return Path(pdf_path).stem


""" Runs important functions per worksheet."""


def run_on_page(pdf_path, document):
    worksheet_name = file_namer(pdf_path)
    question_list = run_splitter(document)
    render_question(question_list, worksheet_name, document)
    return question_list


""" Loop through all worksheets in folder.
    .rglob checks every folder, subfolder
    *.pdf, * is any character.
    pdf.part = tuple of all folders """

for pdf in Path(root).rglob("*.pdf"):

    """ANSWERS ARE STILL JUST PICTURES so skip them"""
    if "answer" in pdf.parts:
        continue

    else:
        document = pymupdf.open(pdf)
        print(pdf)
        question_list = run_on_page(pdf, document)
        export_to_db(question_list, pdf)
        for q in question_list:
            print(q)
