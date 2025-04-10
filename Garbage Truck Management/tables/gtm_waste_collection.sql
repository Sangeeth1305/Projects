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
-- Table structure for table `waste_collection`
--

DROP TABLE IF EXISTS `waste_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waste_collection` (
  `st_id` varchar(4) DEFAULT NULL,
  `collected_date` date DEFAULT NULL,
  `no_of_bins` int DEFAULT NULL,
  `green_bins` int DEFAULT NULL,
  `blue_bins` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `waste_collection`
--

LOCK TABLES `waste_collection` WRITE;
/*!40000 ALTER TABLE `waste_collection` DISABLE KEYS */;
INSERT INTO `waste_collection` VALUES ('sb01','2024-04-10',2,1,1),('sb01','2024-10-25',2,1,1),('sA01','2024-11-02',10,5,5),('sB01','2024-11-09',30,15,15),('sA01','2024-11-09',34,12,5),('sB01','2024-11-11',20,16,4),('sB01','2024-11-11',20,10,10),('sA01','2024-11-28',37,25,12),('sB01','2024-11-29',40,25,15),('sA01','2024-11-29',35,25,10),('st01','2025-01-19',14,9,5),('st03','2025-01-19',13,7,6),('st02','2025-01-19',12,6,6),('st04','2025-01-19',12,8,4),('st01','2025-01-19',14,9,5),('st03','2025-01-19',13,7,6),('st02','2025-01-19',12,6,6),('st04','2025-01-19',12,8,4);
/*!40000 ALTER TABLE `waste_collection` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-19 15:15:56
