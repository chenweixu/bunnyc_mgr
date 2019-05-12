# 2018-09-18 11:14:02
# Version: 0.2
# bmgr

FROM chenwx/bmgr_platform:0.4
LABEL author="chenwx"
LABEL version="0.3"

# add bmgr server
ADD src /usr/local/bunnyc_mgr

WORKDIR /usr/local/bunnyc_mgr

# CMD
# CMD python3 /usr/local/bunnyc_mgr/run.py
# gunicorn run:app -c app/conf/gunicorn.conf
CMD ["gunicorn", "run:app", "-c", "app/conf/gunicorn.conf"]

EXPOSE 9002
