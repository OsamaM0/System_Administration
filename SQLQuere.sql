

CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(20) NOT NULL,
  `MidName` varchar(20) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `IDCard` varchar(15) NOT NULL,
  `DOB` date NOT NULL,
  `Jop` varchar(100) NOT NULL,
  `Address` varchar(200) NOT NULL,
  `Role` varchar(50) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `Privileges` varchar(10) NOT NULL,
  `UserName` varchar(45) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `RegisterDate` date NOT NULL,
  `Rate` double DEFAULT '0',
  `email` varchar(45) DEFAULT NULL,
  `Picture` longblob,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `ID_UNIQUE` (`user_id`),
  UNIQUE KEY `UserName_UNIQUE` (`UserName`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `recever_id` int NOT NULL,
  `ReportStartDate` date NOT NULL,
  `ReportEndDate` date NOT NULL,
  `State` varchar(25) NOT NULL,
  `Importance` varchar(25) NOT NULL,
  `ReportHeadText` text NOT NULL,
  PRIMARY KEY (`report_id`),
  UNIQUE KEY `report_id_UNIQUE` (`report_id`),
  KEY `sender_id` (`sender_id`),
  KEY `recever_id` (`recever_id`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `report_ibfk_2` FOREIGN KEY (`recever_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `message` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `recever_id` int NOT NULL,
  `message_report_id` int DEFAULT NULL,
  `MessageDate` datetime NOT NULL,
  `MessageHeadText` text,
  `MessageBodyText` longblob,
  PRIMARY KEY (`message_id`),
  UNIQUE KEY `message_id_UNIQUE` (`message_id`),
  KEY `message_report_id` (`message_report_id`),
  KEY `sender_id` (`sender_id`),
  KEY `recever_id` (`recever_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`message_report_id`) REFERENCES `report` (`report_id`),
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `message_ibfk_3` FOREIGN KEY (`recever_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;







