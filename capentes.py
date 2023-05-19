#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Manto  de Vendedores DRBR 26-May-2007
import sys
import types
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
import datetime
platform = sys.platform 

global mydb
global cia_z
global mibd
global cias
global vendedor
global almacen
global ptovta
global businven_z
global dirprogs_z

#-- Define additional constants
EXIT         = utils.EXIT
CONTINUE     = utils.CONTINUE
NUEVO        = utils.NUEVO
MODIFICA     = utils.MODIFICA
BORRAR       = utils.BORRAR
NUEVOREN     = utils.NUEVOREN
ESPERAREN    = utils.ESPERAREN
CONCEPTOS    = def_tablas.CONCEPTOS
POBLACIONES  = def_tablas.POBLACIONES
ALMACEN      = def_tablas.ALMACEN
PTOVTA       = def_tablas.PTOVTA
VENDEDOR     = def_tablas.VENDEDOR
businven_z   = False
modo_z       = 0

estoyren_z   = 0
estoyen_z    = def_tablas.ENTRADAS
mibd         = utils.lee_basedato_ini()
cias         = def_tablas.define_cias()
vendedor     = def_tablas.define_vendedor()
almacen      = def_tablas.define_almacen()
ptovta       = def_tablas.define_ptovta()
entradas     = def_tablas.define_entradas()
renentra     = def_tablas.define_renentra()
inven        = def_tablas.define_inven()
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


