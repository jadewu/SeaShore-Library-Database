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
-- Table `seashore`.`authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`authors` (
  `author_id` INT NOT NULL AUTO_INCREMENT,
  `author_firstname` VARCHAR(32) NOT NULL,
  `author_lastname` VARCHAR(32) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`author_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`books` (
  `book_id` INT NOT NULL AUTO_INCREMENT,
  `book_name` VARCHAR(32) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`book_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`authors_has_books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`authors_has_books` (
  `author_id` INT NOT NULL,
  `book_id` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`author_id`, `book_id`),
  INDEX `fk_authors_has_books_books1_idx` (`book_id` ASC) VISIBLE,
  INDEX `fk_authors_has_books_authors1_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_authors_has_books_authors1`
    FOREIGN KEY (`author_id`)
    REFERENCES `seashore`.`authors` (`author_id`),
  CONSTRAINT `fk_authors_has_books_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `seashore`.`books` (`book_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`rooms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`rooms` (
  `room_id` INT NOT NULL AUTO_INCREMENT,
  `floor` VARCHAR(32) NOT NULL,
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
    REFERENCES `seashore`.`rooms` (`room_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`books_storage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`books_storage` (
  `book_sto_id` INT NOT NULL AUTO_INCREMENT,
  `instock` CHAR(1) NOT NULL,
  `shelves_level` INT NULL DEFAULT NULL,
  `shelves_counting` INT NULL DEFAULT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    REFERENCES `seashore`.`shelves` (`shelf_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`requests` (
  `request_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `request_status` VARCHAR(16) NOT NULL COMMENT 'Customer user name',
  `request_start` DATETIME NOT NULL,
  `request_stop` DATETIME NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    REFERENCES `seashore`.`requests` (`request_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`courses` (
  `course_id` INT NOT NULL AUTO_INCREMENT,
  `course_name` VARCHAR(32) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`course_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`books_has_courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`books_has_courses` (
  `book_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`book_id`, `course_id`),
  INDEX `fk_books_has_courses_courses1_idx` (`course_id` ASC) VISIBLE,
  INDEX `fk_books_has_courses_books1_idx` (`book_id` ASC) VISIBLE,
  CONSTRAINT `fk_books_has_courses_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `seashore`.`books` (`book_id`),
  CONSTRAINT `fk_books_has_courses_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `seashore`.`courses` (`course_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`events` (
  `event_id` INT NOT NULL AUTO_INCREMENT,
  `event_type` VARCHAR(16) NOT NULL,
  `start_time` DATETIME NOT NULL,
  `stop_time` DATETIME NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`campaigns`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`campaigns` (
  `event_id` INT NOT NULL,
  PRIMARY KEY (`event_id`),
  INDEX `fk_campaigns_events1_idx` (`event_id` ASC) VISIBLE,
  CONSTRAINT `fk_campaigns_events10`
    FOREIGN KEY (`event_id`)
    REFERENCES `seashore`.`events` (`event_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`reservations` (
  `reservation_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `reservation_start` DATETIME NOT NULL,
  `reservation_stop` DATETIME NOT NULL,
  `reservation_type` CHAR(12) NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`reservation_id`),
  INDEX `fk_requests_customers1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_requests_customers10`
    FOREIGN KEY (`customer_id`)
    REFERENCES `seashore`.`customers` (`customer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`e_reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`e_reservations` (
  `reservation_id` INT NOT NULL,
  PRIMARY KEY (`reservation_id`),
  INDEX `fk_e_reservations_reservations1_idx` (`reservation_id` ASC) VISIBLE,
  CONSTRAINT `fk_e_reservations_reservations1`
    FOREIGN KEY (`reservation_id`)
    REFERENCES `seashore`.`reservations` (`reservation_id`))
ENGINE = InnoDB
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
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`employee_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`equipments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`equipments` (
  `equipment_id` INT NOT NULL AUTO_INCREMENT,
  `equipment_name` VARCHAR(32) NOT NULL,
  `equipment_amount` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`equipment_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`equipments_has_e_reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`equipments_has_e_reservations` (
  `equipment_id` INT NOT NULL,
  `reservation_id` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`equipment_id`, `reservation_id`),
  INDEX `fk_equipments_has_e_reservations_e_reservations1_idx` (`reservation_id` ASC) VISIBLE,
  INDEX `fk_equipments_has_e_reservations_equipments1_idx` (`equipment_id` ASC) VISIBLE,
  CONSTRAINT `fk_equipments_has_e_reservations_e_reservations1`
    FOREIGN KEY (`reservation_id`)
    REFERENCES `seashore`.`e_reservations` (`reservation_id`),
  CONSTRAINT `fk_equipments_has_e_reservations_equipments1`
    FOREIGN KEY (`equipment_id`)
    REFERENCES `seashore`.`equipments` (`equipment_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`exhibitions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`exhibitions` (
  `event_id` INT NOT NULL,
  PRIMARY KEY (`event_id`),
  INDEX `fk_campaigns_events1_idx` (`event_id` ASC) VISIBLE,
  CONSTRAINT `fk_campaigns_events1`
    FOREIGN KEY (`event_id`)
    REFERENCES `seashore`.`events` (`event_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`r_reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`r_reservations` (
  `reservation_id` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reservation_id`),
  INDEX `fk_e_reservations_reservations1_idx` (`reservation_id` ASC) VISIBLE,
  CONSTRAINT `fk_e_reservations_reservations10`
    FOREIGN KEY (`reservation_id`)
    REFERENCES `seashore`.`reservations` (`reservation_id`))
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
    REFERENCES `seashore`.`bills` (`bill_id` , `request_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`rooms_has_events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`rooms_has_events` (
  `room_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  `last_edit` TIMESTAMP NOT NULL,
  PRIMARY KEY (`room_id`, `event_id`),
  INDEX `fk_rooms_has_events_events1_idx` (`event_id` ASC) VISIBLE,
  INDEX `fk_rooms_has_events_rooms1_idx` (`room_id` ASC) VISIBLE,
  CONSTRAINT `fk_rooms_has_events_events1`
    FOREIGN KEY (`event_id`)
    REFERENCES `seashore`.`events` (`event_id`),
  CONSTRAINT `fk_rooms_has_events_rooms1`
    FOREIGN KEY (`room_id`)
    REFERENCES `seashore`.`rooms` (`room_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `seashore`.`rooms_has_r_reservations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seashore`.`rooms_has_r_reservations` (
  `room_id` INT NOT NULL,
  `reservation_id` INT NOT NULL,
  PRIMARY KEY (`room_id`, `reservation_id`),
  INDEX `fk_rooms_has_r_reservations_copy1_r_reservations_copy11_idx` (`reservation_id` ASC) VISIBLE,
  INDEX `fk_rooms_has_r_reservations_copy1_rooms1_idx` (`room_id` ASC) VISIBLE,
  CONSTRAINT `fk_rooms_has_r_reservations_r_reservations`
    FOREIGN KEY (`reservation_id`)
    REFERENCES `seashore`.`r_reservations` (`reservation_id`),
  CONSTRAINT `fk_rooms_has_r_reservations_rooms1`
    FOREIGN KEY (`room_id`)
    REFERENCES `seashore`.`rooms` (`room_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
