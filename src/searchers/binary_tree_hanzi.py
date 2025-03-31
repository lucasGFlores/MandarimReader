import dataclasses
import re
from abc import ABC
from typing import Optional
import pypinyin
from src import Hanzi
from src.base import RBNode,RBTree


def pinyin_transform(icon) -> str:
    pinyin_list = pypinyin.pinyin(icon, style=pypinyin.Style.TONE3)
    return ' '.join([pin[0] for pin in pinyin_list])

class NotFatherError(Exception):
    def __init__(self,message = "the sub trees dont match with grandparent node",node1 = None,node2 =None):
        super().__init__(message,node1,node2)

class BinaryTreeHanzi(RBTree, ABC):
    def __init__(self):
        self.root: Optional["RBNode"] = None

    def _update_root(self,node: "RBNode"):
        if node.get_father() is None:
            self.root = node

    def insert_node(self, other_data: Hanzi):
        if self.root is None:
            root = HanziNode(other_data, None)
            root.to_black()
            self._update_root(root)
        else:
            self._insert_iterative(self.root, other_data)

    def _insert_iterative(self, actual_node: "RBNode", other_data: Hanzi):
        current_node = actual_node
        while True:
            if current_node.get_id() < other_data.simplified:
                print(f"O node {current_node.get_id()} cor {"vermelho" if current_node.is_red() else "preto"} envio o hanzi {other_data.simplified} --- {other_data.pinyin} para a direita")
                if current_node.get_right() is None:
                    # Insere à direita e corrige a árvore
                    print(f"Nova casa para o {other_data.simplified} na direita")
                    current_node.set_right(HanziNode(other_data, current_node))
                    self._fix_tree(current_node.get_right())
                    print("terminou a correção")
                    break
                else:
                    print("Tem um node na direita já")
                    current_node = current_node.get_right()  # Move para a direita
            elif current_node.get_id() > other_data.simplified:
                print(f"O node {current_node.get_id()} cor {"vermelho" if current_node.is_red() else "preto"} envio o hanzi {other_data.simplified} --- {other_data.pinyin} para a esquerda")
                if current_node.get_left() is None:
                    print(f"Nova casa para o {other_data.simplified} na esquerda")
                    # Insere à esquerda e corrige a árvore
                    current_node.set_left(HanziNode(other_data, current_node))
                    self._fix_tree(current_node.get_left())
                    print("terminou a correção")
                    break
                else:
                    print("Tem um node no left já")
                    current_node = current_node.get_left()  # Move para a esquerda
            elif current_node.get_id() == other_data.simplified:
                # Key collision
                if isinstance(current_node,HanziNode):
                    father = current_node.get_father()
                    new_list_node = ListNode(data_root=current_node)
                    new_list_node.add_node(other_data)
                    if father:
                        #switch father pointers
                        if father.get_left() and father.get_left().get_id() == current_node.get_id():
                            new_list_node.get_father().set_left(new_list_node)
                        elif father.get_right():
                            new_list_node.get_father().set_right(new_list_node)
                    #switch children pointers
                    if new_list_node.get_right():
                        new_list_node.get_right().set_father(new_list_node)
                    if new_list_node.get_left():
                        new_list_node.get_left().set_father(new_list_node)

                if isinstance(current_node, ListNode):
                    current_node.add_node(other_data)
                break

    def _fix_tree(self,child: "RBNode") -> None:
        """
        :param child: is the actual_node used in '_inset_recursive'. This method is going to reference the last insert node as child.
        Therefore, other nodes are going to be referenced in that view point, like grandfather and uncle
        :return: Don't return anything, just organize the tree without problem
        """
        if child is None:
            return
        father = child.get_father()
        if father is None:
            self._update_root(child)
            child.to_black()
            return

        if not(father.is_red() and child.is_red()):
            return
        #otherwise is red
        grand = father.get_father()
        if grand is None:
            father.to_black()
            return
        uncle = grand.get_left() if father == grand.get_right() else grand.get_right()
        if uncle is None or uncle.is_black(): # case red nodes in line
            if (father.get_left() == child and grand.get_left() == father) or (father.get_right() == child and grand.get_right() == father):
                if father == grand.get_left():
                    new_grand, old_grand = self._right_rotation(grand)
                else:
                    new_grand, old_grand = self._left_rotation(grand)
                new_grand.to_black()
                old_grand.to_red()
                if new_grand.get_father() is None:
                    self._update_root(new_grand)
                    self.root.to_black()
                return self._fix_tree(new_grand.get_father())
            else:
                if child == father.get_left():
                    new_father, old_father = self._right_rotation(father)
                else:
                    new_father, old_father = self._left_rotation(father)

                if new_father == grand.get_left():
                    new_grand, old_grand = self._right_rotation(grand)
                else:
                    new_grand, old_grand = self._left_rotation(grand)
                new_grand.to_black()
                old_grand.to_red()
                return self._fix_tree(new_grand)
        else: #uncle is red
            grand.to_red()
            uncle.to_black()
            father.to_black()
            if self.root == grand:
                grand.to_black()
            return self._fix_tree(grand)


    def _left_rotation(self,node_high: "RBNode") -> tuple["RBNode","RBNode"]:
        """
        :param node_high: is the node to be rotated to organize the tree by putting yourself under a node bellow
        :return: return the modified nodes, the 'node_high' was putting bellow of his child 'node_below'
        This method DON'T change the colors. The colors need to be changed after the transformation
        """
        node_below = node_high.right
        old_left = node_below.left
        if old_left:
            old_left.father = node_high
        node_high.right = old_left

        node_below.father = node_high.father

        if node_below.father is None:
            self._update_root(node_below)
        elif node_below.father.left == node_high:
            node_below.father.left = node_below
        elif node_below.father.right == node_high:
            node_below.father.right = node_below
        else:
            raise NotFatherError(
                message=f"Deu ruim o {node_high.get_data()} não é filho do {node_below.get_data()}",node1=node_high,node2=node_below)

        node_below.left = node_high
        node_high.father = node_below

        return node_below, node_high


    def _right_rotation(self,node_high: "RBNode") -> tuple["RBNode","RBNode"]:
        """
        :param node_high: is the node to be rotated to organize the tree by putting yourself under a node bellow
        :return: return the modified nodes, the 'node_high' was putting bellow of his child 'node_below'
        This method DON'T change the colors. The colors need to be changed after the transformation
        """
        node_below = node_high.left
        old_right = node_below.right
        if old_right:
            old_right.father = node_high
        node_high.left = old_right
        node_below.father = node_high.father


        if node_below.father is None:
            self._update_root(node_below)
        elif node_below.father.left == node_high:
            node_below.father.left = node_below
        elif node_below.father.right == node_high:
            node_below.father.right = node_below
        else:
            raise NotFatherError(
                message=f"Deu ruim o {node_high.get_data().simplified} não é filho do {node_below.get_data().simplified}",
                node1=node_high, node2=node_below)

        node_below.right = node_high
        node_high.father = node_below
        return node_below, node_high

    def search_data(self, hanzi: str) -> Optional[Hanzi]:
        return self._recursive_search(self.root,hanzi)

    def _recursive_search(self, actual_node: "RBNode", hanzi_text: str) -> Optional[Hanzi]:
        if actual_node is None:
            return None
        if actual_node.get_id() == hanzi_text:
            if isinstance(actual_node, ListNode):
                for node in actual_node.get_data():
                    if node.simplified == hanzi_text or node.traditional == hanzi_text:
                        return node
                return None
            if isinstance(actual_node,HanziNode):
                return actual_node.get_data()

        if actual_node.get_id() < hanzi_text:
            print(f"{hanzi_text} indo para a direita")
            return self._recursive_search(actual_node.get_right(), hanzi_text)
        elif actual_node.get_id() > hanzi_text:
            print(f"{hanzi_text} indo para a esquerda")
            return self._recursive_search(actual_node.get_left(),hanzi_text)

    def _print_tree(self):
        self._recursive_print_tree(self.root)

    def _recursive_print_tree(self, root, level=0):
        if root:
            self._recursive_print_tree(root.right, level + 1)
            print(' ' * 4 * level + '->', root.data.simplified)
            self._recursive_print_tree(root.left, level + 1)

