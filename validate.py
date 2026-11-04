import pymupdf
import re
from models import WorksheetReport

""" To be ran on document """

from utility import SOURCES, pdf

doc = pymupdf.open(pdf)

# Need to fix too many lambda & regular functions combined.


def flatten(by_page):
    # [[1,2,3],[1,2,3]] = [1,2,3,1,2,3]
    # print(by_page)
    return [n for nums in by_page for n in nums]


def list_minus(a, b):
    remove = set(b)  # set allows hash(quicker)
    return [x for x in a if x not in remove]


def is_sequential(numbers):  # [ 1,2,3,4,5]
    length = len(numbers)
    return numbers == list(range(1, length + 1)) or length <= 1


def missing_q(pattern):
    return lambda r: list_minus(
        flatten(r.pdf_numbering[pattern]), r.extracted_numbering
    )


def extra_q(pattern):
    return lambda r: list_minus(
        r.extracted_numbering, flatten(r.pdf_numbering[pattern])
    )


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


# need to add new question number converter for "marks)" so list makes sense
def is_missing_extra(name: str, calculation):
    def check(r):
        flags = []
        for pattern in r.pdf_numbering.keys():
            difference = calculation(pattern)(r)
            if difference:
                flags.append((f"{name} based on {pattern}", difference))
        return flags

    return check


def non_sequential(name, number_list):
    def check(r):
        nums = number_list(r)
        # print(f"name: {name}, nums: {nums}")
        if not is_sequential(nums):
            return [(name, nums)]
        return []

    return check


FAILURE_MODES = {
    "MISSING_QUESTION": "Questions found in the PDF text greater than extracted one",
    "EXTRA_QUESTION": "Questions found in PDF is less than extracted ones",
    "SEQUENCE": "Numbers extracted but out of order or with gaps, like 1,2,4,3 or 1,2,5",
    "PDF_NON-SEQUENTIAL": "PDF is NON-SEQUENTIAL",
    "EXTRACTED_NON-SEQUENTIAL": "EXTRACTED is NON-SEQUENTIAL",
    "SPLIT_QUESTION": "One question cut into multiple pieces",
    "MERGED_QUESTION": "Multiple questions joined into one",
    "EMPTY_QUESTION": "Number found but no body content",
    "NONE": "No known failures",
}


# add check for split question, merged_question and empty
""" Checks contains checks and flags to raise, needs output a (str, list)"""
CHECKS = [
    is_missing_extra("MISSING_QUESTION", missing_q),
    is_missing_extra("EXTRA_QUESTION", extra_q),
    # no of marks is not sequential so only ran on numbering
    non_sequential("PDF_NON-SEQUENTIAL", lambda r: r.pdf_numbering["numbering"]),
    non_sequential("EXTRACTED_NON-SEQUENTIAL", lambda r: r.extracted_numbering),
]


def get_numbers(questions):
    num_re = re.compile(r"\d+")
    numbers = []
    for q in questions:
        text = "".join(q)
        m = num_re.search(text)  # finds digit anywhere in string
        if m:
            numbers.append(int(m.group()))  # .group() is text from matched
    return numbers  # [1, 2, 3, 4]


""" Get a list of stripped numbers from 1., 1:, etc """


def strip_number(questions, condition, integer: bool):
    numbers = []
    for q in questions:
        m = condition.search(q)  # finds digit anywhere in string
        # print(m)
        # need to add condition to prevent additional
        if m and integer:
            numbers.append(int(m.group()))  # .group() is text from matched
        elif m:
            numbers.append(m.group())
    # print(numbers)
    return numbers  # [1, 2, 3, 4]


""" get just number from " (Total x marks) " """


"""How failure mode is selected
    For each check in CHECKS, then for each flag in what that check returns, collect the flag.
    if [] then nothing to loop over so it is skipped."""


def select_failure_mode(report):
    # print(f"extracted numbering: {report.extracted_numbering}")
    # print(f"pdf numbering      : {report.pdf_numbering['numbering']}")
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


""" Pattern is dependent on the worksheet."""


def count_matches(document, pattern):
    # Number of "marks)" on across all pages or question numbers found anywhere on page.
    regex = re.compile(pattern)
    question_list = []  # output
    flattened = []
    total = 0
    for page in document:
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

    # [4, ["1.","2.","3.","4."]]
    return total, question_list


def count_expected_no(document, config):
    counts = {}
    count_list = {}
    marks_list = {}
    quest_list = {}
    for method in config["patterns"]:  # e.g. ["marks", "numbering"]
        counts[method], count_list[method] = count_matches(
            document, config["patterns"][method]
        )
        # Prints raw strings.
        # print(f"\n{method} : {count_list[method]}")
        if method == "numbering":
            quest_list[method] = [
                strip_number(
                    strip_number(line, re.compile(r"^\d+\.(\s|$)"), integer=False),
                    re.compile(r"\d+"),
                    integer=True,
                )
                for line in count_list[method]
            ]
        if method == "marks":
            marks_list[method] = [
                strip_number(line, re.compile(r"\d+"), integer=True)
                for line in count_list[method]
            ]
            quest_list["marks"] = marks_to_numbers(marks_list[method])

        # Prints processed data
        # print(f"\n{method} : {quest_list[method]}")

    return (
        counts,
        quest_list,
    )  # ({"marks": 3, "numbering": 5, {"marks": [1,2,3,4], "numbering": [1,2,3,4,5]


def count_actual_no(question_list):
    numbers = []
    for question in question_list:
        numbers.append(question.number)
    stripped_numbers = strip_number(numbers, re.compile(r"\d+"), integer=True)
    return len(question_list), stripped_numbers  # [3, ["1", "2" ,"3"]]


def validate_on_sheet(name, document, config, question_list):
    expected, exp_questions = count_expected_no(document, config)
    actual, act_questions = count_actual_no(question_list)
    # print(exp_questions, act_questions)
    report = WorksheetReport(
        name,
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
    print(report.flag)

    for name, pattern in report.flag:
        if report.name == "INSERT NAME HERE":
            continue
            print(f"{report.name}: {report.flag}")

    return report
