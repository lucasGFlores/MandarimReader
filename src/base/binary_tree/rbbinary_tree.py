from abc import  abstractmethod

from .binary_tree import BinaryTree
from .node import RBNode

class RBTree(BinaryTree):
    @abstractmethod
    def _left_rotation(self, node_to_rotate: RBNode) -> None:
        pass

    @abstractmethod
    def _right_rotation(self, node_to_rotate: RBNode) -> None:
        pass

    @abstractmethod
    def _fix_tree(self,node: RBNode):
        pass

    @abstractmethod
    def search_data(self,id_):
        pass