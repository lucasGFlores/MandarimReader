from typing import Protocol


class Node(Protocol):
    def get_data(self) -> any:
        pass
