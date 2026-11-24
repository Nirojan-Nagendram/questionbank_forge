"""To be ran per document"""

import pymupdf
import re
import csv
import logging
import os
from models import WorksheetReport
from utility import pdf
from helpers import find_footer_limit, strip_chain

logging.basicConfig(level=logging.DEBUG)
validator_logger = logging.getLogger("validator")
validator_logger.disabled = True

# need to fix dot should be universal
doc = pymupdf.open(pdf)
BLANK = re.compile(r"\s*(\d+\.)?\s*")  # nothing, or just a number and a dot
DIGIT = re.compile(r"\d+")


# Need to fix too many lambda & regular functions combined.


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


def is_sequential(numbers):  # [1,2,3,4,5] or [1,2,3,1,2,3]
    expected = 1
    for n in numbers:
        if n == 1:
            expected = 1
        elif n != expected:
            return False
        expected += 1
    return True


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
            return [(name, f"sequence: {nums}")]
        return []

    return check


# ---------------------------------------------------------------------------
# Per-PAGE checks
# ---------------------------------------------------------------------------


# lost_words: Checks if there is any text (within limits) that is not attached to a question
# starts from first question
def lost_words(name, doc, get_numbers, get_regions, cfg, tolerance=1.5):
    def check(r):
        by_page = {}
        for number, question in zip(get_numbers(r), get_regions(r)):
            for page_no, y_start, y_end in question:
                # sets default when no question is discovered
                by_page.setdefault(page_no, []).append((number, y_start, y_end))
        first_page = min(by_page, default=None)
        intro_limit = (
            min(y_start for number, y_start, y_end in by_page[first_page])
            if first_page is not None
            else 0
        )

        output = {}
        for idx, page in enumerate(doc(r)):
            if cfg(r)["SKIP_PAGE_ONE"] and idx == 0:
                continue
            header_limit = cfg(r)["header cutoff"]
            if idx == first_page:
                header_limit = max(header_limit, intro_limit - tolerance)
            footer_limit = page.rect.height - cfg(r)["footer cutoff"]
            if cfg(r)["LAST_PAGE_FOOTER"] and idx + 1 == len(doc(r)):
                footer_limit = find_footer_limit(page, cfg(r), footer_limit)
            page_regions = by_page.get(idx, [])
            for _, y0, _, y1, text, *_ in page.get_text("words"):
                # print(text)
                if y0 > footer_limit or y0 < header_limit:
                    continue
                mid = (y0 + y1) / 2
                if not any(
                    y_start - tolerance <= mid and mid - tolerance <= y_end
                    for _, y_start, y_end in page_regions
                ):
                    entry = output.setdefault(
                        f"pg.{idx+1}",
                        {
                            "cutoff": sorted({n for n, _, _ in page_regions}),
                            "words": [],
                            "y": [],
                        },
                    )
                    entry["words"].append(text)
                    entry["y"].append((round(y0)))
            # print(e["words"] for pg, e in output.items())
            # print(output["words"])
            summary = {
                pg: f"{len(e['words'])} words, e.g. {e['words'][:2]} ... {e['words'][-1:]}, "
                f"y={e['y'][:3]} ... {e['y'][-3:]}, near questions {e['cutoff']}"  # printing raw characters rather than newline
                for pg, e in output.items()
            }
        # l your working. (3 marks) ___________________________________________________________________________
        if output:
            return [
                (
                    name,
                    f"Missing words:\n"
                    + "\n".join(f"{pg}: {info}" for pg, info in summary.items()),
                )
            ]
        return []

    return check


# ---------------------------------------------------------------------------
# Per-QUESTION checks
# ---------------------------------------------------------------------------


# split_question: every question should contain at least one marker (e.g. "2."),
# so a question with zero matches is flagged together with the previous question.
def split_question(name, get_numbers, get_texts, get_pattern):
    # input = ['1. (a) blah blah'] = missing end of question or ['(b) blah'] = missing beginning of question
    def check(r):
        numbers = get_numbers(r)
        split = []
        regex = re.compile(get_pattern(r), re.MULTILINE)
        for idx, text in enumerate(get_texts(r)):
            matches = [m.group(0) for m in regex.finditer(text)]
            if len(matches) == 0:  # checks if there is not question number
                prev = numbers[idx - 1] if idx > 0 else None
                split.append((prev, numbers[idx]))
        if split:
            return [(name, f"question split between these pairs, {split}")]
        return []

    return check


