"""
Worksheet sources and their layout settings. Copy this file to utility.py and edit.
Add one entry to SOURCES per worksheet type, and measure the values for your own
PDFs (helpers.print_page_details prints each word's position).

enabled          : set to False to skip this source when running main.py
root             : folder searched (including subfolders) for PDFs
header cutoff    : how far down from the top to ignore (0 = nothing)
footer cutoff    : how far up from the bottom to cut off
left margin      : x position (in points) where a question number starts
gap              : spacing used when stitching regions together
question marker  : the character a question number ends with, e.g. "1." or "1:"
SKIP_PAGE_ONE    : ignore the first page (e.g. a cover sheet)
LAST_PAGE_FOOTER : the last page has its own footer that needs cutting off
"""

SOURCES = {
    "example source a": {
        "enabled": True,
        "root": R"pdf_folder\example_source_a",
        "header cutoff": 0,
        "footer cutoff": 60,
        "left margin": 50,
        "gap": 1,
        "question marker": ".",
        "SKIP_PAGE_ONE": False,
        "LAST_PAGE_FOOTER": False,
    },
    "example source b": {
        "enabled": False,
        "root": R"pdf_folder\example_source_b",
        "header cutoff": 120,
        "footer cutoff": 60,
        "left margin": 100,
        "gap": 1,
        "question marker": ":",
        "SKIP_PAGE_ONE": True,
        "LAST_PAGE_FOOTER": True,
    },
}
