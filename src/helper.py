import dataclasses
from typing import Protocol, Optional
from typing import List


class Reader(Protocol):
    def read_image(self,page_image) -> str:
        pass
@dataclasses.dataclass

class Hanzi:
    simplified: str
    traditional: str
    pinyin: str
    description: List[str]
    def add_description(self,new_description: str):
        self.description.append(new_description)

    def hanzi_iterator(self):
        return zip(iter(self.simplified) , iter(self.traditional))

    def __contains__(self, other):
        if isinstance(other, Hanzi):
            return other.simplified in self.simplified or other.traditional in self.traditional

    def __eq__(self, other):
        if isinstance(other, Hanzi):
            print(other.simplified == self.simplified or other.traditional == self.traditional)
            return other.simplified == self.simplified or other.traditional == self.traditional
        return False

@dataclasses.dataclass
class Info:
    hanzi: "Hanzi"
    example:Optional[str]
    ai_explanation: Optional[str]


class Searcher(Protocol):
    def search_meaning(self,text: str) -> List[Info]:
        pass

class ArtificialIntelligence:
    pass

class Helper:
    __slots__ = ("reader","searcher","ai")
    def __init__(self, reader: Reader, searcher: Searcher, ai: Optional[ArtificialIntelligence]):
        self.reader = reader
        self.searcher = searcher
        self.ai = ai

    def what_is_this_hanzi(self,page_image) -> List[Info]:
        return self.searcher.search_meaning(self.reader.read_image(page_image))
