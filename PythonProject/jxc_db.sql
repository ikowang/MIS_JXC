/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50620
Source Host           : localhost:3306
Source Database       : jxc_db

Target Server Type    : MYSQL
Target Server Version : 50620
File Encoding         : 65001

Date: 2019-09-20 13:05:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `t_admin`
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin` (
  `username` varchar(20) NOT NULL DEFAULT '',
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES ('a', 'a');

-- ----------------------------
-- Table structure for `t_buyinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_buyinfo`;
CREATE TABLE `t_buyinfo` (
  `buyId` int(11) NOT NULL AUTO_INCREMENT COMMENT '进货编号',
  `productObj` varchar(20) NOT NULL COMMENT '进货产品',
  `buyDate` varchar(20) DEFAULT NULL COMMENT '进货日期',
  `price` varchar(20) NOT NULL COMMENT '进货单价',
  `count` int(11) NOT NULL COMMENT '进货数量',
  `supplyerObj` int(11) NOT NULL COMMENT '供应商',
  `personName` varchar(20) DEFAULT NULL COMMENT '负责人',
  PRIMARY KEY (`buyId`),
  KEY `productObj` (`productObj`),
  KEY `supplyerObj` (`supplyerObj`),
  CONSTRAINT `t_buyinfo_ibfk_1` FOREIGN KEY (`productObj`) REFERENCES `t_productinfo` (`productNo`),
  CONSTRAINT `t_buyinfo_ibfk_2` FOREIGN KEY (`supplyerObj`) REFERENCES `t_supplyer` (`supplyerId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_buyinfo
-- ----------------------------
INSERT INTO `t_buyinfo` VALUES ('1', 'SP001', '2019-09-19', '50', '10', '2', '李明阳');
INSERT INTO `t_buyinfo` VALUES ('2', 'SP002', '2019-09-18', '300', '5', '1', '刘国光');

