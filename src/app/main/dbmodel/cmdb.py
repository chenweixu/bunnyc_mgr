
from app import db

class t_conf_host(db.Model):
    """定义数据模型"""
    __tablename__ = 't_conf_host'
    id = db.Column(db.Integer, primary_key=True)
    ip_v4 = db.Column(db.String(20),nullable=False,comment='主业务IP')
    ip_v6 = db.Column(db.String(40),nullable=True,comment='主业务IP')
    ip_v4_m = db.Column(db.String(20),nullable=True,comment='管理网')
    name = db.Column(db.String(50),nullable=False,comment='主机别名')
    operating_system = db.Column(db.String(50),nullable=True,comment='操作系统')
    hostname = db.Column(db.String(50),nullable=True,comment='操作系统主机名')

    cpu_number = db.Column(db.SmallInteger,nullable=True,comment='CPU核心数')
    memory_size = db.Column(db.SmallInteger,nullable=True,comment='内存大小MB')
    sn = db.Column(db.String(100),unique=True,nullable=True,comment='序列号')

    address = db.Column(db.String(200),nullable=True,comment='地理位置')
    belong_machineroom = db.Column(db.String(50),nullable=True,comment='机房')
    rack = db.Column(db.String(50),nullable=True,comment='机柜')
    manufacturer = db.Column(db.String(50),nullable=True,comment='厂商')
    dev_type = db.Column(db.String(50),nullable=True,comment='设备类型')
    dev_category = db.Column(db.String(50),nullable=False,default='服务器', comment='设备类别')

    produce = db.Column(db.SmallInteger,nullable=False,comment='生产')
    level = db.Column(db.SmallInteger,nullable=False,comment='级别')
    info = db.Column(db.Text,nullable=True,comment='备注')

    def to_json(self):
        # 返回字典类型的数据
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
