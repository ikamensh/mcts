from __future__ import annotations

from nodes.node import Node

from typing import Optional
import math
import random


class Mcts:

    def __init__(self, root: Node, epsilon = 0.02):
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

        while best.results and best.left:

            if self.epsilon > random.random():
                best = random.choice([best.left, best.right])
            else:
                best = max(best.left, best.right, key=lambda n: self.prio(n))

        return best

    def decide(self):
        choice = self.prio_descent()
        action = choice.rollout()

        child = choice

        can_expand = child.expand()
        while can_expand:
            child = [c for c in [child.left, child.right] if c.contains(action)][0]
            can_expand = child.expand()

        self.last_tried = child

        return action


    def register(self, result: float):

        self.last_tried.register(result)
        self.expectation = 0.98 * self.expectation  +  0.02 * result


if __name__ == '__main__':

    # from nodes.float_node import FloatNode
    #
    # root = FloatNode(0, 10)
    #
    # mcts = Mcts(root)
    #
    # for i in range(100):
    #     action = mcts.decide()
    #     print(mcts.prio(root.left), mcts.prio(root.right))
    #     print(f'{action:.4f}')
    #     mcts.register(action)
    #
    # print(len(root.left.results), len(root.right.results))


    from nodes.int_node import IntNode

    root = IntNode(0, 100)

    mcts = Mcts(root)

    for i in range(100):
        action = mcts.decide()
        print(mcts.prio(root.left), mcts.prio(root.right))
        print(f'{action}')
        mcts.register(action)

    print(len(root.left.results), len(root.right.results))

