import os.path

import numpy as np
from tqdm import tqdm
import json
import matplotlib.pyplot as plt

from gym.wrappers.monitoring.video_recorder import VideoRecorder

from es_augmentenv.es import SimpleGA, CMAES, OpenES, PEPG
from es_augmentenv.model import make_model, simulate
from es_augmentenv import config

def infinity():
    while True:
        yield

def train_es_augment(make_env, seed, name, pop_size=16, max_len=3000, num_episodes=1, sigma_init=0.3,
                     sigma_decay=.99, optimizer="cmaes", predictor=None, num_gens=None,
                     show_video=False, store_params=False):
    game_name = "augment_hopper"
    game = config.games[game_name]

    model = make_model(game, make_env_inner=make_env)
    model.make_env()
    seeder = Seeder(seed)
    num_params = model.param_count
    es = None
    if optimizer == "cmaes":
        es = CMAES(num_params,
                sigma_init=sigma_init,
                popsize=pop_size)
    elif optimizer == "ga":
        es = SimpleGA(num_params,
                  sigma_init=sigma_init,
                  sigma_decay=sigma_decay,
                  sigma_limit=0.02,
                  elite_ratio=0.1,
                  weight_decay=0.005,
                  popsize=pop_size)
    elif optimizer == "open_es":
        es = OpenES(num_params,
                    sigma_init=sigma_init,
                    sigma_decay=sigma_decay,
                    popsize=pop_size)
    elif optimizer == "pepg":
        es = PEPG(num_params,
                  sigma_init=sigma_init,
                  sigma_decay=sigma_decay,
                  popsize=pop_size)
    else:
        print(f"{optimizer} not a valid optimizer")

    gen = 0
    episodes = 0

    # initialize logging data
    # start_time = int(time.time())
    #
    # history = []
    # eval_log = []

    if show_video:
        vid_dir = f"{os.path.dirname(__file__)}/saved_videos/{name}"
        os.mkdir(vid_dir)

    if store_params:
        param_dir = f"{os.path.dirname(__file__)}/saved_params/{name}"
        os.mkdir(param_dir)

    train_data = []

    iterator = range(num_gens) if num_gens is not None else infinity()
    for _ in iterator:
        #get population
        solutions = es.ask()

        #evaluate population
        reward_list = []
        t_list = []
        paths = []
        seeds = seeder.next_batch(pop_size)
        for i, solution in enumerate(tqdm(solutions)):
            model.set_model_params(solution)
            model.make_env()

            recorder = VideoRecorder(model.env, path=f"{vid_dir}/sol_{i}_gen_{gen}_{name}.mp4") if show_video else None

            if store_params:
                with open(f"{param_dir}/sol_{i}_gen_{gen}_{name}.npy", "wb") as f:
                    np.save(f, np.array(solution).round(4))

            path, rewards, ts = simulate(model, train_mode=True, render_mode=False, num_episode=num_episodes, seed=seeds[i],
                                   max_len=max_len, predictor=predictor, recorder=recorder)
            episodes += num_episodes
            paths.append(path)
            reward_list.append(np.min(rewards))
            t_list.append(np.mean(ts))

        #add paths to comparison reward predictor
        for path in paths:
            predictor.path_callback(path)

        es.tell(reward_list)

        #update parameters
        es_solution = es.result()
        model_params = es_solution[0]  # best historical solution
        reward = es_solution[1]  # best reward
        curr_reward = es_solution[2]  # best of the current batch
        model.set_model_params(np.array(model_params).round(4))

        #calculate "true" rewards
        true_rewards = [path["original_rewards"] for path in paths]
        true_curr_reward = np.max(true_rewards)

        num_comparisons = len(predictor.comparison_collector) if hasattr(predictor, "comparison_collector") else 0

        #record training data
        gen += 1
        print("Generation: ", gen)
        print("Comparisons: ", num_comparisons)
        print("cur best reward: ", curr_reward)
        print("cur best true reward", true_curr_reward)
        print("best reward: ", reward)

        train_data.append({
            "gen": gen,
            "best_reward": float(curr_reward),
            "best_true_reward": float(true_curr_reward),
            "comparisons": num_comparisons
        })

        if store_params:
            file_path = os.path.join(os.path.dirname(__file__), f"saved_params/gen_{gen}_{name}.npy")
            with open(file_path, "wb") as f:
                np.save(f, np.array(model_params).round(4))

    #save training data
    train_data_dir = os.path.join(os.path.dirname(__file__), "saved_train_data")
    train_data_path = os.path.join(train_data_dir, f"{name}.json")

    with open(train_data_path, 'w') as f:
        json.dump(train_data, f)

    f = open(train_data_path)
    train_data = json.load(f)

class Seeder:

    def __init__(self, init_seed=0):
        np.random.seed(init_seed)
        self.limit = np.int32(2**31-1)

    def next_seed(self):
        result = np.random.randint(self.limit)
        return result

    def next_batch(self, batch_size):
        result = np.random.randint(self.limit, size=batch_size).tolist()
        return result






