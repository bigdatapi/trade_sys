drop database if exists test_trade_sys;
create database test_trade_sys
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

use test_trade_sys;

drop table if exists tb_hsi_type;
create table tb_hsi_type
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    code varchar(64) NOT NULL,
    name varchar(64) NOT NULL,
    remark varchar(256) NOT NULL DEFAULT '',
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*
drop table if exists tb_ohlc_type;
create table tb_ohlc_type
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    code varchar(64) NOT NULL DEFAULT '',
    period_id int(11) unsigned NOT NULL,
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

drop table if exists tb_period;
create table tb_period
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    name varchar(24) NOT NULL,
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
*/

drop table if exists tb_ohlc_hour;
create table tb_ohlc_hour
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    is_exchange int(11) unsigned NOT NULL,
    hsi_type_id int(11) unsigned NOT NULL,
    open_num int(11) NOT NULL,
    high_num int(11) NOT NULL,
    low_num int(11) NOT NULL,
    close_num int(11) NOT NULL,
    ohlc_time datetime NOT NULL,
    percent float(10) NOT NULL,
    diff int(11) NOT NULL,
    vol int(10) NOT NULL,
    amount int(10) NOT NULL,
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    UNIQUE KEY (ohlc_time),
    FOREIGN KEY (hsi_type_id) REFERENCES tb_hsi_type(id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

drop table if exists tb_ohlc_day;
create table tb_ohlc_day
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    is_exchange int(11) unsigned NOT NULL,
    hsi_type_id int(11) unsigned NOT NULL,
    open_num int(11) NOT NULL,
    high_num int(11) NOT NULL,
    low_num int(11) NOT NULL,
    close_num int(11) NOT NULL,
    percent float(10) NOT NULL,
    diff int(11) NOT NULL,
    vol int(10) NOT NULL,
    amount int(10) NOT NULL,
    ohlc_time datetime NOT NULL,
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    UNIQUE KEY(ohlc_time),
    FOREIGN KEY (hsi_type_id) REFERENCES tb_hsi_type(id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

drop table if exists tb_ma_hour;
create table tb_ma_hour
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    hsi_type_id int(11) unsigned NOT NULL,
    ma_value int(11) unsigned NOT NULL,
    ma_time datetime NOT NULL,
    period int(11) unsigned NOT NULL,
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ma_type varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

drop table if exists tb_ma_day;
create table tb_ma_day
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    hsi_type_id int(11) unsigned NOT NULL,
    ma_value int(11) unsigned NOT NULL,
    ma_time datetime NOT NULL,
    period int(11) unsigned NOT NULL,
    mod_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

drop table if exists tb_trade_rec;
create table tb_trade_rec
(
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    code varchar(64) NOT NULL,
    name varchar(64) NOT NULL,
    direction varchar(64) NOT NULL,
    num int(11) NOT NULL,
    price float NOT NULL,
    amount float NOT NULL,
    trade_time datetime NOT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

