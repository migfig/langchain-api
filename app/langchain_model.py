from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel


@dataclass
class Argument:
    name: str
    value: str


@dataclass
class Element:
    type: str
    name: str
    arguments: Optional[list[Argument]]
    index: int


class ElementsRequest(BaseModel):
    elements: list[Element]
