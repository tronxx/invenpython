#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Manto  de Vendedores DRBR 26-May-2007
import sys
import string, os
try:
  import pygtk
  pygtk.require('2.0')
except:
  pass
try:
  import gtk
  import gtk.glade
except:
  sys.exit(1)
try:
  import MySQLdb
except:
  sys.exit(1)
import def_tablas
import utils

global mydb
global cia_z
global mibd
global cias
global vendedor
dirprogs_z = ".." + os.sep + "altaalm" + os.sep

#-- Define additional constants
EXIT         = 0
CONTINUE     = 1
NUEVO        = 1
MODIFICA     = 2
BORRAR       = 3
modo_z       = 0
mibd = def_tablas.lee_basedato_ini()
cias = def_tablas.define_cias()
vendedor = def_tablas.define_vendedor()

class analisma:
  """Esta es una aplicación Alta Almacenes"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "reporte.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_aceptar_clicked": self.on_btn_aceptar_clicked, \
            "on_btn_cancelar_clicked": self.on_btn_cancelar_clicked
            }
#                "on_win_dialog_destroy": gtk.main_quit }
    self.wTree.signal_autoconnect(dic)
    global cias
    global vendedor
    global cia_z
    global mydb
    cia_z = 1
    cias_lines = []
    basedato_z = []

    fh_cias = open('.cias.ini')
    for line in fh_cias.readlines():
        cias_lines.append(string.rstrip(line))
    cia_z = cias_lines[0]

# execute SQL statement
    mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])

    sql_z = "select * from ciasinv where cia = " + repr(cia_z)
    cias['razon']="MDS"
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    cias['cia'] = record[0]
    cias['razon'] = record[1]
    cias['dir'] = record[2]
    cias['dir2'] = record[3]
    cias['nomfis'] = record[4]
    cias['tel'] = record[5]
    cias['fax'] = record[6]
    cias['rfc'] = record[7]
    miwin = self.wTree.get_widget("win_dialog")
    miwin.set_title(cias['razon'] + " Analitico de Ventas")
#    self.editable_onoff(False)
    
  def on_btn_aceptar_clicked(self, widget):
      fecini_z = utils.StrToDate(self.wTree.get_widget("edt_fecini").get_text())
      fecfin_z = utils.StrToDate(self.wTree.get_widget("edt_fecfin").get_text())
      print "Presionaste Aceptar Fecini", fecini_z, " Fecfin:", fecfin_z

  def on_btn_cancelar_clicked(self, widget):
      print "Presionaste Cancelar"
   

if __name__ == "__main__":
   hwg = analisma()
   gtk.main()

def main():

    gtk.main()
    return 0
