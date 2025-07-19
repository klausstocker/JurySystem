/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `JurySystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `JurySystem`;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `team` varchar(50) DEFAULT NULL,
  `registered` datetime DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `restrictions` tinyint(4) DEFAULT NULL,
  `locked` tinyint(4) DEFAULT NULL,
  `hidden` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users` (`id`, `username`, `password`, `email`, `team`, `registered`, `expires`, `restrictions`, `locked`, `hidden`) VALUES
	(1, 'admin', 'pass', 'john.doe@example.com', '', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 3, 0, 0),
	(2, 'host', 'pass', 'john.doe@example.com', '', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 1, 0, 0),
	(3, 'michelhausen', 'pass', 'john.doe@example.com', 'Sportunion Michelhausen', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 0, 0, 0),
	(4, 'tulln', 'pass', 'john.doe@example.com', 'Sportunion Tulln', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 0, 0, 0),
	(5, 'judge', 'pass', 'john.doe@example.com', '', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 2, 0, 0);

CREATE TABLE IF NOT EXISTS `athletes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `givenname` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `userId` int(10) unsigned NOT NULL,
  `birth` datetime DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  `hidden` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`userId`) REFERENCES users(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `athletes` (`id`, `givenname`, `surname`, `userId`, `birth`, `gender`, `hidden`) VALUES
	(1, 'Klaus', 'Stocker', 3, '1978-07-15', 0, 0),
	(2, 'Christoph', 'Hogl', 4, '1977-07-13', 0, 0),
	(3, 'Johanna', 'Stocker', 3, '2010-05-20', 1, 0),
  (4, 'Herbet', 'Mayer', 4, '2010-05-20', 0, 0);

CREATE TABLE IF NOT EXISTS `events` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `userId` int(10) unsigned NOT NULL,
  `date` datetime NOT NULL,
  `progress` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`userId`) REFERENCES users(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `events` (`id`, `name`, `userId`, `date`, `progress`) VALUES
  (1, 'Bezirksmeisterschaften 2025', 2, '2025-05-28', 0);

CREATE TABLE IF NOT EXISTS `event_judges` (
  `eventId` int(10) unsigned NOT NULL,
  `userId` int(10) unsigned NOT NULL,
  PRIMARY KEY (`eventId`, `userId`),
  FOREIGN KEY (`eventId`) REFERENCES events(`id`),
  FOREIGN KEY (`userId`) REFERENCES users(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `event_judges` (`eventId`, `userId`) VALUES
  (1, 5);

CREATE TABLE IF NOT EXISTS `event_categories` (
  `name` varchar(50) NOT NULL,
  `eventId` int(10) unsigned NOT NULL,
  `gender` tinyint(4) NOT NULL,
  `birthFrom` datetime NOT NULL,
  `birthTo` datetime NOT NULL,
  `rankingType` tinyint(4),
  PRIMARY KEY (`name`, `eventId`),
  FOREIGN KEY (`eventId`) REFERENCES events(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `event_categories` (`name`, `eventId`, `gender`, `birthFrom`, `birthTo`, `rankingType`) VALUES
  ('Kn01', 1, 0, '2020-01-01', '2021-12-31', 0),
  ('Md01', 1, 1, '2020-01-01', '2021-12-31', 0);

CREATE TABLE IF NOT EXISTS `event_disciplines` (
  `name` varchar(50) NOT NULL,
  `eventId` int(10) unsigned NOT NULL,
  PRIMARY KEY (`name`, `eventId`),
  FOREIGN KEY (`eventId`) REFERENCES events(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `event_disciplines` (`name`, `eventId`) VALUES
  ('Reck', 1),
  ('Boden', 1),
  ('Sprung', 1),
  ('Barren/Balken', 1);

CREATE TABLE IF NOT EXISTS `attendances` (
  `athleteId` int(10) unsigned NOT NULL,
  `eventId` int(10) unsigned NOT NULL,
  `eventCategoryName` varchar(50) NOT NULL,
  `group` varchar(50) NOT NULL,
  PRIMARY KEY (`athleteId`, `eventId`, `eventCategoryName`),
  FOREIGN KEY (`eventId`) REFERENCES events(`id`),
  FOREIGN KEY (`athleteId`) REFERENCES athletes(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `attendances` (`athleteId`, `eventId`, `eventCategoryName`, `group`) VALUES
  (1, 1, 'Kn01', 'Riege1'),
  (2, 1, 'Kn01', 'Riege1'),
  (3, 1, 'Md01', 'Riege2');

CREATE TABLE IF NOT EXISTS `ratings` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `athleteId` int(10) unsigned NOT NULL,
  `eventDisciplineName` varchar(50) NOT NULL,
  `eventId` int(10) unsigned NOT NULL,
  `userId` int(10) unsigned NOT NULL,
  `difficulty` decimal(8,4) NOT NULL,
  `execution` decimal(8,4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`athleteId`, `eventId`, `eventDisciplineName`),
  FOREIGN KEY (`eventId`) REFERENCES events(`id`),
  FOREIGN KEY (`athleteId`) REFERENCES athletes(`id`),
  FOREIGN KEY (`userId`) REFERENCES users(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `ratings` (`id`, `athleteId`, `eventDisciplineName`, `eventId`, `userId`, `difficulty`, `execution`) VALUES
  (1, 1, 'Reck', 1, 5, 6.7, 2.0),
  (2, 2, 'Reck', 1, 5, 5.7, 1.0),
  (3, 1, 'Boden', 1, 5, 4.0, 2.0);


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

-- Benutzer erstellen
CREATE USER 'JurySystem'@'%' IDENTIFIED BY 'asdfuas347lkasudhr';
-- Optional: Berechtigungen gewähren
GRANT ALL PRIVILEGES ON `JurySystem`.* TO 'JurySystem'@'%' WITH GRANT OPTION;
-- Änderungen anwenden
FLUSH PRIVILEGES;

