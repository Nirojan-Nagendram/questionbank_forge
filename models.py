from dataclasses import dataclass


# printable class
@dataclass
class Question:
    idx: int
    number: str
    regions: list
    path: str = ""
    height: int = 0
    width: int = 0
