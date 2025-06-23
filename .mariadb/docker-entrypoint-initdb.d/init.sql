/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `foo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `foo`;

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `registered` datetime DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `restrictions` tinyint(4) DEFAULT NULL,
  `locked` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `user` (`id`, `username`, `password`, `email`, `registered`, `expires`, `restrictions`, `locked`) VALUES
	(1, 'John Doe', 'verysecret', 'john.doe@example.com', '2025-06-12 11:24:32', '2099-06-12 11:24:34', 0, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

-- Benutzer erstellen
CREATE USER 'foo'@'%' IDENTIFIED BY 'foo';
-- Optional: Berechtigungen gewähren
GRANT ALL PRIVILEGES ON foo.user TO 'foo'@'%' WITH GRANT OPTION;
-- Änderungen anwenden
FLUSH PRIVILEGES;

-- used by wordpress
CREATE USER 'live_user'@'%' IDENTIFIED BY 'password';
CREATE USER 'specs_user'@'%' IDENTIFIED BY 'password';
CREATE USER 'wordpress'@'%' IDENTIFIED BY 'wordpress';
CREATE USER 'supertokens'@'%' IDENTIFIED BY 'supertokens';

CREATE DATABASE IF NOT EXISTS `live`;
CREATE DATABASE IF NOT EXISTS `specs`;
CREATE DATABASE IF NOT EXISTS `wordpress`;
CREATE DATABASE IF NOT EXISTS `supertokens`;

GRANT ALL ON live.* TO 'live_user'@'%';
GRANT ALL ON specs.* TO 'specs_user'@'%';
GRANT ALL ON wordpress.* TO 'wordpress'@'%';
GRANT ALL ON supertokens.* TO 'supertokens'@'%';
FLUSH PRIVILEGES;