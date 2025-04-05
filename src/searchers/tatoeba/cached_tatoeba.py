from .tatoeba import Tatoeba
from ...utils.archiver import Archiver, DontHavePathError


class CachedTatoeba:
    """
    This class is a decorator for TatoebaAPI class, who add the functionality to cache the information early get
    """
    _examples_cache: dict[str,list]= {}
    _archiver = Archiver()
    _tatoeba = Tatoeba
    def __init__(self):
        self._examples_cache = self._load_cache()

    def get_examples(self,words: list, translate_lang="eng", num_examples=5):
        rest_words, examples_cache = self._get_examples_from_cache(words)
        if rest_words:
            example_list = self._tatoeba.get_examples(rest_words,translate_lang,num_examples)
            self._add_list(words,example_list)
            self._save_cache()
            return example_list + examples_cache
        return examples_cache

    def _get_examples_from_cache(self,words:list) -> tuple[list,list]:
        examples_from_cache = [self._examples_cache[word] for word in words if self._examples_cache.get(word,None) is not None]
        rest_words = list(filter(lambda word: word not in self._examples_cache ,words))
        return rest_words, examples_from_cache

    def _add_list(self,words,examples_list:list[list]) -> None:
        """
        Add into cache, all the examples of certain word

        :param
            words: ['我']
            examples_list: [{'text': '我！', 'translations': ['Me!', "It's me!"]}, {'text': '我。', 'translations': ['Me.']}]
        :return: None (update cache)
        """
        for word,examples in zip(words,examples_list):
            self._examples_cache[word] = examples

    def _save_cache(self):
        self._archiver.save(client_class=self.__class__,data=self._examples_cache)

    def _load_cache(self) -> dict[str,list]:
        try:
            return self._archiver.load(self.__class__)
        except DontHavePathError:
            return {}