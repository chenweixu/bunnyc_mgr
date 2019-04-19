CREATE TABLE `t_conf_host` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ip_v4` VARCHAR(20) NOT NULL COMMENT '主业务IP',
    `ip_v6` VARCHAR(40) NULL COMMENT '主业务IPv6',
    `ip_v4_m` VARCHAR(20) NULL COMMENT '管理网IP',
    `name` VARCHAR(50) NOT NULL COMMENT '主机别名',
    `operating_system` VARCHAR(50) NULL COMMENT '操作系统',
    `hostname` VARCHAR(50) NULL COMMENT '操作系统主机名',
    `cpu_number` SMALLINT(5) UNSIGNED NULL COMMENT 'CPU核心数',
    `memory_size` MEDIUMINT(8) UNSIGNED NULL COMMENT '内存大小GB',
    `sn` VARCHAR(100) NULL UNIQUE COMMENT '序列号',
    `address` VARCHAR(200) NULL COMMENT '地理位置',
    `belong_machineroom` VARCHAR(50) NULL COMMENT '机房',
    `rack` VARCHAR(50) NULL COMMENT '机柜',
    `manufacturer` VARCHAR(50) NULL COMMENT '厂商',
    `dev_type` VARCHAR(50) NULL COMMENT '设备型号',
    `dev_category` VARCHAR(50) NOT NULL COMMENT '设备类别',
    `produce` TINYINT(3) UNSIGNED NOT NULL COMMENT '生产',
    `level` TINYINT(5) UNSIGNED NOT NULL COMMENT '级别',
    `info` TEXT COMMENT '备注'
)
COLLATE='utf8_general_ci' ENGINE=InnoDB;
