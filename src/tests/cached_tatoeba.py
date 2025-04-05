import unittest

from src.searchers.tatoeba.cached_tatoeba import CachedTatoeba


class TestCachedTatoeba(unittest.TestCase):
    def setUp(self):
        self.cached_tatoeba = CachedTatoeba()
        self.word_list = ["我","是","的","没有","商店","狗","妹妹"]

    def test_get_examples(self):
        examples = self.cached_tatoeba.get_examples(self.word_list)
        self.assertNotEqual(examples,None, "The API arent getting the examples. Maybe the problem is the abstraction or API broke")

    def test_get_example_from_cache(self):
        self.test_get_examples()
        rest_words, _ = self.cached_tatoeba._get_examples_from_cache(self.word_list + ["狩猎","学习"])
        self.assertNotEqual(_, None,
                            "The system to register the cache of the examples are broken")
        print(_)

        self.assertEqual(rest_words, ["狩猎","学习"],"Error to remove the hanzis outside the list")

        cached_examples = self.cached_tatoeba.get_examples(self.word_list + ["狩猎","学习"])
        self.assertNotEqual(cached_examples,None)