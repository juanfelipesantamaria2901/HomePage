-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema green_project_bd
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema green_project_bd
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `green_project_bd` DEFAULT CHARACTER SET utf32 ;
USE `green_project_bd` ;

-- -----------------------------------------------------
-- Table `green_project_bd`.`USUARIO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`USUARIO` (
  `correo_electronico` VARCHAR(100) NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `apellido` VARCHAR(50) NOT NULL,
  `edad` INT NOT NULL,
  `sexo` VARCHAR(20) NOT NULL,
  `tipo_usuario` VARCHAR(50) NOT NULL,
  `identificacion` VARCHAR(20) NOT NULL,
  `direccion_residencia` VARCHAR(100) NOT NULL,
  `ocupacion` VARCHAR(100) NOT NULL,
  `numero_telefonico` VARCHAR(20) NOT NULL,
  `contrasena` VARCHAR(100) NOT NULL,
  `fecha_creacion` DATETIME NOT NULL,
  `estado_usuario` TINYINT NOT NULL,
  `nacionalidad` VARCHAR(50) NOT NULL,
  `ciudad` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`correo_electronico`),
  UNIQUE INDEX `correo_electronico_UNIQUE` (`correo_electronico` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`PROYECTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`PROYECTO` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre_proyecto` VARCHAR(50) NOT NULL,
  `descripcion` TEXT NOT NULL,
  `justificacion` TEXT NOT NULL,
  `objetivos` TEXT NOT NULL,
  `impacto` VARCHAR(100) NOT NULL,
  `alineacion_ods` VARCHAR(100) NOT NULL,
  `fecha_creacion` DATETIME NOT NULL,
  `fecha_finalizacion` DATETIME NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  `tipo_proyecto` VARCHAR(50) NOT NULL,
  `url_video` TEXT NOT NULL,
  `url_imagen` TEXT NOT NULL,
  `ciudad` VARCHAR(100) NOT NULL,
  `donacion_requerida` DOUBLE NOT NULL,
  `perfil_colaborador` VARCHAR(100) NOT NULL,
  `correo_electronico` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `correo_electronico_idx` (`correo_electronico` ASC) VISIBLE,
  CONSTRAINT `correo_electronico`
    FOREIGN KEY (`correo_electronico`)
    REFERENCES `green_project_bd`.`USUARIO` (`correo_electronico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`AVANCE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`AVANCE` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `url_imagen` TEXT NOT NULL,
  `titulo_avance` VARCHAR(80) NOT NULL,
  `descripcion_avance` TEXT NOT NULL,
  `id_proyecto` BIGINT NOT NULL,
  `fecha_avance` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_idx` (`id_proyecto` ASC) VISIBLE,
  CONSTRAINT `id`
    FOREIGN KEY (`id_proyecto`)
    REFERENCES `green_project_bd`.`PROYECTO` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`DONACION_MONETARIA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`DONACION_MONETARIA` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `correo_usuario` VARCHAR(100) NOT NULL,
  `id_proyecto` BIGINT NOT NULL,
  `cantidad_donacion` DOUBLE NOT NULL,
  `fecha_realizada` DATETIME NOT NULL,
  `numero_autorizacion` BIGINT NOT NULL,
  `moneda` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `correo_electronico_idx` (`correo_usuario` ASC) VISIBLE,
  INDEX `id_proyecto_idx` (`id_proyecto` ASC) VISIBLE,
  CONSTRAINT `correo_usuario_monetaria`
    FOREIGN KEY (`correo_usuario`)
    REFERENCES `green_project_bd`.`USUARIO` (`correo_electronico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_proyecto_monetaria`
    FOREIGN KEY (`id_proyecto`)
    REFERENCES `green_project_bd`.`PROYECTO` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`PERFIL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`PERFIL` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre_perfil` VARCHAR(200) NOT NULL,
  `cantidad_participantes` INT NOT NULL,
  `id_proyecto` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_proyecto_idx` (`id_proyecto` ASC) VISIBLE,
  CONSTRAINT `id_proyecto_perfil`
    FOREIGN KEY (`id_proyecto`)
    REFERENCES `green_project_bd`.`PROYECTO` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`PARTICIPANTE_PROYECTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`PARTICIPANTE_PROYECTO` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `correo_usuario` VARCHAR(100) NOT NULL,
  `id_perfil` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `correo_usuario_idx` (`correo_usuario` ASC) VISIBLE,
  INDEX `id_perfil_idx` (`id_perfil` ASC) VISIBLE,
  CONSTRAINT `correo_usuario_participante`
    FOREIGN KEY (`correo_usuario`)
    REFERENCES `green_project_bd`.`USUARIO` (`correo_electronico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_perfil`
    FOREIGN KEY (`id_perfil`)
    REFERENCES `green_project_bd`.`PERFIL` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`RECURSO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`RECURSO` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre_recurso` VARCHAR(50) NOT NULL,
  `cantidad_recurso` INT NOT NULL,
  `id_proyecto` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_proyecto_idx` (`id_proyecto` ASC) VISIBLE,
  CONSTRAINT `id_proyecto_recurso`
    FOREIGN KEY (`id_proyecto`)
    REFERENCES `green_project_bd`.`PROYECTO` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `green_project_bd`.`DONACION_RECURSO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `green_project_bd`.`DONACION_RECURSO` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `correo_usuario` VARCHAR(100) NOT NULL,
  `id_recurso` BIGINT NOT NULL,
  `cantidad_recurso` INT NOT NULL,
  `fecha_donativo` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `correo_usuaro_idx` (`correo_usuario` ASC) VISIBLE,
  INDEX `id_recurso_idx` (`id_recurso` ASC) VISIBLE,
  CONSTRAINT `correo_usuario_donacion`
    FOREIGN KEY (`correo_usuario`)
    REFERENCES `green_project_bd`.`USUARIO` (`correo_electronico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_recurso_donacion`
    FOREIGN KEY (`id_recurso`)
    REFERENCES `green_project_bd`.`RECURSO` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;