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

#-- Define additional constants
EXIT         = 0
CONTINUE     = 1
NUEVO        = 1
MODIFICA     = 2
BORRAR       = 3
modo_z       = 0
mibd = def_tablas.lee_basedato_ini()
cias = def_tablas.define_cias()
mayoris = def_tablas.define_mayoris()
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

class Altamay:
  """Esta es una aplicación Alta Mayoristas"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "altamay.glade"
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
    self.wTree.signal_autoconnect(dic)
    global cias
    global mayoris
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
    miwin = self.wTree.get_widget("win_altamay")
    miwin.set_title(cias['razon'] + " Mantenimiento de Mayoristas")
    self.editable_onoff(False)
    #self.agrega_grd_alm()

  def on_btn_primero_clicked(self, widget):
      self.busca_vnd("P")

  def on_btn_anter_clicked(self, widget):
      self.busca_vnd("A", mayoris['codigo'])

  def on_btn_sigte_clicked(self, widget):
      self.busca_vnd("S", mayoris['codigo'])

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
      codigo_z = mayoris['codigo']
      nombre_z = mayoris['nombre']
      resp_z = utils.yesnodlg("Seguro de Eliminar este Mayorista ?" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from mayoris where codigo='" + codigo_z + "'" 
         sql_z = sql_z + " and cia= " + utils.IntToStr(cia_z)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         self.limpia_campos()
         def_tablas.commit_trans(mydb)
        #End if
# --- Finde on_btn_borra_clicked(self, widget): ---------

  def on_btn_cancelar_clicked(self, widget):
      self.editable_onoff(False)

  def on_btn_aceptar_clicked(self, widget):
      self.editable_onoff(False)
      global modo_z
      sql_z = ''
      self.okcancel = True

      mayoris['codigo']  = self.wTree.get_widget("edt_codigo").get_text().upper()
      mayoris['nombre']  = self.wTree.get_widget("edt_nombre").get_text().upper()
      mayoris['direc']   = self.wTree.get_widget("edt_direc").get_text().upper()
      mayoris['cia']     = cia_z
      mayoris['nombre2'] = self.wTree.get_widget("edt_nombre2").get_text().upper()
      mayoris['nompag1'] = self.wTree.get_widget("edt_nompagare").get_text().upper()
      mayoris['nompag2'] = self.wTree.get_widget("edt_nompag2").get_text().upper()
      mayoris['dirpag1'] = self.wTree.get_widget("edt_dirpagare").get_text().upper()
      mayoris['dirpag2'] = self.wTree.get_widget("edt_dirpag2").get_text().upper()
      mayoris['ciupag']  = self.wTree.get_widget("edt_ciupagare").get_text().upper()
      mayoris['ciu']     = self.wTree.get_widget("edt_ciudad").get_text().upper()
      mayoris['rfc']     = self.wTree.get_widget("edt_rfc").get_text().upper()
      mayoris['pdsc']    = utils.StrToFloat(self.wTree.get_widget("edt_factordsc").get_text())
      mayoris['tel']     = self.wTree.get_widget("edt_telefono").get_text()
      if modo_z == NUEVO:
         sql_z = def_tablas.insert_into_mayoris(mayoris)
          
      elif modo_z == MODIFICA:
         sql_z = "update mayoris set "
         sql_z = sql_z + "nombre = '" + mayoris['nombre'] + "',"
         sql_z = sql_z + "direc = '" + mayoris['direc'] + "',"
         sql_z = sql_z + "nompag1 = '" + mayoris['nompag1'] + "',"
         sql_z = sql_z + "nompag2 = '" + mayoris['nompag2'] + "',"
         sql_z = sql_z + "dirpag1 = '" + mayoris['dirpag1'] + "',"
         sql_z = sql_z + "dirpag2 = '" + mayoris['dirpag2'] + "',"
         sql_z = sql_z + "ciupag = '" + mayoris['ciupag'] + "',"
         sql_z = sql_z + "rfc = '" + mayoris['rfc'] + "',"
         sql_z = sql_z + "tel = '" + mayoris['tel'] + "',"
         sql_z = sql_z + "pdsc = " + repr(mayoris['pdsc']) + ","
         sql_z = sql_z + "nombre2 = '" + mayoris['nombre2'] + "'"
         sql_z = sql_z + " where codigo = '" + mayoris['codigo'] + "'"
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
## ----- Fin de on_btn_aceptar_clicked(self, widget): --------------


  def busca_vnd(self, hacia_z, codigo_z=''):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      sql_z = "select codigo, nombre, direc, ciu, rfc, tel, pdsc,"
      sql_z = sql_z + "cia, nompag1, nompag2, dirpag1, dirpag2, ciupag, nombre2 "
      sql_z = sql_z + " from mayoris where "
      if hacia_z == 'P':
        sql_z = sql_z + "codigo = ( select min(codigo) from mayoris where cia = " 
        sql_z = sql_z + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == 'U':
        sql_z = sql_z + "codigo = ( select max(codigo) from mayoris where cia = " 
        sql_z = sql_z + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == 'A':
        sql_z = sql_z + "codigo = ( select max(codigo) from mayoris where codigo < '" 
        sql_z = sql_z + codigo_z + "' and cia = " + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == 'S':
        sql_z = sql_z + "codigo = ( select min(codigo) from mayoris where codigo > '" 
        sql_z = sql_z + codigo_z + "' and cia = " + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
# execute SQL statement
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        mayoris['codigo']    = record[0]
        mayoris['nombre']    = record[1]
        mayoris['direc']     = record[2]
        mayoris['ciu']       = record[3]
        mayoris['rfc']       = record[4]
        mayoris['tel']       = record[5]
        mayoris['pdsc']      = record[6]
        mayoris['cia']       = record[7]
        mayoris['nompag1']   = record[8]
        mayoris['nompag2']   = record[9]
        mayoris['dirpag1']   = record[10]
        mayoris['dirpag2']   = record[11]
        mayoris['ciupag']    = record[12]
        mayoris['nombre2']   = record[13]
        self.despliega_datos()

  def despliega_datos(self):

      self.wTree.get_widget("edt_codigo").set_text(mayoris['codigo'])
      self.wTree.get_widget("edt_nombre").set_text(mayoris['nombre'])
      self.wTree.get_widget("edt_nombre2").set_text(mayoris['nombre2'])
      self.wTree.get_widget("edt_direc").set_text(mayoris['direc'])
      self.wTree.get_widget("edt_ciudad").set_text(mayoris['ciu'])
      self.wTree.get_widget("edt_rfc").set_text(mayoris['rfc'])
      self.wTree.get_widget("edt_telefono").set_text(mayoris['tel'])
      self.wTree.get_widget("edt_nompagare").set_text(mayoris['nompag1'])
      self.wTree.get_widget("edt_nompag2").set_text(mayoris['nompag2'])
      self.wTree.get_widget("edt_dirpagare").set_text(mayoris['dirpag1'])
      self.wTree.get_widget("edt_dirpag2").set_text(mayoris['dirpag2'])
      self.wTree.get_widget("edt_ciupagare").set_text(mayoris['ciupag'])
      self.wTree.get_widget("edt_factordsc").set_text(utils.currency(mayoris['pdsc']))

  def limpia_campos(self):
      campos_z = [ "edt_codigo", "edt_nombre", "edt_nombre2", "edt_direc", \
      "edt_ciudad", "edt_rfc", "edt_telefono", "edt_factordsc", \
      "edt_nompag2", "edt_dirpag2", "edt_nompagare", "edt_dirpagare", "edt_ciupagare" ]
      for micampo_z in campos_z:
          self.wTree.get_widget(micampo_z).set_text('')

# --- Fin de limpia_campos(self): -----

  def editable_onoff(self, modo):
      campos_z = [ "edt_codigo", "edt_nombre", "edt_nombre2", "edt_direc", \
      "edt_ciudad", "edt_rfc", "edt_telefono", "edt_factordsc", \
      "edt_nompagare", "edt_dirpagare", "edt_ciupagare" ]
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
   global mydb
   global cia_z
   hwg = Altamay()
   gtk.main()

def main():
    global mydb
    gtk.main()
    return 0
