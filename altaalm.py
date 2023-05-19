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
import def_tablas
import utils
platform = sys.platform 

global mydb
global cia_z
global mibd
global cias
global almacen
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
almacen = def_tablas.define_almacen()
if mibd['tipobd'] == "MYSQL":
   try:
     import MySQLdb
   except:
     print "No pudo importar librerias MySQLdb \n"
     sys.exit(1)
elif mibd['tipobd'] == "ODBC":
   try:
     import pyodbc
   except:
     print "No pudo importar librerias ODBC \n"
     sys.exit(1)
elif mibd['tipobd'] == "SOLID":
   try:
     import Solid
   except:
     print "No pudo importar librerias Solid de Solid \n"
     sys.exit(1)

class Altavnd:
  """Esta es una aplicación Alta Almacenes"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "pantalla_gral.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_nuevo_clicked": self.on_btn_nuevo_clicked, \
            "on_btn_modif_clicked": self.on_btn_modif_clicked, \
            "on_btn_borra_clicked": self.on_btn_borra_clicked, \
            "on_btn_aceptar_clicked": self.on_btn_aceptar_clicked, \
            "on_btn_cancelar_clicked": self.on_btn_cancelar_clicked
            }
#                "on_win_altavnd_destroy": gtk.main_quit }
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
    elif mibd['tipobd'] == "SOLID":
       dsn_z = mibd['base']+" " + mibd['user']+" "+mibd['password']
       mydb = Solid.DB(dsn_z)

    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_altavnd")
    miwin.set_title(cias['razon'] + " Mantenimiento de Almacenes")
    self.editable_onoff(False)

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


  def on_btn_primero_clicked(self, widget):
      self.busca_vnd("P")

  def on_btn_anter_clicked(self, widget):
      self.busca_vnd("A", vendedor['codigo'])

  def on_btn_sigte_clicked(self, widget):
      self.busca_vnd("S", vendedor['codigo'])

  def on_btn_ultimo_clicked(self, widget):
      self.busca_vnd("U")

  def on_btn_nuevo_clicked(self, widget):
      global modo_z
      modo_z = NUEVO
      arch_dlg_datosalm = dirprogs_z + "altaalm.glade"
      self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosalm)
      btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
      btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
      btn_aceptar.connect  ("clicked", self.on_btn_aceptar_clicked)
      btn_cancelar.connect ("clicked", self.on_btn_cancelar_clicked)

  def on_btn_modif_clicked(self, widget):
      global modo_z
      modo_z = MODIFICA
      modo_z = NUEVO
      arch_dlg_datosmay = dirprogs_z + "altaalm.glade"
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
      codigo_z = vendedor['codigo']
      nombre_z = vendedor['nombre']
      resp_z = utils.yesnodlg("Seguro de Eliminar este Almacén: " + nombre_z + " ?")
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from almacen where clave='" + codigo_z + "' and cia = " + str(cia_z)
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         def_tablas.commit_trans(mydb)
         self.llena_vendedores()
        #End if
  # --- Fin de on_btn_borra_clicked(self, widget): ---------

  def on_grd_vendedor_activate(self, widget, row=None, value=None):
      colcodigo_z = 0
      codigo_z = ""
      grd_vendedor = widget
      selection = grd_vendedor.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, colcodigo_z)
          arch_dlg_datosmay = dirprogs_z + "altaalm.glade"
          self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
          self.busca_vnd("0", codigo_z)
          btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
          btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
          btn_cancelar.set_child_visible(False)
          btn_aceptar.connect  ("clicked", self.on_btn_cancelar_clicked)
          btn_aceptar.grab_focus();
      #Fin de if
  # --- Fin de on_grd_vendedor_activate ---------


  def on_btn_cancelar_clicked(self, widget):
      win_altaalm = self.dlg_datosalm.get_widget("win_altaalm")
      win_altaalm.destroy()

  def on_btn_aceptar_clicked(self, widget):
      self.editable_onoff(False)
      global modo_z
      sql_z = ''
      self.okcancel = True
      win_altaalm = self.dlg_datosalm.get_widget("win_altaalm")
     
      edt_codigo  = self.dlg_datosalm.get_widget("edt_codigo")
      edt_nombre  = self.dlg_datosalm.get_widget("edt_nombre")
      edt_direc   = self.dlg_datosalm.get_widget("edt_direc")
      edt_ordiary = self.dlg_datosalm.get_widget("edt_ordiary")
      edt_exib    = self.dlg_datosalm.get_widget("edt_exib")
      edt_zona    = self.dlg_datosalm.get_widget("edt_zona")
      edt_ordtab  = self.dlg_datosalm.get_widget("edt_ordtab")

      almacen['clave']   = edt_codigo.get_text().upper()
      if almacen['clave'] == "":
         utils.msgdlg("El Codigo de Almacen no puede estar vacio")
         return
      #End if
      almacen['nombre']  = edt_nombre.get_text().upper()
      almacen['direc']   = edt_direc.get_text().upper()
      almacen['cia']     = cia_z
      almacen['ordiary'] = utils.StrToInt(edt_ordiary.get_text())
      almacen['exib']    = edt_exib.get_text()
      almacen['zona']    = edt_zona.get_text()
      almacen['ordtab']  = utils.StrToInt(edt_ordtab.get_text())
      if modo_z == NUEVO:
         sql_z = "insert into almacen (clave,nombre,direc,sdoini,impent,impsal,sdofin,cia,ordiary,exib,zona,ordtabt) values ( "
         sql_z = sql_z + "'" + almacen['clave'] + "',"
         sql_z = sql_z + "'" + almacen['nombre'] + "',"
         sql_z = sql_z + "'" + almacen['direc'] + "',"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + str(cia_z) + ","
         sql_z = sql_z + str(almacen['ordiary']) + ","
         sql_z = sql_z + "'" + almacen['exib'] + "',"
         sql_z = sql_z + "'" + almacen['zona'] + "',"
         sql_z = sql_z + str(almacen['ordtab']) + ")"
          
      elif modo_z == MODIFICA:
         sql_z = "update almacen set "
         sql_z = sql_z + "nombre = '" + almacen['nombre'] + "',"
         sql_z = sql_z + "direc = '" + almacen['direc'] + "',"
         sql_z = sql_z + "ordiary = " + str(almacen['ordiary']) + ","
         sql_z = sql_z + "exib = '" + almacen['exib'] + "',"
         sql_z = sql_z + "zona = '" + almacen['zona'] + "',"
         sql_z = sql_z + "ordtabt = " + str(almacen['ordtab'])
         sql_z = sql_z + " where clave = '" + almacen['clave'] + "'"
         sql_z = sql_z + " and cia = " + str(cia_z)
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
      win_altaalm.destroy()
      self.llena_vendedores()

  def llena_vendedores(self):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      sql_z = "select clave, nombre, direc from almacen where cia = " + repr(cia_z) + " order by clave"
      cursor.execute(sql_z)
      result = cursor.fetchall()
      self.lista_vendedores.clear()
      for record in result:
          self.lista_vendedores.append([ record[0], record[1], record[2] ])

  def busca_vnd(self, hacia_z, codigo_z=''):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      sql_z = "SELECT clave,nombre,direc,sdoini,impent,impsal,sdofin,\
      cia,ordiary,exib,zona,ordtabt FROM almacen where "
      if hacia_z == 'P':
        sql_z = sql_z + "clave = ( select min(clave) from almacen where cia = "
        sql_z = sql_z + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == 'U':
        sql_z = sql_z + "clave = ( select max(clave) from almacen where cia = "
        sql_z = sql_z + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == 'A':
        sql_z = sql_z + "clave = ( select max(clave) from almacen where clave < '" + codigo_z + "' and cia = "
        sql_z = sql_z + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == 'S':
        sql_z = sql_z + "clave = ( select min(clave) from almacen where clave > '" + codigo_z + "' and cia = "
        sql_z = sql_z + utils.IntToStr(cia_z) + ") and cia = " + utils.IntToStr(cia_z)
      elif hacia_z == '0':
        sql_z = sql_z + "clave =  '" + codigo_z + "' and cia = " + utils.IntToStr(cia_z)
# execute SQL statement
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        almacen['clave']   = record[0]
        almacen['nombre']  = record[1]
        almacen['direc']   = record[2]
        almacen['sdoini']  = record[3]
        almacen['impent']  = record[4]
        almacen['impsal']  = record[5]
        almacen['sdofin']  = record[6]
        almacen['cia']     = record[7]
        almacen['ordiary'] = record[8]
        almacen['exib']    = record[9]
        almacen['ordtabt'] = record[10]
        self.despliega_datos()

  def despliega_datos(self):
      edt_codigo  = self.dlg_datosalm.get_widget("edt_codigo")
      edt_nombre  = self.dlg_datosalm.get_widget("edt_nombre")
      edt_direc   = self.dlg_datosalm.get_widget("edt_direc")
      edt_ordiary = self.dlg_datosalm.get_widget("edt_ordiary")
      edt_exib    = self.dlg_datosalm.get_widget("edt_exib")
      edt_zona    = self.dlg_datosalm.get_widget("edt_zona")
      edt_ordtab  = self.dlg_datosalm.get_widget("edt_ordtab")

      edt_codigo.set_text(utils.convierte_string(almacen['clave']))
      edt_nombre.set_text(utils.convierte_string(almacen['nombre']))
      edt_direc.set_text(utils.convierte_string(almacen['direc']))
      edt_ordiary.set_text(str(utils.convierte_string(almacen['ordiary'])))
      edt_exib.set_text(utils.convierte_string(almacen['exib']))
      edt_zona.set_text(utils.convierte_string(almacen['zona']))
      edt_ordtab.set_text(str(utils.convierte_string(almacen['ordtab'])))

  def limpia_campos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")

  def get_seleccion(self, widget, data=None, data2=None):
      colcodigo_z = 0
      codigo_z = ""
      grd_vendedor = widget
      selection = grd_vendedor.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, colcodigo_z)
          arch_dlg_datosmay = dirprogs_z + "altaalm.glade"
          self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
          self.busca_vnd("0", codigo_z)
          btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
          btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
          btn_cancelar.set_child_visible(False)
          btn_aceptar.connect  ("clicked", self.on_btn_cancelar_clicked)
          btn_aceptar.grab_focus();
      #Fin de if
  # --- Fin de on_btn_borra_clicked(self, widget): ---------

  def limpia_campos(self):
      campo_z = ""

  def editable_onoff(self, modo):
      codigo_z=""

if __name__ == "__main__":
   hwg = Altavnd()
   hwg.wTree.get_widget("win_altavnd").connect("destroy", gtk.main_quit )
   gtk.main()

def main():

    gtk.main()
    return 0
