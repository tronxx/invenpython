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
global zonainv
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
zonainv = def_tablas.define_zonainv()
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

class Altazonas:
  """Esta es una aplicación Alta Zonas de Inventario"""
       
  def __init__(self, tipo_z=def_tablas.ZONASINVEN):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "altazon.glade"
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
    global zonainv
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
    miwin.set_title(cias['razon'] + " Mantenimiento de Zonas")
    self.editable_onoff(False)
    self.asigna_tipo(tipo_z)

    self.lista_vendedores = gtk.ListStore(str, str, str)
    grd_vendedores = self.wTree.get_widget("grd_vendedores")
    grd_vendedores.set_model(self.lista_vendedores)
    if self.tipent_z == def_tablas.ZONASINVEN:
       columnas_z = ["Zona", "Nombre", "Tipo" ]
    elif self.tipent_z == def_tablas.INV_GRUPOS:
       columnas_z = ["Codigo", "Nombre", "Imprimible" ]
    elif self.tipent_z == def_tablas.GPODIARY:
       columnas_z = ["Codigo", "Nombre", "Imprimible" ]
    
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

  def asigna_tipo (self, tipo_z):
      self.tipent_z = tipo_z
      if tipo_z == def_tablas.ZONASINVEN:
         titulo_z = "Manto Zonas"
         self.wTree.get_widget("lbl_carac").set_text(" Tipo")
      elif tipo_z == def_tablas.INV_GRUPOS:
         titulo_z = "Manto Grupos Artdesp"
         self.wTree.get_widget("lbl_carac").set_text(" Imprimible")
      elif tipo_z == def_tablas.GPODIARY:
         titulo_z = "Manto Grupos Diary"
         self.wTree.get_widget("lbl_carac").set_text(" Imprimible")
      #End if
  #End Asigna tipo
  
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
      codigo_z = zonainv['zona']
      nombre_z = zonainv['nombre']
      resp_z = utils.yesnodlg("Seguro de Eliminar ? \n" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         if self.tipent_z == def_tablas.ZONASINVEN:
            sql_z = "delete from zonainv where zona ='" + codigo_z + "'"
         elif self.tipent_z == def_tablas.INV_GRUPOS:
            sql_z = "delete from inv_grupos where codigo ='" + codigo_z + "'"
            sql_z = sql_z + " and cia =" + str(cia_z)
         elif self.tipent_z == def_tablas.GPODIARY:
            sql_z = "delete from gpodiary where grupo ='" + codigo_z + "'"
            sql_z = sql_z + " and cia =" + str(cia_z)
         #End if
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
      tipo_z = self.wTree.get_widget("edt_tipo").get_text()
      if self.tipent_z == def_tablas.ZONASINVEN:
         if tipo_z <> "1" and tipo_z <> "2":
            utils.msgdlg("El tipo de ser 1=Ventas 2=Cancelaciones")
            return (-1)
         #End if
      elif self.tipent_z == def_tablas.INV_GRUPOS:
         if tipo_z <> "S" and tipo_z <> "N":
            txt_z = "Este campo define si se imprime En el reporte de Articulos desplazados\n"
            txt_z = txt_z + "y debe ser S=Si se imprime, N=No se imprime" 
            utils.msgdlg(txt)
            return (-1)
         #End if
      elif self.tipent_z == def_tablas.GPODIARY:
         if tipo_z <> "S" and tipo_z <> "N":
            txt_z = "Este campo define si se imprime En el reporte de Diary\n"
            txt_z = txt_z + "y debe ser S=Si se imprime, N=No se imprime" 
            utils.msgdlg(txt)
            return (-1)
         #End if
      #End if

      zonainv['zona']   =  self.wTree.get_widget("edt_codigo").get_text().upper()
      zonainv['nombre']  = self.wTree.get_widget("edt_nombre").get_text().upper()
      zonainv['tipo']    = tipo_z
      if modo_z == NUEVO:
         if self.tipent_z == def_tablas.ZONASINVEN:
            sql_z = "insert into zonainv ( zona, nombre, tipo ) values ( "
            sql_z = sql_z + "'" + zonainv['zona'] + "',"
            sql_z = sql_z + "'" + zonainv['nombre'] + "', "
            sql_z = sql_z + "'" + zonainv['tipo'] + "')"
         elif self.tipent_z == def_tablas.INV_GRUPOS:
            idgrupo_z = def_tablas.busca_sigte(mydb, "", "", 0, cia_z, def_tablas.INV_GRUPOS)
            sql_z = "insert into inv_grupos (idgrupo,codigo,descri,impri,cia) values ( "
            sql_z = sql_z + str(idgrupo_z) + ","
            sql_z = sql_z + "'" + zonainv['zona'] + "',"
            sql_z = sql_z + "'" + zonainv['nombre'] + "', "
            sql_z = sql_z + "'" + zonainv['tipo'] + "',"
            sql_z = sql_z + str(cia_z) + ")"
         elif self.tipent_z == def_tablas.GPODIARY:
            idgrupo_z = def_tablas.busca_sigte(mydb, "", "", 0, cia_z, def_tablas.GPODIARY)
            sql_z = "insert into gpodiary (idgpodiary,grupo,descri,imprime,cia) values ( "
            sql_z = sql_z + str(idgrupo_z) + ","
            sql_z = sql_z + "'" + zonainv['zona'] + "',"
            sql_z = sql_z + "'" + zonainv['nombre'] + "', "
            sql_z = sql_z + "'" + zonainv['tipo'] + "',"
            sql_z = sql_z + str(cia_z) + ")"
         #Fin de If         
      elif modo_z == MODIFICA:
         if self.tipent_z == def_tablas.ZONASINVEN:
            sql_z = "update zonainv set "
            sql_z = sql_z + "nombre = '" + zonainv['nombre'] + "',"
            sql_z = sql_z + " tipo = '" + zonainv['tipo'] + "',"
            sql_z = sql_z + " where zona = '" + zonainv['zona'] + "'"
         elif self.tipent_z == def_tablas.INV_GRUPOS:
            sql_z = "update inv_grupos set "
            sql_z = sql_z + " descri = '" + zonainv['nombre'] + "',"
            sql_z = sql_z + " impri = '" + zonainv['tipo'] + "' "
            sql_z = sql_z + " where codigo = '" + zonainv['zona'] + "'"
            sql_z = sql_z + " and cia = " + str(cia_z)
         elif self.tipent_z == def_tablas.GPODIARY:
            sql_z = "update gpodiary set "
            sql_z = sql_z + " descri = '" + zonainv['nombre'] + "',"
            sql_z = sql_z + " imprime = '" + zonainv['tipo'] + "' "
            sql_z = sql_z + " where grupo = '" + zonainv['zona'] + "'"
            sql_z = sql_z + " and cia = " + str(cia_z)
         #End if
      #End if
      cursor = mydb.cursor()
      def_tablas.start_trans(mydb)
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
      self.llena_vendedores()

  def llena_vendedores(self):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      if self.tipent_z == def_tablas.ZONASINVEN:
         sql_z = "SELECT zona, nombre, tipo FROM zonainv order by zona "
      elif self.tipent_z == def_tablas.INV_GRUPOS:
         sql_z = "SELECT codigo, descri, impri FROM inv_grupos order by codigo "
      elif self.tipent_z == def_tablas.GPODIARY:
         sql_z = "SELECT grupo, descri, imprime FROM gpodiary order by grupo"
      #End if
      cursor.execute(sql_z)
      result = cursor.fetchall()
      self.lista_vendedores.clear()
      for record in result:
          self.lista_vendedores.append([ record[0], record[1], record[2] ])

  def despliega_datos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")

      edt_codigo.set_text  (zonainv['zona'])
      edt_nombre.set_text  (zonainv['nombre'])
      self.wTree.get_widget("edt_tipo").set_text(zonainv['tipo'])

  def get_seleccion(self, widget, data=None, data2=None):
      grd_vendedores = self.wTree.get_widget("grd_vendedores")
      selection = grd_vendedores.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lista_vendedores.get_value(selection_iter, 0)
          nombre_z = self.lista_vendedores.get_value(selection_iter, 1)
          tipo_z   = self.lista_vendedores.get_value(selection_iter, 2)
          zonainv['zona'] = codigo_z;
          zonainv['nombre'] = nombre_z;
          zonainv['tipo'] = tipo_z;
          self.despliega_datos()

  def limpia_campos(self):
      campos_z = [ "edt_codigo", "edt_nombre", "edt_tipo" ]
      for micampo_z in campos_z:
          self.wTree.get_widget(micampo_z).set_text("")

  def editable_onoff(self, modo):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_tipo    = self.wTree.get_widget("edt_nombre")
      btn_aceptar = self.wTree.get_widget("btn_aceptar")
      btn_cancel  = self.wTree.get_widget("btn_cancelar")
      btn_nuevo   = self.wTree.get_widget("btn_nuevo")
      btn_modif   = self.wTree.get_widget("btn_modif")
      btn_borra   = self.wTree.get_widget("btn_borra")
    
      edt_codigo.set_editable(modo)
      edt_nombre.set_editable(modo)
      edt_tipo.set_editable(modo)
      edt_tipo.set_editable(modo)
      btn_aceptar.set_child_visible(modo)
      btn_cancel.set_child_visible(modo)
      btn_nuevo.set_child_visible(not(modo))
      btn_modif.set_child_visible(not(modo))
      btn_borra.set_child_visible(not(modo))

if __name__ == "__main__":
   hwg = Altazonas()
   hwg.wTree.get_widget("win_altavnd").connect("destroy", gtk.main_quit )
   gtk.main()

def main():
    gtk.main()
    return 0
