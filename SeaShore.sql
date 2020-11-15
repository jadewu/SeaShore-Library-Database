-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema seashore
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `seashore` ;

-- -----------------------------------------------------
-- Schema seashore
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `seashore` DEFAULT CHARACTER SET utf8 ;
USE `seashore` ;

-- -----------------------------------------------------
-- Table `seashore`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`books` (
  `book_id` INT NOT NULL AUTO_INCREMENT,
  `book_name` VARCHAR(32) NOT NULL,
  `author_firstname` VARCHAR(32) NOT NULL,
  `author_lastname` VARCHAR(32) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`book_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 28
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`rooms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`rooms` (
  `room_id` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`room_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`shelves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`shelves` (
  `shelf_id` INT NOT NULL AUTO_INCREMENT,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `room_id` INT NOT NULL,
  PRIMARY KEY (`shelf_id`),
  INDEX `fk_shelves_rooms1_idx` (`room_id` ASC) VISIBLE,
  CONSTRAINT `fk_shelves_rooms1`
    FOREIGN KEY (`room_id`)
    REFERENCES `seashore`.`rooms` (`room_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`books_storage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`books_storage` (
  `book_sto_id` INT NOT NULL AUTO_INCREMENT,
  `instock` CHAR(1) NOT NULL DEFAULT 'Y',
  `shelf_level` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `book_id` INT NOT NULL,
  `shelf_id` INT NOT NULL,
  PRIMARY KEY (`book_sto_id`),
  INDEX `fk_books_storage_books1_idx` (`book_id` ASC) VISIBLE,
  INDEX `fk_books_storage_shelves1_idx` (`shelf_id` ASC) VISIBLE,
  CONSTRAINT `fk_books_storage_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `seashore`.`books` (`book_id`),
  CONSTRAINT `fk_books_storage_shelves1`
    FOREIGN KEY (`shelf_id`)
    REFERENCES `seashore`.`shelves` (`shelf_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 53
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`questions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`questions` (
  `question` VARCHAR(100) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`question`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `customer_username` VARCHAR(32) NOT NULL COMMENT 'Customer user name',
  `customer_firstname` VARCHAR(32) NOT NULL COMMENT 'Customer first name',
  `customer_lastname` VARCHAR(32) NOT NULL COMMENT 'Customer last name',
  `customer_password` VARCHAR(32) NOT NULL,
  `question` VARCHAR(100) NOT NULL,
  `customer_answer` VARCHAR(100) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`),
  INDEX `fk_customers_questions1_idx` (`question` ASC) VISIBLE,
  CONSTRAINT `fk_customers_questions1`
    FOREIGN KEY (`question`)
    REFERENCES `seashore`.`questions` (`question`))
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`requests` (
  `request_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `request_status` CHAR(1) NOT NULL COMMENT 'Three types: ‘Y’ (yes), ‘W’ (waiting), ‘F’ (finished)',
  `request_start` DATE NOT NULL DEFAULT (curdate()),
  `request_stop` DATE NULL DEFAULT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `customer_id` INT NOT NULL,
  `book_sto_id` INT NOT NULL,
  PRIMARY KEY (`request_id`),
  INDEX `fk_requests_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_requests_books1_idx` (`book_sto_id` ASC) VISIBLE,
  CONSTRAINT `fk_requests_books_storage`
    FOREIGN KEY (`book_sto_id`)
    REFERENCES `seashore`.`books_storage` (`book_sto_id`),
  CONSTRAINT `fk_requests_customers`
    FOREIGN KEY (`customer_id`)
    REFERENCES `seashore`.`customers` (`customer_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 38
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`bills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`bills` (
  `bill_id` INT NOT NULL AUTO_INCREMENT,
  `bill_amount` FLOAT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `request_id` INT NOT NULL,
  PRIMARY KEY (`bill_id`, `request_id`),
  INDEX `fk_bills_requests1_idx` (`request_id` ASC) VISIBLE,
  CONSTRAINT `fk_bills_requests1`
    FOREIGN KEY (`request_id`)
    REFERENCES `seashore`.`requests` (`request_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 34
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`employees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`employees` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `employee_firstname` VARCHAR(32) NOT NULL,
  `employee_lastname` VARCHAR(32) NOT NULL,
  `employee_username` VARCHAR(32) NOT NULL,
  `employee_password` VARCHAR(45) NOT NULL,
  `question` VARCHAR(100) NOT NULL,
  `employee_answer` VARCHAR(100) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`employee_id`),
  INDEX `fk_employees_questions1_idx` (`question` ASC) VISIBLE,
  CONSTRAINT `fk_employees_questions1`
    FOREIGN KEY (`question`)
    REFERENCES `seashore`.`questions` (`question`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`events` (
  `event_id` INT NOT NULL AUTO_INCREMENT,
  `event_name` VARCHAR(32) NOT NULL,
  `event_type` CHAR(1) NOT NULL,
  `start_time` DATETIME NOT NULL,
  `stop_time` DATETIME NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`receipts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`receipts` (
  `receipt_id` INT NOT NULL AUTO_INCREMENT,
  `holder_first_name` VARCHAR(32) NOT NULL,
  `holder_last_name` VARCHAR(32) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bill_id` INT NOT NULL,
  `request_id` INT NOT NULL,
  PRIMARY KEY (`receipt_id`, `bill_id`, `request_id`),
  INDEX `fk_receipts_bills1_idx` (`bill_id` ASC, `request_id` ASC) VISIBLE,
  CONSTRAINT `fk_receipts_bills1`
    FOREIGN KEY (`bill_id` , `request_id`)
    REFERENCES `seashore`.`bills` (`bill_id` , `request_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`reservations` (
  `reservation_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `reservation_date` DATE NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`reservation_id`),
  INDEX `fk_requests_customers1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_requests_customers10`
    FOREIGN KEY (`customer_id`)
    REFERENCES `seashore`.`customers` (`customer_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`rooms_has_reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`rooms_has_reservations` (
  `room_id` INT NOT NULL,
  `reservation_id` INT NOT NULL,
  PRIMARY KEY (`room_id`, `reservation_id`),
  INDEX `fk_rooms_has_r_reservations_rooms_idx` (`room_id` ASC) VISIBLE,
  INDEX `fk_rooms_has_r_reservations_r_reservations_idx` (`reservation_id` ASC) VISIBLE,
  CONSTRAINT `reservation_id`
    FOREIGN KEY (`reservation_id`)
    REFERENCES `seashore`.`reservations` (`reservation_id`),
  CONSTRAINT `room_id`
    FOREIGN KEY (`room_id`)
    REFERENCES `seashore`.`rooms` (`room_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
