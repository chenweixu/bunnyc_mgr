#!/bin/bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cp $work_dir/produce.yaml $work_dir/../src/conf/conf.yaml
cp $work_dir/produce.key $work_dir/../src/conf/conf.key
cp $work_dir/produce.py $work_dir/../src/config.py
