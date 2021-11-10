-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: green_project_bd
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `avance`
--

DROP TABLE IF EXISTS `avance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `avance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url_imagen` text NOT NULL,
  `titulo_avance` varchar(80) NOT NULL,
  `descripcion_avance` text NOT NULL,
  `id_proyecto` bigint NOT NULL,
  `fecha_avance` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_idx` (`id_proyecto`),
  CONSTRAINT `id` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avance`
--

LOCK TABLES `avance` WRITE;
/*!40000 ALTER TABLE `avance` DISABLE KEYS */;
/*!40000 ALTER TABLE `avance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donacion_monetaria`
--

DROP TABLE IF EXISTS `donacion_monetaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donacion_monetaria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `correo_usuario` varchar(100) NOT NULL,
  `id_proyecto` bigint NOT NULL,
  `cantidad_donacion` double NOT NULL,
  `fecha_realizada` datetime NOT NULL,
  `numero_autorizacion` bigint NOT NULL,
  `moneda` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `correo_electronico_idx` (`correo_usuario`),
  KEY `id_proyecto_idx` (`id_proyecto`),
  CONSTRAINT `correo_usuario_monetaria` FOREIGN KEY (`correo_usuario`) REFERENCES `usuario` (`correo_electronico`),
  CONSTRAINT `id_proyecto_monetaria` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donacion_monetaria`
--

LOCK TABLES `donacion_monetaria` WRITE;
/*!40000 ALTER TABLE `donacion_monetaria` DISABLE KEYS */;
/*!40000 ALTER TABLE `donacion_monetaria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donacion_recurso`
--

DROP TABLE IF EXISTS `donacion_recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donacion_recurso` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `correo_usuario` varchar(100) NOT NULL,
  `id_recurso` bigint NOT NULL,
  `cantidad_recurso` int NOT NULL,
  `fecha_donativo` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `correo_usuaro_idx` (`correo_usuario`),
  KEY `id_recurso_idx` (`id_recurso`),
  CONSTRAINT `correo_usuario_donacion` FOREIGN KEY (`correo_usuario`) REFERENCES `usuario` (`correo_electronico`),
  CONSTRAINT `id_recurso_donacion` FOREIGN KEY (`id_recurso`) REFERENCES `recurso` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donacion_recurso`
--

LOCK TABLES `donacion_recurso` WRITE;
/*!40000 ALTER TABLE `donacion_recurso` DISABLE KEYS */;
/*!40000 ALTER TABLE `donacion_recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participante_proyecto`
--

DROP TABLE IF EXISTS `participante_proyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participante_proyecto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `correo_usuario` varchar(100) NOT NULL,
  `id_perfil` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `correo_usuario_idx` (`correo_usuario`),
  KEY `id_perfil_idx` (`id_perfil`),
  CONSTRAINT `correo_usuario_participante` FOREIGN KEY (`correo_usuario`) REFERENCES `usuario` (`correo_electronico`),
  CONSTRAINT `id_perfil` FOREIGN KEY (`id_perfil`) REFERENCES `perfil` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participante_proyecto`
--

LOCK TABLES `participante_proyecto` WRITE;
/*!40000 ALTER TABLE `participante_proyecto` DISABLE KEYS */;
/*!40000 ALTER TABLE `participante_proyecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfil`
--

DROP TABLE IF EXISTS `perfil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perfil` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_perfil` varchar(200) NOT NULL,
  `cantidad_participantes` int NOT NULL,
  `id_proyecto` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_proyecto_idx` (`id_proyecto`),
  CONSTRAINT `id_proyecto_perfil` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfil`
--

LOCK TABLES `perfil` WRITE;
/*!40000 ALTER TABLE `perfil` DISABLE KEYS */;
/*!40000 ALTER TABLE `perfil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proyecto`
--

DROP TABLE IF EXISTS `proyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proyecto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_proyecto` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `justificacion` text NOT NULL,
  `objetivos` text NOT NULL,
  `impacto` varchar(100) NOT NULL,
  `alineacion_ods` varchar(100) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `fecha_finalizacion` datetime NOT NULL,
  `estado` varchar(20) NOT NULL,
  `tipo_proyecto` varchar(50) NOT NULL,
  `url_video` text NOT NULL,
  `url_imagen` text NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `donacion_requerida` double NOT NULL,
  `perfil_colaborador` varchar(100) NOT NULL,
  `correo_electronico` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `correo_electronico_idx` (`correo_electronico`),
  CONSTRAINT `correo_electronico` FOREIGN KEY (`correo_electronico`) REFERENCES `usuario` (`correo_electronico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proyecto`
--

LOCK TABLES `proyecto` WRITE;
/*!40000 ALTER TABLE `proyecto` DISABLE KEYS */;
/*!40000 ALTER TABLE `proyecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recurso`
--

DROP TABLE IF EXISTS `recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recurso` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_recurso` varchar(50) NOT NULL,
  `cantidad_recurso` int NOT NULL,
  `id_proyecto` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_proyecto_idx` (`id_proyecto`),
  CONSTRAINT `id_proyecto_recurso` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recurso`
--

LOCK TABLES `recurso` WRITE;
/*!40000 ALTER TABLE `recurso` DISABLE KEYS */;
/*!40000 ALTER TABLE `recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `correo_electronico` varchar(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` int NOT NULL,
  `sexo` varchar(20) NOT NULL,
  `tipo_usuario` varchar(50) NOT NULL,
  `identificacion` varchar(20) NOT NULL,
  `direccion_residencia` varchar(100) NOT NULL,
  `ocupacion` varchar(100) NOT NULL,
  `numero_telefonico` varchar(20) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `estado_usuario` tinyint NOT NULL,
  `nacionalidad` varchar(50) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  PRIMARY KEY (`correo_electronico`),
  UNIQUE KEY `correo_electronico_UNIQUE` (`correo_electronico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES ('julian.nunez@correo.edu.co','Julian','Nuñez',12,'124','Proponente','1234','KR 24B Oeste # 2 - 61    | KR 24B OESTE 2 61 |','1234','+573003420459','$2b$12$Ubk056uVAyTAwfW51Gm58ut1za/9ZrhvAcrWlTwVvEZ8ClQ5Bf9ey','2021-11-10 17:07:13',1,'1234','1243');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-10 17:25:57
