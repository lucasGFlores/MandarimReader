from typing import List
from src import Info
from .cccedict import CeDictionary
from .tatoeba import Tatoeba


class MeaningSearch:
    """
    This class works as a Facade for the modules to search the meaning and any data from the mandarin words
    This class can be modified to be used with other modules unless the function 'search_meaning' from the Searcher interface
    """

    @staticmethod
    def search_meaning(text: str) -> List[Info]:
        hanzi_list = CeDictionary().search_data(text)
        word_list = [hanzi.simplified for hanzi in hanzi_list]
        example_list = Tatoeba.get_examples(word_list,num_examples=3)
        info_list = [Info(hanzi=hanzi,example=example,ai_explanation=None) for hanzi, example in zip(hanzi_list,example_list)]
        return info_list
