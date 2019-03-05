#!/bin/bash
# 1.0.4         2018-11-30 05:39:25
work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

version=1.0.1
container=bmgr_platform
img_dir=/data/share/docker_images

img_file=$img_dir/chenwx_${container}_${version}.tar

docker stop $container
docker rm $container
docker rmi chenwx/$container:$version
rm $img_dir/chenwx_$container_$version.tar

#------------------------------------------------

docker build -t chenwx/$container:$version -f $work_dir/dockerfile .

sleep 2

docker save chenwx/$container:$version > $img_file


# docker run --name $container -h $container --net="host" -d chenwx/$container:$version
# docker run --name $container -h $container --net="host" -d chenwx/$container:1.0.2

# docker run --name bmgr -h bmgr --net="host" -d chenwx/bmgr:1.0.4
