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
platform = sys.platform 

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
elif mibd['tipobd'] == "SOLID":
   try:
     import Solid
   except:
     print "No pudo importar librerias Solid de Solid \n"
     sys.exit(1)

class Altamay:
  """Esta es una aplicación Alta Mayoristas"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "pantalla_gral.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_nuevo_clicked": self.on_btn_nuevo_clicked, \
            "on_btn_modif_clicked": self.on_btn_modif_clicked, \
            "on_btn_borra_clicked": self.on_btn_borra_clicked
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
    elif mibd['tipobd'] == "SOLID":
       dsn_z = mibd['base']+" " + mibd['user']+" "+mibd['password']
       mydb = Solid.DB(dsn_z)

    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_altavnd")
    miwin.set_title(cias['razon'] + " Mantenimiento de Mayoristas")

    self.lista_vendedores = gtk.ListStore(str, str, str)
    grd_vendedores = self.wTree.get_widget("grd_vendedores")
    grd_vendedores.set_model(self.lista_vendedores)
    columnas_z = ["Codigo", "Nombre", "Direccion" ]
    
    ii_z = 0
    for micol_z in columnas_z:
      col = gtk.TreeViewColumn(micol_z)
      grd_vendedores.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1
    if platform in utils.grd_lines_soported:  
       grd_vendedores.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    self.llena_vendedores()
    grd_vendedores.connect("row_activated", self.on_grd_vendedor_activate)

    #self.editable_onoff(False)
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
      arch_dlg_datosmay = dirprogs_z + "altamay.glade"
      self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
      btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
      btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
      btn_aceptar.connect  ("clicked", self.on_btn_aceptar_clicked)
      btn_cancelar.connect ("clicked", self.on_btn_cancelar_clicked)

  def on_btn_modif_clicked(self, widget):
      global modo_z
      modo_z = MODIFICA
      global modo_z
      modo_z = NUEVO
      arch_dlg_datosmay = dirprogs_z + "altamay.glade"
      self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
      colcodigo_z = 0
      codigo_z = ""
      grd_vendedores = self.wTree.get_widget("grd_vendedores")
      selection = grd_vendedores.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, colcodigo_z)
      self.busca_vnd("0", codigo_z)
      btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
      btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
      btn_aceptar.connect  ("clicked", self.on_btn_aceptar_clicked)
      btn_cancelar.connect ("clicked", self.on_btn_cancelar_clicked)

  def on_btn_borra_clicked(self, widget):
      global modo_z
      modo_z = BORRAR
      colcodigo_z = 0
      colnombre_z = 1
      codigo_z = ""
      nombre_z = ""
      grd_vendedores = self.wTree.get_widget("grd_vendedores")
      selection = grd_vendedores.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, colcodigo_z)
          nombre_z = self.lista_vendedores.get_value(selection_iter, colnombre_z)
      resp_z = utils.yesnodlg("Seguro de Eliminar este Mayorista ?" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from mayoris where codigo='" + codigo_z + "'" 
         sql_z = sql_z + " and cia= " + utils.IntToStr(cia_z)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         def_tablas.commit_trans(mydb)
         self.llena_vendedores()
        #End if
# --- Finde on_btn_borra_clicked(self, widget): ---------

  def on_grd_vendedor_activate(self, widget, row=None, value=None):
      colcodigo_z = 0
      codigo_z = ""
      grd_vendedor = widget
      selection = grd_vendedor.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, colcodigo_z)
          arch_dlg_datosmay = dirprogs_z + "altamay.glade"
          self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
          self.busca_vnd("0", codigo_z)
          btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
          btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
          btn_cancelar.set_child_visible(False)
          btn_aceptar.connect  ("clicked", self.on_btn_cancelar_clicked)
          btn_aceptar.grab_focus();
      #Fin de if
  # --- Fin de on_btn_borra_clicked(self, widget): ---------

  def on_btn_cancelar_clicked(self, widget):
      win_altaalm = self.dlg_datosalm.get_widget("win_altamay")
      win_altaalm.destroy()

  def on_btn_aceptar_clicked(self, widget):
      global modo_z
      sql_z = ''
      self.okcancel = True
      win_altaalm = self.dlg_datosalm.get_widget("win_altamay")

      mayoris['codigo']  = self.dlg_datosalm.get_widget("edt_codigo").get_text().upper()
      mayoris['nombre']  = self.dlg_datosalm.get_widget("edt_nombre").get_text().upper()
      mayoris['direc']   = self.dlg_datosalm.get_widget("edt_direc").get_text().upper()
      mayoris['cia']     = cia_z
      mayoris['nombre2'] = self.dlg_datosalm.get_widget("edt_nombre2").get_text().upper()
      mayoris['nompag1'] = self.dlg_datosalm.get_widget("edt_nompagare").get_text().upper()
      mayoris['nompag2'] = self.dlg_datosalm.get_widget("edt_nompag2").get_text().upper()
      mayoris['dirpag1'] = self.dlg_datosalm.get_widget("edt_dirpagare").get_text().upper()
      mayoris['dirpag2'] = self.dlg_datosalm.get_widget("edt_dirpag2").get_text().upper()
      mayoris['ciupag']  = self.dlg_datosalm.get_widget("edt_ciupagare").get_text().upper()
      mayoris['ciu']     = self.dlg_datosalm.get_widget("edt_ciudad").get_text().upper()
      mayoris['rfc']     = self.dlg_datosalm.get_widget("edt_rfc").get_text().upper()
      mayoris['pdsc']    = utils.StrToFloat(self.dlg_datosalm.get_widget("edt_factordsc").get_text())
      mayoris['tel']     = self.dlg_datosalm.get_widget("edt_telefono").get_text()
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
      win_altaalm.destroy()
      self.llena_vendedores()
## ----- Fin de on_btn_aceptar_clicked(self, widget): --------------

  def llena_vendedores(self):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      sql_z = "select codigo, nombre, direc from mayoris where cia = " + repr(cia_z) + " order by codigo"
      cursor.execute(sql_z)
      result = cursor.fetchall()
      self.lista_vendedores.clear()
      for record in result:
          self.lista_vendedores.append([ record[0], record[1], record[2] ])
## ----- Fin de Llena Vendedores --------------
      
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
      elif hacia_z == '0':
        sql_z = sql_z + "codigo = '" + codigo_z + "'"
        sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
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
      self.dlg_datosalm.get_widget("edt_codigo").set_text(utils.convierte_string(mayoris['codigo']))
      self.dlg_datosalm.get_widget("edt_nombre").set_text(utils.convierte_string(mayoris['nombre']))
      self.dlg_datosalm.get_widget("edt_nombre2").set_text(utils.convierte_string(mayoris['nombre2']))
      self.dlg_datosalm.get_widget("edt_direc").set_text(utils.convierte_string(mayoris['direc']))
      self.dlg_datosalm.get_widget("edt_ciudad").set_text(utils.convierte_string(mayoris['ciu']))
      self.dlg_datosalm.get_widget("edt_rfc").set_text(utils.convierte_string(mayoris['rfc']))
      self.dlg_datosalm.get_widget("edt_telefono").set_text(utils.convierte_string(mayoris['tel']))
      self.dlg_datosalm.get_widget("edt_nompagare").set_text(utils.convierte_string(mayoris['nompag1']))
      self.dlg_datosalm.get_widget("edt_nompag2").set_text(utils.convierte_string(mayoris['nompag2']))
      self.dlg_datosalm.get_widget("edt_dirpagare").set_text(utils.convierte_string(mayoris['dirpag1']))
      self.dlg_datosalm.get_widget("edt_dirpag2").set_text(utils.convierte_string(mayoris['dirpag2']))
      self.dlg_datosalm.get_widget("edt_ciupagare").set_text(utils.convierte_string(mayoris['ciupag']))
      self.dlg_datosalm.get_widget("edt_factordsc").set_text(utils.currency(mayoris['pdsc']))

  def limpia_campos(self):
      campos_z = [ "edt_codigo", "edt_nombre", "edt_nombre2", "edt_direc", \
      "edt_ciudad", "edt_rfc", "edt_telefono", "edt_factordsc", \
      "edt_nompag2", "edt_dirpag2", "edt_nompagare", "edt_dirpagare", "edt_ciupagare" ]
      for micampo_z in campos_z:
          self.wTree.get_widget(micampo_z).set_text('')

# --- Fin de limpia_campos(self): -----

  def editable_onoff(self, modo):
      campos_z = []
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
   hwg.wTree.get_widget("win_altavnd").connect("destroy", gtk.main_quit )
   gtk.main()

def main():
    global mydb
    gtk.main()
    return 0
