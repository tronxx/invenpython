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
global poblacs
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
poblacs = def_tablas.define_poblacs()
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

class Altapob:
  """Esta es una aplicación Mantenimiento de Poblaciones"""
       
  def __init__(self, tipo_z=def_tablas.POBLACIONES):
       
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
    global vendedor
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
    self.asigna_tipo(tipo_z)

    self.lista_vendedores = gtk.ListStore(str, str)
    grd_vendedores = self.wTree.get_widget("grd_vendedores")
    grd_vendedores.set_model(self.lista_vendedores)
    columnas_z = ["Nombre", "Codigo" ]
    
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
   
  def asigna_tipo (self, tipo_z):
      self.tipent_z = tipo_z
      if tipo_z == def_tablas.POBLACIONES:
         titulo_z = "Manto Poblaciones"
      elif tipo_z == def_tablas.VENDEDOR:
         titulo_z = "Manto Vendedores"
      elif tipo_z == def_tablas.INV_SITUACIONES:
         titulo_z = "Manto Situaciones"
      elif tipo_z == def_tablas.INV_MARCAS:
         titulo_z = "Manto Marcas"
      #End if
      miwin = self.wTree.get_widget("win_altavnd")
      miwin.set_title(cias['razon'] + " " + titulo_z)
  #End Asigna tipo

  def on_btn_nuevo_clicked(self, widget):
      global modo_z
      modo_z = NUEVO
      arch_dlg_datosmay = dirprogs_z + "altavnd.glade"
      self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
      edt_nombre = self.dlg_datosalm.get_widget("edt_nombre")
      if (self.tipent_z == def_tablas.INV_SITUACIONES) or \
         (self.tipent_z == def_tablas.POBLACIONES):
         self.dlg_datosalm.get_widget("lbl_codigo").set_child_visible(False)
         self.dlg_datosalm.get_widget("edt_codigo").set_child_visible(False)
         edt_nombre.grab_focus()

      ## End if
      btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
      btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
      btn_aceptar.connect  ("clicked", self.on_btn_aceptar_clicked)
      btn_cancelar.connect ("clicked", self.on_btn_cancelar_clicked)

  def on_btn_modif_clicked(self, widget):
      global modo_z
      modo_z = MODIFICA
      arch_dlg_datosmay = dirprogs_z + "altavnd.glade"
      self.dlg_datosalm = gtk.glade.XML(arch_dlg_datosmay)
      edt_codigo = self.dlg_datosalm.get_widget("edt_codigo")
      edt_nombre = self.dlg_datosalm.get_widget("edt_nombre")
      colcodigo_z = 1
      colnombre_z = 0
      codigo_z = ""
      nombre_z = ""
      grd_vendedores = self.wTree.get_widget("grd_vendedores")
      selection = grd_vendedores.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, colcodigo_z)
          nombre_z = self.lista_vendedores.get_value(selection_iter, colnombre_z)
          edt_codigo.set_text(utils.convierte_string(codigo_z))
          edt_nombre.set_text(utils.convierte_string(nombre_z))

      if (self.tipent_z == def_tablas.INV_SITUACIONES) or \
         (self.tipent_z == def_tablas.POBLACIONES):
         self.dlg_datosalm.get_widget("lbl_codigo").set_child_visible(False)
         self.dlg_datosalm.get_widget("edt_codigo").set_child_visible(False)
      ## End if
      btn_aceptar  = self.dlg_datosalm.get_widget("btn_ok")
      btn_cancelar = self.dlg_datosalm.get_widget("btn_cancel")
      btn_aceptar.connect  ("clicked", self.on_btn_aceptar_clicked)
      btn_cancelar.connect ("clicked", self.on_btn_cancelar_clicked)
      edt_nombre.grab_focus();
  ## Fin de def on_btn_modif_clicked(self, widget):


  def on_btn_borra_clicked(self, widget):
      codigo_z = poblacs['numero']
      nombre_z = poblacs['nombre']
      resp_z = utils.yesnodlg("Seguro de Eliminar ?\n" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         if self.tipent_z == def_tablas.POBLACIONES:
            sql_z = "delete from poblacs where numero=" + str(codigo_z)
         elif self.tipent_z == def_tablas.INV_SITUACIONES:
            sql_z = "delete from inv_situaciones where idsituac=" + str(codigo_z)
         elif self.tipent_z == def_tablas.VENDEDOR:
            sql_z = "delete from vendedor where codigo='" + codigo_z + "'"
         elif self.tipent_z == def_tablas.INV_MARCAS:
            sql_z = "delete from inv_marcas where codigo='" + codigo_z + "'"
         
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         def_tablas.commit_trans(mydb)
         self.llena_vendedores()
      #End if

  def on_btn_cancelar_clicked(self, widget):
      win_altaalm = self.dlg_datosalm.get_widget("win_altavnd")
      win_altaalm.destroy()

  def on_btn_aceptar_clicked(self, widget):
      global modo_z
      sql_z = ''
      self.okcancel = True
      edt_codigo  = self.dlg_datosalm.get_widget("edt_codigo")
      edt_nombre  = self.dlg_datosalm.get_widget("edt_nombre")
      nombre_z    = edt_nombre.get_text().upper()
      codigo_z    = edt_codigo.get_text().upper()

      if modo_z == NUEVO:
        if self.tipent_z == def_tablas.INV_SITUACIONES:
           def_tablas.busca_iddato(mydb, nombre_z, def_tablas.INV_SITUACIONES)
        elif self.tipent_z == def_tablas.POBLACIONES:
           def_tablas.busca_iddato(mydb, nombre_z, def_tablas.POBLACIONES)
        elif self.tipent_z == def_tablas.VENDEDOR:
           sql_z = "insert into vendedor (  codigo, nombre ) values ( "
           sql_z = sql_z + "'" + codigo_z + "', "
           sql_z = sql_z + "'" + nombre_z + "') "
           def_tablas.start_trans(mydb)
           cursor = mydb.cursor()
           cursor.execute(sql_z)
           def_tablas.commit_trans(mydb)
        elif self.tipent_z == def_tablas.INV_MARCAS:
           idmarcainv_z = def_tablas.busca_sigte("", "", 0, 0, def_tablas.INV_MARCAS)
           sql_z = "insert into inv_marcas ( idmarcainv, codigo, descri ) values ( "
           sql_z = sql_z + utils.IntToStr(idmarcainv_z) + ","
           sql_z = sql_z + "'" + codigo_z + "', "
           sql_z = sql_z + "'" + nombre_z + "') "
           def_tablas.start_trans(mydb)
           cursor = mydb.cursor()
           cursor.execute(sql_z)
           def_tablas.commit_trans(mydb)
        #End if
      elif modo_z == MODIFICA:
        if self.tipent_z == def_tablas.POBLACIONES:
            sql_z = "update poblacs set "
            sql_z = sql_z + "nombre = '" + nombre_z + "'"
            sql_z = sql_z + " where numero = " + str(utils.StrToInt(codigo_z))
        elif self.tipent_z == def_tablas.INV_SITUACIONES:
            sql_z = "update inv_situaciones set "
            sql_z = sql_z + "situacion = '" + nombre_z + "'"
            sql_z = sql_z + " where idsituac = " + str(utils.StrToInt(codigo_z))
        elif self.tipent_z == def_tablas.VENDEDOR:
            sql_z = "update vendedor set "
            sql_z = sql_z + "nombre = '" + nombre_z + "'"
            sql_z = sql_z + " where codigo = '" + codigo_z + "'"
        elif self.tipent_z == def_tablas.INV_MARCAS:
            sql_z = "update inv_marcainv set "
            sql_z = sql_z + "descri = '" + nombre_z + "'"
            sql_z = sql_z + " where codigo = '" + codigo_z + "'"
        #End if
        def_tablas.start_trans(mydb)
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        def_tablas.commit_trans(mydb)
      #End if
      win_altaalm = self.dlg_datosalm.get_widget("win_altavnd")
      win_altaalm.destroy()
      self.llena_vendedores()
  #End on_btn_aceptar_clicked(self, widget)

  def llena_vendedores(self):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      if self.tipent_z == def_tablas.POBLACIONES:
         sql_z = "SELECT nombre, numero FROM poblacs order by nombre "
      if self.tipent_z == def_tablas.INV_SITUACIONES:
         sql_z = "SELECT situacion, idsituac FROM inv_situaciones order by situacion "
      elif self.tipent_z == def_tablas.VENDEDOR:
         sql_z = "SELECT nombre, codigo FROM vendedor order by nombre "
      elif self.tipent_z == def_tablas.INV_MARCAS:
         sql_z = "SELECT descri, codigo FROM inv_marcainv order by descri "
      #End if
      cursor.execute(sql_z)
      result = cursor.fetchall()
      self.lista_vendedores.clear()
      for record in result:
          self.lista_vendedores.append([ record[0], record[1] ])

  def despliega_datos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_codigo.set_text  (str(poblacs['numero']))
      edt_nombre.set_text  (poblacs['nombre'])

if __name__ == "__main__":
   hwg = Altapob()
   hwg.wTree.get_widget("win_altavnd").connect("destroy", gtk.main_quit )
   gtk.main()

def main():
    gtk.main()
    return 0
