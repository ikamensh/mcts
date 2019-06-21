from __future__ import annotations
import random
from nodes.node import Node

class FloatNode(Node):

    def __init__(self,
                 min: float,
                 max: float,
                 parent: Node = None, maxlen = 200,
                 maxdepth = 10):

        self.min = min
        self.max = max
        self.size = self.max - self.min
        self.maxdepth = maxdepth
        super().__init__(parent, maxlen)


    def expand(self):
        if self.maxdepth > 0:
            if not self.is_expanded:

                next_maxlen = max(15, int(self.results.maxlen * 0.85))

                self.left = FloatNode(self.min, self.min + self.size / 2, self,
                                 maxlen=next_maxlen, maxdepth = self.maxdepth - 1)

                self.right = FloatNode(self.min + self.size / 2, self.max, self,
                                  maxlen=next_maxlen, maxdepth = self.maxdepth - 1)
            return True
        else:
            return False

    def rollout(self) -> float:
        return self.min + (self.max - self.min) * random.random()

    def contains(self, n):
        return self.min <= n <= self.max

    def __repr__(self):
        return f"Node [{self.min:.4f}, {self.max:.4f}]"