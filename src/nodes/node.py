from __future__ import annotations
from collections import deque
import abc


class Node(abc.ABC):

    def __init__(self, parent: Node = None, maxlen = 200):

        self.results = deque(maxlen=maxlen)
        self.parent = parent
        self.left: Node = None
        self.right: Node = None

    def expand(self):
        raise NotImplementedError()

    def rollout(self):
        raise NotImplementedError()

    def contains(self, x):
        raise NotImplementedError()

    @property
    def is_expanded(self):
        return self.left is not None


    def append_result(self, result: float):
        self.results.append(result)


    def register(self, result: float):
        self.append_result(result)
        parent = self.parent
        while parent:
            parent.append_result(result)
            parent = parent.parent


    def __repr__(self):
        return f"Abstract Node"