class Capentes:
  """Esta es una aplicación Captura de Entradas Especiales"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.tipent_z="P"
    self.gladefile = dirprogs_z + "capentes.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_nuevo_clicked": self.on_btn_nuevo_clicked, \
            "on_btn_modif_clicked": self.on_btn_modif_clicked, \
            "on_btn_borra_clicked": self.on_btn_borra_clicked, \
            "on_btn_aceptar_clicked": self.on_btn_aceptar_clicked, \
            "on_btn_cancelar_clicked": self.on_btn_cancelar_clicked, \
            "on_btn_renglones_clicked": self.on_btn_renglones_clicked, \
            "on_btn_entradas_clicked": self.on_btn_entradas_clicked, \
            "on_btn_cierra_clicked": self.on_btn_cierra_clicked, \
            "on_btn_nuevoren_clicked": self.on_btn_nuevoren_clicked, \
            "on_btn_borraren_clicked": self.on_btn_borraren_clicked, \
            "on_btn_cierraren_clicked": self.on_btn_cierraren_clicked, \
            "on_btn_primero_clicked": self.on_btn_primero_clicked, \
            "on_btn_anter_clicked": self.on_btn_anter_clicked, \
            "on_btn_sigte_clicked": self.on_btn_sigte_clicked, \
            "on_btn_ultimo_clicked": self.on_btn_ultimo_clicked, \
            "on_btn_imprime_clicked": self.on_btn_imprime_clicked, \
            "on_edt_almacen_focus_out_event": self.on_edt_almacen_focus_out_event,\
            "on_edt_vend_focus_out_event": self.on_edt_vend_focus_out_event,\
            "on_edt_ptovta_focus_out_event": self.on_edt_ptovta_focus_out_event,\
            "on_edt_codigo_focus_out_event": self.on_edt_codigo_focus_out_event, \
            "on_edt_nomcli_focus_out_event": self.on_edt_nomcli_focus_out_event, \
            "on_edt_preciovta_focus_out_event": self.on_edt_preciovta_focus_out_event, \
            "on_edt_numero_activate": self.on_edt_numero_activate, \
            "on_edt_poblac_focus_out_event": self.on_edt_poblac_focus_out_event \
            }
    self.wTree.get_widget("edt_almacen").connect("activate", self.on_edt_almacen_focus_out_event)
    self.wTree.get_widget("edt_codigo").connect("activate", self.on_edt_codigo_focus_out_event)
    self.wTree.get_widget("edt_nomcli").connect("activate", self.on_edt_nomcli_focus_out_event)
    self.wTree.get_widget("edt_preciovta").set_property('xalign', 1)
    self.wTree.get_widget("edt_canti").set_property('xalign', 1)

    self.wTree.signal_autoconnect(dic)
    global mydb
    global cias
    global vendedor
    global cia_z
    global estoyen_z
    cia_z = 1
    cias_lines = []
    basedato_z = []

    fh_cias = open('.cias.ini')
    for line in fh_cias.readlines():
        cias_lines.append(string.rstrip(line))
    cia_z = utils.StrToInt(cias_lines[0])
    mibd = utils.lee_basedato_ini()
    dsn_z = "dsn="+mibd['base']+";uid="+mibd['user']+";pwd="+mibd['password']
    if mibd['tipobd'] == "MYSQL":
       mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
    elif mibd['tipobd'] == "ODBC":
       mydb = pyodbc.connect(dsn_z)
    elif mibd['tipobd'] == "SOLID":
       dsn_z = mibd['base']+" " + mibd['user']+" "+mibd['password']
       mydb = Solid.DB(dsn_z)

    cias = def_tablas.busca_cia(mydb, cia_z)
    self.asigna_tipent("P")

    self.editable_onoff(False)
    self.activa_aceptar_cancelar(False)
    self.activa_renglones(False)
    self.lst_renentra = gtk.ListStore(str, str, int, str, str, str, str, str, int)
    grd_renentra = self.wTree.get_widget("grd_renentra")
    grd_renentra.set_model(self.lst_renentra)
    columnas_z = ["Codigo", "Descripcion", "Folio", "Serie", "Costo.U", "S/N", "Vend", "Status"]
    
    ii_z = 0
    for micol_z in columnas_z:
      col = gtk.TreeViewColumn(micol_z)
      grd_renentra.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1
    grd_renentra.connect("cursor-changed", self.ren_seleccionado)
    if platform in utils.grd_lines_soported:  
       grd_renentra.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
    estoyen_z = def_tablas.ENTRADAS

  def asigna_tipent(self, tipo_z):
    self.tipent_z = tipo_z
    miwin = self.wTree.get_widget("win_capentes")
    miwin.set_title(cias['razon'] + " Captura de " + def_tablas.tipoentra(self.tipent_z)[2])
    self.objetos_invisibles=[]
    self.objetos_invisibles=["edt_nomptovt", "edt_ptovta", "edt_vend", "edt_poblac", \
       "edt_nomvnd", "lbl_poblac", "lbl_ptovta", "lbl_vend"]
    if self.tipent_z == "P":
       visibles_z = False
    elif self.tipent_z in ["C", "O", "J", "U", "2" ]:
       visibles_z = True
    for objeto_z in self.objetos_invisibles:
        self.wTree.get_widget(objeto_z).set_child_visible(visibles_z)
    return(self.tipent_z)

  def on_btn_primero_clicked(self, widget):
      self.mueve_entrada("P", alm_z)

  def on_btn_anter_clicked(self, widget):
      self.mueve_entrada("A")

  def on_btn_sigte_clicked(self, widget):
      self.mueve_entrada("S")

  def on_btn_ultimo_clicked(self, widget):
      self.mueve_entrada("U")

  def on_edt_numero_activate(self, widget):
      alm_z   = self.wTree.get_widget("edt_almacen").get_text().upper()
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == False ):
         utils.msgdlg("No existe la entrada " + alm_z + " " + repr(numero_z));
         return (-1)
      ## -- End If
      self.despliega_datos()

  def on_btn_renglones_clicked(self, widget):
      global estoyen_z
      global estoyren_z
      alm_z   = self.wTree.get_widget("edt_almacen").get_text().upper()
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == False ):
         utils.msgdlg("No existe la entrada " + alm_z + " " + repr(numero_z));
         return (-1)
      ## -- End If
      self.despliega_datos()
      self.editable_onoff(True)
      self.activa_renglones(True)
      self.activa_aceptar_cancelar(False)
      self.renglon_editable_onoff(False)
      estoyen_z = def_tablas.RENENTRA
      estoyren_z = ESPERAREN
      
  def on_btn_entradas_clicked(self, widget):
      global estoyen_z
      estoyen_z = def_tablas.ENTRADAS
      self.editable_onoff(False)
      self.activa_renglones(False)
      
  def on_btn_cierra_clicked(self, widget):
      label = widget.get_label()
      if label == "_Cierra":
         widget.set_label("_Cerrado")
      else:
         widget.set_label("_Cierra")
      
  def on_edt_almacen_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.ENTRADAS:
         return (-1)
      edt_almacen  = widget
      if self.busca_alm(edt_almacen.get_text().upper()) == True:
         edt_almacen.set_text(almacen['clave'])

  def on_btn_nuevoren_clicked(self, widget):
      global modo_z
      modo_z = NUEVOREN
      self.renglon_editable_onoff(True)
      self.activa_aceptar_cancelar(True)
      self.wTree.get_widget("edt_canti").set_text("1")
      self.wTree.get_widget("edt_codigo").grab_focus()

  def on_btn_borraren_clicked(self, widget):
      if estoyen_z <> def_tablas.RENENTRA:
         return (-1)
      if entradas['status'] == "C":
         utils.msgdlg("Entrada Cerrada, No puede afectar")
         return (-1)
      if renentra['status'] == "C":
         utils.msgdlg("Renglon Cerrado, No puede Eliminar")
         return (-1)
      resp_z = utils.yesnodlg("Seguro de Eliminar este Renglon ?")
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from renentra "
         sql_z = sql_z + " where tipo = '" + self.tipent_z + "'"
         sql_z = sql_z  + " and alm = '" + entradas['alm'] + "'"
         sql_z = sql_z + " and numero = " + utils.IntToStr(entradas['numero']) 
         sql_z = sql_z + " and conse=" + utils.IntToStr(renentra['conse']) 
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         def_tablas.commit_trans(mydb)
         self.lista_renglones()

  def on_btn_cierraren_clicked(self, widget):
      if estoyen_z <> def_tablas.RENENTRA:
         return (-1)
      if entradas['status'] == "C":
         utils.msgdlg("Entrada Cerrada, No puede afectar")
         return (-1)
      if renentra['status'] == "C":   
         utils.msgdlg("Renglon Cerrado, No puede afectar")
         return (-1)
      def_tablas.afecta_renentra(mydb, renentra, entradas)
      self.lista_renglones()

  def on_edt_codigo_focus_out_event(self, widget, tipo=None):
      global businven_z
      if businven_z == True:
         return(-1)
      businven_z = True
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      codigo_z = widget.get_text().upper()
      if ( self.busca_inv(codigo_z) == True):
         widget.set_text(inven['codigo'])
         self.wTree.get_widget("edt_descri").set_text(inven['descri'])
         self.wTree.get_widget("edt_preciovta").set_text(repr(inven['costos']))
      businven_z = False

  def on_edt_ptovta_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      vend_z = widget.get_text().upper()
      if ( self.busca_ptovta(vend_z) == True):
         widget.set_text(ptovta['clave'])

  def on_edt_vend_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      vend_z = widget.get_text().upper()
      if ( self.busca_vnd(vend_z) == True):
         widget.set_text(vendedor['codigo'])

  def on_edt_poblac_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      pob_z = widget.get_text().upper()
      self.busca_pob(pob_z)
        
  def on_edt_nomcli_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      nomcli_z = widget.get_text().upper()
      widget.set_text(nomcli_z)
        
  def on_edt_tipago_focus_out_event(self, widget, tipo=None):
      tipo_z=''
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      tipo_z = widget.get_text().upper()
      widget.set_text(utils.obten_tipago(tipo_z))
  
  def on_edt_preciovta_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
  
  def on_btn_nuevo_clicked(self, widget):
      global modo_z
      modo_z = NUEVO
      edt_almacen  = self.wTree.get_widget("edt_almacen")
      edt_numero  = self.wTree.get_widget("edt_numero")
      edt_fecha  = self.wTree.get_widget("edt_fecha")
      tengoalm_z = self.busca_alm(edt_almacen.get_text().upper())
      if (tengoalm_z <> True):
         utils.msgdlg("Debe seleccionar un Almacen");
         return (-1)
      ## -- End If
      alm_z = edt_almacen.get_text().upper()
      self.editable_onoff(True)
      self.activa_aceptar_cancelar(True)
      numero_z = def_tablas.busca_sigte(mydb, self.tipent_z, alm_z, 0, cia_z, def_tablas.ENTRADAS)
      edt_numero.set_text(repr(numero_z))
      edt_fecha.set_text(datetime.date.today().strftime('%d/%m/%Y'))
      edt_numero.grab_focus()

  def busca_alm(self, alm_z = ''):
      edt_almacen  = self.wTree.get_widget("edt_almacen")
      edt_nombre   = self.wTree.get_widget("edt_nomalm")
      if alm_z == '':
         alm_z = edt_almacen.get_text().upper()
         
      sql_z = "select clave, nombre from almacen where clave = '" + alm_z + "' and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        almacen['clave']    = record[0]
        almacen['nombre']  = record[1]
        edt_almacen.set_text(almacen['clave'])
        edt_nombre.set_text(almacen['nombre'])
        resp_z = True
      else:
        sql_z = "select clave, nombre from almacen where cia = " + repr(cia_z) + " order by clave"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El Almacen")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           almacen['clave']   = miresp_z[0]
           almacen['nombre']  = miresp_z[1]
           edt_almacen.set_text(almacen['clave'])
           edt_nombre.set_text(almacen['nombre'])
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif  
      return (resp_z)

  def busca_ptovta(self, alm_z = ''):
      edt_almacen  = self.wTree.get_widget("edt_ptovta")
      edt_nombre   = self.wTree.get_widget("edt_nomptovt")
      if alm_z == '':
         alm_z = edt_almacen.get_text().upper()
         
      sql_z = "select clave, nombre from ptovta where clave = '" + alm_z + "' and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        ptovta['clave']    = record[0]
        ptovta['nombre']  = record[1]
        edt_almacen.set_text(ptovta['clave'])
        edt_nombre.set_text(ptovta['nombre'])
        resp_z = True
      else:
        sql_z = "select clave, nombre from ptovta where cia = " + repr(cia_z) + " order by clave"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El Punto de Venta")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           ptovta['clave']   = miresp_z[0]
           ptovta['nombre']  = miresp_z[1]
           edt_almacen.set_text(ptovta['clave'])
           edt_nombre.set_text(ptovta['nombre'])
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif  
      return (resp_z)

  def busca_pob(self, pob_z = ''):
      edt_poblac  = self.wTree.get_widget("edt_poblac")
      if pob_z == '':
         pob_z = edt_poblac.get_text().upper()
         
      sql_z = "select nombre from poblacs where nombre = '" + pob_z + "'"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        edt_poblac.set_text(pob_z)
        resp_z = True
      else:
        sql_z = "select nombre,numero from poblacs order by nombre"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Poblacion:Codigo", "Seleccione la Poblacion")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           pob_z   = miresp_z[0]
           edt_poblac.set_text(pob_z)
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif  
      return (resp_z)

  def busca_vnd(self, vend_z = ''):
      edt_vend  = self.wTree.get_widget("edt_vend")
      edt_nombre   = self.wTree.get_widget("edt_nomvnd")
      if vend_z == '':
         vend_z = edt_vend.get_text().upper()
         
      sql_z = "select codigo, nombre from vendedor where codigo = '" + vend_z + "'"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        vendedor['codigo']    = record[0]
        vendedor['nombre']  = record[1]
        edt_vend.set_text(vendedor['codigo'])
        edt_nombre.set_text(vendedor['nombre'])
        resp_z = True
      else:
        sql_z = "select codigo, nombre from vendedor order by codigo"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El Vendedor")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           vendedor['codigo']    = miresp_z[0]
           vendedor['nombre']    = miresp_z[1]
           edt_vend.set_text(vendedor['codigo'])
           edt_nombre.set_text(vendedor['nombre'])
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif  
      return (resp_z)

  def busca_inv(self, codigo_z = ''):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_descri   = self.wTree.get_widget("edt_descri")
      if codigo_z == '':
         codigo_z = edt_codigo.get_text().upper()
         
      sql_z = "select codigo, descri, tipo, costos, coston, piva from inven where codigo = '" + codigo_z + "' and cia=" + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        inven['codigo']    = record[0]
        inven['descri']    = record[1]
        inven['tipo']      = record[2]
        inven['costos']    = record[3]
        inven['coston']    = record[4]
        inven['piva']      = record[5]
        edt_codigo.set_text(inven['codigo'])
        edt_descri.set_text(inven['descri'])
        resp_z = True
      else:
        sql_z = "select codigo, descri, tipo from inven where codigo like '" + codigo_z + "%' and cia = " + repr(cia_z) + " order by codigo"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Descri:Tipo", "Seleccione El Articulo")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           inven['codigo']    = miresp_z[0]
           inven['descri']    = miresp_z[1]
           inven['tipo']      = miresp_z[2]
           edt_codigo.set_text(inven['codigo'])
           edt_descri.set_text(inven['descri'])
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif  
      return (resp_z)

  def on_btn_modif_clicked(self, widget):
      global modo_z
      modo_z = MODIFICA
      edt_nombre = self.wTree.get_widget("edt_nombre")
      self.editable_onoff(True)
      edt_nombre.grab_focus()

  def on_btn_borra_clicked(self, widget):
      global modo_z
      modo_z = BORRAR
      if entradas['status'] == "C":
         utils.msgdlg("Entrada Cerrada, No puede eliminar")
         return (-1)
      if def_tablas.tiene_renglones_cerrados(mydb, entradas['tipo'], entradas['alm'], entradas['numero'], cia_z) == True:
         utils.msgdlg("Entrada con renglones Cerrados, No puede eliminarla por completo")
         return (-1)
      resp_z = utils.yesnodlg("Seguro de Eliminar esta Entrada completa ?")
      if resp_z == gtk.RESPONSE_OK:
         def_tablas.borra_entradas(mydb, entradas['tipo'], entradas['alm'], entradas['numero'], cia_z)
         self.limpia_campos()

  def on_btn_cancelar_clicked(self, widget):
      if modo_z == NUEVO or modo_z == MODIFICA:
         self.editable_onoff(False)
      elif modo_z == NUEVOREN:
         self.renglon_editable_onoff(False)
      self.activa_aceptar_cancelar(False)

  def on_btn_aceptar_clicked(self, widget):
      if modo_z == NUEVO or modo_z == MODIFICA:
         self.nueva_modif_entradas()
      elif modo_z == NUEVOREN:
         self.agrega_nuevo_ren()

  def agrega_nuevo_ren(self):
      alm_z = entradas['alm']
      numero_z = entradas['numero']
      codigo_z = self.wTree.get_widget("edt_codigo").get_text().upper()
      if  self.busca_inv(codigo_z) == False:
         utils.msgdlg("No tiene un articulo valido...")
         self.wTree.get_widget("edt_codigo").grab_focus()
         return ( -1)

      nomcli_z = self.wTree.get_widget("edt_nomcli").get_text().upper()
      vend_z = self.wTree.get_widget("edt_vend").get_text().upper()
      poblac_z = self.wTree.get_widget("edt_poblac").get_text().upper()
      ptovta_z = self.wTree.get_widget("edt_ptovta").get_text().upper()
      tipago_z = ""
      #tipago_z = self.wTree.get_widget("edt_tipago").get_text().upper()
      if len(tipago_z) > 1:
         tipago_z = tipago_z[0]
      costou_z = utils.StrToFloat(self.wTree.get_widget("edt_preciovta").get_text())
      canti_z = utils.StrToInt(self.wTree.get_widget("edt_canti").get_text())
      serie_z = ''
      folios_z = []
      datos_z = ()
      ultfol_z = def_tablas.busca_sigfolio(mydb, codigo_z, alm_z, cia_z)
      if inven['tipo'] == "ALF":
         pideserie_z = "S"
      else:
         pideserie_z = "N"

      for ii_z in range (canti_z):
          datos_z = ( ultfol_z + ii_z, serie_z, pideserie_z )
          folios_z.append(datos_z)

      if inven['tipo'] == "ALF":
         pide_series = utils.pide_series("Folio:Serie:Editable", "Proporcione las Series", folios_z, "E", canti_z)
         folios_z = pide_series.ejecuta()
      if self.wTree.get_widget("chk_sino").get_active() == True:
         siono_z = 'S'
         piva_z = inven['piva']
      else:
         siono_z = 'N'
         piva_z = 0
      if self.wTree.get_widget("chk_cancel").get_active() == True:
         entcan_z = 'S'
      else:
         entcan_z = 'N'
      folent_z = 0
      preciovta_z = 0
      npob_z   = 0
      ncli_z   = def_tablas.busca_iddato(mydb, nomcli_z, def_tablas.CONCEPTOS)
      npob_z   = def_tablas.busca_iddato(mydb, poblac_z, def_tablas.POBLACIONES)
      conse_z = def_tablas.busca_sigte(mydb, self.tipent_z, alm_z, numero_z, cia_z, def_tablas.RENENTRA)
      def_tablas.start_trans(mydb)
      for misfolios_z in folios_z:
        renentra['tipo'] = self.tipent_z
        renentra['alm'] = alm_z
        renentra['recemi'] = ptovta_z
        renentra['numero'] = entradas['numero']
        renentra['conse']= conse_z
        renentra['codinv']= codigo_z
        renentra['serie']= misfolios_z[1]
        renentra['siono']= siono_z
        renentra['folsal']= 0
        renentra['folent']= utils.StrToInt(misfolios_z[0])
        renentra['unids']= 1
        renentra['costou']= costou_z
        renentra['piva']= piva_z
        renentra['importe']= costou_z
        renentra['cantmueve']= 1
        renentra['status']= 'A'
        renentra['persenvrec']= ncli_z
        renentra['cia']= cia_z
        renentra['vend']= vend_z
        renentra['poblac']= npob_z
        renentra['tipago']= tipago_z
        renentra['prvta']= preciovta_z
        renentra['entosal']= 'E'
        renentra['entcan']= entcan_z
        sql_z = def_tablas.insert_into_renentra(renentra)
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        conse_z = conse_z + 1
      def_tablas.commit_trans(mydb)
      self.lista_renglones(alm_z, numero_z)
      self.renglon_editable_onoff(False)
      self.activa_aceptar_cancelar(False)

  def nueva_modif_entradas(self):
      global modo_z
      sql_z = ''
      edt_almacen  = self.wTree.get_widget("edt_almacen")
      edt_fecha    = self.wTree.get_widget("edt_fecha")
      edt_numero   = self.wTree.get_widget("edt_numero")
      fecha_z = utils.StrToDate(edt_fecha.get_text())
      if ( fecha_z == -1):
         utils.msgdlg("Fecha Invalida:" + edt_fecha.get_text());
         edt_fecha.grab_focus()
         return (-1)
      ## -- End If
      
      alm_z   = edt_almacen.get_text().upper()
      numero_z = utils.StrToInt(edt_numero.get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == True ):
         utils.msgdlg("Ya existe esa entrada");
         edt_numero.grab_focus()
         return (-1)
      ## -- End If

      entradas['tipo']   = self.tipent_z
      entradas['alm']  = alm_z
      entradas['recemi']  = ''
      entradas['numero']  = numero_z
      entradas['facpro']  = ''
      entradas['prove']  = ''
      entradas['perenvrec']  = 0
      entradas['status']  = 'A'
      entradas['coniva']  = ''
      entradas['fecha']  = fecha_z
      entradas['importe']  = 0
      entradas['iva']  = 0
      entradas['total']  = 0
      entradas['vence']  = fecha_z
      entradas['ctofin']  = 0
      entradas['tascomp']  = 0
      entradas['taspro']  = 0
      entradas['fechafac']  = fecha_z
      entradas['letras']  = 0
      entradas['plazocfp']  = 0
      entradas['fletes']  = 0
      entradas['desxap']  = 0
      entradas['fechaprp']  = fecha_z
      entradas['ctofincomp']  = 0
      entradas['usuario']  = ''
      entradas['cia']  = cia_z
      def_tablas.start_trans(mydb)
      if modo_z == NUEVO:
         sql_z = def_tablas.insert_into_entradas(entradas)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
      self.lista_renglones(alm_z, numero_z)
      self.activa_aceptar_cancelar(False)
      self.editable_onoff(False)

  def on_btn_ultimo_clicked(self, widget):
      self.mueve_entrada('U')

  def on_btn_primero_clicked(self, widget):
      self.mueve_entrada('P')

  def on_btn_anter_clicked(self, widget):
      self.mueve_entrada('A')

  def on_btn_sigte_clicked(self, widget):
      self.mueve_entrada('S')

  def on_btn_imprime_clicked(self, widget):
      alm_z   = self.wTree.get_widget("edt_almacen").get_text().upper()
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == False ):
         utils.msgdlg("No existe la entrada " + alm_z + " " + repr(numero_z));
         return (-1)
      ## -- End If
      self.despliega_datos()
      pag_z = 1
      miarchivo_z = "capentes.tex"
      arch_z = open(miarchivo_z, "w")
      arch_z.write(cias['razon'].center(80) + "\n")
      condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")
      hora_z = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
      arch_z.write(condensado_on + "capentes " + condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      arch_z.write(("Impresion de " + def_tablas.tipoentra(self.tipent_z)[2] + " Pag:" + '%d' % pag_z).center(80) + "\n")
      arch_z.write("Numero:" + self.tipent_z + "%6d" % entradas['numero'])
      arch_z.write(" Almacen: " + entradas['alm'] + " " + almacen['nombre'])
      arch_z.write(" Fecha: " + entradas['fecha'].strftime('%d/%m/%Y') + "\n")
      arch_z.write(condensado_on)
      arch_z.write(subrayado_on)
      arch_z.write("Codigo".ljust(13)+"|")
      arch_z.write("Descripcion".ljust(30)+"|")
      arch_z.write("Folio".rjust(5)+"|")
      arch_z.write("Costo Unit".rjust(12)+"|")
      arch_z.write("C|")
      arch_z.write("S|")
      arch_z.write("Serie".ljust(20)+ "|")
      if self.tipent_z in ["C"]:
         arch_z.write("Vend".ljust(4)+ "|")
         arch_z.write("PTVT".ljust(4)+ "|")
         arch_z.write("Poblac".ljust(10)+ "|")
         arch_z.write("Nombre".ljust(20))
      else:
         arch_z.write("Nombre".ljust(30))
      arch_z.write(subrayado_off)
      arch_z.write("\n")
      sql_z = "select a.tipo,a.alm,a.recemi,a.numero,a.conse,a.codinv,a.serie,"
      sql_z = sql_z + "a.siono,a.folsal,a.folent,a.unids,a.costou,a.piva,a.importe,a.cantmueve,"
      sql_z = sql_z + "a.status,a.persenvrec,a.cia,a.vend,a.poblac,a.tipago,a.prvta,a.entosal,a.entcan,"
      sql_z = sql_z + "b.descri"
      sql_z = sql_z + " from renentra a"
      sql_z = sql_z + " join inven b on a.codinv = b.codigo and a.cia = b.cia"
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + entradas['alm'] + "' and a.numero = " + repr(entradas['numero']) 
      sql_z = sql_z + " and a.cia = " + repr(cia_z) + " order by conse"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      ren_z = 0
      impcosto_z = 0
      iva_z = 0
      for record in result:
        ren_z = ren_z + 1
        ptovta_z = record[2]
        codigo_z = record[5]
        vend_z   = record[18]
        prvta_z  = record[21]
        descri_z = record[24]
        folent_z = '%5d' % record[9]
        nomcli_z = def_tablas.busca_dato(mydb, record[16], CONCEPTOS)
        poblac_z = def_tablas.busca_dato(mydb, record[19], POBLACIONES)

        entcan_z = record[23]
        siono_z  = record[7]
        serie_z  = record[6]
        costou_z = utils.currency(record[11])
        impcosto_z = impcosto_z + record[11]
        iva_z = iva_z + record[11] * record[12] / 100
        if ren_z == numrows:
           arch_z.write(subrayado_on)
        arch_z.write(codigo_z.ljust(13)+"|")
        arch_z.write(descri_z.ljust(30)+"|")
        arch_z.write(folent_z.rjust(5)+"|")
        arch_z.write(costou_z.rjust(12)+"|")
        arch_z.write(entcan_z + "|")
        arch_z.write(siono_z + "|")
        arch_z.write(serie_z.ljust(20)+ "|")
        if self.tipent_z in ["C"]:
           arch_z.write(vend_z.ljust(4)+ "|")
           arch_z.write(ptovta_z.ljust(4)+ "|")
           poblac_z = poblac_z[:9]
           nomcli_z = nomcli_z[:20]
           arch_z.write(poblac_z.ljust(10)+ "|")
           arch_z.write(nomcli_z.ljust(20))
        else:
           arch_z.write(nomcli_z.ljust(30))
        if ren_z == numrows:
           arch_z.write(subrayado_off)
        arch_z.write("\n")
      total_z = impcosto_z + iva_z
      arch_z.write(subrayado_on + "|")
      arch_z.write("Importe:" + utils.currency(impcosto_z).ljust(12) + "|")
      arch_z.write("Iva    :" + utils.currency(iva_z).ljust(12) + "|")
      arch_z.write("Total  :" + utils.currency(total_z).rjust(12) + "|")
      arch_z.write(subrayado_off + "\n")
      arch_z.close()
      visor = utils.visor_editor()
      resp_z = visor.ejecuta(miarchivo_z)

  def mueve_entrada(self, hacia_z, alm_z=''):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      edt_almacen  = self.wTree.get_widget("edt_almacen")
      edt_numero  = self.wTree.get_widget("edt_numero")
      if self.busca_alm(edt_almacen.get_text().upper()) <> True:
         utils.msgdlg("Debe seleccionar un Almacen");
         return (-1)
      ## -- End If
      alm_z   = edt_almacen.get_text().upper()
      numero_z = utils.StrToInt(edt_numero.get_text())
      where_z = " from entradas where tipo = '" + self.tipent_z + "' and alm = '" + alm_z + "' and cia = " + repr(cia_z)
      if hacia_z == 'P':
        sql_z = "select min(numero) "
        sql2_z = ""
      elif hacia_z == 'U':
        sql_z = "select max(numero) "
        sql2_z = ""
      elif hacia_z == 'A':
        sql_z = "select max(numero) "
        sql2_z = " and numero < " + repr(numero_z)
      elif hacia_z == 'S':
        sql_z = "select min(numero) "
        sql2_z = " and numero > " + repr(numero_z)
# execute SQL statement
      sql_z = sql_z + where_z + sql2_z
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         if type(record[0]) == types.IntType:
            numero_z  = record[0]
         if(self.busca_entrada ( alm_z, numero_z) == True):
            self.despliega_datos()

  def busca_entrada(self, alm_z = '', numero_z = 0):
      sql_z = "select tipo, alm, numero, fecha from entradas where "
      sql_z = sql_z + " tipo = '" + self.tipent_z + "' and alm = '" + alm_z + "' and numero = "  + repr(numero_z) + " and cia= " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         entradas['tipo']   = self.tipent_z
         entradas['alm']  = alm_z
         entradas['numero']  = numero_z
         entradas['fecha']  = record[3]
         resp_z = True
      else:
         resp_z = False
      return ( resp_z)

  def despliega_datos(self):
      alm_z = entradas['alm'];
      numero_z = entradas['numero']
      self.busca_alm(alm_z)
      self.wTree.get_widget("edt_numero").set_text(repr(numero_z))
      self.wTree.get_widget("edt_fecha").set_text(entradas['fecha'].strftime('%d/%m/%Y'))
      self.lista_renglones(alm_z, numero_z)

  def lista_renglones(self, alm_z='', numero_z=0):
      self.lst_renentra.clear()
      sql_z = "select a.tipo,alm,numero,codinv,serie,folent,costou,siono,"
      sql_z = sql_z + "persenvrec,vend,poblac,tipago,costou,b.descri,status,conse, siono, entcan"
      sql_z = sql_z + " from renentra a"
      sql_z = sql_z + " join inven b on a.codinv = b.codigo and a.cia = b.cia"
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + entradas['alm'] + "' and numero = "
      sql_z = sql_z + repr(entradas['numero']) + " and a.cia = " + repr(cia_z)
      sql_z = sql_z + " order by conse"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      # get and display one row at a time
      result = cursor.fetchall()
      for record in result:
          descri_z = record[13]
          renentra['tipo']        = record[0]
          renentra['alm']         = record[1]
          renentra['numero']      = record[2]
          renentra['codinv']      = record[3]
          renentra['serie']       = record[4]
          renentra['folent']      = record[5]
          renentra['costou']      = record[6]
          renentra['siono']       = record[7]
          renentra['persenvrec']  = record[8]
          renentra['vend']        = record[9]
          renentra['poblac']      = record[10]
          renentra['tipago']      = record[11]
          renentra['prvta']       = record[12]
          renentra['status']      = record[14]
          renentra['conse']       = record[15]
          costou_z = utils.currency(renentra['costou'])
          self.lst_renentra.append([ renentra['codinv'], descri_z, renentra['folent'], renentra['serie'], costou_z, renentra['siono'], renentra['vend'], renentra['status'], renentra['conse'] ])

  def ren_seleccionado(self, alm_z='', numero_z=0, tipo_z=0):
      colconse_z = 8
      grd_renentra = self.wTree.get_widget("grd_renentra")
      selection = grd_renentra.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          conse_z = self.lst_renentra.get_value(selection_iter, colconse_z)
      self.despliega_renglon(entradas['alm'], entradas['numero'], conse_z)

  def despliega_renglon(self, alm_z='', numero_z=0, conse_z=0):
      sql_z = "select a.tipo,a.alm,a.recemi,a.numero,a.conse,a.codinv,a.serie,"
      sql_z = sql_z + "a.siono,a.folsal,a.folent,a.unids,a.costou,a.piva,a.importe,a.cantmueve,"
      sql_z = sql_z + "a.status,a.persenvrec,a.cia,a.vend,a.poblac,a.tipago,a.prvta,a.entosal,a.entcan,"
      sql_z = sql_z + "b.descri"
      sql_z = sql_z + " from renentra a"
      sql_z = sql_z + " join inven b on a.codinv = b.codigo and a.cia = b.cia"
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + alm_z + "' and a.numero = " + repr(numero_z) 
      sql_z = sql_z + " and conse = " + repr(conse_z) + " and a.cia = " + repr(cia_z)
      codigo_z = ''
      vend_z = ''
      tipago_z = ''
      prvta_z = 0
      descri_z = ''
      poblac_z = ''
      nomvnd_z = ''
      nomptvt_z = ''
      nomcli_z = ''
      costou_z = ''
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      for record in result:
          renentra['tipo']       = record[0]
          renentra['alm']        = record[1]
          renentra['recemi']     = record[2]
          renentra['numero']     = record[3]
          renentra['conse']      = record[4]
          renentra['codinv']     = record[5]
          renentra['serie']      = record[6]
          renentra['siono']      = record[7]
          renentra['folsal']     = record[8]
          renentra['folent']     = record[9]
          renentra['unids']      = record[10]
          renentra['costou']     = record[11]
          renentra['piva']       = record[12]
          renentra['importe']    = record[13]
          renentra['cantmueve']  = record[14]
          renentra['status']     = record[15]
          renentra['persenvrec'] = record[16]
          renentra['cia']        = record[17]
          renentra['vend']       = record[18]
          renentra['poblac']     = record[19]
          renentra['tipago']     = record[20]
          renentra['prvta']      = record[21]
          renentra['entosal']    = record[22]
          renentra['entcan']     = record[23]
          descri_z               = record[24]
          nomcli_z               = def_tablas.busca_dato(mydb, renentra['persenvrec'], CONCEPTOS)
          costou_z               = utils.currency(renentra['costou'])
          if self.tipent_z in "C":
             poblac_z               = def_tablas.busca_dato(mydb, renentra['poblac'], POBLACIONES)
             nomvnd_z               = def_tablas.busca_nombre(mydb, renentra['vend'], cia_z, VENDEDOR)
             nomptovt_z             = def_tablas.busca_nombre(mydb, renentra['recemi'], cia_z, PTOVTA)
      
      self.wTree.get_widget("edt_codigo").set_text(renentra['codinv'])
      self.wTree.get_widget("edt_descri").set_text(descri_z)
      self.wTree.get_widget("edt_nomcli").set_text(nomcli_z)
      self.wTree.get_widget("edt_preciovta").set_text(costou_z)
      self.wTree.get_widget("chk_sino").set_active(renentra['siono'] == 'S')
      self.wTree.get_widget("chk_cancel").set_active(renentra['entcan'] == 'S')
      if self.tipent_z in "C":
         self.wTree.get_widget("edt_vend").set_text(renentra['vend'])
         self.wTree.get_widget("edt_nomvnd").set_text(nomvnd_z)
         self.wTree.get_widget("edt_poblac").set_text(poblac_z)
         self.wTree.get_widget("edt_ptovta").set_text(renentra['recemi'])
         self.wTree.get_widget("edt_nomptovt").set_text(nomptovt_z)

  def limpia_campos(self):
      self.wTree.get_widget("edt_codigo").set_text('')
      self.wTree.get_widget("edt_descri").set_text('')
      self.wTree.get_widget("edt_nomcli").set_text('')
      #self.wTree.get_widget("edt_tipago").set_text('')
      self.wTree.get_widget("edt_preciovta").set_text('')
      self.wTree.get_widget("chk_sino").set_active(False)
      self.wTree.get_widget("chk_cancel").set_active(False)
      self.wTree.get_widget("edt_numero").set_text('')
      self.wTree.get_widget("edt_fecha").set_text('')
      if self.tipent in "C":
         self.wTree.get_widget("edt_vend").set_text('')
         self.wTree.get_widget("edt_nomvnd").set_text('')
         self.wTree.get_widget("edt_poblac").set_text('')
         self.wTree.get_widget("edt_nomptovt").set_text('')
         self.wTree.get_widget("edt_ptovta").set_text('')
      self.lst_renentra.clear()

  def editable_onoff(self, modo):
      self.wTree.get_widget("btn_nuevo").set_child_visible(not(modo))
      self.wTree.get_widget("btn_modif").set_child_visible(not(modo))
      self.wTree.get_widget("btn_borra").set_child_visible(not(modo))
      self.wTree.get_widget("btn_primero").set_child_visible(not(modo))
      self.wTree.get_widget("btn_anter").set_child_visible(not(modo))
      self.wTree.get_widget("btn_sigte").set_child_visible(not(modo))
      self.wTree.get_widget("btn_ultimo").set_child_visible(not(modo))
      self.wTree.get_widget("btn_renglones").set_child_visible(not(modo))
      self.wTree.get_widget("btn_imprime").set_child_visible(not(modo))
      self.wTree.get_widget("btn_cierra").set_child_visible(not(modo))

  def renglon_editable_onoff(self, modo):
      self.wTree.get_widget("edt_codigo").set_editable(modo)
      self.wTree.get_widget("edt_nomcli").set_editable(modo)
      #self.wTree.get_widget("edt_vend").set_editable(modo)
      #self.wTree.get_widget("edt_poblac").set_editable(modo)
      #self.wTree.get_widget("edt_tipago").set_editable(modo)
      self.wTree.get_widget("edt_preciovta").set_editable(modo)
      self.wTree.get_widget("btn_nuevoren").set_child_visible(not(modo))
      self.wTree.get_widget("btn_borraren").set_child_visible(not(modo))
      self.wTree.get_widget("btn_cierraren").set_child_visible(not(modo))
      #btn_cierra.set_child_visible(not(modo))

  def activa_aceptar_cancelar(self, modo):
     self.wTree.get_widget("btn_aceptar").set_child_visible(modo)
     self.wTree.get_widget("btn_cancelar").set_child_visible(modo)

  def activa_renglones(self, modo):
      self.wTree.get_widget("btn_nuevoren").set_child_visible(modo)
      self.wTree.get_widget("btn_borraren").set_child_visible(modo)
      self.wTree.get_widget("btn_cierraren").set_child_visible(modo)
      self.wTree.get_widget("btn_entradas").set_child_visible(modo)
      self.wTree.get_widget("edt_almacen").set_editable(not(modo))
      self.wTree.get_widget("edt_numero").set_editable(not(modo))
      self.wTree.get_widget("edt_fecha").set_editable(not(modo))


if __name__ == "__main__":
   hwg = Capentes()
   hwg.wTree.get_widget("win_capentes").connect("destroy", gtk.main_quit )
   gtk.main()

def main():

    gtk.main()
    return 0
