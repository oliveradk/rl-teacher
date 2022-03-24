#!/bin/bash

python ../rl_teacher/teach.py --conf ../config/es_augment_predictor/es_augment_synth.json
python ../rl_teacher/teach.py --conf ../config/es_augment_predictor/es_augment_synth.json
python ../rl_teacher/teach.py --conf ../config/es_augment_predictor/es_augment_synth.json

python ../rl_teacher/teach.py --conf ../config/es_augment_predictor/es_augment_rl.json
python ../rl_teacher/teach.py --conf ../config/es_augment_predictor/es_augment_rl.json
python ../rl_teacher/teach.py --conf ../config/es_augment_predictor/es_augment_rl.json


