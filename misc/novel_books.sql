/*
Navicat MySQL Data Transfer

Source Server         : wsl
Source Server Version : 50724
Source Host           : localhost:3306
Source Database       : saintic

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2019-04-16 10:31:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for novel_books
-- ----------------------------
DROP TABLE IF EXISTS `novel_books`;
CREATE TABLE `novel_books` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `book_id` char(32) CHARACTER SET utf8 NOT NULL COMMENT '书名name的md5值',
  `name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `summary` varchar(300) CHARACTER SET utf8 NOT NULL,
  `cover` varchar(100) CHARACTER SET utf8 NOT NULL,
  `ctime` int(10) unsigned NOT NULL,
  `link` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of novel_books
-- ----------------------------
INSERT INTO `novel_books` VALUES ('1', '7b0fdf127ced366001bb939e8f36e1e5', '仙反', '混沌未分天地乱，茫茫渺渺无人见。自从先圣破鸿蒙，开辟从兹清浊辨。', 'https://static.saintic.com/novel/xianfan_cover.jpg', '1555510260', '');

-- ----------------------------
-- Table structure for novel_chapters
-- ----------------------------
DROP TABLE IF EXISTS `novel_chapters`;
CREATE TABLE `novel_chapters` (
  `chapter_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `book_id` char(32) NOT NULL,
  `title` varchar(50) CHARACTER SET utf8 NOT NULL,
  `content` longtext CHARACTER SET utf8 NOT NULL,
  `word_count` int(11) unsigned NOT NULL DEFAULT '0',
  `ctime` int(10) unsigned NOT NULL,
  `mtime` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`chapter_id`),
  KEY `book_id` (`book_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
