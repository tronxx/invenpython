import os
 
highestnumbers = {}
highestfiles = {}

linea_z = "ante"
directorio_z =  "html" + os.sep + linea_z
print("Directorio:" + directorio_z)
for filename in os.listdir(directorio_z):
    extension_z = filename[-3:]
    if extension_z == "JPG":
       print("Archivo:" + filename)
       nvofilename_z = "html" + os.sep + linea_z + os.sep + filename[0:-3] + "jpg"
       oldfilename_z = "html" + os.sep + linea_z + os.sep + filename
       print("Renombrando:" + oldfilename_z + " -> " + nvofilename_z)
       os.rename(oldfilename_z, nvofilename_z)
    #End if
#End for
