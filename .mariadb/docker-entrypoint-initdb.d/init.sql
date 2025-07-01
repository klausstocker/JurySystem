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
  PRIMARY KEY (`id`),
  UNIQUE (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users` (`id`, `username`, `password`, `email`, `team`, `registered`, `expires`, `restrictions`, `locked`) VALUES
	(1, 'admin', 'pass', 'john.doe@example.com', '', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 1, 0),
	(2, 'michelhausen', 'pass', 'john.doe@example.com', 'Sportunion Michelhausen', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 0, 0),
	(3, 'tulln', 'pass', 'john.doe@example.com', 'Sportunion Tulln', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 0, 0);

CREATE TABLE IF NOT EXISTS `athletes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `givenname` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `userId` int(10) unsigned NOT NULL,
  `birth` datetime DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `athletes` (`id`, `givenname`, `surname`, `userId`, `birth`, `gender`) VALUES
	(1, 'Klaus', 'Stocker', 2, '1978-07-15', 0),
	(2, 'Christoph', 'Hogl', 3, '1977-07-13', 0),
	(3, 'Johanna', 'Stocker', 2, '2010-05-20', 1);

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

