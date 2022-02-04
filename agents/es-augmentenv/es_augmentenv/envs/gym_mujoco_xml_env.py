import numpy as np

from gym.envs.mujoco import MujocoEnv
from gym import spaces
from mujoco_py import MjSim, load_model_from_path


class AugmentMujocoXmlEnv(MujocoEnv):
    """
    Base class for modifiable MuJoCo .xml environment
    """

    def set_model(self, model_path):
        self.model = load_model_from_path(model_path)
        self.sim = MjSim(self.model)
        self.data = self.sim.data
        self.viewer = None
        self._viewers = {}

        self.init_qpos = self.sim.data.qpos.ravel().copy()
        self.init_qvel = self.sim.data.qvel.ravel().copy()

        self._set_action_space()

        action = self.action_space.sample()
        observation, _reward, done, _info = self.step(action)
        assert not done

        self._set_observation_space(observation)

        self.seed()
