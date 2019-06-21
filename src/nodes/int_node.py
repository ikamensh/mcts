from __future__ import annotations
import random

from nodes.node import Node

class IntNode(Node):

    def __init__(self,
                 min: int, max: int,
                 parent: IntNode = None,
                 maxlen = 200):

        self.min = int(min)
        self.max = int(max)
        self.size = self.max - self.min + 1

        super().__init__(parent, maxlen)


    def expand(self):
        if self.size == 1:
            return False
        else:
            if not self.left and not self.right:
                next_maxlen = max(15, int(self.results.maxlen * 0.85))
                mid = self.min + self.size // 2 - 1
                self.left = IntNode(self.min, mid, self, maxlen=next_maxlen)
                self.right = IntNode(mid + 1, self.max, self, maxlen=next_maxlen)

            return True

    def rollout(self) -> float:
        return random.randint(self.min, self.max)


    def append_result(self, result: float):
        self.results.append(result)


    def register(self, result: float):
        self.append_result(result)
        parent = self.parent
        while parent:
            parent.append_result(result)
            parent = parent.parent

    def contains(self, n):
        return self.min <= n <= self.max

    def __repr__(self):
        return f"Node [{self.min}, {self.max}]"