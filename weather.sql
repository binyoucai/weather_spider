CREATE DATABASE IF NOT EXISTS `weather`;
USE `weather`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for weather
-- ----------------------------
DROP TABLE IF EXISTS `weather`;
CREATE TABLE `weather` (
  `city` varchar(32) DEFAULT NULL COMMENT '城市',
  `city_code` varchar(32) NOT NULL COMMENT '城市编码',
  `ymd` date NOT NULL COMMENT '日期',
  `bWendu` int(11) DEFAULT NULL COMMENT '最高气温单位℃',
  `yWendu` int(11) DEFAULT NULL COMMENT '最低气温单位℃',
  `tianqi` varchar(64) DEFAULT NULL COMMENT '天气',
  `fengxiang` varchar(64) DEFAULT NULL COMMENT '风向',
  `fengli` varchar(64) DEFAULT NULL COMMENT '风力',
  `aqi` int(11) DEFAULT NULL COMMENT '空气质量指数',
  `aqiInfo` varchar(64) DEFAULT NULL COMMENT '空气质量等级',
  `aqiLevel` int(11) DEFAULT NULL COMMENT '空气质量水平',
  PRIMARY KEY (`city_code`,`ymd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
