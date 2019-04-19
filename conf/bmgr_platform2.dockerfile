# 2018-09-18 11:11:39
# Version: 0.2
# opsmgr

# docker build -t chenwx/bmgr_platform:0.1 -f conf/bmgr_platform.dockerfile .
# docker build -t chenwx/bmgr_platform:0.2 -f conf/bmgr_platform2.dockerfile .

FROM chenwx/bmgr_platform:0.1

RUN pip3 install Flask-SQLAlchemy
