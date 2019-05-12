import datetime
from app import db


class t_host_cpu(db.Model):
    """定义数据模型"""

    __tablename__ = "t_host_cpu"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ctime = db.Column(db.DateTime, nullable=False, comment="采集时间", index=True)
    itime = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now, comment="入库时间"
    )
    ip = db.Column(db.String(20), nullable=False, comment="服务器IP")
    cpu = db.Column(db.Float(5, 2), nullable=False, comment="使用率")
    cpu_user_rate = db.Column(db.Float(5, 2), nullable=False, comment="用户态")
    cpu_nice_rate = db.Column(db.Float(5, 2), nullable=False, comment="权限调整")
    cpu_system_rate = db.Column(db.Float(5, 2), nullable=False, comment="内核态")
    cpu_idle_rate = db.Column(db.Float(5, 2), nullable=False, comment="空闲")
    cpu_iowait_rate = db.Column(db.Float(5, 2), nullable=False, comment="IO阻塞")
    cpu_irq_rate = db.Column(db.Float(5, 2), nullable=False, comment="硬中断")
    cpu_softirq_rate = db.Column(db.Float(5, 2), nullable=False, comment="软中断")
    ld_1 = db.Column(db.Float(5, 2), nullable=False, comment="1分钟负载")
    ld_2 = db.Column(db.Float(5, 2), nullable=False, comment="5分钟负载")
    ld_3 = db.Column(db.Float(5, 2), nullable=False, comment="15分钟负载")
    proc_run = db.Column(db.SmallInteger(), nullable=False, comment="当前运行pid")
    proc_sub = db.Column(db.SmallInteger(), nullable=False, comment="合计PID数")


class t_host_ram(db.Model):
    """定义数据模型"""

    __tablename__ = "t_host_ram"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ctime = db.Column(db.DateTime, nullable=False, comment="采集时间", index=True)
    itime = db.Column(db.DateTime, default=datetime.datetime.now, comment="入库时间")
    ip = db.Column(db.String(20), nullable=False, comment="服务器IP")
    mem = db.Column(db.SmallInteger(), nullable=False, comment="内存使用率")
    swap = db.Column(db.SmallInteger(), nullable=False, comment="swap使用率")
