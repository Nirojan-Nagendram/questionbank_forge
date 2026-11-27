from dataclasses import dataclass, field

""" Temp storage for open questions during splitting."""


@dataclass(frozen=True)  # replaces rather than saves
class Open_question:
    page_idx: int
    number: str
    y: float


"""A printable class for all features of a question."""


@dataclass
class Question:
    idx: int
    number: str
    region: list
    text: str
    path: str = ""
    height: int = 0
    width: int = 0


""" A printable class for validating all questions were properly split,
    including flag: likely causes, status if it has worked."""


@dataclass
class WorksheetReport:
    name: str
    numbers: list
    texts: list
    regions: list
    paths: list
    document: object = field(repr=False)
    config: dict = field(repr=False)

    pdf_no: dict
    extracted_no: int
    pdf_numbering: dict
    extracted_numbering: list
    missing: list
    status: dict
    flag: list = field(default_factory=list)
