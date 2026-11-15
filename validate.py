"""To be ran per document"""

import pymupdf
import re
import csv
import logging
from models import WorksheetReport
from utility import SOURCES, pdf, strip_chain

logging.basicConfig(level=logging.DEBUG)
validator_logger = logging.getLogger("validator")
validator_logger.disabled = True

# need to fix dot should be universal
doc = pymupdf.open(pdf)
BLANK = re.compile(r"\s*(\d+\.)?\s*")  # nothing, or just a number and a dot


# Need to fix too many lambda & regular functions combined.


# Sets up marker for different markers re.escape does literal marker.
def marker_pattern(marker):
    return rf"^\d+{re.escape(marker)}(\s|$)"


def is_blank(text):
    # compile once not multiple times.
    return BLANK.fullmatch(text) is not None


def flatten(by_page):
    # [[1,2,3],[1,2,3]] = [1,2,3,1,2,3]
    return [n for nums in by_page for n in nums]


def list_minus(a, b):
    remove = set(b)  # set allows hash(quicker)
    return [x for x in a if x not in remove]


def missing_q(pattern):
    return lambda r: list_minus(
        flatten(r.pdf_numbering[pattern]), r.extracted_numbering
    )


def extra_q(pattern):
    return lambda r: list_minus(
        r.extracted_numbering, flatten(r.pdf_numbering[pattern])
    )


def is_sequential(numbers):  # [ 1,2,3,4,5]
    length = len(numbers)
    return numbers == list(range(1, length + 1)) or length <= 1


def marks_to_numbers(nested):
    # [[3,2], [1], [3,2]]
    results = []
    i = 1
    for page in nested:
        new_page = []
        for _ in page:
            new_page.append(i)
            i += 1
        results.append(new_page)
    return results


# ---------------------------------------------------------------------------
# Per-DOCUMENT checks
# ---------------------------------------------------------------------------


# Checks if any questions are missing/extra from pdf/extracted
def is_missing_extra(name: str, calculation):
    def check(r):
        flags = []
        for pattern in r.pdf_numbering.keys():
            difference = calculation(pattern)(r)
            if difference:
                flags.append((f"{name} based on {pattern}", difference))
        return flags

    return check


# Checks both pdf and extracted are sequential.
def non_sequential(name, number_list):
    def check(r):
        nums = number_list(r)
        # print(f"name: {name}, nums: {nums}")
        if not is_sequential(nums):
            return [(name, nums)]
        return []

    return check


# ---------------------------------------------------------------------------
# Per-PAGE checks
# ---------------------------------------------------------------------------


# lost_words: Checks if there is any text (within limits) that is not attached to a question
def lost_words(name, doc, get_numbers, get_regions, cfg, tolerance=1.5):
    def check(r):
        # total height per page dict
        by_page = {}
        for number, question in zip(get_numbers(r), get_regions(r)):
            for page_no, y_start, y_end in question:
                # sets default when no question is discovered
                by_page.setdefault(page_no, []).append((number, y_start, y_end))

        output = {}
        for idx, page in enumerate(doc(r)):
            if cfg(r)["SKIP_PAGE_ONE"] and idx == 0:
                continue
            limit = page.rect.height - cfg(r)["footer cutoff"]
            page_regions = by_page.get(idx, [])
            for x0, y0, x1, y1, text, *_ in page.get_text("words"):
                if y0 > limit:
                    continue
                if not any(
                    y_start - tolerance <= y0 and y1 - tolerance <= y_end
                    for _, y_start, y_end in page_regions
                ):
                    entry = output.setdefault(
                        f"pg.{idx+1}",
                        {
                            "questions": sorted({n for n, _, _ in page_regions}),
                            "y": [],
                        },
                    )
                    entry["y"].append((round(y0, 1)))

        if output:
            return [name, f"Missing words from any questions: {output}"]
        return []

    return check


# ---------------------------------------------------------------------------
# Per-QUESTION checks
# ---------------------------------------------------------------------------


