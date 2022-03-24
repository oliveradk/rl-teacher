#!/bin/bash

python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train500.json
python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train500.json
python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train500.json

python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train1000.json
python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train1000.json
python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train1000.json

python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train1500.json
python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train1500.json
python ../rl_teacher/teach.py --conf ../config/es_augment_train/es_augment_synth_train1500.json

