#!/bin/bash

python ../rl_teacher/teach.py --conf ../config/es_augment_popsize/es_augment_synth_pop16.json
python ../rl_teacher/teach.py --conf ../config/es_augment_popsize/es_augment_synth_pop16.json
python ../rl_teacher/teach.py --conf ../config/es_augment_popsize/es_augment_synth_pop16.json

python ../rl_teacher/teach.py --conf ../config/es_augment_popsize/es_augment_synth_pop32.json
python ../rl_teacher/teach.py --conf ../config/es_augment_popsize/es_augment_synth_pop32.json
python ../rl_teacher/teach.py --conf ../config/es_augment_popsize/es_augment_synth_pop32.json