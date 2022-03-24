import os
import numpy as np
from tqdm import tqdm
import multiprocessing as mp

from es_augmentenv.model import make_model
from es_augmentenv import config
from rl_teacher.envs import make_with_torque_removed
from gym.wrappers.monitoring.video_recorder import VideoRecorder

PARAM_DIR = os.path.join(os.path.dirname(__file__), 'saved_params')
VIDEO_DIR = os.path.join(os.path.dirname(__file__), 'saved_videos')


def run_episode(game, video_dir, param_dir, param_file, max_len=3000):
    def make_env():
        return make_with_torque_removed("AugmentHopper-v1")

    model = make_model(game, make_env_inner=make_env)
    params = np.load(os.path.join(param_dir, param_file))
    model.set_model_params(params)
    model.make_env()
    model.augment_env()

    recorder = VideoRecorder(model.env, path=f"{video_dir}/{os.path.splitext(param_file)[0]}.mp4")
    obs = model.env.reset()
    for t in range(max_len):
        recorder.capture_frame()
        action = model.get_action(obs, t=t)
        obs, reward, done, _ = model.env.step(action)
    recorder.close()


def make_video(game, video_dir, param_dir, param_file):
    p = mp.Process(target=run_episode, args=(game, video_dir, param_dir, param_file))
    p.start()
    p.join()


if __name__ == "__main__":

    # settable params
    game_name = "augment_hopper"
    game = config.games[game_name]
    experiment = 'es_augment_synth_ga_03_11_22_16_01_32'

    # get and create experiment dirs
    param_dir = os.path.join(PARAM_DIR, experiment)
    video_dir = os.path.join(VIDEO_DIR, experiment)
    if not os.path.isdir(video_dir):
        os.mkdir(video_dir)

    # generate videos
    param_files = [param_file for param_file in sorted(os.listdir(param_dir))]
    gen_num = 30
    #param_files = [param_file for param_file in param_files if f"gen_{29}" in param_file]
    param_files = [param_file for param_file in param_files if f"sol_{0} " in param_file]
    pop_size = 64
    for i in tqdm(range(pop_size)):
        make_video(game, video_dir, param_dir, param_files[-i])
    # for param_file in tqdm(os.listdir(param_dir)):
    #     p = mp.Process(target=run_episode, args=(game, video_dir, param_dir, param_file))
    #     p.start()
    #     p.join()