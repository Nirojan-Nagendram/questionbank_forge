import pymupdf
from models import Question

open("output.txt", "w", encoding="utf8").close()


def detect_question(page_idx, w, left_margin, question_marker):
    x0, y0, x1, y1, text, block_no, line_no, word_no = w
    if abs(x0 - left_margin) < 3 and text[len(text) - 1] == question_marker:
        # floats can differ here, cannot just check against 54 exactly
        y_start = y0
    else:
        y_start = None
    return y_start


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


def calculate_end_region(page, y_start_list, y_end_list, current_question):
    y_end_region = []
    for idx, i in enumerate(y_start_list):
        if idx == 0:
            continue
        if i[idx][0] == prev_i[idx][1]:
            # if the next question starts at the top of the page, take the end of the previous page to be the end of the question
            y_end_region.append(y_end_list[0])

        prev_i = i


def store_region(current_region):
    current_question, page, y_start_list, y_end_list = list(zip(*current_region))
    """ For printing readable numbers"""
    round_y_start = [round(item) for item in y_start_list]
    round_y_end = [round(item) for item in y_end_list]
    # print(f"{current_question[0][:2]}, {page}, {round_y_start}, {round_y_end}")
    question = "\n".join(current_question)

    return (page, y_start_list, y_end_list)


""" regions currently outputs [()] so format unpacks it and groups same questions in a list."""


def format_data(regions):
    all_pieces = [list(zip(*q, strict=True)) for q in regions]
    return all_pieces


def run_splitter(doc, config):
    questions = []
    idx = []
    number = []
    regions = []
    current_region = []  # text start, page number(s), y start(s), y end(s)
    i = 0
    prev_start = None
    for page_idx, page in enumerate(doc):  # inside page
        # x0, y0, x1, y1, text, block_no, line_no, word_no = w
        if config["SKIP_PAGE_ONE"]:
            if page_idx == 0:
                continue
            else:
                words = [
                    w
                    for w in page.get_text("words")
                    if w[1]
                    < page.rect.height
                    - config["footer cutoff"]  # and w[1] > header_cutoff
                ]
        else:
            words = [
                w
                for w in page.get_text("words")
                if w[1]
                < page.rect.height - config["footer cutoff"]  # and w[1] > header_cutoff
            ]
        if words:
            top_word = min(w[1] for w in words)
            bottom_word = max(w[3] for w in words)
        for w in words:
            y_start = detect_question(
                page_idx, w, config["left margin"], config["question marker"]
            )
            if y_start is None:
                """if no question start, then skip rest of loop until you find one"""
                continue

            if prev_start is not None:
                """Checks if current page had previous question on it"""
                if prev_start[0] == page_idx:
                    current_region.append(
                        (
                            clip_text(page, prev_start[1], y_start - config["gap"]),
                            page_idx,
                            prev_start[1] - config["gap"],
                            y_start - config["gap"],
                        )
                    )
                # elif use top of this page to start of the next question (only works if there is a next question otherwise banks it)
                # Question ends here if another question to come
                elif (
                    y_start - config["gap"] >= top_word
                ):  # check y_start against top_word
                    current_region.append(
                        (
                            clip_text(page, top_word, y_start - config["gap"]),
                            page_idx,
                            top_word - config["gap"],
                            y_start - config["gap"],
                        )
                    )

                i += 1
                idx.append(i)
                number.append(prev_start[3])
                regions.append(store_region(current_region))
                write_output(current_region)
                current_region = []
            """ idx, start, end, text"""
            prev_start = (page_idx, y_start, page, w[4])

        if prev_start is not None:
            """need to figure out cutoff, currently does cuts extra off but not enough? What should the rule be? i need more info"""
            cut_off = config["gap"]
            start = prev_start[1] if prev_start[0] == page_idx else top_word
            if config["LAST_PAGE_FOOTER"]:
                cut_off -= config["footer cutoff"]
            current_region.append(
                (
                    clip_text(page, start, bottom_word),
                    page_idx,
                    start - config["gap"],
                    bottom_word + cut_off,
                )
            )
    # last question is written no matter what
    # Question ends here if no more quesions
    if current_region:
        assert prev_start is not None
        i += 1
        idx.append(i)
        number.append(prev_start[3])
        regions.append(store_region(current_region))
        write_output(current_region)
    # doc.close()
    data = zip(
        idx, number, format_data(regions), strict=True
    )  # strict errors if wrong amount of anything

    for idx, no, regions in data:
        questions.append(Question(idx, no, regions))
    return questions


if __name__ == "__main__":
    pass
