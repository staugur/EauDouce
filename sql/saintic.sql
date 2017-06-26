/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : saintic

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-04-25 23:21:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for blog_article
-- ----------------------------
DROP TABLE IF EXISTS `blog_article`;
CREATE TABLE `blog_article` (
  `id` int(4) NOT NULL AUTO_INCREMENT COMMENT 'BlogId',
  `title` varchar(88) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '文章标题',
  `content` varchar(20000) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '文章',
  `create_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '文章创建时间',
  `update_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '文章更新时间',
  `tag` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '技术' COMMENT '文章标签',
  `catalog` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '未分类' COMMENT '文章分类目录',
  `sources` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '原创' COMMENT '''Original\n,Reprint\n,Translate|原创,转载,翻译''',
  `author` varchar(255) DEFAULT 'admin',
  `recommend` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT 'false',
  `top` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT 'false',
  PRIMARY KEY (`id`),
  KEY `id` (`id`,`create_time`,`tag`,`catalog`,`sources`,`author`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for blog_catalog
-- ----------------------------
DROP TABLE IF EXISTS `blog_catalog`;
CREATE TABLE `blog_catalog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalog` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for blog_clicklog
-- ----------------------------
DROP TABLE IF EXISTS `blog_clicklog`;
CREATE TABLE `blog_clicklog` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `requestId` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `agent` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `method` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ip` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `status_code` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `referer` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


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
  `seo_description` varchar(100) DEFAULT NULL
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `msg` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- ----------------------------
-- Table structure for user_lauth
-- ----------------------------
DROP TABLE IF EXISTS `user_lauth`;
CREATE TABLE `user_lauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lauth_username` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `lauth_password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`,`lauth_username`),
  UNIQUE KEY `username` (`lauth_username`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of user_lauth
-- ----------------------------
INSERT INTO `user_lauth` VALUES ('1', 'admin', '21232f297a57a5a743894a0e4a801fc3');

-- ----------------------------
-- Table structure for user_oauth
-- ----------------------------
DROP TABLE IF EXISTS `user_oauth`;
CREATE TABLE `user_oauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `oauth_username` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `oauth_type` varchar(9) COLLATE utf8_unicode_ci NOT NULL,
  `oauth_openid` varchar(41) COLLATE utf8_unicode_ci NOT NULL,
  `oauth_access_token` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `oauth_expires` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`,`oauth_username`),
  UNIQUE KEY `openid` (`oauth_openid`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of user_oauth
-- ----------------------------

-- ----------------------------
-- Table structure for user_profile
-- ----------------------------
DROP TABLE IF EXISTS `user_profile`;
CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cname` varchar(25) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cover` varchar(300) COLLATE utf8_unicode_ci DEFAULT '/static/img/bg.jpg' COMMENT '''封面''',
  `motto` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `time` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `weibo` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `github` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `extra` text COLLATE utf8_unicode_ci,
  `isAdmin` varchar(5) COLLATE utf8_unicode_ci DEFAULT 'false' COMMENT '是否为管理员',
  `isAuthor` varchar(5) COLLATE utf8_unicode_ci DEFAULT 'false' COMMENT '是否为作者',
  PRIMARY KEY (`id`,`username`),
  UNIQUE KEY `username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of user_profile
-- ----------------------------
INSERT INTO `user_profile` VALUES ('1', 'admin', 'staugur@saintic.com', '迷迷糊糊de管理员', '/static/img/upload/201704222118114355.jpg', '/static/img/upload/201704222104445935.jpg', 'Men always fight alone, always in the challenge of their own.', 'https://www.saintic.com', '2016-10-14', 'https://weibo.com/staugur', 'https://github.com/staugur', '男', 'Administrator', 'true', '0');
