import os
import pymupdf
from PIL import Image


def make_fold(folder):
    path = "images/" + folder
    if not os.path.exists(path):
        # print("does not exist")
        os.mkdir(path)


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


"""Currently overrides page spanning questions"""


def clip_question(question_list, path, document):
    combined = None
    questions = []
    question_parts = []
    for q in question_list:
        pieces = q.regions
        for page_idx, y0, y1 in pieces:
            page = document[page_idx]
            clip = pymupdf.Rect(x0=0, y0=y0, x1=page.rect.width, y1=y1)

            """ returns pixmap(RGB, (boundary), alpha)"""
            picture = page.get_pixmap(clip=clip, dpi=150)
            question_parts.append(picture)
        combined = combine_parts(question_parts)
        q.path = f"images/{path}/question{q.number.rstrip('.')}.png"
        combined.save(q.path)
        q.width, q.height = combined.size
        questions.append(combined)
        question_parts = []
    return questions


def render_question(question_list, folder_name, document):
    make_fold(folder_name)
    clip_question(question_list, folder_name, document)


if __name__ == "__main__":
    pass
