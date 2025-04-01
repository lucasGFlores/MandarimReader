from gettext import translation
from typing import List

import requests


class Tatoeba:
    """
    This class have the purpose to get the examples of the mandarin words.
    For this mission the Tatoeba API will be used.
    Documentation for tatoeba API: https://en.wiki.tatoeba.org/articles/show/api
    """

    @staticmethod
    def _get_response(word: str, translate_lang="eng") -> str:
        url = f"https://tatoeba.org/pt-br/api_v0/search?query={word}&from=cmn&to={translate_lang}"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def _extract_examples(api_response, num_examples=5) -> list:
        results = api_response["results"]
        results = results[:num_examples]
        example_list = [
            {"text": info['text'],
             "translations": [translation_[0]["text"] for translation_ in info["translations"] if translation_ != []]
             } for info in results]
        return example_list

    def get_examples(self,word: str, translate_lang="eng",num_examples=5) -> List:
        response = self._get_response(word,translate_lang)
        examples = self._extract_examples(response,num_examples)
        return examples
