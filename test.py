import os

import patoolib

#os.rename(".\\DataFiles\\D02_100C_D122_IV.tbl", ".\\DataFiles\\D002_100C_D122_IV.txt")
var = '("wafer" "cdgchejld")'
print(var.split(' ')[0].replace('"', '')[1:])
