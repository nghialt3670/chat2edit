from dataclasses import dataclass
from abc import ABC

@dataclass
class Filter(ABC):
    value: float = 0


@dataclass
class Brigtness(Filter):
    name: str = 'brightness'
