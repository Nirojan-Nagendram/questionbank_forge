"""
Which worksheet source to process. Copy this file to utility.py and edit.
Pick ONE source by setting its flag to True, then point the paths at your PDFs.
"""

import pymupdf
from config import example_source_a_dict, example_source_b_dict
from helpers import print_page_details  # noqa: F401 (re-exported for printer.py)

# Source flags
example_source_a = True
example_source_b = False

debug = True

if example_source_a:
    pdf_path = r"pdf_folder\example_source_a\questions\Example Worksheet.pdf"
    root = r"pdf_folder\example_source_a"
    footer_cutoff = example_source_a_dict["footer cutoff"]
    left_margin = example_source_a_dict["left margin"]
    gap = example_source_a_dict["gap"]
    question_marker = example_source_a_dict["question marker"]
    SKIP_PAGE_ONE = False

elif example_source_b:
    pdf_path = r"pdf_folder\example_source_b\questions\Example Worksheet.pdf"
    root = r"pdf_folder\example_source_b"
    header_cutoff = example_source_b_dict["header cutoff"]
    footer_cutoff = example_source_b_dict["footer cutoff"]
    left_margin = example_source_b_dict["left margin"]
    gap = example_source_b_dict["gap"]
    question_marker = example_source_b_dict["question marker"]
    SKIP_PAGE_ONE = True

doc = pymupdf.open(pdf_path)
