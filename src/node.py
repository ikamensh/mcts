from __future__ import annotations
import random

class Node:

    def __init__(self,
                 min: float, max: float,
                 parent: Node = None):
        self.min = min
        self.max = max
        self.size = self.max - self.min

        self.results = []
        self.parent = parent
        self.left: Node = None
        self.right: Node = None
        self._prio = None


    def expand(self):
        if not self.left and not self.right:
            self.left = Node(self.min, self.min + self.size / 2, self)
            self.right = Node(self.min + self.size / 2, self.max, self)

    def rollout(self) -> float:
        self.expand()
        return self.min + (self.max - self.min) * random.random()


    def append_result(self, result: float):
        self._prio = None
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
        return f"Node [{self.min:.4f}, {self.max:.4f}]"