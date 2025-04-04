import logging
import os
import pickle
import re
from pathlib import Path
from threading import Lock
from src import Hanzi
from ..binary_tree_hanzi import BinaryTreeHanzi
from .parser import get_list
from ...utils.archiver.archiver import Archiver, DontHavePathError




class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, *kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]


class CeDictionary(metaclass=SingletonMeta):
    _path = os.path.join(__file__, "archive", "dictionary.pickle")
    _dir_pool = Path(__file__).parent.resolve().joinpath("archive", "pool")

    def __init__(self):
        super().__init__()
        self._tree_pool: dict[int:BinaryTreeHanzi] = {}
        try:
           self._tree_pool = Archiver().load(CeDictionary)
        except DontHavePathError:
            self._generate_list()
            Archiver().save(CeDictionary,self._tree_pool)

    def search_data(self, hanzi_text: str) -> list:
        text_size = len(hanzi_text)
        searchers = []
        result = []
        for kernel in range(1, text_size + 1, 1):
            #pointer, kernel,
            searchers.append([0, kernel])
        while searchers:
            for searcher in searchers:
                result.append(self._get_tree_from_pool(searcher[1] - 1).search_data(
                    hanzi_text[searcher[0]:searcher[0] + searcher[1]]))
                searcher[0] += 1
            searchers.pop(-1)
        return list(filter(lambda x: x, result))

    def _get_tree_from_pool(self, index: int) -> BinaryTreeHanzi:
        return self._tree_pool.setdefault(index, BinaryTreeHanzi())

    def _generate_list(self):
        for info in get_list():
            hanzi_length = len(info['simplified'])
            self._get_tree_from_pool(hanzi_length - 1).insert_node(Hanzi(
                simplified=info['simplified'],
                traditional=info['traditional'],
                pinyin=info['pinyin'],
                description=[info['english']]
            ))