# split_question: every question should contain at least one marker (e.g. "2."),
# so a question with zero matches is flagged together with the previous question.
def split_question(name, get_numbers, get_texts, get_marker):
    # input = ['1. (a) blah blah'] = missing end of question or ['(b) blah'] = missing beginning of question
    def check(r):
        numbers = get_numbers(r)
        split = []
        regex = re.compile(marker_pattern(get_marker(r)), re.MULTILINE)
        for idx, text in enumerate(get_texts(r)):
            matches = [m.group(0) for m in regex.finditer(text)]
            if len(matches) == 0:  # checks if there is not question number
                prev = numbers[idx - 1] if idx > 0 else None
                split.append((prev, numbers[idx]))
        if split:
            return [name, f"question split between these pairs, {split}"]
        return []

    return check


# Checks if multiple questions are attached to one question object
def merged_question(name, get_texts, get_marker):  # ['1. why blah blah\n 2. blah blah']
    # marker is per source, so the regex is built per report, not at import.
    def check(r):
        flags = []
        regex = re.compile(marker_pattern(get_marker(r)), re.MULTILINE)
        for text in get_texts(r):
            matches = [m.group(0) for m in regex.finditer(text)]
            if len(matches) >= 2:
                flags.append((name, matches, len(matches)))
        return flags

    return check


# Checks if there is any text in question object
def empty_question(name, get_numbers, get_texts):
    def check(r):
        flags = []
        for number, text in zip(get_numbers(r), get_texts(r)):
            if is_blank(text):
                flags.append((name, number, text))
        return flags

    return check


FAILURE_MODES = {
    # Per-DOC checks
    "MISSING_QUESTION": "Questions found in the PDF text greater than extracted one",
    "EXTRA_QUESTION": "Questions found in PDF is less than extracted ones",
    "SEQUENCE": "Numbers extracted but out of order or with gaps, like 1,2,4,3 or 1,2,5",
    "PDF_NON-SEQUENTIAL": "PDF is NON-SEQUENTIAL",
    "EXTRACTED_NON-SEQUENTIAL": "EXTRACTED is NON-SEQUENTIAL",
    # Per-PAGE checks
    "LOST_WORDS": "Words on page are missing from any questions on page",
    # Per-QUESTION checks
    "SPLIT_QUESTION": "One question cut into multiple pieces",
    "MERGED_QUESTION": "Multiple questions joined into one",
    "EMPTY_QUESTION": "Number found but no body content",
    "NONE": "No known failures",
}


""" Checks contains checks and flags to raise, needs output a (str, list)
    [] means no failure and is skipped when building true flags """
CHECKS = [
    is_missing_extra("MISSING_QUESTION", missing_q),
    is_missing_extra("EXTRA_QUESTION", extra_q),
    # no of marks is not sequential so only ran on numbering
    non_sequential(
        "PDF_NON-SEQUENTIAL", lambda r: flatten(r.pdf_numbering["numbering"])
    ),
    non_sequential("EXTRACTED_NON-SEQUENTIAL", lambda r: r.extracted_numbering),
    lost_words(
        "LOST WORDS",
        lambda r: r.document,
        lambda r: r.numbers,
        lambda r: r.regions,
        lambda r: r.config,
    ),
    split_question(
        "SPLIT QUESTION",
        lambda r: r.numbers,
        lambda r: r.texts,
        lambda r: r.config["question marker"],
    ),
    merged_question(
        "MERGED_QUESTION", lambda r: r.texts, lambda r: r.config["question marker"]
    ),  #   add question marker pattern
    empty_question("EMPTY_QUESTION", lambda r: r.numbers, lambda r: r.texts),
]


# Get a list of stripped numbers from 1., 1:, etc
def strip_number(questions, conditions: list):
    numbers = []
    for q in questions:
        stripped = strip_chain(q, conditions)
        if stripped:
            numbers.append(stripped)
    return numbers  # [1, 2, 3, 4]


