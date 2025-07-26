CREATE TABLE IF NOT EXISTS `items` (
  `serial` varchar(32) NOT NULL,
  `data` mediumblob NOT NULL,
  PRIMARY KEY (`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
