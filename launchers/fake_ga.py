import random
import math
from ControlledParam import ControlledParam

from mcts import Node


class Optimum:
    def __init__(self, mag, std, x, y):
        self.mag = mag
        self.std = std
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Optimum at {self.x, self.y} with m={self.mag}, std={self.std}'

x_range = Node(0, 10)
y_range = Node(-5, -1)


def random_optimum():
    return Optimum(random.random(),
                   random.random(),
                   x_range.rollout(),
                   y_range.rollout())


class FakeGa:

    use_x = ControlledParam('x', x_range)
    use_y = ControlledParam('y', y_range)

    cps = [use_x, use_y]

    def __init__(self, max_turns: int = 10, steepness = 6, noise_factor = 1):
        self.optima = [random_optimum() for _ in range(5)]

        self.steepness = steepness
        self.noise_factor = noise_factor
        self.max_turns = max_turns
        self.done = False
        self.ctr = 0

        ControlledParam.init(self, self.cps)


    def reset(self):
        self.ctr = 0
        self.done = False

        ControlledParam.init(self, self.cps)


    def rwrd(self, x, y):
        tr = 0
        for o in self.optima:
            log_miss = self.steepness * math.sqrt((x - o.x)**2 + (y - o.y)**2)
            reward = o.mag * 10 ** (-log_miss / 10) * (
                        1 + self.noise_factor * o.std * (0.5 - random.random()))
            tr += reward

        tr += 10 * (math.sin(x/(y+1)) ** 3) * (1 + self.noise_factor * o.std * (0.5 - random.random()))
        return tr

    def step(self):

        result = self.rwrd(self.use_x, self.use_y)
        ControlledParam.step(self, result)

        self.ctr += 1
        if self.ctr > self.max_turns:
            self.done = True

        return result

class CompareGa:
    def __init__(self, max_turns: int = 10, steepness = 6, noise_factor = 1,
                 use_x = None, use_y = None):
        self.optima = [random_optimum() for _ in range(5)]

        self.steepness = steepness
        self.noise_factor = noise_factor
        self.max_turns = max_turns
        self.done = False
        self.ctr = 0

        self.use_x = use_x
        self.use_y = use_y

    def reset(self):
        self.ctr = 0
        self.done = False


    def rwrd(self, x, y):
        tr = 0
        for o in self.optima:
            log_miss = self.steepness * math.sqrt((x - o.x)**2 + (y - o.y)**2)
            reward = o.mag * 10 ** (-log_miss / 10) * (
                        1 + self.noise_factor * o.std * (0.5 - random.random()))
            tr += reward

        tr += 10 * (math.sin(x/(y+1)) ** 3) * (1 + self.noise_factor * o.std * (0.5 - random.random()))
        return tr

    def step(self):
        if self.use_x:
            x = self.use_x
        else:
            x = x_range.rollout()

        if self.use_y:
            y = self.use_y
        else:
            y = y_range.rollout()

        result = self.rwrd(x, y)


        self.ctr += 1
        if self.ctr > self.max_turns:
            self.done = True

        return result


if __name__ == "__main__":
    from ilya_ezplot import Metric, plot_group

    ga_1 = FakeGa(max_turns=400, noise_factor=5)


    def one_run(ga):
        ga.reset()
        m = Metric('steps', 'score')

        while not ga.done:
            r = ga.step()
            m.add_record(ga.ctr, r)

        return m

    metrics = [one_run(ga_1) for _ in range(100)]

    ga_rand = CompareGa(max_turns=400, noise_factor=5)
    metrics_rand = [one_run(ga_rand) for _ in range(100)]

    plot_group({
                'mcts' : sum(metrics),
                'random': sum(metrics_rand)
                 },
               'temp')




