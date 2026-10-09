from pathlib import Path
import pymupdf
from utility import root
from question_splitter import run_splitter
from render_question import render_question

""" Finds name of worksheet using the filename"""


def file_namer(pdf_path):
    return Path(pdf_path).name.rstrip(".pdf")


""" Runs important functions per worksheet."""


def run_on_page(pdf_path, document):
    worksheet_name = file_namer(pdf_path)
    regions = run_splitter(document)
    render_question(regions, worksheet_name, document)


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
        run_on_page(pdf, document)
