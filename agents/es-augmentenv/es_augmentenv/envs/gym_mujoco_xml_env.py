import numpy as np

from gym.envs.mujoco import MujocoEnv
from gym import spaces
import mujoco_py


class AugmentMujocoXmlEnv(MujocoEnv):
    """
    Base class for modifiable MuJoCo .xml environment
    """

    def set_model(self, model_path):
        self.model = mujoco_py.MjModel(model_path)
        self.data = self.model.data
        self.viewer = None

        self.init_qpos = self.model.data.qpos.ravel().copy()
        self.init_qvel = self.model.data.qvel.ravel().copy()
        observation, _reward, done, _info = self._step(np.zeros(self.model.nu))
        assert not done
        self.obs_dim = observation.size

        bounds = self.model.actuator_ctrlrange.copy()
        low = bounds[:, 0]
        high = bounds[:, 1]
        self.action_space = spaces.Box(low, high)

        high = np.inf * np.ones(self.obs_dim)
        low = -high
        self.observation_space = spaces.Box(low, high)

        self._seed()
