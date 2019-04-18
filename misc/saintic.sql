/*
Navicat MySQL Data Transfer

Source Server         : Aliyun
Source Server Version : 50638
Source Host           : 127.0.0.1:33306
Source Database       : saintic

Target Server Type    : MYSQL
Target Server Version : 50638
File Encoding         : 65001

Date: 2019-03-28 14:37:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for blog_applyauthor
-- ----------------------------
DROP TABLE IF EXISTS `blog_applyauthor`;
CREATE TABLE `blog_applyauthor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL COMMENT '申请作者的用户名',
  `req_time` varchar(20) NOT NULL,
  `ack_time` varchar(20) DEFAULT NULL,
  `req_state` varchar(5) DEFAULT 'wait' COMMENT '初始结果wait；申请结果allow、deny',
  `isActive` int(1) NOT NULL DEFAULT '1' COMMENT '此条请求是否有效：0无效off，1有效on',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for blog_article
-- ----------------------------
DROP TABLE IF EXISTS `blog_article`;
CREATE TABLE `blog_article` (
  `id` int(4) NOT NULL AUTO_INCREMENT COMMENT 'BlogId',
  `title` varchar(88) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '文章标题',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '文章',
  `create_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '文章创建时间',
  `update_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '文章更新时间',
  `tag` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '技术' COMMENT '文章标签',
  `catalog` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '未分类' COMMENT '文章分类目录',
  `sources` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '原创' COMMENT '''Original\n,Reprint\n,Translate|原创,转载,翻译''',
  `author` varchar(255) DEFAULT 'admin',
  `recommend` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT 'false',
  `top` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT 'false',
  `comment_num` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `id` (`id`,`create_time`,`tag`,`catalog`,`sources`,`author`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for blog_catalog
-- ----------------------------
DROP TABLE IF EXISTS `blog_catalog`;
CREATE TABLE `blog_catalog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalog` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for blog_clicklog
-- ----------------------------
DROP TABLE IF EXISTS `blog_clicklog`;
CREATE TABLE `blog_clicklog` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `agent` varchar(500) COLLATE utf8_unicode_ci NOT NULL,
  `method` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  `ip` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `status_code` char(3) COLLATE utf8_unicode_ci NOT NULL,
  `referer` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `isp` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `browserType` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '浏览器终端类型，入pc mobile bot tablet',
  `browserDevice` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '浏览器设备，如pc，xiaomi，iphone',
  `browserOs` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '浏览器所在操作系统，如windows10，iPhone',
  `browserFamily` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '浏览器种类及版本，如chrome 60.0.3122',
  `clickTime` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config` (
  `about_awi` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '一句话介绍本站',
  `about_ww` varchar(140) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '站长的话',
  `about_address` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '地址',
  `about_phone` char(11) DEFAULT NULL COMMENT '手机号',
  `about_email` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '邮件',
  `about_beian` varchar(30) DEFAULT NULL,
  `seo_keywords` varchar(20) DEFAULT NULL,
  `seo_description` varchar(100) DEFAULT NULL,
  `site_title` varchar(30) DEFAULT NULL COMMENT '站点后缀标题',
  `site_feedname` varchar(15) NOT NULL DEFAULT '' COMMENT 'feed订阅源名称',
  `applet` varchar(300) DEFAULT NULL COMMENT '微信小程序码链接'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for sys_friendlink
-- ----------------------------
DROP TABLE IF EXISTS `sys_friendlink`;
CREATE TABLE `sys_friendlink` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `msg` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for novel_books
-- ----------------------------
DROP TABLE IF EXISTS `novel_books`;
CREATE TABLE `novel_books` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `book_id` char(32) NOT NULL COMMENT '书名name的md5值',
  `name` varchar(50) NOT NULL,
  `summary` varchar(300) NOT NULL,
  `cover` varchar(100) NOT NULL,
  `ctime` int(10) unsigned NOT NULL,
  `link` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for novel_chapters
-- ----------------------------
DROP TABLE IF EXISTS `novel_chapters`;
CREATE TABLE `novel_chapters` (
  `chapter_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `book_id` char(32) CHARACTER SET latin1 NOT NULL,
  `title` varchar(50) CHARACTER SET utf8 NOT NULL,
  `content` longtext CHARACTER SET utf8 NOT NULL,
  `word_count` int(11) unsigned NOT NULL DEFAULT '0',
  `ctime` int(10) unsigned NOT NULL,
  `mtime` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`chapter_id`),
  KEY `book_id` (`book_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
