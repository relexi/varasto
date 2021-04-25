CREATE TABLE `valine` (
  `ta_no` varchar(255) PRIMARY KEY,
  `va_luokka_id` int,
  `valine_nimi` varchar(255),
  `huomautus` varchar(255),
  `va_paikka_id` int,
  `active` tinyint
);

CREATE TABLE `luokka` (
  `luokka_id` INTEGER PRIMARY KEY,
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

CREATE TABLE `tapahtuma` (
  `tapaht_id` int PRIMARY KEY,
  `ta_ta_no` varchar(255),
  `ta_luokka` int,
  `ta_paikka_id` int,
  `tapahtunut` datetime DEFAULT (now())
);

CREATE TABLE `tapahtuma_luokka` (
  `tapaht_luokka_id` int PRIMARY KEY,
  `tapaht_kuvaus` varchar(255)
);

CREATE TABLE `meta` (
  `version` int PRIMARY KEY,
  `version_info` varchar(255),
  `version_date` datetime DEFAULT (now())
);

CREATE TABLE `hyllyt` (
  `hylly` varchar(255) PRIMARY KEY,
  `tasot` varchar(255),
  `valit` varchar(255),
  `lavat` varchar(255)
);

ALTER TABLE `valine` ADD FOREIGN KEY (`va_luokka_id`) REFERENCES `luokka` (`luokka_id`);

ALTER TABLE `valine` ADD FOREIGN KEY (`va_paikka_id`) REFERENCES `paikka` (`paikka_id`);

ALTER TABLE `tapahtuma` ADD FOREIGN KEY (`ta_ta_no`) REFERENCES `valine` (`ta_no`);

ALTER TABLE `tapahtuma` ADD FOREIGN KEY (`ta_paikka_id`) REFERENCES `paikka` (`paikka_id`);

ALTER TABLE `tapahtuma` ADD FOREIGN KEY (`ta_luokka`) REFERENCES `tapahtuma_luokka` (`tapaht_luokka_id`);
