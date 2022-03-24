#!/bin/bash

python ../rl_teacher/teach.py --conf ../config/es_augment_optim/es_augment_synth_ga.json
python ../rl_teacher/teach.py --conf ../config/es_augment_optim/es_augment_synth_ga.json
python ../rl_teacher/teach.py --conf ../config/es_augment_optim/es_augment_synth_ga.json

python ../rl_teacher/teach.py --conf ../config/es_augment_optim/es_augment_synth_cmaes.json
python ../rl_teacher/teach.py --conf ../config/es_augment_optim/es_augment_synth_cmaes.json
python ../rl_teacher/teach.py --conf ../config/es_augment_optim/es_augment_synth_cmaes.json