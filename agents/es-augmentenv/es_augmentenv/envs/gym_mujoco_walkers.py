from es_augmentenv.envs.gym_mujoco_xml_env import AugmentMujocoXmlEnv
from es_augmentenv.envs.generate_hopper_xml import generate_hopper_xml

import numpy as np

from PIL import Image
import time

FILE_SLEEP_TIME = 0

#TODO: refactor somehow to make all mujoco envs augmentable
class AugmentHopper(AugmentMujocoXmlEnv):
    def __init__(self):
        super().__init__("hopper.xml", 4)

    def augment_env(self, scale_vector):
        self.set_model(generate_hopper_xml(scale_vector))
        time.sleep(FILE_SLEEP_TIME) # sleep for a random amount of time to avoid harddisk file errors.

    def step(self, a):
        posbefore = self.sim.data.qpos[0]
        self.do_simulation(a, self.frame_skip)
        posafter, height, ang = self.sim.data.qpos[0:3]
        alive_bonus = 1.0
        reward = (posafter - posbefore) / self.dt
        reward += alive_bonus
        reward -= 1e-3 * np.square(a).sum()
        s = self.state_vector()
        done = not (np.isfinite(s).all() and (np.abs(s[2:]) < 100).all() and
                    (height > .7) and (abs(ang) < .2))
        ob = self.get_obs()
        return ob, reward, done, {}

    def get_obs(self):
        return np.concatenate([
            self.sim.data.qpos.flat[1:],
            np.clip(self.sim.data.qvel.flat, -10, 10)
        ])

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(low=-.005, high=.005, size=self.model.nq)
        qvel = self.init_qvel + self.np_random.uniform(low=-.005, high=.005, size=self.model.nv)
        self.set_state(qpos, qvel)
        return self.get_obs()

    def viewer_setup(self):
        self.viewer.cam.trackbodyid = 2
        self.viewer.cam.distance = self.model.stat.extent * 0.75
        self.viewer.cam.lookat[2] += .8
        self.viewer.cam.elevation = -20


def main():
    env = AugmentHopper()
    env.augment_env([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    rgb = env.render(mode="rgb_array")

    im = Image.fromarray(rgb)
    im.save("snaps/snap.jpg")

if __name__ == "__main__":
    main()
