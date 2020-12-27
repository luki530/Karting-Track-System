CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`kart_model` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `power` INT NOT NULL,
  `number_of_seats` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`kart` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `kart_number` INT NOT NULL,
  `kart_model_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `kart_number_UNIQUE` (`kart_number` ASC) VISIBLE,
  INDEX `kart_mdel_id_idx` (`kart_model_id` ASC) VISIBLE,
  CONSTRAINT `kart_mdel_id`
    FOREIGN KEY (`kart_model_id`)
    REFERENCES `JSivppQrAr`.`kart_model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`client` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `client_number` VARCHAR(45) NOT NULL,
  `sex` BINARY(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`track` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`race` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `number` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`race_drivers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `kart_id` INT NOT NULL,
  `client_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `race_id_UNIQUE` (`race_id` ASC) VISIBLE,
  UNIQUE INDEX `kart_id_UNIQUE` (`kart_id` ASC) VISIBLE,
  UNIQUE INDEX `client_id_UNIQUE` (`client_id` ASC) VISIBLE,
  CONSTRAINT `race_id`
    FOREIGN KEY (`race_id`)
    REFERENCES `JSivppQrAr`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `kart_id`
    FOREIGN KEY (`kart_id`)
    REFERENCES `JSivppQrAr`.`kart` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `client_id`
    FOREIGN KEY (`client_id`)
    REFERENCES `JSivppQrAr`.`client` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `JSivppQrAr`.`lap` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `start_time` TIMESTAMP(3) NOT NULL,
  `end_time` TIMESTAMP(3) NULL,
  `track_id` INT NOT NULL,
  `race_drivers_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) INVISIBLE,
  INDEX `track_id_idx` (`track_id` ASC) VISIBLE,
  INDEX `race_drivers_id_idx` (`race_drivers_id` ASC) VISIBLE,
  CONSTRAINT `track_id`
    FOREIGN KEY (`track_id`)
    REFERENCES `JSivppQrAr`.`track` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `race_drivers_id`
    FOREIGN KEY (`race_drivers_id`)
    REFERENCES `JSivppQrAr`.`race_drivers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;