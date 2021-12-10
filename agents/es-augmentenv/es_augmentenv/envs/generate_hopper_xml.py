import numpy as np
import os

def generate_hopper_xml(s):
  random_filename = str(np.random.randint(0, 100000000000000))+".xml"
  filename = os.path.dirname(__file__) + "/assets/augment/" + random_filename

  param_default = [0.4, 0.4, 0.4, 0.1, -0.13, 0.26, 0.05, 0.05, 0.04, 0.06]

  param_offset = [1.45-0.4, 1.06-0.4, 0.6-0.4, 0, 0, 0, 0, 0, 0, 0]

  scale_vector = [s[0], s[1], s[2], s[3], s[4], s[4], s[5], s[6], s[7], s[8]]

  num_param = len(param_default)

  param_xml = '''
  <mujoco model="hopper">
    <compiler angle="degree" coordinate="global" inertiafromgeom="true"/>
    <default>
      <joint armature="1" damping="1" limited="true"/>
      <geom conaffinity="1" condim="1" contype="1" margin="0.001" friction="0.8 .1 .1" material="geom" rgba="0.8 0.6 .4 1" solimp=".8 .8 .01" solref=".02 1"/>
      <motor ctrllimited="true" ctrlrange="-.4 .4"/>
    </default>
    <option integrator="RK4" timestep="0.002"/>
    <visual>
    <map znear="0.02"/>
    </visual>
    <worldbody>
      <light cutoff="100" diffuse="1 1 1" dir="-0 0 -1.3" directional="true" exponent="1" pos="0 0 1.3" specular=".1 .1 .1"/>
      <geom conaffinity="1" condim="3" name="floor" pos="0 0 0" rgba="0.8 0.9 0.8 1" size="20 20 .125" type="plane" material="MatPlane"/>
      <body name="torso" pos="0 0 1.25">
        <camera name="track" mode="trackcom" pos="0 -3 1" xyaxes="1 0 0 0 0 1"/>
        <joint armature="0" axis="1 0 0" damping="0" limited="false" name="ignore1" pos="0 0 0" stiffness="0" type="slide"/>
        <joint armature="0" axis="0 0 1" damping="0" limited="false" name="ignore2" pos="0 0 0" ref="1.25" stiffness="0" type="slide"/>
        <joint armature="0" axis="0 1 0" damping="0" limited="false" name="ignore3" pos="0 0 0" stiffness="0" type="hinge"/>
        <geom fromto="0 0 {0} 0 0 {1}" name="torso_geom" size="{6}" type="capsule"/> <!-- friction=.9 -->
        <body name="thigh" pos="0 0 1.05">
          <joint axis="0 -1 0" name="thigh_joint" pos="0 0 {1}" range="-150 0" type="hinge"/>
          <geom fromto="0 0 {1} 0 0 {2}" name="thigh_geom" size="{7}" type="capsule"/>
          <body name="leg" pos="0 0 0.35">
            <joint axis="0 -1 0" name="leg_joint" pos="0 0 {2}" range="-150 0" type="hinge"/>
            <geom fromto="0 0 {2} 0 0 {3}" name="leg_geom" size="{8}" type="capsule"/>
            <body name="foot" pos="0.13/2 0 0.1">
              <joint axis="0 -1 0" name="foot_joint" pos="0 0 {3}" range="-45 45" type="hinge"/>
              <geom fromto="{4} 0 {3} {5} 0 {3}" name="foot_geom" size="{9}" type="capsule"/>
            </body>
          </body>
        </body>
      </body>
    </worldbody>
    <actuator>
      <motor ctrllimited="true" ctrlrange="-1.0 1.0" gear="200.0" joint="thigh_joint"/>
      <motor ctrllimited="true" ctrlrange="-1.0 1.0" gear="200.0" joint="leg_joint"/>
      <motor ctrllimited="true" ctrlrange="-1.0 1.0" gear="200.0" joint="foot_joint"/>
    </actuator>
        <asset>
        <texture type="skybox" builtin="gradient" rgb1=".4 .5 .6" rgb2="0 0 0"
            width="100" height="100"/>
        <texture builtin="flat" height="1278" mark="cross" markrgb="1 1 1" name="texgeom" random="0.01" rgb1="0.8 0.6 0.4" rgb2="0.8 0.6 0.4" type="cube" width="127"/>
        <texture builtin="checker" height="100" name="texplane" rgb1="0 0 0" rgb2="0.8 0.8 0.8" type="2d" width="100"/>
        <material name="MatPlane" reflectance="0.5" shininess="1" specular="1" texrepeat="60 60" texture="texplane"/>
        <material name="geom" texture="texgeom" texuniform="true"/>
    </asset>
  </mujoco>
  '''

  for i in range(num_param):
    param_xml = param_xml.replace("{"+str(i+0)+"}", str(param_default[i]*scale_vector[i]+param_offset[i]))

  fp = open(os.path.join(os.path.dirname(__file__), filename), "w")
  fp.write(param_xml)
  fp.close()

  return filename

def main():
  generate_hopper_xml([0.4, 0.4, 0.4, 0.1, -0.13, 0.26, 0.05, 0.05, 0.04, 0.06])

if __name__ == "__main__":
  main()