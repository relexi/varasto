from create_module import luo_db_file, luo_db_paikat
from create_module import luo_db_luokat, luo_db_tapahtumaluokat

# this program creates a new db-structure
# with the help of functions in create_module and the parameters
# given below

# define parameters for the new db

str_db_file = "test33.db"

hyllyt = {
    "A": [3, 5, [3, 3, 4]],
    "B": [3, 3, [3, 3, 3]],
    "C": [3, 3, [3, 3, 3]],
    "D": [3, 3, [3, 3, 3]],
    "E": [2, 4, [4, 4]]
        }

luokat = {
    "181210": "sängyt",
    "043306": "painehaavapatjat",
    "122203": "pyörätuolit",
    "120606": "kävelytelineet",
    "181224": "sängynpäädynkohottaja",
    "044808": "seisontatuet, kehikot",
    "044821": "kippilaudat",
    "093312": "suihkupaarit",
    "093303": "suihkutuolit, pyörättömät",
    "091203": "suihkupyörätuolit",
    "120612": "kävelypöydät",
             }

tapahtumaluokat = [
    "sisään",
    "ulos",
    "siirto"
]

# call functions from create_module to create first the
# database and then fill it with the tables given above

luo_db_file(str_db_file)
luo_db_paikat(str_db_file, hyllyt)
luo_db_luokat(str_db_file, luokat)
luo_db_tapahtumaluokat(str_db_file, tapahtumaluokat)
