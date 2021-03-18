CREATE TABLE `valine` (
  `ta_no` varchar(255) PRIMARY KEY,
  `luokka_id` int,
  `valine_nimi` varchar(255),
  `huomautus` varchar(255),
  `paikka_id` int,
  `active` tinyint
);

CREATE TABLE `luokka` (
  `luokka_id` int PRIMARY KEY,
  `luokka_nimi` varchar(255)
);

CREATE TABLE `paikka` (
  `paikka_id` int PRIMARY KEY,
  `lyhytnimi` varchar(255),
  `hylly` varchar(255),
  `taso` tinyint,
  `vali` tinyint,
  `lava` tinyint,
  `active` tinyint
);

CREATE TABLE `taphtuma` (
  `tapath_id` int PRIMARY KEY,
  `ta_no` varchar(255),
  `tluokka` int,
  `paikka_id` int,
  `tapahtunut` datetime DEFAULT (now())
);

CREATE TABLE `tapahtuma_luokka` (
  `tapaht_luokka_id` int PRIMARY KEY,
  `tapaht_kuvaus` varchar(255)
);

ALTER TABLE `valine` ADD FOREIGN KEY (`luokka_id`) REFERENCES `luokka` (`luokka_id`);

ALTER TABLE `valine` ADD FOREIGN KEY (`paikka_id`) REFERENCES `paikka` (`paikka_id`);

ALTER TABLE `taphtuma` ADD FOREIGN KEY (`ta_no`) REFERENCES `valine` (`ta_no`);

ALTER TABLE `taphtuma` ADD FOREIGN KEY (`paikka_id`) REFERENCES `paikka` (`paikka_id`);

ALTER TABLE `taphtuma` ADD FOREIGN KEY (`tluokka`) REFERENCES `tapahtuma_luokka` (`tapaht_luokka_id`);
