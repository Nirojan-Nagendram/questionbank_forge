def print_page_details(info, page_index=None):
    x0, y0, x1, y1, text, block_no, line_no, word_no = info
    if page_index is not None:
        print(
            f"pg{page_index+1}: {text}, (x0,y0) : {round(x0),round(y0)}, (x1,y1) : {round(x1),round(y1)} line no: {line_no}, word no: {word_no}"
        )
    else:
        print(
            f"{text}, (x0,y0) : {round(x0),round(y0)}, (x1,y1) : {round(x1),round(y1)} line no: {line_no}, word no: {word_no}"
        )
