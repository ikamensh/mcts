from exp_range_hard import ExponentialEnv
from mcts import Mcts, Node
from mcts_v2 import Mcts as Mcts_v2
from ilya_ezplot import Metric, plot_group


env = ExponentialEnv(max_turns = 200)
trials = 100
print(env)

def run_action(action: float):
    if env.done:
        return None
    else:
        _, r, done, _ = env.step(action)
        return r

def run_trials():
    metrics_mcts = []

    for i in range(trials):
        env.reset()
        m = Metric('step', 'score')
        root = Node(0, 10)
        mcts = Mcts(run_action, root)

        done = False
        while not done:
            done = mcts.step()

        for j, r in enumerate(root.results):
            m.add_record(j, r)

        metrics_mcts.append(m)
        print('Score by MCTS:', sum(root.results))


from cProfile import Profile
profiler = Profile()
profiler.runcall(run_trials)
profiler.print_stats('cumulative')

