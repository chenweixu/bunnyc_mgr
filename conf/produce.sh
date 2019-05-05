#!/bin/bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"
cd $work_dir
mkdir $work_dir/src/conf
mkdir $work_dir/src/log
mkdir $work_dir/src/tmp

cp $work_dir/conf/produce.yaml $work_dir/src/conf/conf.yaml
cp $work_dir/conf/produce.key $work_dir/src/conf/conf.key
cp $work_dir/conf/produce.py $work_dir/src/config.py

version=0.2
container=bmgr

docker stop $container
docker rm $container
docker rmi chenwx/$container:$version

#------------------------------------------------
rm $work_dir/src/log/*
rm $work_dir/src/tmp/*
echo '-------------------------build start--------------------'
docker build -t chenwx/$container:$version -f conf/bmgr.dockerfile .

docker run --name $container -h $container --net="host" -d chenwx/$container:$version
# docker run --name bmgr -h bmgr --net="host" -d chenwx/bmgr:0.2
