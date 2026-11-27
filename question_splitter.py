import pymupdf
import re
from pprint import pprint

from utility import DIGIT
from models import Question, Open_question
from helpers import find_footer_limit, strip_chain, group_line

WRITE = False

if WRITE:
    open("output.txt", "w", encoding="utf8").close()


def collect_text(page, config):
    page_words = page.get_text("words")
    words = [
        w
        for w in page_words
        if config["header cutoff"] <= w[1] < page.rect.height - config["footer cutoff"]
    ]
    line_texts = []
    line_y0s = []
    for line_text, line_words in group_line(page_words):
        line_texts.append(line_text)
        line_y0s.append(min(w[1] for w in line_words))
    return words, line_texts, line_y0s


def detect_question(info: tuple, pattern):
    regex = re.compile(pattern)
    matches = [
        (m.group(0), y0)
        for text, y0 in list(zip(*info, strict=True))
        for m in regex.finditer(text)
        if m.group(0) is not None
    ]
    return matches


def clip_text(page, y0_cut, y1_cut):
    # rectangle width is 0 -> page width
    # rectangle height is ques start -> ques end
    clip = pymupdf.Rect(x0=0, y0=y0_cut, x1=page.rect.width, y1=y1_cut)
    text = page.get_text("text", clip=clip, sort=True)
    return text


def write_output(current_region):
    current_question, page, y_start_list, y_end_list = list(zip(*current_region))
    question = "\n".join(current_question)
    with open("output.txt", "a", encoding="utf8") as output:
        output.write(question + "\n")  # write text of page


""" format_data: regions currently outputs [()] so format unpacks it and groups same questions in a list."""


def format_data(regions):
    all_pieces = [list(zip(*q, strict=True)) for q in regions]
    return all_pieces


def question_finder(doc, config):
    page_info = []
    for page_idx, page in enumerate(doc):  # inside page
        # x0, y0, x1, y1, text, block_no, line_no, word_no = w
        if config["SKIP_PAGE_ONE"] and page_idx == 0:
            continue
        # Only words between the header and footer cutoffs count, otherwise
        # top_word lands in the header and questions swallow it.
        words, line_texts, line_y0s = collect_text(page, config)
        if words:
            top_word = min(w[1] for w in words)  # top word y0
            bottom_word = max(w[3] for w in words)  # bottom word y1

        if config["LAST_PAGE_FOOTER"] and page_idx + 1 == len(doc):
            bottom_word = find_footer_limit(page, config, bottom_word)
        page_info.append(
            (
                page_idx,
                detect_question(
                    (line_texts, line_y0s), config["patterns"]["numbering"]
                ),
                top_word,
                bottom_word,
            )
        )
    return page_info


def allow_sequential_only(page_records, condition: list):
    """Drops hits that don't continue the numbering (1, 2, 3...).
    A hit numbered 1 mid-sequence counts as a restart only if the next hit is 2."""
    filtered_records = []

    # every hit in the document, in order: (page_idx, number as int, y)
    all_hits = [
        (page_idx, strip_chain(label, condition), y)
        for page_idx, hits, top, bottom in page_records
        for label, y in hits
    ]
    # each hit paired with the one after it (sentinel after the last hit)
    hit_pairs = list(zip(all_hits, all_hits[1:] + [(None, 0)]))

    last_number = 0
    kept_hits = []
    for hit, next_hit in hit_pairs:
        page_idx, number, y = hit
        if number is None:
            continue
        if number == 1 and number + 1 == next_hit[1]:
            last_number = 0  # restart confirmed by the following hit being 2
        if last_number + 1 == number:
            kept_hits.append(hit)
            last_number = number

    # a hit is identified by its page and y position
    kept_positions = {(page_idx, y) for page_idx, _, y in kept_hits}
    for page_idx, hits, top, bottom in page_records:
        page_hits = [(label, y) for label, y in hits if (page_idx, y) in kept_positions]
        filtered_records.append((page_idx, page_hits, top, bottom))
    return filtered_records


def region_calculator(page_records, config):
    # output lists
    numbers = []
    regions = []

    # temp variables
    current_region = []  # text start, page number(s), y start(s), y end(s)
    open_quest = None
    for page_idx, hits, top, bottom in page_records:
        for label, y in hits:  # hits are [] for page-spanning questions
            # Guard: a hit closer to the open question's own start than the gap
            # is not a new question (e.g. a stray number on the same line).
            if (
                open_quest is not None
                and open_quest.page_idx == page_idx
                and y - config["gap"] <= open_quest.y
            ):
                continue
            if open_quest is not None:
                if open_quest.page_idx == page_idx:
                    current_region.append((page_idx, open_quest.y, y - config["gap"]))
                elif (y - config["gap"]) >= top:
                    current_region.append((page_idx, top, y - config["gap"]))

                # Save closed question
                numbers.append(open_quest.number)
                regions.append(list(zip(*current_region)))  # (idx, y start, y end)
                if WRITE:
                    write_output(current_region)
                current_region = []
            # hold open question
            # page_idx, numbering, y0
            open_quest = Open_question(page_idx, label, y)

        # Find start of question/end
        if open_quest is not None:
            start = open_quest.y if open_quest.page_idx == page_idx else top
            current_region.append((page_idx, start, bottom))
    # last question is written no matter what
    # Question ends here if no more quesions
    if current_region:
        assert open_quest is not None
        numbers.append(open_quest.number)
        regions.append(list(zip(*current_region)))
        if WRITE:
            write_output(current_region)
    # strict errors if wrong amount of anything
    idx = range(1, len(numbers) + 1)
    data = list(zip(idx, numbers, format_data(regions), strict=True))
    return data


# clip pages based on regions (page_idx, y0,y1)
def split_text(doc, data):
    texts = []
    idx, numbers, regions = zip(*data, strict=True)
    for question_regions in regions:
        pieces = []
        for page_idx, y0, y1 in question_regions:
            pieces.append(clip_text(doc[page_idx], y0, y1))
        texts.append("\n".join(pieces))  # joins page-span questions
    questions = list(zip(idx, numbers, regions, texts, strict=True))
    return questions


def run_splitter(doc, config):
    paper_info = question_finder(doc, config)
    # returns [page_idx, (questions details), top word, bottom word]
    sequential_info = allow_sequential_only(paper_info, [DIGIT])
    data = region_calculator(sequential_info, config)
    questions = split_text(doc, data)
    output = []
    for idx, number, region, text in questions:
        output.append(Question(idx, number, region, text))
    return output


if __name__ == "__main__":
    pass
