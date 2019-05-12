#!/bin/bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"
cd $work_dir

#------------------------------------------------
rm -f ${work_dir}/src/log/*
rm -f ${work_dir}/src/tmp/*
rm -rf ${work_dir}/src/app/conf/*
#------------------------------------------------
mkdir $work_dir/src/app/conf
mkdir $work_dir/src/log
mkdir $work_dir/src/tmp

cp $work_dir/conf/produce/* $work_dir/src/app/conf/

version=0.3
container=bmgr

docker stop $container
docker rm $container
docker rmi chenwx/$container:$version

echo '-------------------------build start--------------------'
docker build -t chenwx/$container:$version -f conf/bmgr.dockerfile .

docker run --name $container -h $container --net="host" -d chenwx/$container:$version
# docker run --name bmgr -h bmgr --net="host" -d chenwx/bmgr:0.2
