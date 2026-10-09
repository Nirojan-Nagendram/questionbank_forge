import os
import pymupdf
from PIL import Image


def make_fold(folder):
    path = "images/" + folder
    if not os.path.exists(path):
        # print("does not exist")
        os.mkdir(path)


""" question splitter currently outputs [()] so format unpacks it and groups same questions in a list."""


def format_data(regions):
    all_pieces = [list(zip(*q, strict=True)) for q in regions]
    return all_pieces


def combine_parts(pix_list):  # list of pxl maps of question parts
    image_list = []
    for pix in pix_list:
        image_list.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    max_width = max([i.width for i in image_list])
    total_height = sum([i.height for i in image_list])

    """ Creates blank canvas """
    combined = Image.new("RGB", (max_width, total_height), "white")
    current_height = 0
    for image in image_list:
        combined.paste(image, (0, current_height))
        current_height += image.height
    return combined


""" Currently overrides page spanning questions (q7 pmt)"""


def clip_question(question_pieces, path, document):
    questions = []
    question_parts = []
    """Testing with paths"""
    for q_no, pieces in enumerate(question_pieces):
        for piece_no, (page_idx, y0, y1) in enumerate(pieces):
            page = document[page_idx]
            clip = pymupdf.Rect(x0=0, y0=y0, x1=page.rect.width, y1=y1)

            """ returns pixmap(RGB, (boundary), alpha)"""
            picture = page.get_pixmap(clip=clip, dpi=150)
            question_parts.append(picture)
        combined = combine_parts(question_parts)
        combined.save(f"images/{path}/question{q_no+1}.png")
        questions.append(combined)
        question_parts = []
    return combined


def render_question(regions, folder_name, document):
    make_fold(folder_name)
    all_pieces = format_data(regions)
    data = clip_question(all_pieces, folder_name, document)
    print(data)


if __name__ == "__main__":
    from main import regions, worksheet_name, document

    render_question(regions, worksheet_name, document)
