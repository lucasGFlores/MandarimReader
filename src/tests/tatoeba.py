import asyncio
import time
import unittest

from ..searchers.tatoeba import Tatoeba

class TatoebaTest(unittest.TestCase):
    """
    Test from Tatoeba API
    """
    def setUp(self):
        self.tatoeba = Tatoeba()
        self.words = ["我","是","你有","商店","狗","我","是","你有","商店","狗"]
        self.output_lang = "eng"

    def test_api_requisition(self) -> list[list]:
        response =  asyncio.run(self.tatoeba._get_response(words=self.words))
        self.assertNotEqual(response,None)
        return response

    def test_extract_examples(self) -> list:
        response =  self.test_api_requisition()
        extracted = []
        for example in response:
            extracted.append(self.tatoeba._extract_examples(example))
        self.assertNotEqual(extracted,None,"Don't get it his own examples")
        print(extracted)
        return extracted
