import unittest

from .. import Hanzi
from src.searchers.binary_tree_hanzi import BinaryTreeHanzi, ListNode

YE_NODE = Hanzi(
        simplified="叶",
        traditional="枼",
        description=["foinha"],
        pinyin= "ye4"
    )
WO_NODE = Hanzi(
        simplified="我",
        traditional="我",
        description=["eu"],
        pinyin= "wo3"
    )
SHI_NODE = Hanzi(
        simplified="是",
        traditional="是",
        description=["verbo to be"],
        pinyin="shi1"
    )
KUAI_NODE =Hanzi(
        simplified="快",
        traditional="快",
        description=["gota goo fast"],
        pinyin="kuai4"
    )
FIFTH_NODE = Hanzi(
        simplified="熊猫",
        traditional="熊猫",
        description=["panda"],
        pinyin="xion3g mao3"
    )
SIXTH_NODE = Hanzi(
        simplified="弟弟",
        traditional="弟弟",
        description=["panda"],
        pinyin="di4 di5"
    )
SEVENTH_NODE = Hanzi(
        simplified="狗",
        traditional="狗",
        description=["dog"],
        pinyin="gou3"
    )
LIE_NODE = Hanzi(
        simplified="猎",
        traditional="猎",
        description=["caçar"],
        pinyin="lie4"
    )
ZHE1_NODE = Hanzi(
        simplified="褶",
        traditional="褶",
        description=["Deus sabe"],
        pinyin="zhe3"
    )
ZHE2_NODE = Hanzi(
        simplified="啫",
        traditional="啫",
        description=["Deus sabe"],
        pinyin="zhe3"
    )
ZHE3_NODE = Hanzi(
        simplified="锗",
        traditional="锗",
        description=["Deus sabe"],
        pinyin="zhe3"
    )
ZHE4_NODE = Hanzi(
        simplified="者",
        traditional="者",
        description=["Deus sabe"],
        pinyin="zhe3"
    )

class TreeTest(unittest.TestCase):
    """ Test class with binary tree function"""
    def setUp(self):
        self.tree = BinaryTreeHanzi()

    def test_insert_node_right_rotation(self):
        self.tree.insert_node(YE_NODE)
        self.tree.insert_node(WO_NODE)
        self.tree.insert_node(SHI_NODE)
        self.assertEqual(self.tree.root.get_data(), WO_NODE)
        self.assertEqual(self.tree.root.get_left().get_data(), SHI_NODE)
        self.assertEqual(self.tree.root.get_right().get_data(), YE_NODE)
        self.assertEqual(self.tree.root.get_right().is_red() and self.tree.root.left.is_red(), True, "Cores certas")
        self.assertEqual(self.tree.root.is_black(), True, "Root é preto")

    def test_insert_node_left_rotation(self):
        self.tree.insert_node(SHI_NODE)
        self.tree.insert_node(WO_NODE)
        self.tree.insert_node(YE_NODE)

        self.assertEqual(self.tree.root.get_data(), WO_NODE)
        self.assertEqual(self.tree.root.get_left().get_data(), SHI_NODE)
        self.assertEqual(self.tree.root.get_right().get_data(), YE_NODE)
        self.assertEqual(self.tree.root.get_right().is_red() and self.tree.root.left.is_red(), True, "Cores certas")
        self.assertEqual(self.tree.root.is_black(), True, "Root é preto")

    def test_insert_color_inversion(self):
        self.tree.insert_node(YE_NODE)
        self.tree.insert_node(WO_NODE)
        self.tree.insert_node(SHI_NODE)
        self.tree.insert_node(LIE_NODE)
        self.assertEqual(self.tree.root.get_data(), WO_NODE)
        self.assertEqual(self.tree.root.get_left().get_data(), SHI_NODE)
        self.assertEqual(self.tree.root.get_right().get_data(), YE_NODE)
        self.assertEqual(self.tree.root.get_left().get_left().get_data(), LIE_NODE)
        self.assertEqual(self.tree.root.is_black(),True,"O root está com a cor preta")
        self.assertEqual(self.tree.root.get_left().is_black(), True,"left parent is black")
        self.assertEqual(self.tree.root.get_right().is_black(),True,"right uncle is black")
        self.assertEqual(self.tree.root.get_left().get_left().is_red(), True, "left children is red")

    def test_color_rotation_after_inversion(self):
        self.tree.insert_node(YE_NODE)
        self.tree.insert_node(WO_NODE)
        self.tree.insert_node(SHI_NODE)
        self.tree.insert_node(LIE_NODE)
        self.tree.insert_node(KUAI_NODE)
        self.assertEqual(self.tree.root.get_data(), WO_NODE)
        self.assertEqual(self.tree.root.get_left().get_data(), LIE_NODE)
        self.assertEqual(self.tree.root.get_right().get_data(), YE_NODE)
        self.assertEqual(self.tree.root.get_left().get_left().get_data(), KUAI_NODE)
        self.assertEqual(self.tree.root.get_left().get_right().get_data(), SHI_NODE)
        self.assertEqual(self.tree.root.is_black(), True, "O root está com a cor preta")
        self.assertEqual(self.tree.root.get_left().is_black(), True, "left parent is black")
        self.assertEqual(self.tree.root.get_right().is_black(), True, "right uncle is black")
        self.assertEqual(self.tree.root.get_left().get_left().is_red(), True, "left children is red")
        self.assertEqual(self.tree.root.get_left().get_right().is_red(), True, "left children is red")

    def test_search_hanzi(self):
        self.tree.insert_node(YE_NODE)
        self.tree.insert_node(WO_NODE)
        self.tree.insert_node(SHI_NODE)
        self.tree.insert_node(LIE_NODE)
        self.tree.insert_node(KUAI_NODE)
        hanzi = self.tree.search_data("快")
        self.assertEqual(hanzi,KUAI_NODE,"Hanzi finded")

    def test_list_nodes(self):
        self.tree.insert_node(YE_NODE)
        self.tree.insert_node(WO_NODE)
        self.tree.insert_node(SHI_NODE)
        self.tree.insert_node(ZHE1_NODE)
        self.tree.insert_node(ZHE2_NODE)
        self.tree.insert_node(ZHE3_NODE)
        self.tree.insert_node(ZHE4_NODE)
        self.assertIsInstance(self.tree.root.get_right().get_right(),ListNode, "This node is not a Node List")
        self.assertEqual(self.tree.root.is_black(), True, "The root isn't black")
        self.assertEqual(self.tree.root.get_left().is_black(), True, "left parent isn't black")
        self.assertEqual(self.tree.root.get_right().is_black(), True, "right uncle isn't black")
        self.assertEqual(self.tree.root.get_right().get_right().is_red(), True, "left children isn't red")

    def test_find_hanzi_in_node_list(self):
        self.test_list_nodes()
        self.assertEqual(self.tree.search_data("者"), ZHE4_NODE, "Node wasn't found ")
