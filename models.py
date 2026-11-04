from dataclasses import dataclass, field

"""A printable class for all features of a question."""


@dataclass
class Question:
    idx: int
    number: str
    regions: list
    path: str = ""
    height: int = 0
    width: int = 0


""" A printable class for validating all questions were properly split,
    including flag: likely causes, status if it has worked."""


@dataclass
class WorksheetReport:
    name: str
    pdf_no: dict
    extracted_no: int
    pdf_numbering: dict
    extracted_numbering: list
    missing: list
    status: dict
    flag: list = field(default_factory=list)
