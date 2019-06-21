from exp_range_hard import ExponentialEnv
from mcts import Mcts, Node
import time

from ilya_ezplot import Metric, plot_group

from multiprocessing import Process

def one_run(env, n_turns, steepness, noise):

    env.max_turns = n_turns
    env.steepness = steepness
    env.noise_factor = noise

    trials = int(20 * 400 / n_turns)

    t = time.time()
    metrics_mcts_v3 = []
    for i in range(trials):
        env.reset()
        m = Metric('step', 'score')
        root = Node(0, 10)
        mcts = Mcts(root)

        done = False
        while not done:
            action = mcts.decide()
            _, r, done, _ = env.step(action)
            mcts.register(r)

        for j, r in enumerate(root.results):
            m.add_record(j, r)

        metrics_mcts_v3.append(m)

    metrics_mcts_v3 = sum(metrics_mcts_v3)
    print('Time for MCTSv3:', time.time() - t)



    t = time.time()
    import random
    metrics_rnd = []
    for i in range(trials):

        env.reset()
        m = Metric('step', 'score')
        rand_results = []
        done = False
        while not done:
            action = random.random() * 10
            _, r, done, _ = env.step(action)
            rand_results.append(r)

        for j, r in enumerate(rand_results):
            m.add_record(j, r)

        metrics_rnd.append(m)

    print('Time for RND:', time.time() - t)

    plot_group({
        'mcts_v3': metrics_mcts_v3,
        'random': sum(metrics_rnd)
    },
        'temp', name=f'{n_turns}_st{steepness}_n{noise}')

if __name__ == '__main__':

    env = ExponentialEnv(max_turns=400)
    print(env)

    for n_turns in [400]:
        for noise in [9]:
            processes = []
            # for noise in [0.3, 1, 3, 9]:
            for steepness in [2, 6, 10]:
                p = Process(target=one_run, args=(env, n_turns, steepness, noise))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

