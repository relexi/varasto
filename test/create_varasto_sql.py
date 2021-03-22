def create_string():
    create_string = ["""CREATE TABLE `valine` (
    `ta_no` varchar(255) NOT NULL PRIMARY KEY,
    `va_luokka_id` INTEGER REFERENCES luokka,
    `valine_nimi` varchar(255),
    `huomautus` varchar(255),
    `va_paikka_id` INTEGER REFERENCES paikka,
    `active` tinyint
    );
    """,
    """
    CREATE TABLE `luokka` (
    `luokka_id` INTEGER NOT NULL PRIMARY KEY,
    `luokka_nimi` varchar(255)
    );
    """,
    """
    CREATE TABLE `paikka` (
    `paikka_id` INTEGER NOT NULL PRIMARY KEY,
    `lyhytnimi` varchar(255),
    `hylly` varchar(255),
    `taso` tinyint,
    `vali` tinyint,
    `lava` tinyint,
    `active` tinyint
    );
    """,
    """
    CREATE TABLE `tapahtuma` (
    `tapaht_id` INTEGER NOT NULL PRIMARY KEY,
    `ta_ta_no` varchar(255) REFERENCES valine,
    `ta_luokka` INTEGER REFERENCES tapahtuma_luokka,
    `ta_paikka_id` INTEGER REFERENCES paikka,
    `tapahtunut` datetime DEFAULT (now())
    );
    """,
    """
    CREATE TABLE `tapahtuma_luokka` (
    `tapaht_luokka_id` INTEGER NOT NULL PRIMARY KEY,
    `tapaht_kuvaus` varchar(255)
    );
    """]
    return create_string
