#!/bin/bash

python ../rl_teacher/teach.py --conf ../config/es_morph/es_fixed_synth.json
python ../rl_teacher/teach.py --conf ../config/es_morph/es_fixed_synth.json
python ../rl_teacher/teach.py --conf ../config/es_morph/es_fixed_synth.json

python ../rl_teacher/teach.py --conf ../config/es_morph/es_fixed_rl.json
python ../rl_teacher/teach.py --conf ../config/es_morph/es_fixed_rl.json
python ../rl_teacher/teach.py --conf ../config/es_morph/es_fixed_rl.json



