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
  
import utils
import altavnd
import altaalm
import altaptov
import altamay
import capentes
import capentpro
import capsales
import captrasp
import altainv
import capmvint
import hazfacma
import polcobma
import polcampre
import capped
import altazon
import altapob
import altamarca
import def_tablas

global mydb
global cia_z
global mibd
global cias
global vendedor
global ventanas_abiertas_z
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

class Menu:
  """Esta es una aplicación Alta Almacenes"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "menu.glade"
    self.wTree = gtk.glade.XML(self.gladefile)

    dic = { "on_vendedores1_activate": self.on_vendedores1_activate, \
            "on_almacenes1_activate":self.on_almacenes1_activate, \
            "on_punto_de_venta1_activate":self.on_punto_de_venta1_activate, \
            "on_zonas1_activate":self.on_zonas1_activate, \
            "on_situaciones1_activate":self.on_situaciones1_activate, \
            "on_grupos1_activate":self.on_grupos1_activate, \
            "on_grupos_diary1_activate":self.on_grupos_diary1_activate, \
            "on_marcas1_activate":self.on_marcas1_activate, \
            "on_poblaciones1_activate":self.on_poblaciones1_activate, \
            "on_mayoristas1_activate":self.on_mayoristas1_activate, \
            "on_capentes1_activate":self.on_capentes1_activate, \
            "on_cancelaciones_tradicionales1_activate":self.on_cancelaciones_tradicionales1_activate, \
            "on_cancel_fon_activate":self.on_cancel_fon_activate, \
            "on_sabana_fonacot1_activate":self.on_sabana_fonacot1_activate, \
            "on_capsales1_activate":self.on_capsales1_activate, \
            "on_salidas_mayoreo1_activate":self.on_salidas_mayoreo1_activate, \
            "on_capvtas_trad_activate":self.on_capvtas_trad_activate, \
            "on_traspasos1_activate":self.on_traspasos1_activate, \
            "on_devalm_activate":self.on_devalm_activate, \
            "on_movint_activate":self.on_movint_activate, \
            "on_inven1_activate":self.on_inven1_activate, \
            "on_compras1_activate":self.on_compras1_activate, \
            "on_canxcamtrad_activate":self.on_canxcamtrad_activate, \
            "on_polcob_may_activate":self.on_polcob_may_activate, \
            "on_polcampre_activate":self.on_polcampre_activate, \
            "on_factur_may_activate":self.on_factur_may_activate, \
            "on_pedido_may_activate":self.on_pedido_may_activate, \
            "on_pedido_prove_activate":self.on_pedido_prove_activate, \
            "on_cerrar_ventana_activa1_activate":self.cierra_tabactual, \
            "on_salir1_activate":  gtk.main_quit , \
            "on_win_menu_destroy_event": gtk.main_quit }
    self.wTree.signal_autoconnect(dic)
    self.ventanas_abiertas_z = []
    global cias
    global cia_z
    cia_z = 1
    cias_lines = []
    miwin = self.wTree.get_widget("win_menu")
    miwin.connect("destroy", gtk.main_quit)
    #self.wTree.get_widget("on_cerrar_ventana_activa1_activate", self.cierra_tabactual)
    self.notebook=gtk.Notebook()
    self.notebook.set_tab_pos(gtk.POS_TOP)
    self.notebook.set_scrollable(True)
    vbox_main = self.wTree.get_widget("vbox_main")
    #vbox_main = self.wTree.get_widget("viewport1")
    vbox_main.pack_start(self.notebook, True, True, 0)
    vbox_main.show()

    self.wingroup = gtk.WindowGroup()
    self.wingroup.add_window(miwin)

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
    miwin.set_title(cias['razon'] + " Menu Principal Inventarios")

  def on_vendedores1_activate(self, widget):
      self.activa_manto("VENDEDORES", "Manto de Vendedores", "win_altavnd")
  #Fin on_vendedores1_activate

  def on_poblaciones1_activate(self, widget):
      self.activa_manto("POBLACS", "Manto de Poblaciones", "win_altavnd")
  #Fin on_vendedores1_activate

  def on_situaciones1_activate(self, widget):
      self.activa_manto("SITUACS", "Manto de Situaciones", "win_altavnd")
  #Fin on_vendedores1_activate

  def on_almacenes1_activate(self, widget):
      self.activa_manto("ALMACENES", "Manto de Almacenes", "win_altaalm")
  #Fin on_almacenes1_activate

  def on_zonas1_activate(self, widget):
      self.activa_manto("ZONAS", "Manto de Zonas", "win_altavnd")
  #Fin on_almacenes1_activate

  def on_grupos1_activate(self, widget):
      self.activa_manto("GRUPOS", "Manto de Grupos", "win_altavnd")
  #Fin on_almacenes1_activate

  def on_grupos_diary1_activate(self, widget):
      self.activa_manto("DIARY", "Manto Grupos Diary", "win_altavnd")
  #Fin on_almacenes1_activate

  def on_marcas1_activate(self, widget):
      self.activa_manto("MARCAS", "Manto de Marcas", "win_altavnd")
  #Fin on_almacenes1_activate

  def on_punto_de_venta1_activate(self, widget):
      self.activa_manto("PTOVTA", "Manto de Punto Vta", "win_altaalm")
  #Fin on_almacenes1_activate

  def on_inven1_activate(self, widget):
      self.activa_manto("INVEN", "Mantenimiento de Articulos", "win_altainv")
  #Fin on_almacenes1_activate

  def on_mayoristas1_activate(self, widget):
      self.activa_manto("MAYORISTAS", "Manto de Mayoristas", "win_altamay")
  #Fin on_vendedores1_activate

  def on_factur_may_activate(self, widget):
      self.activa_manto("FACTURMAY", "Facturacion Mayoreo", "win_hazfacma")
  #Fin on_vendedores1_activate

  def on_compras1_activate(self, widget):
      self.activa_manto("COMPRAS", "Entradas Proveedor", "win_capentes")
  #Fin on_vendedores1_activate

  def on_devalm_activate(self, widget):
      self.activa_manto("CAPDEVS", "Devoluciones/Almacenes", "win_captrasp", "D")
  #Fin on_vendedores1_activate

  def on_traspasos1_activate(self, widget):
      self.activa_manto("CAPTRASP", "Traspasos/Almacenes", "win_captrasp", "T")
  #Fin on_vendedores1_activate

  def on_movint_activate(self, widget):
      self.activa_manto("MOVINT", "Movtos Internos", "win_capsales", "I")
  #Fin on_vendedores1_activate

  def on_canxcamtrad_activate(self, widget):
      self.activa_manto("CANXCAMTRAD", "Can x Cam Trad", "win_capsales", "X")
  #Fin on_vendedores1_activate

  def on_sabana_fonacot1_activate(self, widget):
      self.activa_manto("CAPVTAS_FON", "Sabana Vtas Fonacot", "win_capsales", "F")
  #Fin on_vendedores1_activate

  def on_capvtas_trad_activate(self, widget):
      self.activa_manto("CAPVTAS_TRAD", "Sabana Vtas Tradicional", "win_capsales", "V")
  #Fin on_vendedores1_activate

  def on_capsales1_activate(self, widget):
      self.activa_manto("CAPSALES", "Salidas Especiales", "win_capsales", "S")
  #Fin on_vendedores1_activate

  def on_salidas_mayoreo1_activate(self, widget):
      self.activa_manto("CAPSMAY", "Salidas Mayoreo", "win_capsales", "M")
  #Fin on_vendedores1_activate

  def on_capentes1_activate(self, widget):
      self.activa_manto("CAPENTES", "Entradas Especiales", "win_capentes", "P")
  #Fin on_vendedores1_activate

  def on_cancelaciones_tradicionales1_activate(self, widget):
      self.activa_manto("CAPCANCEL", "Cancel Tradicionales", "win_capentes", "C")
  #Fin on_vendedores1_activate

  def on_cancel_fon_activate(self, widget):
      self.activa_manto("CAPCANCELFON", "Cancel FONACOT", "win_capentes", "O")
  #Fin on_vendedores1_activate

  def on_pedido_may_activate(self, widget):
      self.activa_manto("PEDIDOMAY", "Pedidos Mayoreo", "win_capped", "G")
  #Fin on_vendedores1_activate

  def on_pedido_prove_activate(self, widget):
      self.activa_manto("PEDIDOPROVE", "Pedidos Proveedor", "win_capped", "B")
  #Fin on_vendedores1_activate

  def on_polcob_may_activate(self, widget):
      self.activa_manto("POLCOBMA", "Cobranza Mayoreo", "win_polcobma")
  #Fin on_vendedores1_activate

  def on_polcampre_activate(self, widget):
      self.activa_manto("POLCAMPRE", "Cambios de Precio", "win_polcobma")
  #Fin on_vendedores1_activate

  def activa_manto(self, opcion_z="VENDEDORES", titulo_z="", win_z="win_altavnd", tipent_z="-1"):
      if opcion_z in self.ventanas_abiertas_z:
          pagina_z = self.ventanas_abiertas_z.index(opcion_z)
          self.notebook.set_current_page(pagina_z)
          return(-1)
      #End If
      if opcion_z == "VENDEDORES":
         altavend = altapob.Altapob(def_tablas.VENDEDOR)
      elif opcion_z == "POBLACS":
         altavend = altapob.Altapob(def_tablas.POBLACIONES)
      elif opcion_z == "SITUACS":
         altavend = altapob.Altapob(def_tablas.INV_SITUACIONES)
      elif opcion_z == "MAYORISTAS":
         altavend = altamay.Altamay()
      elif opcion_z == "ZONAS":
         altavend = altazon.Altazonas(def_tablas.ZONASINVEN)
      elif opcion_z == "GRUPOS":
         altavend = altazon.Altazonas(def_tablas.INV_GRUPOS)
      elif opcion_z == "DIARY":
         altavend = altazon.Altazonas(def_tablas.GPODIARY)
      elif opcion_z == "MARCAS":
         altavend = altamarca.Altamarca()
      elif opcion_z == "ALMACENES":
         altavend = altaalm.Altaalm()
      elif opcion_z == "PTOVTA":
         altavend = altaptov.Altaptov()
      elif opcion_z == "INVEN":
         altavend = altainv.Altainv()
      elif opcion_z == "COMPRAS":
         altavend = capentpro.Capentpro()
      elif opcion_z == "FACTURMAY":
         altavend = hazfacma.Hazfacma()
      elif opcion_z == "POLCOBMA":
         altavend = polcobma.Polcobma()
      elif opcion_z == "POLCAMPRE":
         altavend = polcampre.Polcampre()
      elif opcion_z in [ "CAPDEVS", "CAPTRASP" ]:
         altavend = captrasp.Captrasp()
         altavend.asigna_tipent(tipent_z)
      elif opcion_z in [ "CANXCAMTRAD", "MOVINT" ]:
         altavend = capmvint.Capmvint()
         altavend.asigna_tipent(tipent_z)
      elif opcion_z in [ "CAPENTES", "CAPCANCEL", "CAPCANCELFON" ]:
         altavend = capentes.Capentes()
         altavend.asigna_tipent(tipent_z)
      elif opcion_z in [ "PEDIDOMAY", "PEDIDOPROVE" ]:
         altavend = capped.Capped()
         altavend.asigna_tipent(tipent_z)
      elif opcion_z in [ "CAPVTAS_FON", "CAPVTAS_TRAD", "CAPSMAY", "CAPSALES" ]:
         altavend = capsales.Capsales()
         altavend.asigna_tipent(tipent_z)
      #End if
      #print opcion_z, ":", titulo_z, ":", win_z, ":", tipent_z

      miwin = altavend.wTree.get_widget(win_z)
      vbox1 = gtk.VBox()
      hbox1 = gtk.HBox()
      vbox_altavnd = altavend.wTree.get_widget("vbox_main")
      miwin.remove(vbox_altavnd)
      # --> Para agregar el boton de cerrado
      #btn_cierra = gtk.Button("Salir")
      #btn_cierra = self.crea_boton("Salir", gtk.STOCK_QUIT)
      #btn_cierra.connect("clicked", self.cierra_tabactual)
      #hbox1.pack_end(btn_cierra, False, True, 0)
      #btn_cierra.show()
      hbox1.show()
      vbox1.pack_start(hbox1, False, False, 0)
      vbox1.show()
      vbox1.pack_start(vbox_altavnd, True, True, 0)
      vbox1.show()
      # --> Para agregar el boton de cerrado
      label = gtk.Label(titulo_z)
      #miven_z = self.notebook.append_page(vbox_altavnd, label)
      miven_z = self.notebook.append_page(vbox1, label)
      self.notebook.show()
      miwin.destroy()
      self.ventanas_abiertas_z.append(opcion_z)
      self.notebook.set_current_page(miven_z)
  #Fin de activa_manto

  def cierra_tabactual(self, widget):
      mitab_z = self.notebook.get_current_page()
      if mitab_z <> -1:
         quien_z = self.ventanas_abiertas_z[mitab_z]
         self.ventanas_abiertas_z.remove(quien_z)
         self.notebook.remove_page(mitab_z)
      #Fin de If
  #Fin cierra_tabactual

  def crea_boton(self, etiqueta_z, imgicon_z=None):
    btn_nuevo = gtk.Button()
    hbox = gtk.HBox()
    hbox.set_border_width(2)
    icono_z = gtk.Image()
    icono_z.set_from_file("info.xpm")
    label = gtk.Label(etiqueta_z)
    hbox.pack_start(icono_z, True, True, 3)
    hbox.pack_start(label, True, True, 3)
    btn_nuevo.add(hbox)
    btn_nuevo.show()
    return(btn_nuevo)


if __name__ == "__main__":
#   global mydb
#   global cia_z
#   mibd = def_tablas.lee_basedato_ini()
#   mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
   hwg = Menu()
   gtk.main()

def main():
#    global mydb
#    mibd = def_tablas.lee_basedato_ini()
#    mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])

    gtk.main()
    return 0
