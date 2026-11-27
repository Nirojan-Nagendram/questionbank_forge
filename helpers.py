import re


def find_footer_limit(page, config, default):
    footer_markers = [
        w[1] for w in page.get_text("words") if w[4] == config["LAST_PAGE_FOOTER"]
    ]
    if footer_markers:
        return footer_markers[-1] - config["gap"]
    return default


def strip_chain(text, steps):  # "8:" or "*2." etc
    for step in steps:
        m = re.search(step, text)  # finds digit anywhere in string
        if not m:
            return None
        text = m.group()
    return int(text)  # 8 or 2 etc


def group_line(page_words):
    lines = {}
    for w in page_words:
        # sets line by adding word with block_no, line_no
        lines.setdefault((w[5], w[6]), []).append(w)
    for words in lines.values():
        # Sorts by word no
        words.sort(key=lambda w: w[7])
        # generator yielding lines and line info every pass
        yield " ".join(w[4] for w in words), words
