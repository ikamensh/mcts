from __future__ import annotations
from src.node import Node
from typing import Optional
import math
import random


class Mcts:

    resolution = 1e-3

    def __init__(self, root: Node, epsilon = 0.05):
        self.root = root
        self.expectation = 1
        self.last_tried: Optional[Node] = None
        self.epsilon = epsilon

    def prio(self, node: Node):
        if node.results:
            return sum(node.results) / len(node.results) + \
                   5 * self.expectation / len(node.results)
        else:
            return math.inf


    def prio_descent(self):
        best = self.root

        while best.results and best.size > self.resolution * self.root.size:
            best.expand()
            if self.epsilon > random.random():
                best = random.choice([best.left, best.right])
            else:
                best = max(best.left, best.right, key=lambda n: self.prio(n))

        return best

    def decide(self):
        choice = self.prio_descent()
        action = choice.rollout()

        child = choice
        while child.size > self.resolution * self.root.size:
            child.expand()
            child = [c for c in [child.left, child.right] if c.contains(action)][0]
        self.last_tried = child

        return action


    def register(self, result: float):

        self.last_tried.register(result)
        self.expectation = 0.98 * self.expectation  +  0.02 * result


if __name__ == '__main__':

    root = Node(0, 10)

    mcts = Mcts(root)

    for i in range(100):
        action = mcts.decide()
        print(mcts.prio(root.left), mcts.prio(root.right))
        print(f'{action:.4f}')
        mcts.register(action)

    print(len(root.left.results), len(root.right.results))

