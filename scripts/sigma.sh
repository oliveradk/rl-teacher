#!/bin/bash

python ../rl_teacher/teach.py --conf ../config/es_augment_sigma/es_augment_synth_sigma1.json
python ../rl_teacher/teach.py --conf ../config/es_augment_sigma/es_augment_synth_sigma1.json
python ../rl_teacher/teach.py --conf ../config/es_augment_sigma/es_augment_synth_sigma1.json

python ../rl_teacher/teach.py --conf ../config/es_augment_sigma/es_augment_synth_sigma2.json
python ../rl_teacher/teach.py --conf ../config/es_augment_sigma/es_augment_synth_sigma2.json
python ../rl_teacher/teach.py --conf ../config/es_augment_sigma/es_augment_synth_sigma2.json
