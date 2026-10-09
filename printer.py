import pymupdf
from utility import print_page_details

pdf = r"pdf_folder\PMT\Maths\question_by_topic\edexcel\grade_1-2\Addition and Subtraction QP\question\Addition and Subtraction QP.pdf"
#pdf_answers = r"pdf_folder\PMT\Maths\question_by_topic\edexcel\grade_1-2\Addition and Subtraction QP\answers\Addition and Subtraction MA.pdf"



doc = pymupdf.open(pdf) # open a document

questions = []
offset = [] # pages offset slightly
running = 0
for page_idx, page in enumerate(doc):
    offset.append(running)
    running += page.rect.height

    for w in page.get_text("words"):    # (x0, y0, x1, y1, "word", block_no, line_no, word_no)
        x0,y0,x1,y1, text, line_no, word_no = w[0], w[1], w[2], w[3], w[4], w[5], w[6]
        if abs(x0 - 54) < 3 and word_no == 0 and text[len(text)-1] == "." :    # floats can differ here, cannot just check against 54 exactly
            #print_page_details(w, page_index= page_idx)
            pass
        # question end in "(Total marks)", x0 = (505), x1 = 541, nothing else is consistent.
        if text == "marks)" and abs(x0 - 505) > 3 and abs(x1 - 541) > 3:
            print_page_details(w,page_index=page_idx)

print(offset)
doc.close()

