from typing import Protocol
from .node import Node

class RBNode(Node,Protocol):

    def get_data(self):
        pass
    def is_red(self) -> bool:
        pass

    def is_black(self) -> bool:
        pass

    def to_red(self) -> None:
        pass
    def to_black(self) -> None:
        pass
    def set_father(self, node: "RBNode") -> None:
        pass
    def set_left(self, node: "RBNode") -> None:
        pass
    def set_right(self, node: "RBNode") -> None:
        pass
    def get_father(self) -> "RBNode":
        pass
    def get_left(self) -> "RBNode":
        pass
    def get_right(self) -> "RBNode":
        pass
    def get_id(self) -> any:
        pass
