from abc import ABC, abstractmethod
from typing import Protocol, Optional
from .node import Node

class BinaryTree(ABC):
    _root: Optional[Node]

    @abstractmethod
    def insert_node(self,data) -> None:
        pass


