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
