import logging
import os
import pickle
import re
import time
from pathlib import Path
from threading import Lock
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from src import Hanzi, Info
from ..binary_tree_hanzi import BinaryTreeHanzi
from .parser import get_list

class OldTreeFileError(Exception):
    def __init__(self,motive):
        self.add_note(f"Some files are in old versions\nexcuse: {motive}")

def list_files(path):
    pasta = Path(path)
    return sorted([arq.resolve() for arq in pasta.glob('**/*') if arq.is_file()], key=lambda x: int(re.findall(r'\d+',str(x))[0]) )

class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args,*kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]



class CeDictionary(metaclass=SingletonMeta):
    _path = os.path.join(__file__, "archive","dictionary.pickle")
    _dir_pool = Path(__file__).parent.resolve().joinpath("archive","pool")

    def __init__(self):
        super().__init__()
        self._tree_pool: dict[int:BinaryTreeHanzi] = {}
        self._feed_tree_pool()

    def search_meaning(self, text:str) -> List[Info]:
        get_hanzi_stamp = time.perf_counter()
        hanzi_in_text = list(filter(lambda x: x,self._search_hanzi(text)))
        list_info = []
        get_examples_stamp = time.perf_counter()
        for hanzi in hanzi_in_text:
            examples = self._get_hanzi_examples(hanzi.simplified)
            list_info.append(Info(hanzi,examples,None))
        return list_info

    def _search_hanzi(self, hanzi_text: str) -> list[Hanzi]:
        #理想主义
        text_size = len(hanzi_text)
        searchers = []
        result = []
        for kernel in range(1,text_size+1,1):
            #pointer, kernel,
            searchers.append([0,kernel])

        while searchers:
            for searcher in searchers:
                result.append(self._get_tree_from_pool(searcher[1] - 1).search_data(hanzi_text[searcher[0]:searcher[0] + searcher[1]]))
                searcher[0] += 1
            searchers.pop(-1)
        return result

    @staticmethod
    def _get_hanzi_examples(hanzi: str,output_language="eng"):
        url = f"https://tatoeba.org/en/sentences/search?query={hanzi}&from=cmn&to={output_language}"

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Rodar sem abrir janela
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)

        # 🕒 Aguarda até que pelo menos um elemento de frases apareça na página
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".sentence-and-translations"))
            )
        except:
            print("Nenhuma frase encontrada ou a página demorou para carregar.")
            driver.quit()
            return []

        # Pegando as frases e traduções
        examples = []
        sentences = driver.find_elements(By.CSS_SELECTOR, ".sentence-and-translations")

        for sentence in sentences:
            original = sentence.find_element(By.CSS_SELECTOR, ".text").text
            try:
                translation = sentence.find_element(By.CSS_SELECTOR, ".translations .text").text
            except:
                translation = "Sem tradução encontrada"
            examples.append((original, translation))

        driver.quit()
        return examples

    def _get_tree_from_pool(self, index: int) -> BinaryTreeHanzi:
         return self._tree_pool.setdefault(index,BinaryTreeHanzi())


    def _feed_tree_pool(self):

        if os.path.exists(self._dir_pool) and list_files(self._dir_pool) != []:
            try:
                for pos, file in enumerate(list_files(self._dir_pool)):
                    self._tree_pool[pos] = self._load_dictionary(file)
            except OldTreeFileError:
                self._generate_list()
        else:
            self._generate_list()

    @staticmethod
    def _load_dictionary(path) -> BinaryTreeHanzi | None:
        try:
            with open(path, 'rb') as file:
                return pickle.loads(file.read())
        except ModuleNotFoundError as e:
            logging.warning(e)
            print("trying to load old written files, need to convert again")
            raise OldTreeFileError(e)

    def _generate_list(self):
        for info in get_list():
            hanzi_length = len(info['simplified'])
            self._get_tree_from_pool(hanzi_length - 1).insert_node(Hanzi(
                simplified=info['simplified'],
                traditional=info['traditional'],
                pinyin=info['pinyin'],
                description=[info['english']]
            ))


    def save_dictionary(self):
        if not os.path.exists(self._dir_pool):
            os.makedirs(self._dir_pool)
        for pos,tree_ in sorted(self._tree_pool.items(),key=lambda x: x[0]):
            self._write_dictionary(tree_, self._dir_pool.joinpath(f"shelf{pos}.pickle"))

    @staticmethod
    def _write_dictionary(tree, path):
        os.makedirs(path.parent,exist_ok=True)
        with open(path,'wb') as file:
            file.write(pickle.dumps(tree)) #it is to work, but the type system is yelling about that

