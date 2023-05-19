#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
import def_tablas
import utils

global mydb
global cia_z
global mibd
global cias
global almacen

#-- Define additional constants
EXIT         = 0
CONTINUE     = 1
NUEVO        = 1
MODIFICA     = 2
BORRAR       = 3
modo_z       = 0
mibd = def_tablas.lee_basedato_ini()
cias = def_tablas.define_cias()
almacen = def_tablas.define_almacen()
dirprogs_z = ".." + os.sep + "altaalm" + os.sep
if mibd['tipobd'] == "MYSQL":
   try:
     import MySQLdb
   except:
     sys.exit(1)
elif mibd['tipobd'] == "ODBC":
   try:
     import pyodbc
   except:
     sys.exit(1)

class Altaptov:
  """Esta es una aplicación Alta Almacenes"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "altaalm.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_primero_clicked": self.on_btn_primero_clicked, \
            "on_btn_sigte_clicked": self.on_btn_sigte_clicked, \
            "on_btn_anter_clicked": self.on_btn_anter_clicked, \
            "on_btn_ultimo_clicked": self.on_btn_ultimo_clicked, \
            "on_btn_nuevo_clicked": self.on_btn_nuevo_clicked, \
            "on_btn_modif_clicked": self.on_btn_modif_clicked, \
            "on_btn_borra_clicked": self.on_btn_borra_clicked, \
            "on_btn_aceptar_clicked": self.on_btn_aceptar_clicked, \
            "on_btn_cancelar_clicked": self.on_btn_cancelar_clicked
            }
#                "on_win_altaalm_destroy": gtk.main_quit }
    self.wTree.signal_autoconnect(dic)
    global cias
    global almacen
    global cia_z
    global mydb
    cia_z = 1
    cias_lines = []
    basedato_z = []

    fh_cias = open('.cias.ini')
    for line in fh_cias.readlines():
        cias_lines.append(string.rstrip(line))
    cia_z = utils.StrToInt(cias_lines[0])

# execute SQL statement
    dsn_z = "dsn="+mibd['base']+";uid="+mibd['user']+";pwd="+mibd['password']
    if mibd['tipobd'] == "MYSQL":
       mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
    elif mibd['tipobd'] == "ODBC":
       mydb = pyodbc.connect(dsn_z)

    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_altaalm")
    miwin.set_title(cias['razon'] + " Mantenimiento de Puntos de Venta")
    self.editable_onoff(False)
    objetos_invisibles = [ "edt_exib", "edt_zona", "edt_ordtab", \
       "lbl_exib", "lbl_zona", "lbl_ordtab" ]
    for objeto_z in objetos_invisibles:
        self.wTree.get_widget(objeto_z).set_child_visible(False)

  def on_btn_primero_clicked(self, widget):
      self.busca_vnd("P")

  def on_btn_anter_clicked(self, widget):
      self.busca_vnd("A", almacen['clave'])

  def on_btn_sigte_clicked(self, widget):
      self.busca_vnd("S", almacen['clave'])

  def on_btn_ultimo_clicked(self, widget):
      self.busca_vnd("U")

  def on_btn_nuevo_clicked(self, widget):
      global modo_z
      modo_z = NUEVO
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      self.editable_onoff(True)
      edt_codigo.grab_focus()

  def on_btn_modif_clicked(self, widget):
      global modo_z
      modo_z = MODIFICA
      edt_nombre = self.wTree.get_widget("edt_nombre")
      self.editable_onoff(True)
      edt_nombre.grab_focus()

  def on_btn_borra_clicked(self, widget):
      global modo_z
      modo_z = BORRAR
      codigo_z = almacen['clave']
      nombre_z = almacen['nombre']
      resp_z = utils.yesnodlg("Seguro de Eliminar este Punto de Venta ?" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from ptovta where clave='" + codigo_z + "' and cia= " + str(cia_z)
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         def_tablas.commit_trans(mydb)
         self.limpia_campos()
         #End if
# --- Finde on_btn_borra_clicked(self, widget): ---------

  def on_btn_cancelar_clicked(self, widget):
      self.editable_onoff(False)

  def on_btn_aceptar_clicked(self, widget):
      self.editable_onoff(False)
      global modo_z
      sql_z = ''
      self.okcancel = True
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_direc   = self.wTree.get_widget("edt_direc")
      edt_ordiary = self.wTree.get_widget("edt_ordiary")
      #edt_exib    = self.wTree.get_widget("edt_exib")
      #edt_zona    = self.wTree.get_widget("edt_zona")
      #edt_ordtab  = self.wTree.get_widget("edt_ordtab")

      almacen['clave']   = edt_codigo.get_text().upper()
      almacen['nombre']  = edt_nombre.get_text().upper()
      almacen['direc']   = edt_direc.get_text().upper()
      almacen['cia']     = cia_z
      almacen['ordiary'] = utils.StrToInt(edt_ordiary.get_text())
      #almacen['exib']    = edt_exib.get_text()
      #almacen['zona']    = edt_zona.get_text()
      #almacen['ordtab']  = utils.StrToInt(edt_ordtab.get_text())
      if modo_z == NUEVO:
         sql_z = "insert into ptovta (clave,nombre,direc,sdoini,impent,impsal,sdofin,cia,ordiary) values ( "
         sql_z = sql_z + "'" + almacen['clave'] + "',"
         sql_z = sql_z + "'" + almacen['nombre'] + "',"
         sql_z = sql_z + "'" + almacen['direc'] + "',"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + str(cia_z) + ","
         sql_z = sql_z + str(almacen['ordiary']) + ")"
         #sql_z = sql_z + "'" + almacen['exib'] + "',"
         #sql_z = sql_z + "'" + almacen['zona'] + "',"
         #sql_z = sql_z + repr(almacen['ordtab']) + ")"
          
      elif modo_z == MODIFICA:
         sql_z = "update ptovta set "
         sql_z = sql_z + "nombre = '" + almacen['nombre'] + "',"
         sql_z = sql_z + "direc = '" + almacen['direc'] + "', "
         sql_z = sql_z + "ordiary = " + str(almacen['ordiary']) + " "
         #sql_z = sql_z + "exib = '" + almacen['exib'] + "',"
         #sql_z = sql_z + "zona = '" + almacen['zona'] + "'"
         #sql_z = sql_z + "ordtabt = " + repr(almacen['ordtab'])
         sql_z = sql_z + " where clave = '" + almacen['clave'] + "'"
         sql_z = sql_z + " and cia = " + str(cia_z)
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
## ----- Fin de on_btn_aceptar_clicked(self, widget): --------------


  def busca_vnd(self, hacia_z, codigo_z=''):
      global mydb
      global cia_z
      sql_z = "select clave, nombre, direc, sdoini, impent, impsal, sdofin,"
      sql_z = sql_z + "cia, ordiary from ptovta where "
      if hacia_z == 'P':
        sql_z = sql_z + "clave = ( select min(clave) from ptovta where cia = " + str(cia_z) + ") and cia = " + str(cia_z)
      elif hacia_z == 'U':
        sql_z = sql_z + "clave = ( select max(clave) from ptovta where cia = " + str(cia_z) + ") and cia = " + str(cia_z)
      elif hacia_z == 'A':
        sql_z = sql_z + "clave = ( select max(clave) from ptovta where clave < '" + codigo_z + "' and cia = " + str(cia_z) + ") and cia = " + str(cia_z)
      elif hacia_z == 'S':
        sql_z = sql_z + "clave = ( select min(clave) from ptovta where clave > '" + codigo_z + "' and cia = " + str(cia_z) + ") and cia = " + str(cia_z)
# execute SQL statement
      
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        almacen['clave']    = record[0]
        almacen['nombre']  = record[1]
        almacen['direc']   = record[2]
        almacen['sdoini']  = 0
        almacen['impent']  = 0
        almacen['impsal']  = 0
        almacen['sdofin']  = 0
        almacen['cia']     = record[7]
        almacen['ordiary'] = record[8]
        #almacen['exib']    = record[9]
        #almacen['zona']    = record[10]
        #almacen['ordtab']  = record[11]
        self.despliega_datos()

  def despliega_datos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_direc   = self.wTree.get_widget("edt_direc")
      edt_sdoini  = self.wTree.get_widget("edt_sdoini")
      edt_impent  = self.wTree.get_widget("edt_impent")
      edt_impsal  = self.wTree.get_widget("edt_impsal")
      edt_sdofin  = self.wTree.get_widget("edt_sdofin")
      edt_ordiary = self.wTree.get_widget("edt_ordiary")
      edt_exib    = self.wTree.get_widget("edt_exib")
      edt_zona    = self.wTree.get_widget("edt_zona")
      edt_ordtab  = self.wTree.get_widget("edt_ordtab")
      sdoini_z = utils.currency(almacen['sdoini'])
      impent_z = utils.currency(almacen['impent'])
      impsal_z = utils.currency(almacen['impsal'])
      sdofin_z = utils.currency(almacen['sdofin'])

      edt_codigo.set_text  (almacen['clave'])
      edt_nombre.set_text  (almacen['nombre'])
      edt_direc.set_text   (almacen['direc'])
      edt_sdoini.set_text  (sdoini_z)
      edt_impent.set_text  (impent_z)
      edt_impsal.set_text  (impsal_z)
      edt_sdofin.set_text  (sdofin_z)
      edt_ordiary.set_text (str(almacen['ordiary']))
      #edt_zona.set_text    (almacen['zona'])
      #edt_ordtab.set_text  (repr(almacen['ordtab']))
      #edt_exib.set_text    (almacen['exib'])

  def limpia_campos(self):
      campos_z = [ "edt_codigo", "edt_nombre", "edt_direc", "edt_sdoini",\
      "edt_impent", "edt_impsal", "edt_sdofin", "edt_ordiary", "edt_exib", \
      "edt_zona", "edt_ordtab" ]
      for micampo_z in campos_z:
          self.wTree.get_widget(micampo_z).set_text('')

# --- Fin de limpia_campos(self): -----

  def editable_onoff(self, modo):
      campos_z = [ "edt_codigo", "edt_nombre", "edt_direc", "edt_sdoini",\
      "edt_impent", "edt_impsal", "edt_sdofin", "edt_ordiary", "edt_exib", \
      "edt_zona", "edt_ordtab" ]
      for micampo_z in campos_z:
          self.wTree.get_widget(micampo_z).set_editable(modo)
      botonessi_z = ["btn_ok", "btn_cancel"]
      botonesno_z = ["btn_nuevo", "btn_modif", "btn_borra", "btn_primero", \
      "btn_anter", "btn_sigte", "btn_ultimo"]
      for miboton_z in botonessi_z:
          self.wTree.get_widget(miboton_z).set_child_visible(modo)
      for miboton_z in botonesno_z:
          self.wTree.get_widget(miboton_z).set_child_visible(not(modo))

## --- Finde editable_onoff(self, modo) ----


if __name__ == "__main__":
   hwg = Altaptov()
   hwg.wTree.get_widget("win_altaalm").connect("destroy", gtk.main_quit )
   gtk.main()

def main():
    global mydb

    gtk.main()
    return 0
