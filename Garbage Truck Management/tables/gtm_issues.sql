-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: gtm
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `issues`
--

DROP TABLE IF EXISTS `issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issues` (
  `I_ID` char(4) DEFAULT NULL,
  `ADDRESS` varchar(100) DEFAULT NULL,
  `UID` char(5) DEFAULT NULL,
  `IMAGE` varchar(100) DEFAULT NULL,
  `R_DATE` date DEFAULT NULL,
  `RESOLVED` tinyint(1) DEFAULT NULL,
  `RES_DATE` date DEFAULT NULL,
  `ISSUE_NAME` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issues`
--

LOCK TABLES `issues` WRITE;
/*!40000 ALTER TABLE `issues` DISABLE KEYS */;
INSERT INTO `issues` VALUES ('I001','93/4 2nd street anna nagar ','US001','Issues_Images/garbage1.png','2025-01-19',0,NULL,'Garbage in the road'),('I002','78/2 1st street thinnappa nagar ','US003',NULL,'2025-01-19',0,NULL,'Mosquito breeding'),('I003','99/6 3rd street raja nagar ','US002','Issues_Images/garbage2.png','2025-01-13',0,NULL,'Garbage in the road'),('I004','65/6 5th street tamil nagar ','US004','Issues_Images/waterleak.png','2025-01-19',0,NULL,'Water overflow'),('I005','93/4 2nd street anna nagar ','US001','Issues_Images/waterleak.png','2025-01-16',0,NULL,'Sewage leak '),('I006','78/2 1st street thinnappa nagar ','US003','Issues_Images/garbage2.png','2025-01-19',0,NULL,'Garbage in the road'),('I007','99/6 3rd street raja nagar ','US002','Issues_Images/waterleak.png','2025-01-09',0,'2025-01-19','Water overflow'),('I008','99/6 3rd street raja nagar ','US002','NULL','2025-01-19',0,NULL,'Other Issues'),('I009','65/6 5th street tamil nagar ','US004','Issues_Images/garbage1.png','2025-01-17',0,NULL,'Garbage in the road'),('I010','93/4 2nd street anna nagar ','US001',NULL,'2025-01-17',0,'2025-01-19','Animal carcass');
/*!40000 ALTER TABLE `issues` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-19 15:15:57
