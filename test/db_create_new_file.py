from create_module import luo_db_file, luo_db_paikat, luo_db_luokat


str_db_file = "test27.db"
# Hylly parametrit
hyllyt = {
    "A": [3, 5, [3, 3, 4]],
    "B": [3, 3, [3, 3, 3]],
    "C": [3, 3, [3, 3, 3]],
    "D": [3, 3, [3, 3, 3]],
    "E": [2, 4, [4, 4]]
        }

luokat = {
    "181210": "sängyt",
    "043306": "painehaavapatjat moottoroitu",
    "122203": "pyörätuolit",
    "120606": "kävelytelineet"
         }

luo_db_file(str_db_file)
luo_db_paikat(str_db_file, hyllyt)
luo_db_luokat(str_db_file, luokat)
