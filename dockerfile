# 2018-09-18 11:14:02
# Version: 0.01
# bmgr

FROM chenwx/bmgr_platform:1.0.1
LABEL author="chenwx"
LABEL version="0.6"

# add bserver
ADD requirements.txt /usr/local/requirements.txt

# install python pkg
RUN pip3 install --upgrade pip \
    && pip3 install -r /usr/local/requirements.txt \
    && rm /usr/local/requirements.txt

# add bmgr server
ADD src /usr/local/bunnyc_mgr

# CMD
CMD python3 /usr/local/bunnyc_mgr/run.py

EXPOSE 9002
