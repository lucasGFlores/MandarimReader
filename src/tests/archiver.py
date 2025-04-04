import time
import unittest
from pathlib import WindowsPath, Path

from sympy import refine_root

from src.searchers.binary_tree_hanzi import BinaryTreeHanzi
from src.searchers.cccedict import CeDictionary
from src.utils.archiver.archiver import Archiver, list_files


class TestArchiver(unittest.TestCase):
    def setUp(self):
        self.archiver = Archiver()
        class ClientTest:
            def __init__(self):
                self.value = [1,2,3,4,5,6]
        self.class_test = ClientTest()

    def test_save_data(self):
        self.archiver.save(self.class_test.__class__,self.class_test.value)
        self.assertNotEqual(self.archiver._files_address, None)

    def test_load_data(self):
        self.test_save_data()
        data = self.archiver.load(self.class_test.__class__)
        self.assertNotEqual(data,None)

    def test_save_own_register(self):
        self.test_save_data()
        print(self.archiver._root_library)
        self.archiver._save_register()

    def test_load_own_register(self):
        register = self.archiver._load_register()
        self.assertNotEqual(register,{})
        print(register)

    def test_save_large_amount_of_data(self):
        dictio = CeDictionary()
        self.archiver.save(dictio.__class__,dictio._tree_pool)
        self.assertNotEqual(self.archiver._files_address, {})

    def test_load_amount_of_data(self):
        self.test_save_large_amount_of_data()
        tree_list = self.archiver.load(CeDictionary)
        self.assertNotEqual(tree_list,None)
        dict_ = CeDictionary()
        dict_._tree_pool = tree_list
        result = dict_.search_data("我是猎人")
        self.assertNotEqual(result,None)
    def test_list_library(self):
        print(self.archiver._create_client_path(self.class_test.__class__))
        name, path = self.archiver._list_library_files()[0]
        print(name,path)