@dataclasses.dataclass
class Identification:
    pinyin: str
    simplified: str
    traditional:str

    def __lt__(self, other):
        if isinstance(other,str):
            transformed_pinyin = pinyin_transform(other)
            return self.pinyin < transformed_pinyin

    def __gt__(self, other):
        if isinstance(other, str):
            pinyin_list = pinyin_transform(other)
            return self.pinyin > pinyin_list

    def __eq__(self, other):
        if isinstance(other, Identification):
            return self.simplified == other.simplified and self.traditional == other.traditional
        if isinstance(other,str):
            hanzi = other
            hanzi_pinyin = pinyin_transform(hanzi)
            if re.match(r'\W+',hanzi_pinyin): #if is a symbol
                return  self.simplified == hanzi or self.traditional == hanzi
            return self.pinyin == hanzi_pinyin

class HanziNode:
    def __init__(self, data: Hanzi, father):
        self.id = Identification(pinyin=pinyin_transform(data.simplified),traditional=data.traditional,simplified=data.simplified)
        self.data = data
        self.right: Optional[RBNode] = None
        self.left: Optional[RBNode] = None
        self.father: Optional[RBNode] = father
        self.red = True

    def get_data(self):
        return self.data

    def get_id(self) -> any:
        return  self.id

    def get_father(self) -> RBNode:
        return self.father

    def get_left(self) -> RBNode:
        return self.left

    def get_right(self) -> RBNode:
        return self.right

    def set_father(self, node: RBNode) -> None:
        self.father = node

    def set_left(self, node: RBNode) -> None:
        self.left = node

    def set_right(self, node: RBNode) -> None:
        self.right = node
    def is_red(self) -> bool:
        return self.red

    def is_black(self) -> bool:
        return not self.red

    def to_red(self) -> None:
        self.red = True
    def to_black(self) -> None:
        self.red = False

class ListNode:
    def __init__(self,data_root: HanziNode):
        self.id = data_root.get_id()
        self._list_hanzi: list[Hanzi] = []
        self.right: Optional[RBNode] = data_root.right
        self.left: Optional[RBNode] = data_root.left
        self.father: Optional[RBNode] = data_root.father
        self.red = True
        self._list_hanzi.append(data_root.get_data())

    def get_data(self):
        return self._list_hanzi

    def get_id(self) -> any:
        return  self.id

    def get_father(self) -> RBNode:
        return self.father

    def get_left(self) -> RBNode:
        return self.left

    def get_right(self) -> RBNode:
        return self.right

    def set_father(self, node: RBNode) -> None:
        self.father = node

    def set_left(self,node: RBNode) -> None:
        self.left = node

    def set_right(self,node: RBNode) -> None:
        self.right = node

    def add_node(self,hanzi: Hanzi):
        self._list_hanzi.append(hanzi)

    def is_red(self) -> bool:
        return self.red

    def is_black(self) -> bool:
        return not self.red

    def to_red(self) -> None:
        self.red = True
    def to_black(self) -> None:
        self.red = False

