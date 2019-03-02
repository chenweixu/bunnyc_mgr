#!/bin/bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cp $work_dir/devel.yaml $work_dir/../src/conf/conf.yaml
cp $work_dir/devel.key $work_dir/../src/conf/conf.key
