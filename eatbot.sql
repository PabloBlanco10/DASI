-- MySQL dump 10.13  Distrib 5.7.22, for osx10.13 (x86_64)
--
-- Host: localhost    Database: eatbot
-- ------------------------------------------------------
-- Server version	5.7.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Pedido`
--

DROP TABLE IF EXISTS `Pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pedido` (
  `idPedido` int(11) NOT NULL AUTO_INCREMENT,
  `idUsuario` int(11) DEFAULT NULL,
  `idRestaurante` int(11) DEFAULT NULL,
  `opinion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `idRestaurante` (`idRestaurante`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idRestaurante`) REFERENCES `Restaurante` (`idRestaurante`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `Usuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pedido`
--

LOCK TABLES `Pedido` WRITE;
/*!40000 ALTER TABLE `Pedido` DISABLE KEYS */;
INSERT INTO `Pedido` VALUES (1,262982572,11,NULL),(2,262982572,12,NULL);
/*!40000 ALTER TABLE `Pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PedidoProducto`
--

DROP TABLE IF EXISTS `PedidoProducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PedidoProducto` (
  `idPedido` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  PRIMARY KEY (`idPedido`,`idProducto`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `pedidoproducto_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `Pedido` (`idPedido`),
  CONSTRAINT `pedidoproducto_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `Producto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PedidoProducto`
--

LOCK TABLES `PedidoProducto` WRITE;
/*!40000 ALTER TABLE `PedidoProducto` DISABLE KEYS */;
INSERT INTO `PedidoProducto` VALUES (1,17),(1,19),(2,36),(2,37);
/*!40000 ALTER TABLE `PedidoProducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Producto`
--

DROP TABLE IF EXISTS `Producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Producto` (
  `idProducto` int(11) NOT NULL AUTO_INCREMENT,
  `nombreProducto` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idProducto`),
  UNIQUE KEY `nombreProducto` (`nombreProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Producto`
--

LOCK TABLES `Producto` WRITE;
/*!40000 ALTER TABLE `Producto` DISABLE KEYS */;
INSERT INTO `Producto` VALUES (28,'American Wings'),(17,'Aros de Cebolla'),(9,'Arroz Tres Delicias'),(2,'Calzone'),(26,'Cocido'),(19,'Costillas'),(35,'Croquetas'),(21,'Durum Cordero'),(12,'Falafel'),(15,'Fideos Fritos'),(20,'Fingers Pollo'),(23,'Gazpacho'),(10,'Gyozas'),(16,'Hamburguesa Queso'),(11,'Kebab'),(34,'Maki de Aguacate'),(36,'Morcilla'),(22,'Noodles Pollo'),(37,'Paella'),(6,'Pasta alfredo'),(4,'Pasta carbonara'),(13,'Patatas fritas'),(1,'Pizza bolognesa'),(3,'Pizza hawaiana'),(7,'Pizza mozzarella'),(5,'Pizza napolitana'),(8,'Pizza prosciutto'),(33,'Pollo al Curry'),(32,'Pollo al limon'),(25,'Ramen'),(29,'Rollito primavera'),(14,'Shushi'),(30,'Tallarines'),(27,'Teppanyaki'),(31,'Ternera Bambu'),(18,'Tortilla de Patata'),(24,'Waygu');
/*!40000 ALTER TABLE `Producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Restaurante`
--

DROP TABLE IF EXISTS `Restaurante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Restaurante` (
  `idRestaurante` int(11) NOT NULL AUTO_INCREMENT,
  `nombreRestaurante` varchar(100) DEFAULT NULL,
  `tipoRestaurante` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idRestaurante`),
  UNIQUE KEY `nombreRestaurante` (`nombreRestaurante`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Restaurante`
--

LOCK TABLES `Restaurante` WRITE;
/*!40000 ALTER TABLE `Restaurante` DISABLE KEYS */;
INSERT INTO `Restaurante` VALUES (1,'Yhu Yughae','china'),(2,'La Tagliatella','italiana'),(3,'La mafia','italiana'),(4,'Doner Valdebebas','turca'),(5,'Doner Bernabeu','turca'),(6,'Korean Style','coreana'),(7,'Nyu Jao','japonesa'),(8,'Fosters','americana'),(9,'Casa Jose','española'),(10,'Mcdonals','americana'),(11,'Grill Texas','americana'),(12,'Casa Marisa','española'),(13,'Yahi Moen','coreana'),(14,'Udon','japonesa'),(15,'Yakimi Nei','china');
/*!40000 ALTER TABLE `Restaurante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RestauranteProducto`
--

DROP TABLE IF EXISTS `RestauranteProducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RestauranteProducto` (
  `idRestaurante` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  PRIMARY KEY (`idRestaurante`,`idProducto`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `restauranteproducto_ibfk_1` FOREIGN KEY (`idRestaurante`) REFERENCES `Restaurante` (`idRestaurante`),
  CONSTRAINT `restauranteproducto_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `Producto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RestauranteProducto`
--

LOCK TABLES `RestauranteProducto` WRITE;
/*!40000 ALTER TABLE `RestauranteProducto` DISABLE KEYS */;
INSERT INTO `RestauranteProducto` VALUES (2,2),(3,2),(2,4),(3,5),(2,6),(1,9),(6,9),(7,9),(1,10),(2,10),(14,10),(4,11),(5,11),(4,12),(5,13),(10,13),(6,14),(7,15),(8,16),(10,16),(8,17),(11,17),(9,18),(9,19),(11,19),(8,20),(10,20),(11,20),(4,21),(5,21),(14,22),(12,23),(6,24),(7,24),(14,24),(12,26),(6,27),(8,28),(10,28),(11,28),(6,29),(2,30),(3,30),(13,30),(7,31),(13,31),(13,32),(13,33),(7,34),(14,34),(12,35),(9,36),(12,36),(9,37),(12,37);
/*!40000 ALTER TABLE `RestauranteProducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL,
  `nombreUsuario` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (262982572,'Pablo');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-25 22:28:04
