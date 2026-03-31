-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: quiz_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `attempts`
--

DROP TABLE IF EXISTS `attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attempts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `quiz_id` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  `total_questions` int DEFAULT NULL,
  `attempted_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attempts`
--

LOCK TABLES `attempts` WRITE;
/*!40000 ALTER TABLE `attempts` DISABLE KEYS */;
INSERT INTO `attempts` VALUES (1,2,2,0,2,'2026-02-12 06:16:21'),(2,2,2,2,2,'2026-03-14 05:32:07'),(3,3,1,7,8,'2026-03-14 06:59:24'),(4,4,1,6,8,'2026-03-14 07:57:55'),(5,5,3,1,7,'2026-03-16 13:51:30'),(6,5,3,1,7,'2026-03-17 06:00:26');
/*!40000 ALTER TABLE `attempts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'General Knowledge','active'),(2,'Programming','active'),(3,'Science','active'),(4,'Sports ','active'),(5,'General Science','active');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quiz_id` int DEFAULT NULL,
  `question_text` text NOT NULL,
  `option_a` varchar(200) DEFAULT NULL,
  `option_b` varchar(200) DEFAULT NULL,
  `option_c` varchar(200) DEFAULT NULL,
  `option_d` varchar(200) DEFAULT NULL,
  `correct_option` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,1,'What is the capital of India?','Mumbai','Delhi','Kolkata','Chennai','B'),(2,1,'Who is the President of India?','Modi','Murmu','Kovind','Gandhi','B'),(3,2,'Which keyword is used to define a function in Python?','func','define','def','function','C'),(4,2,'Which data type is immutable in Python?','List','Set','Dictionary','Tuple','D'),(5,1,'Who is known as the father of the nation in india.?','Jawaharlal Neharu','Mahatma Gandhi','Bhagat Singh','Subhash Chandra Bhos','B'),(6,1,'Where is the Taj Mahal Located','Delhi','Agra','Jaipur','Mumbai','B'),(7,1,'Which is the largest planet in the solar system?','Earth ','Marse','Jupiter','Venus','C'),(8,1,'How many states are there in india?','26','27','28','29','C'),(9,1,'Which article of the Indian Constitution gives right to Equality?','Article 14','Article 19','Article 21','Article 32','A'),(10,1,'Which is the longest river in India?','Yamuna ','Ganga','Godavari','Brahmaputra','B'),(11,2,'Which data type is immutable in python?','List','Dictionary','Tuple','set','C'),(12,2,'Which operator is used for exponentiation in python?','^','**','*','//','B'),(13,2,'Which data structure does not allow duplicate values?','List','Tuple ','set ','Dictionary','C'),(14,2,'Which keyword is used for loop in Python ?','For ','Repeat','Loop','Iterate','A'),(15,2,'Which function converts string to integer?','str()','int()','float()','number()','B'),(16,3,'Which country hosted the first modern Olympic Games in 1896?','France','Greece','USA','Germany','B'),(17,3,'Which country won the first Cricket World Cup in 1975?','India','Australia','West Indies','England','C'),(18,3,'In which sport is the term \"LOVE\" used?','Badminton ','Tennis','Table Tennis ','Squash','B'),(19,3,'Which country has won the most FIFA World Cups?\r\n','Germany','Brazil','Argentina','Italy','B'),(20,3,'What is the national sport of India','Cricket','Hockey','Football','Kabbaddi','B'),(21,3,'How many rings are there in  Olympic symbol?','4','5','6','7','B'),(22,3,'Which country hosted the 2016 Summer Olympics','china','Brazil','Japan','Uk','B');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizzes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `time_limit` int DEFAULT '10',
  `total_marks` int DEFAULT '10',
  `status` enum('active','inactive') DEFAULT 'active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
INSERT INTO `quizzes` VALUES (1,1,'GK Basic Quiz',10,10,'active'),(2,2,'Python Basics Quiz',10,10,'active'),(3,4,'All  about sports quize',5,10,'active');
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','student') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Admin','admin@quiz.com','admin1234','admin','2026-01-03 06:21:20'),(3,'Vaishnavi Satappa Chougale','vaishnavichougale196@gmail.com','@Vaishnavi3024','student','2026-03-14 06:52:56'),(4,'gayatri shinde','gayatrishinde81151@gmail.com','admin1234','student','2026-03-14 07:56:29'),(5,'Prachi patil','pp4878792@gmail.com','@prachi123213','student','2026-03-16 13:49:22');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-31 14:12:45