#   How failure mode is selected
#   For each check in CHECKS, then for each flag in what that check returns, collect the flag.
#   if [] then nothing to loop over so it is skipped.
def select_failure_mode(report):
    flags = [flag for check in CHECKS for flag in check(report)]
    return flags or [("NONE", None)]


def group_line(page):
    lines = {}
    for w in page.get_text("words"):
        # sets line by adding word with block_no, line_no
        lines.setdefault((w[5], w[6]), []).append(w)
    for words in lines.values():
        # Sorts by word no
        words.sort(key=lambda w: w[7])
        # generator yielding lines and line info every pass
        yield " ".join(w[4] for w in words), words


def count_matches(document, pattern, SKIP_PAGE_ONE):
    # Number of "marks)" or "1." etc on across all pages or question numbers found anywhere on page.
    regex = re.compile(pattern)
    question_list = []  # output
    flattened = []
    total = 0
    for page_idx, page in enumerate(document):
        if SKIP_PAGE_ONE:
            if page_idx == 0:
                continue
        question_details = []
        for line_text, line_w in group_line(page):
            # x0, y0, x1, y1, text, block_no, line_no, word_no = w
            if regex.search(line_text):
                question_details.append(
                    line_w
                )  # need to move this and only append text
                total += 1
        if question_details:
            text = [word[4] for detail in question_details for word in detail]
            question_list.append(text)  # would currently delete
            flattened.extend(text)

    return total, question_list  # [4, ["1.","2.","3.","4."]]


def count_expected_no(document, config):
    counts = {}
    count_list = {}
    marks_list = {}
    quest_list = {}
    for method in config["patterns"]:  # e.g. ["marks", "numbering"]
        counts[method], count_list[method] = count_matches(
            document, config["patterns"][method], config["SKIP_PAGE_ONE"]
        )
        # Prints raw strings.
        validator_logger.debug(f"\n{method} = {count_list[method]}")
        if method == "numbering":
            quest_list[method] = [
                strip_number(line, [re.compile(r"^\d+\.(\s|$)"), re.compile(r"\d+")])
                for line in count_list[method]
            ]
        if method == "marks":
            marks_list[method] = [
                strip_number(line, [re.compile(r"\d+")]) for line in count_list[method]
            ]
            quest_list["marks"] = marks_to_numbers(marks_list[method])

        # Prints processed data
        validator_logger.debug(f" {method} = {quest_list[method]}")

    # ({"marks": 3, "numbering": 5, {"marks": [1,2,3,4], "numbering": [1,2,3,4,5]
    return (counts, quest_list)


def count_actual_no(question_list):
    numbers = []
    for question in question_list:
        numbers.append(question.number)
    stripped_numbers = strip_number(numbers, [re.compile(r"\d+")])
    return len(question_list), stripped_numbers  # [3, ["1", "2" ,"3"]]


def reset_report(path="validation_flagged.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        pass


def save_validation(report):
    with open("validation_flagged.csv", "a", newline="") as csvfile:
        flag_writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        flag_writer.writerow([report.name, report.flag])


def validate_on_sheet(name, document, config, question_list):
    number_list = [question.number for question in question_list]
    text_list = [question.text for question in question_list]
    region_list = [question.region for question in question_list]
    expected, exp_questions = count_expected_no(document, config)
    actual, act_questions = count_actual_no(question_list)
    marker = config["question marker"]  # "." or ":", turned into a regex per check
    # print(exp_questions, act_questions)

    report = WorksheetReport(
        name,
        number_list,
        text_list,
        region_list,
        document,
        config,
        expected,
        actual,
        exp_questions,
        act_questions,
        list_minus(exp_questions, act_questions),
        status={
            name: ("PASS" if count == actual else "FAIL")
            for name, count in expected.items()
        },  # {"marks": "PASS", "numbering": "FAIL"}
    )
    report.flag = select_failure_mode(report)
    if report.flag[0][1] != None:
        save_validation(report)
        print(report.flag)

    return report
