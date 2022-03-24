/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 10.4.22-MariaDB : Database - fakeimage
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`fakeimage` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `fakeimage`;

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`) values 
(1,'shibla','shibla'),
(2,'shahushibu05@gmail.com','yami'),
(3,'shahushibu05@gmail.com','return'),
(4,'shahushibu05@gmail.com','who are you'),
(5,'shahushibu05@gmail.com','984789'),
(6,'shahushibu05@gmail.com','shibla@98'),
(7,'drishya@1213@gmail.com','123456789'),
(8,'admin@gmail.com','admin');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pin` int(10) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `phoneno` bigint(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

insert  into `user`(`user_id`,`username`,`gender`,`place`,`post`,`pin`,`photo`,`phoneno`,`email`) values 
(2,'Shibla nasreen','female','0','ponnani',669577,'/static/photo/220309-103128.jpg',61031233,'shahushibu05@gmail.com'),
(3,'Shibla nasreen','female','ponnani','ponnani',679583,'/static/photo/220309-105925.jpg',2147483647,'shahushibu05@gmail.com'),
(4,'shibla','femal','ponnani','ponnani',679583,'/static/photo/220311-085952.jpg',9061031233,'shahushibu05@gmail.com'),
(5,'Shibla nasreen mv','femal','ponnani','ponnani',679583,'/static/photo/220315-163632.jpg',9061031233,'shahushibu05@gmail.com'),
(6,'Shibla nasreen mv','femal','ponnani','ponnani',679583,'/static/photo/220315-163659.jpg',9061031233,'shahushibu05@gmail.com'),
(7,'shahul','male','ponnani','ponnani',679583,'/static/photo/220316-102746.jpg',9847899551,'drishya@1213@gmail.com'),
(8,'aaaaa','femal','yyyyy','kkdsork',679577,'/static/photo/220317-090907.jpg',98478995551,'admin@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
