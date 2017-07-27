"""
Tryout
"""
import logging
from algoritmos import *


logging.basicConfig(level=logging.CRITICAL)
# logging.disable(logging.ERROR)

"""
inp = input(
    "(1) LIVE TEST\n"
    "(2) BACK TEST\n"
    "(3) SIMPLE BUY\n"
    "(4) HISTOGRAM\n"
    "Ud. seleccionó: ")
"""

inp = "1"

if inp == "1":
    DatosLive().go()
elif inp == "2":
    DatosHistoricos().go()
elif inp == "3":
    SimpleBuy().go()
elif inp == "4":
    GetData().go()
elif inp == "5":
    ContinousData().go()
elif inp == "6":
    KeepUpdatedData().go()
else:
    print("Opción inválida")
