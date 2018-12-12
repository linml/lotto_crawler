/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50723
 Source Host           : localhost:3306
 Source Schema         : lotto_crawler

 Target Server Type    : MySQL
 Target Server Version : 50723
 File Encoding         : 65001

 Date: 12/12/2018 19:22:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for code_lotto
-- ----------------------------
DROP TABLE IF EXISTS `code_lotto`;
CREATE TABLE `code_lotto` (
  `lotto_id` int(11) NOT NULL COMMENT '彩票编号',
  `name` varchar(36) NOT NULL DEFAULT '' COMMENT '彩票名',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '0:禁用,1:启用',
  PRIMARY KEY (`lotto_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='彩票码表';

-- ----------------------------
-- Records of code_lotto
-- ----------------------------
BEGIN;
INSERT INTO `code_lotto` VALUES (1, '重庆时时彩', 1);
INSERT INTO `code_lotto` VALUES (2, '新疆时时彩', 1);
INSERT INTO `code_lotto` VALUES (3, '天津时时彩', 1);
INSERT INTO `code_lotto` VALUES (4, '分分彩', 1);
INSERT INTO `code_lotto` VALUES (5, '两分彩', 1);
INSERT INTO `code_lotto` VALUES (6, '三分彩', 1);
INSERT INTO `code_lotto` VALUES (7, '五分彩', 1);
INSERT INTO `code_lotto` VALUES (8, '山东11选5', 1);
INSERT INTO `code_lotto` VALUES (9, '江西11选5', 1);
INSERT INTO `code_lotto` VALUES (10, '广东11选5', 1);
INSERT INTO `code_lotto` VALUES (11, '江苏11选5', 1);
INSERT INTO `code_lotto` VALUES (12, '安徽11选5', 1);
INSERT INTO `code_lotto` VALUES (13, '山西11选5', 1);
INSERT INTO `code_lotto` VALUES (14, '上海11选5', 1);
INSERT INTO `code_lotto` VALUES (15, '分分11选5', 1);
INSERT INTO `code_lotto` VALUES (16, '江苏快3', 1);
INSERT INTO `code_lotto` VALUES (17, '安徽快3', 1);
INSERT INTO `code_lotto` VALUES (18, '湖北快3', 1);
INSERT INTO `code_lotto` VALUES (19, '河南快3', 1);
INSERT INTO `code_lotto` VALUES (20, '江苏骰宝', 1);
INSERT INTO `code_lotto` VALUES (21, '分分快3', 1);
INSERT INTO `code_lotto` VALUES (22, '北京PK10', 1);
INSERT INTO `code_lotto` VALUES (23, '幸运飞艇', 1);
INSERT INTO `code_lotto` VALUES (24, '分分PK10', 1);
INSERT INTO `code_lotto` VALUES (25, '福彩3D', 1);
INSERT INTO `code_lotto` VALUES (26, '排列3', 1);
INSERT INTO `code_lotto` VALUES (27, '排列5', 1);
INSERT INTO `code_lotto` VALUES (28, '广东快乐十分', 1);
INSERT INTO `code_lotto` VALUES (29, '重庆快乐十分', 1);
INSERT INTO `code_lotto` VALUES (30, '天津快乐十分', 1);
INSERT INTO `code_lotto` VALUES (31, '北京快乐8', 1);
INSERT INTO `code_lotto` VALUES (32, '加拿大基诺', 1);
INSERT INTO `code_lotto` VALUES (33, '分分快乐彩', 1);
INSERT INTO `code_lotto` VALUES (34, '台湾宾果', 1);
INSERT INTO `code_lotto` VALUES (35, '北京幸运28', 1);
INSERT INTO `code_lotto` VALUES (36, '加拿大幸运28', 1);
INSERT INTO `code_lotto` VALUES (37, '台湾幸运28', 1);
INSERT INTO `code_lotto` VALUES (38, '香港六合彩', 1);
INSERT INTO `code_lotto` VALUES (39, '五分六合彩', 1);
INSERT INTO `code_lotto` VALUES (40, '十分六合彩', 1);
COMMIT;

-- ----------------------------
-- Table structure for issue_factory
-- ----------------------------
DROP TABLE IF EXISTS `issue_factory`;
CREATE TABLE `issue_factory` (
  `lotto_id` int(11) NOT NULL COMMENT '彩票编号',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态',
  `count` int(11) NOT NULL DEFAULT '0' COMMENT '每日期数',
  `issue_interval` int(11) NOT NULL DEFAULT '0' COMMENT '每期间隔时间',
  `iss_bit` tinyint(1) NOT NULL DEFAULT '0',
  `block_sec` int(11) NOT NULL DEFAULT '0' COMMENT '提前封单时间(秒)',
  `start_time` varchar(6) NOT NULL DEFAULT '' COMMENT '开始销售时间',
  `end_time` varchar(6) NOT NULL DEFAULT '' COMMENT '结束销售时间',
  `issue_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '期号类型',
  `offset` int(3) NOT NULL DEFAULT '0' COMMENT '偏移时间',
  `extra_info` text NOT NULL COMMENT '额外信息',
  PRIMARY KEY (`lotto_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='彩票期号工厂';

-- ----------------------------
-- Records of issue_factory
-- ----------------------------
BEGIN;
INSERT INTO `issue_factory` VALUES (1, 1, 120, 600, 3, 0, '000000', '235959', 6, 0, '000000,015500,300|095000,220000,600|220000,235959,300');
INSERT INTO `issue_factory` VALUES (2, 1, 96, 600, 2, 90, '100000', '020000', 2, 0, ' ');
INSERT INTO `issue_factory` VALUES (3, 1, 84, 600, 3, 90, '090000', '225800', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (4, 1, 1440, 60, 4, 5, '000000', '235959', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (5, 1, 720, 120, 3, 5, '000000', '235959', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (6, 1, 480, 180, 3, 5, '000000', '235959', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (7, 1, 288, 300, 3, 5, '000000', '000000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (8, 1, 87, 600, 2, 90, '082500', '225500', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (9, 1, 84, 600, 2, 90, '090000', '230000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (10, 1, 84, 600, 2, 90, '090000', '230000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (11, 1, 82, 600, 2, 90, '082550', '220550', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (12, 1, 81, 600, 2, 90, '080000', '220000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (13, 2, 94, 600, 2, 90, '082000', '235500', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (14, 1, 90, 600, 2, 90, '085000', '235000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (15, 1, 1440, 60, 4, 5, '000000', '235959', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (16, 1, 82, 600, 3, 90, '083000', '221000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (17, 1, 80, 600, 3, 90, '084000', '220000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (18, 1, 78, 600, 3, 90, '090000', '220000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (19, 1, 84, 600, 3, 90, '083500', '223500', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (20, 1, 82, 600, 3, 90, '082000', '221000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (21, 1, 1440, 60, 4, 5, '000000', '235959', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (22, 1, 179, 300, 0, 45, '090230', '235730', 4, 0, '673722|20180329235700');
INSERT INTO `issue_factory` VALUES (23, 1, 180, 500, 3, 45, '120400', '040400', 2, 0, ' ');
INSERT INTO `issue_factory` VALUES (24, 1, 1440, 60, 4, 5, '000000', '235959', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (25, 1, 1, 85500, 3, 900, '203000', '203000', 5, 0, ' ');
INSERT INTO `issue_factory` VALUES (26, 1, 1, 85500, 3, 900, '211500', '211500', 5, 0, ' ');
INSERT INTO `issue_factory` VALUES (27, 1, 1, 85500, 3, 900, '211500', '211500', 5, 0, ' ');
INSERT INTO `issue_factory` VALUES (28, 1, 84, 600, 2, 90, '090000', '230000', 1, 0, ' ');
INSERT INTO `issue_factory` VALUES (29, 2, 97, 600, 2, 90, '', '', 6, 0, ' ');
INSERT INTO `issue_factory` VALUES (30, 1, 84, 600, 3, 90, '085500', '225500', 1, 0, ' ');
COMMIT;

-- ----------------------------
-- Table structure for lotto_parser_url
-- ----------------------------
DROP TABLE IF EXISTS `lotto_parser_url`;
CREATE TABLE `lotto_parser_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lotto_id` int(11) NOT NULL,
  `parser_obj` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(255) NOT NULL DEFAULT '',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of lotto_parser_url
-- ----------------------------
BEGIN;
INSERT INTO `lotto_parser_url` VALUES (1, 1, 'ssc_wangyi', 'http://caipiao.163.com/award/cqssc/', 1);
INSERT INTO `lotto_parser_url` VALUES (2, 25, 'fc3d_gov', 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=3d&issueCount=30', 1);
COMMIT;

-- ----------------------------
-- Procedure structure for CreateLottoIssueTable
-- ----------------------------
DROP PROCEDURE IF EXISTS `CreateLottoIssueTable`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateLottoIssueTable`(lottoID INT)
BEGIN
set @sql_create_table = concat("CREATE TABLE IF NOT EXISTS lotto_result_", lottoID,
"(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lotto_id` int(11) NOT NULL DEFAULT '0' COMMENT '彩票编号',
  `issue` varchar(32) NOT NULL DEFAULT '' COMMENT '期号',
  `draw_number` varchar(128) NOT NULL DEFAULT '' COMMENT '开奖号码',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:未开奖, 1:已开奖, 2:停止购买',
  `start_time` varchar(14) NOT NULL DEFAULT '' COMMENT '开售时间',
  `stop_time` varchar(14) NOT NULL DEFAULT '' COMMENT '封单时间',
  `result_time` varchar(14) NOT NULL DEFAULT '' COMMENT '开奖时间',
  `issue_date` varchar(8) NOT NULL COMMENT '开奖日期',
  `update_time` varchar(14) NOT NULL DEFAULT '' COMMENT '实际开奖时间',
	`crawler_from` varchar(127) NOT NULL DEFAULT '' COMMENT '采集来源',
  PRIMARY KEY (`id`),
	UNIQUE KEY `issue` (`issue`) USING BTREE,
  KEY `status` (`status`),
  KEY `issue_date_issue` (`issue_date`,`issue`) USING BTREE,
  KEY `issue_start` (`issue`,`start_time`) USING BTREE,
  KEY `issue_stop` (`issue`,`stop_time`) USING BTREE,
  KEY `issue_result` (`issue`,`result_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='彩票开奖结果';");
PREPARE sql_create_table FROM @sql_create_table;
EXECUTE sql_create_table;
END;
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
