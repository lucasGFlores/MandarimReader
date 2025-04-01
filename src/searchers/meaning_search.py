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
        list_info = [Info(hanzi,Tatoeba().get_examples(hanzi.simplified),None) for hanzi in hanzi_list]
        return list_info
