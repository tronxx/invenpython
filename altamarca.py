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
global inv_marcas
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
inv_marcas = def_tablas.define_inv_marcas()
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

class Altamarca:
  """Esta es una aplicación Alta Marcas"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "altavnd.glade"
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

    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_altavnd")
    miwin.set_title(cias['razon'] + " Mantenimiento de Marcas")
    self.editable_onoff(False)

    self.lista_vendedores = gtk.ListStore(str, str)
    grd_vendedores = self.wTree.get_widget("grd_vendedores")
    grd_vendedores.set_model(self.lista_vendedores)
    columnas_z = ["Codigo", "Marca" ]
    
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
    grd_vendedores.connect("cursor-changed", self.get_seleccion)
   

  def on_btn_primero_clicked(self, widget):
      self.busca_vnd("P")

  def on_btn_anter_clicked(self, widget):
      self.busca_vnd("A", inv_marcas['codigo'])

  def on_btn_sigte_clicked(self, widget):
      self.busca_vnd("S", inv_marcas['codigo'])

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
      codigo_z = inv_marcas['codigo']
      nombre_z = inv_marcas['marca']
      resp_z = utils.yesnodlg("Seguro de Eliminar esta Marca ?\n" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from inv_marcas where codigo='" + codigo_z + "'"
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         def_tablas.commit_trans(mydb)
         self.llena_vendedores()
        #End if

  def on_btn_cancelar_clicked(self, widget):
      self.editable_onoff(False)

  def on_btn_aceptar_clicked(self, widget):
      self.editable_onoff(False)
      global modo_z
      sql_z = ''
      self.okcancel = True
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")

      inv_marcas['codigo']   = edt_codigo.get_text().upper()
      inv_marcas['marca']  = edt_nombre.get_text().upper()
      if modo_z == NUEVO:
         sigid_z = def_tablas.busca_sigte(mydb, "", "", 0, 0, def_tablas.INV_MARCAS)
         sql_z = "insert into inv_marcas ( idmarcainv, codigo, marca ) values ( "
         sql_z = sql_z + str(sigid_z) + " ,"
         sql_z = sql_z + "'" + inv_marcas['codigo'] + "',"
         sql_z = sql_z + "'" + inv_marcas['marca'] + "')"
          
      elif modo_z == MODIFICA:
         sql_z = "update inv_marcas set "
         sql_z = sql_z + "marca = '" + inv_marcas['marca'] + "'"
         sql_z = sql_z + " where codigo = '" + inv_marcas['codigo'] + "'"
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
      self.llena_vendedores()

  def llena_vendedores(self):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      sql_z = "SELECT codigo, marca from inv_marcas order by codigo "
      cursor.execute(sql_z)
      result = cursor.fetchall()
      self.lista_vendedores.clear()
      for record in result:
          self.lista_vendedores.append([ record[0], record[1] ])

  def busca_vnd(self, hacia_z, codigo_z=''):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      sql_z = "SELECT codigo, nombre from inv_marcas where "
      if hacia_z == 'P':
        sql_z = sql_z + "codigo = ( select min(codigo) from inv_marcas)"
      elif hacia_z == 'U':
        sql_z = sql_z + "codigo = ( select max(codigo) from inv_marcas)"
      elif hacia_z == 'A':
        sql_z = sql_z + "codigo = ( select max(codigo) from inv_marcas where codigo < '" + codigo_z + "')"
      elif hacia_z == 'S':
        sql_z = sql_z + "codigo = ( select min(codigo) from inv_marcas where codigo > '" + codigo_z + "')"
# execute SQL statement
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        inv_marcas['codigo']    = record[0]
        inv_marcas['marca']  = record[1]
        self.despliega_datos()

  def despliega_datos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")

      edt_codigo.set_text  (inv_marcas['codigo'])
      edt_nombre.set_text  (inv_marcas['marca'])

  def limpia_campos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")

  def get_seleccion(self, widget, data=None, data2=None):
      grd_vendedores = self.wTree.get_widget("grd_vendedores")
      selection = grd_vendedores.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, 0)
          nombre_z = self.lista_vendedores.get_value(selection_iter, 1)
          inv_marcas['codigo'] = codigo_z;
          inv_marcas['marca'] = nombre_z;
          self.despliega_datos()

  def limpia_campos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_codigo.set_text  ('')
      edt_nombre.set_text  ('')

  def editable_onoff(self, modo):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      btn_aceptar      = self.wTree.get_widget("btn_aceptar")
      btn_cancel  = self.wTree.get_widget("btn_cancelar")
      btn_nuevo   = self.wTree.get_widget("btn_nuevo")
      btn_modif   = self.wTree.get_widget("btn_modif")
      btn_borra   = self.wTree.get_widget("btn_borra")
    
      edt_codigo.set_editable(modo)
      edt_nombre.set_editable(modo)
      btn_aceptar.set_child_visible(modo)
      btn_cancel.set_child_visible(modo)
      btn_nuevo.set_child_visible(not(modo))
      btn_modif.set_child_visible(not(modo))
      btn_borra.set_child_visible(not(modo))

if __name__ == "__main__":
   hwg = Altamarca()
   hwg.wTree.get_widget("win_altavnd").connect("destroy", gtk.main_quit )
   gtk.main()

def main():

    gtk.main()
    return 0
