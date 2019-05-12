#!/bin/bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"
cd $work_dir

rm -f $work_dir/src/log/*
rm -f $work_dir/src/tmp/*
rm -f $work_dir/src/app/conf/*

cp $work_dir/conf/devel/* $work_dir/src/app/conf/


# version=0.2
# container=bmgr

# docker stop $container
# docker rm $container
# docker rmi chenwx/$container:$version

# echo '-------------------------build start--------------------'
# docker build -t chenwx/$container:$version -f conf/bmgr.dockerfile .


# docker run --name $container -h $container --net="host" -d chenwx/$container:$version
# docker run --name $container -h $container --net="host" -d chenwx/$container:1.0.2

# docker run --name bmgr -h bmgr --net="host" -d chenwx/bmgr:1.0.4
