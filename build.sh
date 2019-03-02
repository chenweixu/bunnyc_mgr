#!/bin/bash
# 0.4           2018-11-30 05:39:25
# 0.5           2019-01-15 10:31:11
# 0.6           2019-03-02 23:10:48
work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

version=0.6
container=bmgr
img_dir=/data/share/docker_images

img_file=$img_dir/chenwx_${container}_${version}.tar

docker stop $container
docker rm $container
docker rmi chenwx/$container:$version
rm $img_dir/chenwx_$container_$version.tar

#------------------------------------------------
rm src/log/work.log
echo '-------------------------build start--------------------'
docker build -t chenwx/$container:$version -f $work_dir/dockerfile .

sleep 2

docker save chenwx/$container:$version > $img_file


docker run --name $container -h $container --net="host" -d chenwx/$container:$version
# docker run --name $container -h $container --net="host" -d chenwx/$container:1.0.2

# docker run --name bmgr -h bmgr --net="host" -d chenwx/bmgr:1.0.4
