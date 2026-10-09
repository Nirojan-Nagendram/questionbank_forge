import pymupdf
from utility import (
    footer_cutoff,
    header_cutoff,
    left_margin,
    question_marker,
    gap,
    SKIP_PAGE_ONE,
)

open("output.txt", "w", encoding="utf8").close()


def detect_question(page_idx, w):
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


def run_splitter(doc):
    number = []
    regions = []
    current_region = []  # text start, page number(s), y start(s), y end(s)

    prev_start = None
    for page_idx, page in enumerate(doc):  # inside page
        # x0, y0, x1, y1, text, block_no, line_no, word_no = w
        if SKIP_PAGE_ONE:
            if page_idx == 0:
                continue
            else:
                words = [
                    w
                    for w in page.get_text("words")
                    if w[1]
                    < page.rect.height - footer_cutoff  # and w[1] > header_cutoff
                ]
        else:
            words = [
                w
                for w in page.get_text("words")
                if w[1] < page.rect.height - footer_cutoff  # and w[1] > header_cutoff
            ]
        if words:
            top_word = min(w[1] for w in words)
            bottom_word = max(w[3] for w in words)
        for w in words:
            y_start = detect_question(page_idx, w)
            if y_start is None:
                """if no question start, then skip rest of loop until you find one"""
                continue

            if prev_start is not None:
                """Checks if current page had previous question on it"""
                if prev_start[0] == page_idx:
                    current_region.append(
                        (
                            clip_text(page, prev_start[1], y_start - gap),
                            page_idx,
                            prev_start[1] - gap,
                            y_start - gap,
                        )
                    )
                # elif use top of this page to start of the next question (only works if there is a next question otherwise banks it)
                elif y_start - gap >= top_word:  # check y_start against top_word
                    current_region.append(
                        (
                            clip_text(page, top_word, y_start - gap),
                            page_idx,
                            top_word - gap,
                            y_start - gap,
                        )
                    )

                number.append(w[4])
                regions.append(store_region(current_region))
                write_output(current_region)
                current_region = []
            prev_start = (page_idx, y_start, page)

        if prev_start is not None:
            start = prev_start[1] if prev_start[0] == page_idx else top_word
            current_region.append(
                (
                    clip_text(page, start, bottom_word),
                    page_idx,
                    start - gap,
                    bottom_word + gap,
                )
            )
    # last question is written no matter what
    if current_region:
        number.append(w[4])
        regions.append(store_region(current_region))
        write_output(current_region)
    # doc.close()
    return number, regions


if __name__ == "__main__":
    from utility import doc

    number, regions = run_splitter(doc)
    print(doc)
    print(f"q_no: {number}, regions : {regions}")