# Checks if multiple questions are attached to one question object
def merged_question(name, get_texts, get_pattern):
    # ['1. why blah blah\n 2. blah blah']
    # pattern is per source, so the regex is built per report, not at import.
    def check(r):
        flags = []
        regex = re.compile(get_pattern(r), re.MULTILINE)
        for text in get_texts(r):
            matches = [m.group(0) for m in regex.finditer(text)]
            # print(matches)
            if len(matches) >= 2:
                flags.append((name, matches, f"{len(matches)} questions"))
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


def image_check(name, get_numbers, get_paths):
    def check(r):
        flags = []
        by_path = {}
        for number, path in zip(get_numbers(r), get_paths(r)):
            by_path.setdefault(path, []).append(number)
        for path, numbers in by_path.items():
            if len(numbers) > 1:
                flags.append((name, (f"shared path {path}", numbers)))
            elif not path or not os.path.exists(path):
                flags.append((name, (f"missing file {path!r}", numbers)))
        return flags

    return check


FAILURE_MODES = {
    # Per-DOC checks
    "MISSING QUESTION": "Questions found in the PDF text greater than extracted one",
    "EXTRA QUESTION": "Questions found in PDF is less than extracted ones",
    "SEQUENCE": "Numbers extracted but out of order or with gaps, like 1,2,4,3 or 1,2,5",
    "PDF NON-SEQUENTIAL": "PDF is NON-SEQUENTIAL",
    "EXTRACTED NON-SEQUENTIAL": "EXTRACTED is NON-SEQUENTIAL",
    # Per-PAGE checks
    "LOST WORDS": "Words on page are missing from any questions on page",
    # Per-QUESTION checks
    "SPLIT QUESTION": "One question cut into multiple pieces",
    "MERGED QUESTION": "Multiple questions joined into one",
    "EMPTY QUESTION": "Number found but no body content",
    "IMAGE CHECK": "Question has no unique image saved on disk",
    "NONE": "No known failures",
}


""" Checks contains checks and flags to raise, needs output a (str, list)
    [] means no failure and is skipped when building true flags """
CHECKS = [
    is_missing_extra("MISSING QUESTION", missing_q),
    is_missing_extra("EXTRA QUESTION", extra_q),
    # no of marks is not sequential so only ran on numbering
    non_sequential(
        "PDF NON-SEQUENTIAL", lambda r: flatten(r.pdf_numbering["numbering"])
    ),
    non_sequential("EXTRACTED NON-SEQUENTIAL", lambda r: r.extracted_numbering),
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
        lambda r: r.config["patterns"]["numbering"],
    ),
    merged_question(
        "MERGED QUESTION",
        lambda r: r.texts,
        lambda r: r.config["patterns"]["numbering"],
    ),
    empty_question("EMPTY QUESTION", lambda r: r.numbers, lambda r: r.texts),
    image_check("IMAGE CHECK", lambda r: r.numbers, lambda r: r.paths),
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
                    line_text
                )  # need to move this and only append text
                total += 1
        if question_details:
            question_list.append(question_details)

    return total, question_list  # [4, ["1.","2.","3.","4."]]


def count_expected_no(document, config):
    counts = {}
    count_list = {}
    marks_list = {}
    quest_list = {}
    numbering_conditions = [re.compile(config["patterns"]["numbering"]), DIGIT]
    for method in config["patterns"]:  # e.g. ["marks", "numbering"]
        counts[method], count_list[method] = count_matches(
            document, config["patterns"][method], config["SKIP_PAGE_ONE"]
        )
        # Prints raw strings.
        validator_logger.debug(f"\n{method} = {count_list[method]}")
        if method == "numbering":
            quest_list[method] = [
                strip_number(page, numbering_conditions) for page in count_list[method]
            ]
        if method == "marks":
            # Stripping marks needs words not line, so needs be turned into list of words
            marks_list[method] = [
                strip_number([w for line in page for w in line.split()], [DIGIT])
                for page in count_list[method]
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
    stripped_numbers = strip_number(numbers, [DIGIT])
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
    path_list = [q.path for q in question_list]
    expected, exp_questions = count_expected_no(document, config)
    actual, act_questions = count_actual_no(question_list)
    # print(exp_questions, act_questions)

    report = WorksheetReport(
        name,
        number_list,
        text_list,
        region_list,
        path_list,
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

    printer = True
    if report.flag[0][1] != None and printer:
        save_validation(report)
        for name, *details in report.flag:
            # continue
            print(f"\n{name}")
            for d in details:
                print(d)

    return report