-- ----------------------------
-- Table structure for `t_customerinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_customerinfo`;
CREATE TABLE `t_customerinfo` (
  `customerId` int(11) NOT NULL AUTO_INCREMENT COMMENT '客户编号',
  `customerName` varchar(20) NOT NULL COMMENT '客户名称',
  `personName` varchar(20) DEFAULT NULL COMMENT '联系人',
  `telephone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `address` varchar(20) DEFAULT NULL COMMENT '联系地址',
  PRIMARY KEY (`customerId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_customerinfo
-- ----------------------------
INSERT INTO `t_customerinfo` VALUES ('1', '小明电脑配件店', '李晓明', '18310931234', '成都二仙桥11号');
INSERT INTO `t_customerinfo` VALUES ('2', '牛哥哥火锅店', '牛达成', '15208421249', '成都十里店20号');

-- ----------------------------
-- Table structure for `t_productclass`
-- ----------------------------
DROP TABLE IF EXISTS `t_productclass`;
CREATE TABLE `t_productclass` (
  `productClassId` int(11) NOT NULL AUTO_INCREMENT COMMENT '商品类别编号',
  `productClassName` varchar(20) NOT NULL COMMENT '商品类别名称',
  PRIMARY KEY (`productClassId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_productclass
-- ----------------------------
INSERT INTO `t_productclass` VALUES ('1', '电子产品类');
INSERT INTO `t_productclass` VALUES ('2', '厨房家具类');

-- ----------------------------
-- Table structure for `t_productinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_productinfo`;
CREATE TABLE `t_productinfo` (
  `productNo` varchar(20) NOT NULL COMMENT 'productNo',
  `productClass` int(11) NOT NULL COMMENT '产品类别',
  `productName` varchar(20) NOT NULL COMMENT '产品名称',
  `productPhoto` varchar(60) NOT NULL COMMENT '产品图片',
  `price` float NOT NULL COMMENT '产品单价',
  `leftCount` int(11) NOT NULL COMMENT '产品库存',
  `madeDate` varchar(20) DEFAULT NULL COMMENT '生产日期',
  `productDesc` varchar(8000) NOT NULL COMMENT '产品描述',
  PRIMARY KEY (`productNo`),
  KEY `productClass` (`productClass`),
  CONSTRAINT `t_productinfo_ibfk_1` FOREIGN KEY (`productClass`) REFERENCES `t_productclass` (`productClassId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_productinfo
-- ----------------------------
INSERT INTO `t_productinfo` VALUES ('SP001', '1', '金士顿U盘', 'img/1.jpg', '68', '30', '2019-09-09', '<p class=\"attr-list-hd tm-clear\" style=\"margin: 0px; padding: 5px 20px; line-height: 22px; color: #999999; font-family: tahoma, arial, 微软雅黑, sans-serif; font-size: 12px;\" data-spm-anchor-id=\"a220o.1000855.0.i0.4f201wJI1wJIu1\">&nbsp;</p>\r\n<ul id=\"J_AttrUL\" style=\"margin: 0px; padding: 0px 20px 18px; list-style: none; zoom: 1; border-top: 1px solid #ffffff; color: #404040; font-family: tahoma, arial, 微软雅黑, sans-serif; font-size: 12px;\">\r\n<li id=\"J_attrBrandName\" style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;Kingston/金士顿\" data-spm-anchor-id=\"a220o.1000855.0.i1.4f201wJI1wJIu1\">品牌:&nbsp;Kingston/金士顿</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;DT100G3(32G)\">金士顿型号:&nbsp;DT100G3(32G)</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;32GB\">闪存容量:&nbsp;32GB</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;全新\">成色:&nbsp;全新</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;全国联保\">售后服务:&nbsp;全国联保</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;DT100G3-32G&nbsp;DT100G3-32G+Type-c转接头&nbsp;DT100G3-32G+紫米苹果转3.5耳机转接头&nbsp;DT100G3-32G+睿志3.0集线器&nbsp;DT100G3-32G+睿志2.0集线器&nbsp;DT100G3-32G+紫米Type-c转接线&nbsp;DT100G3-32G+安卓转接头&nbsp;DT100G3-32G+充电头&nbsp;DT100G3-32G+二合一数据线&nbsp;DT100G3-32G+紫米Type-c转苹果数据线&nbsp;DT100G3-32G+苹果数据线&nbsp;DT100G3-32G+手机支架\">颜色分类:&nbsp;DT100G3-32G&nbsp;DT100G3-32G+Type-c转接头&nbsp;DT100G3-32G+紫米苹果转3.5耳机转接头&nbsp;DT100G3-32G+睿志3.0集线器&nbsp;DT100G3-32G+睿志2.0集线器&nbsp;DT100G3-32G+紫米Type-c转接线&nbsp;DT100G3-32G+安卓转接头&nbsp;DT100G3-32G+充电头&nbsp;DT100G3-32G+二合一数据线&nbsp;DT100G3-32G+紫米Type-c转苹果数据线&nbsp;DT100G3-32G+苹果数据线&nbsp;DT100G3-32G+手机支架</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;套餐一\">套餐类型:&nbsp;套餐一</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;金士顿科技公司\">生产企业:&nbsp;金士顿科技公司</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;USB3.0\">USB类型:&nbsp;USB3.0</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;支持\">是否支持防伪查询:&nbsp;支持</li>\r\n</ul>');
INSERT INTO `t_productinfo` VALUES ('SP002', '2', '苏泊尔电饭煲', 'img/2.jpg', '359', '20', '2019-09-05', '<ul id=\"J_AttrUL\" style=\"margin: 0px; padding: 0px 20px 18px; list-style: none; zoom: 1; border-top: 1px solid #ffffff; color: #404040; font-family: tahoma, arial, 微软雅黑, sans-serif; font-size: 15px;\">\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"2013010718646628\" data-spm-anchor-id=\"a220o.1000855.0.i0.3a7bIj13Ij1381\">证书编号：2013010718646628</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"有效\">证书状态：有效</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"浙江苏泊尔家电制造有限公司\">申请人名称：浙江苏泊尔家电制造有限公司</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"浙江苏泊尔家电制造有限公司\">制造商名称：浙江苏泊尔家电制造有限公司</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"豪华智能电饭煲\">产品名称：豪华智能电饭煲</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"CFXB30FZ16Q-60 3.0L 600W; CFXB40FZ16Q-75, CFXB40FC...\">3C产品型号：CFXB30FZ16Q-60 3.0L 600W; CFXB40FZ16Q-75, CFXB40FC...</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"见附件\">3C规格型号：见附件</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"SUPOR/苏泊尔 CFXB40FC8155-75\">产品名称：SUPOR/苏泊尔 CFXB40FC81...</li>\r\n<li id=\"J_attrBrandName\" style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;SUPOR/苏泊尔\">品牌:&nbsp;SUPOR/苏泊尔</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;CFXB40FC8155-75\">型号:&nbsp;CFXB40FC8155-75</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;快速饭&nbsp;柴火饭&nbsp;煮粥&nbsp;煮饭\">电饭煲多功能:&nbsp;快速饭&nbsp;柴火饭&nbsp;煮粥&nbsp;煮饭</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;釜胆\">内胆材质:&nbsp;釜胆</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;4L\">容量:&nbsp;4L</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;方形\">形状:&nbsp;方形</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;全国联保\">售后服务:&nbsp;全国联保</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;3人-4人\">适用人数:&nbsp;3人-4人</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;摩卡棕\">颜色分类:&nbsp;摩卡棕</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;微电脑式\">控制方式:&nbsp;微电脑式</li>\r\n<li style=\"margin: 10px 15px 0px 0px; padding: 0px; list-style: none; display: inline; float: left; width: 220px; height: 18px; overflow: hidden; line-height: 18px; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; color: #666666;\" title=\"&nbsp;底盘加热\">加热方式:&nbsp;底盘加热</li>\r\n</ul>');

-- ----------------------------
-- Table structure for `t_sellinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_sellinfo`;
CREATE TABLE `t_sellinfo` (
  `sellId` int(11) NOT NULL AUTO_INCREMENT COMMENT '销售编号',
  `productObj` varchar(20) NOT NULL COMMENT '销售产品',
  `sellDate` varchar(20) DEFAULT NULL COMMENT '销售日期',
  `price` float NOT NULL COMMENT '销售价格',
  `count` int(11) NOT NULL COMMENT '销售数量',
  `customerObj` int(11) NOT NULL COMMENT '销售客户',
  `personName` varchar(20) NOT NULL COMMENT '销售负责人',
  PRIMARY KEY (`sellId`),
  KEY `productObj` (`productObj`),
  KEY `customerObj` (`customerObj`),
  CONSTRAINT `t_sellinfo_ibfk_1` FOREIGN KEY (`productObj`) REFERENCES `t_productinfo` (`productNo`),
  CONSTRAINT `t_sellinfo_ibfk_2` FOREIGN KEY (`customerObj`) REFERENCES `t_customerinfo` (`customerId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_sellinfo
-- ----------------------------
INSERT INTO `t_sellinfo` VALUES ('1', 'SP001', '2019-09-20', '80', '10', '1', '邓开拓');
INSERT INTO `t_sellinfo` VALUES ('2', 'SP002', '2019-09-15', '399', '2', '2', '王明贵');

-- ----------------------------
-- Table structure for `t_supplyer`
-- ----------------------------
DROP TABLE IF EXISTS `t_supplyer`;
CREATE TABLE `t_supplyer` (
  `supplyerId` int(11) NOT NULL AUTO_INCREMENT COMMENT '供应商编号',
  `supplyerName` varchar(20) NOT NULL COMMENT '供应商名称',
  `telephone` varchar(20) DEFAULT NULL COMMENT '供应商电话',
  `personName` varchar(20) DEFAULT NULL COMMENT '联系人',
  `address` varchar(20) DEFAULT NULL COMMENT '供应商地址',
  PRIMARY KEY (`supplyerId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_supplyer
-- ----------------------------
INSERT INTO `t_supplyer` VALUES ('1', '成都小花厨具公司', '13980812934', '刘小花', '成都春熙路25号');
INSERT INTO `t_supplyer` VALUES ('2', '成都大华电子供应商', '13590812342', '谢大华', '成都五块石汽车站');
