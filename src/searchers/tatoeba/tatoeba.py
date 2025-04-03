import asyncio
import time
from gettext import translation
from typing import List
import aiohttp
import requests


class Tatoeba:
    """
    This class have the purpose to get the examples of the mandarin words.
    For this mission the Tatoeba API will be used.
    Documentation for tatoeba API: https://en.wiki.tatoeba.org/articles/show/api
    """
    @staticmethod
    def get_examples(words: list, translate_lang="eng",num_examples=5) -> List:
        response = asyncio.run(Tatoeba._get_response(words=words,translate_lang=translate_lang))
        extracted = []
        for example in response:
            extracted.append(Tatoeba._extract_examples(example,num_examples))
        return extracted

    @staticmethod
    async def _get_response(words: list[str], translate_lang="eng",) -> list[list]:
        url_template = 'https://tatoeba.org/pt-br/api_v0/search?query={word}&from=cmn&to={translate_lang}'
        urls = [url_template.format(word=word,translate_lang=translate_lang)for word in words]
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            task = [asyncio.create_task(Tatoeba._fetch_tatoeba(session,url)) for url in urls]
            response = await asyncio.gather(*task)
        return response

    @staticmethod
    async def _fetch_tatoeba(session,url):
        headers = {"Accept-Encoding": "gzip"}
        try:
            start = time.perf_counter()
            async with session.get(url,headers=headers) as response:
                print(time.perf_counter()-start)
                return await response.json()
        except TimeoutError:
            print("The examples cant be founded in time")

    @staticmethod
    def _extract_examples(api_response, num_examples=5) -> list:
        results = api_response["results"]
        results = results[:num_examples]
        example_list = [
            {"text": info['text'],
             "translations": [translation_[0]["text"] for translation_ in info["translations"] if translation_ != []]
             } for info in results]
        return example_list


