"""
Per-source layout settings. Copy this file to config.py and edit the values.
Measure them for your own PDFs (printer.py prints each word's position).

left margin     : x position (in points) where a question number starts
header cutoff   : how far down from the top to ignore (0 = nothing)
footer cutoff   : how far off the bottom to cut off
gap             : spacing used when stitching regions together
question marker : the character a question number ends with, e.g. "1." or "1:"
"""

example_source_a_dict = {
    "left margin": 50,
    "header cutoff": 0,
    "footer cutoff": 60,
    "gap": 1,
    "question marker": ".",
}

example_source_b_dict = {
    "left margin": 100,
    "header cutoff": 120,
    "footer cutoff": 60,
    "gap": 1,
    "question marker": ":",
}
