from collections import namedtuple

Game = namedtuple('Game', ['env_name', 'time_factor', 'body_size', 'augment_mode', 'input_size',  'output_size', 'layers', 'activation', 'noise_bias', 'output_noise'])

games = {}


augment_hopper = Game(env_name='AugmentHopper-v1',
  body_size=9,
  augment_mode="bounded",
  input_size=11,
  output_size=3,
  layers=[75, 15],
  time_factor=1000,
  activation='passthru',
  noise_bias=0.0,
  output_noise=[False, False, True],
)
games['augment_hopper'] = augment_hopper

augment_hopper_lognormal = Game(env_name='AugmentHopper-v1',
  body_size=9,
  augment_mode="lognormal",
  input_size=15,
  output_size=3,
  layers=[75, 15],
  time_factor=1000,
  activation='passthru',
  noise_bias=0.0,
  output_noise=[False, False, True],
)
games['augment_hopper_lognormal'] = augment_hopper_lognormal

fixed_hopper = Game(env_name='FixedHopper-v1',
  body_size=0,
  augment_mode="bounded",
  input_size=11,
  output_size=3,
  layers=[75, 15],
  time_factor=1000,
  activation='passthru',
  noise_bias=0.0,
  output_noise=[False, False, True],
)
games['fixed_hopper'] = fixed_hopper
