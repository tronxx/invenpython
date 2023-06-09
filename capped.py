#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Manto  de Vendedores DRBR 26-May-2007
import sys
import getopt
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
import cap_obsent
import utils
import datetime
platform = sys.platform 

global mydb
global cia_z
global mibd
global cias
global vendedor
global almacen
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
businven_z   = False
modo_z       = 0

estoyren_z   = 0
estoyen_z    = def_tablas.ENTRADAS
mibd = utils.lee_basedato_ini()
cias = def_tablas.define_cias()
prove = def_tablas.define_prove()
mayoris = def_tablas.define_mayoris()
almacen = def_tablas.define_almacen()
entradas = def_tablas.define_entradas()
renentra = def_tablas.define_renentra()
inven    = def_tablas.define_inven()
selfolios_z = "N"

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

class Capped:
  """Esta es una aplicación Captura de Pedidos"""
       
  def __init__(self, tipent_z="B"):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "capped.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    self.tipent_z = tipent_z

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
            "on_btn_observs_clicked": self.on_btn_observs_clicked, \
            "on_edt_almacen_focus_out_event": self.on_edt_almacen_focus_out_event,\
            "on_edt_almrec_focus_out_event": self.on_edt_almrec_focus_out_event,\
            "on_edt_codigo_focus_out_event": self.on_edt_codigo_focus_out_event \
          }
    self.wTree.get_widget("edt_almacen").connect("activate", self.on_edt_almacen_focus_out_event)
    self.wTree.get_widget("edt_almrec").connect("activate", self.on_edt_almrec_focus_out_event)
    self.wTree.get_widget("edt_codigo").connect("activate", self.on_edt_codigo_focus_out_event)
    self.wTree.get_widget("edt_numero").connect("activate", self.on_edt_numero_activate)
    campos_derecha = [ "edt_costou", "edt_canti", "edt_importe", "edt_iva", "edt_total" ]
    for micampo in campos_derecha:
        self.wTree.get_widget(micampo).set_property('xalign', 1)
    #Fin de For
    #self.wTree.get_widget("win_capped").connect("destroy", gtk.main_quit )

    self.wTree.signal_autoconnect(dic)
    global cias
    global vendedor
    global cia_z
    global estoyen_z
    global mydb
    cia_z = 1
    cias_lines = []
    basedato_z = []

    fh_cias = open('.cias.ini')
    for line in fh_cias.readlines():
        cias_lines.append(string.rstrip(line))
    cia_z = utils.StrToInt(cias_lines[0])

# execute SQL statement
# execute SQL statement
    dsn_z = "dsn="+mibd['base']+";uid="+mibd['user']+";pwd="+mibd['password']
    if mibd['tipobd'] == "MYSQL":
       mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
    elif mibd['tipobd'] == "ODBC":
       mydb = pyodbc.connect(dsn_z)

    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_capped")
    miwin.set_title(cias['razon'] + " Captura de " + def_tablas.tipoentra(self.tipent_z)[2])
    self.wTree.get_widget("edt_almacen").set_text(utils.Fecha_a_Perio(datetime.date.today()))

    self.editable_onoff(False)
    self.activa_aceptar_cancelar(False)
    self.activa_renglones(False)
    self.lst_renentra = gtk.ListStore(int, str, str, str, str, int)
    grd_renentra = self.wTree.get_widget("grd_renentra")
    grd_renentra.set_model(self.lst_renentra)
    columnas_z = ["Canti", "Codigo", "Descripcion", "Costo", "Importe" ]
    
    ii_z = 0
    for micol_z in columnas_z:
      col = gtk.TreeViewColumn(micol_z)
      grd_renentra.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1
    if platform in utils.grd_lines_soported:  
       grd_renentra.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    grd_renentra.connect("cursor-changed", self.ren_seleccionado)
    estoyen_z = def_tablas.ENTRADAS
    self.asigna_tipent("B")

  def asigna_tipent(self, tipo_z):
    self.tipent_z = tipo_z
    miwin = self.wTree.get_widget("win_capped")
    miwin.set_title(cias['razon'] + " Captura de " + def_tablas.tipoentra(self.tipent_z)[2])
    if self.tipent_z == "B":
       self.wTree.get_widget("lbl_prove").set_text("Proveedor")
    elif self.tipent_z == "G":
       self.wTree.get_widget("lbl_prove").set_text("Mayorista")

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
         utils.msgdlg("No existe el Pedido " + alm_z + " " + repr(numero_z));
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
         utils.msgdlg("No existe el Pedido " + alm_z + " " + str(numero_z));
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
      fechaperio_z = utils.Perio_a_Fecha(edt_almacen.get_text().upper())
      if (fechaperio_z == -1):
         utils.msgdlg("Debe seleccionar un Periodo Valido")
         edt_almacen.grab_focus()
         return (-1)
      ## -- End If

  def on_edt_almrec_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.ENTRADAS:
         return (-1)
      edt_almrec  = widget
      if self.busca_mayoris(edt_almrec.get_text().upper()) == True:
         edt_almrec.set_text(mayoris['codigo'])

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
         utils.msgdlg("Pedido Cerrado, No puede afectar")
         return (-1)
      resp_z = utils.yesnodlg("Seguro de Eliminar este Renglon ?")
      if resp_z == gtk.RESPONSE_OK:
         numero_z = entradas['numero']
         alm_z    = entradas['alm']
         importe_z = renentra['importe']
         iva_z     = round( renentra['importe'] * renentra['piva'] / 100, 2)
         total_z   = importe_z + iva_z
         sql_z = "delete from renentra "
         sql_z = sql_z + " where tipo = '" + self.tipent_z + "' "
         sql_z = sql_z + " and alm = '" + alm_z + "'"
         sql_z = sql_z + " and numero = " + str(numero_z) + " and conse=" + str(renentra['conse']) 
         sql_z = sql_z + " and cia = " + str(cia_z)
         sql2_z = "update entradas set importe = importe - " + str(importe_z) + ", "
         sql2_z = sql2_z + " iva = iva - " + str(iva_z) + ", "
         sql2_z = sql2_z + " total = total - " + str(total_z)
         sql2_z = sql2_z + " where tipo = '" + self.tipent_z + "' "
         sql2_z = sql2_z + " and alm = '" + alm_z + "' "
         sql2_z = sql2_z + " and numero = " + str(numero_z) + " "
         sql2_z = sql2_z + " and cia = " + str(cia_z)
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         cursor.execute(sql2_z)
         def_tablas.commit_trans(mydb)
         self.busca_entrada( alm_z, numero_z)
         self.despliega_datos()

  def on_btn_cierraren_clicked(self, widget):
      if estoyen_z <> def_tablas.RENENTRA:
         return (-1)
      if entradas['status'] == "C":
         utils.msgdlg("Pedido Cerrado, No puede afectar")
         return (-1)
      if renentra['status'] == "C":   
         utils.msgdlg("Renglon Cerrado, No puede afectar")
         return (-1)
      #def_tablas.afecta_renentra(mydb, renentra, entradas)
      self.lista_renglones()

  def on_edt_codigo_focus_out_event(self, widget, tipo=None):
      global businven_z
      if businven_z == True:
         return(-1)
      businven_z = True
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      codigo_z = widget.get_text().upper()
      if codigo_z <> "AUXILIAR":
        if ( self.busca_inv(codigo_z) == True):
           widget.set_text(inven['codigo'])
           self.wTree.get_widget("edt_descri").set_text(inven['descri'])
           self.wTree.get_widget("edt_costou").set_text(utils.currency(inven['costos']))
           self.wTree.get_widget("edt_descri").set_editable(False)
      else:
         self.wTree.get_widget("edt_descri").set_editable(True)
      #End if
      businven_z = False

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
      perio_z = edt_almacen.get_text().upper()
      fechaperio_z = utils.Perio_a_Fecha(perio_z)
      if (fechaperio_z == -1):
         utils.msgdlg("Debe seleccionar un Periodo Valido");
         return (-1)
      ## -- End If
      self.editable_onoff(True)
      self.activa_aceptar_cancelar(True)
      numero_z = def_tablas.busca_sigte(mydb, self.tipent_z, perio_z, 0, cia_z, def_tablas.ENTRADAS)
      edt_numero.set_text(repr(numero_z))
      edt_fecha.set_text(fechaperio_z.strftime('%d/%m/%Y'))
      edt_numero.grab_focus()

  def busca_alm(self, alm_z = ''):
      almacen['clave']  = self.wTree.get_widget("edt_almacen").get_text()
      #edt_nombre   = self.wTree.get_widget("edt_nomalm")
      resp_z = True
      return (resp_z)

  def busca_mayoris(self, mayoris_z = ''):
      edt_vend  = self.wTree.get_widget("edt_almrec")
      edt_nombre   = self.wTree.get_widget("edt_nomalmrec")
      if mayoris_z == '':
         mayoris_z = edt_vend.get_text().upper()
      resp_z = self.busca_codmay(mayoris_z)
      if resp_z <> True:
        sql_z = "select codigo, nombre from "
        if self.tipent_z == "B":
           sql_z = sql_z + " proveedor "
        else:
           sql_z = sql_z + " mayoris "
        #End if
        sql_z = sql_z + " where cia = " + utils.IntToStr(cia_z) + " order by codigo"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El dato")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           mayoris_z = miresp_z[0]
           resp_z = self.busca_codmay(mayoris_z)
        else:
           resp_z = False
        #endif
      #endif
      if resp_z == True:
         self.wTree.get_widget("edt_almrec").set_text(mayoris['codigo'])
         self.wTree.get_widget("edt_nomalmrec").set_text(mayoris['nombre'])
      #End If
      return (resp_z)

  def busca_codmay(self, codigo_z=''):
      resp_z = False
      sql_z = "select codigo, nombre from "
      if self.tipent_z == "B":
         sql_z = sql_z + " proveedor "
      else:
         sql_z = sql_z + " mayoris "
      #End if
      sql_z = sql_z + " where codigo = '" + codigo_z + "'"
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         mayoris['codigo']  = record[0]
         mayoris['nombre']  = record[1]
         resp_z = True
      return (resp_z)
  #Fin de busca_codmay()

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
        sql_z = "select nombre from poblacs order by nombre"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Poblacion", "Seleccione la Poblacion")
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
      #End if
      if codigo_z == "AUXILIAR":
         resp_z = True
         return (resp_z)
      #End if
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

  def on_btn_observs_clicked(self, widget):
      alm_z    = self.wTree.get_widget("edt_almacen").get_text().upper()
      nomalm_z = self.wTree.get_widget("edt_nomalmrec").get_text().upper()
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      obsent_z = cap_obsent.Capobsent(alm_z, numero_z, self.tipent_z)
      resp_z = obsent_z.ejecuta()

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
         utils.msgdlg("Pedido Cerrado, No puede eliminar")
         return (-1)
      if def_tablas.tiene_renglones_cerrados(mydb, entradas['tipo'], entradas['alm'], entradas['numero'], cia_z) == True:
         utils.msgdlg("Entrada con renglones Cerrados, No puede eliminarla por completo")
         return (-1)
      resp_z = utils.yesnodlg("Seguro de Eliminar este Pedido completo ?")
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
      almrec_z = ""
      codigo_z = self.wTree.get_widget("edt_codigo").get_text().upper()
      if codigo_z <> "AUXILIAR":
         if self.busca_inv(codigo_z) == False:
            utils.msgdlg("No tiene un articulo valido...")
            self.wTree.get_widget("edt_codigo").grab_focus()
            return ( -1)
         #End if
      #End if
      canti_z = utils.StrToInt(self.wTree.get_widget("edt_canti").get_text())
      descri_z = ""
      descri_z = self.wTree.get_widget("edt_descri").get_text().upper()
      vend_z = ""
      poblac_z = ""
      tipago_z = ""
      costou_z = utils.StrToFloat(self.wTree.get_widget("edt_costou").get_text())
      canti_z = utils.StrToInt(self.wTree.get_widget("edt_canti").get_text())
      serie_z = ''
      fecha_z = entradas['fecha']
      folent_z = 0
      folsal_z = 0
      preciovta_z = 0
      npob_z   = 0
      siono_z = ""
      entcan_z = ""
      ndescri_z   = def_tablas.busca_iddato(mydb, descri_z, def_tablas.CONCEPTOS)
      conse_z = def_tablas.busca_sigte(mydb, self.tipent_z, alm_z, numero_z, cia_z, def_tablas.RENENTRA)
      piva_z = inven['piva']
      importe_z = canti_z * costou_z
      iva_z = round(importe_z * piva_z / 100, 2)
      total_z = importe_z + iva_z
      renentra['tipo'] = self.tipent_z
      renentra['alm'] = alm_z
      renentra['recemi'] = almrec_z
      renentra['numero'] = entradas['numero']
      renentra['conse']= conse_z
      renentra['codinv']= codigo_z
      renentra['serie']= ""
      renentra['siono']= siono_z
      renentra['folsal']= folsal_z
      renentra['folent']= folent_z
      renentra['unids']= canti_z
      renentra['costou']= costou_z
      renentra['piva']= piva_z
      renentra['importe']= costou_z * canti_z
      renentra['cantmueve']= canti_z
      renentra['status']= 'A'
      renentra['persenvrec']= ndescri_z
      renentra['cia']= cia_z
      renentra['vend']= vend_z
      renentra['poblac']= npob_z
      renentra['tipago']= tipago_z
      renentra['prvta']= preciovta_z
      renentra['entosal']= ""
      renentra['entcan']= entcan_z
      entradas['importe'] = entradas['importe'] + importe_z
      entradas['iva'] = entradas['iva'] + iva_z
      entradas['total'] = entradas['total'] + total_z
      sql_z = def_tablas.insert_into_renentra(renentra)
      sql2_z = "update entradas set importe = importe + " + str(importe_z) + ", "
      sql2_z = sql2_z + " iva = iva + " + str(iva_z) + ", "
      sql2_z = sql2_z + " total = total + " + str(total_z)
      sql2_z = sql2_z + " where tipo = '" + self.tipent_z + "' "
      sql2_z = sql2_z + " and alm = '" + alm_z + "' "
      sql2_z = sql2_z + " and numero = " + str(numero_z) + " "
      sql2_z = sql2_z + " and cia = " + str(cia_z)
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      cursor.execute(sql2_z)
      def_tablas.commit_trans(mydb)
      self.lista_renglones(alm_z, numero_z)
      self.despliega_totales()
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
      fechaperio_z = utils.Perio_a_Fecha(alm_z)
      if ( fechaperio_z == -1):
         utils.msgdlg("Periodo Invalido:" + alm_z);
         edt_almacen.grab_focus()
         return (-1)
      ## -- End If
      strfecper_z = fechaperio_z.strftime('%m/%Y') 
      strfecha_z  = fecha_z.strftime('%m/%Y')
      if strfecper_z <> strfecha_z:
         utils.msgdlg("El periodo de la fecha " + strfech_z + \
            " No corresponde al periodo :" + strfecper_z);
         edt_fecha.grab_focus()
         return (-1)
      ## -- End If
      numero_z = utils.StrToInt(edt_numero.get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == True ):
         utils.msgdlg("Ya existe ese Pedido");
         edt_numero.grab_focus()
         return (-1)
      ## -- End If
      
      plazo_z = self.wTree.get_widget("edt_plazo").get_text().upper()
      prove_z = self.wTree.get_widget("edt_almrec").get_text()
      contacto_z = self.wTree.get_widget("edt_contacto").get_text().upper()
      idconcep_z = def_tablas.busca_iddato(mydb, contacto_z, def_tablas.CONCEPTOS)

      entradas['tipo']   = self.tipent_z
      entradas['alm']  = alm_z
      entradas['recemi']  = ''
      entradas['numero']  = numero_z
      entradas['facpro']  = plazo_z
      entradas['prove']  = prove_z
      entradas['perenvrec']  = idconcep_z
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
      if modo_z == NUEVO:
         sql_z = def_tablas.insert_into_entradas(entradas)
      def_tablas.start_trans(mydb)
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
         utils.msgdlg("No existe el Pedido " + alm_z + " " + repr(numero_z));
         return (-1)
      ## -- End If
      self.despliega_datos()
      self.pag_z = 1
      self.nlineas_z = 0
      miarchivo_z = "capped.tex"
      self.arch_z = open(miarchivo_z, "w")
      sql_z = "select a.tipo,a.alm,a.recemi,a.numero,a.conse,a.codinv,a.serie,a.siono,"
      sql_z = sql_z + "a.folsal,a.folent,a.unids,a.costou,a.piva,a.importe,a.cantmueve,"
      sql_z = sql_z + "a.status,a.persenvrec,a.cia,a.vend,a.poblac,a.tipago,a.prvta,"
      sql_z = sql_z + "a.entosal,a.entcan"
      sql_z = sql_z + " from renentra a"
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + entradas['alm'] + "' and a.numero = " + repr(entradas['numero']) 
      sql_z = sql_z + " and a.cia = " + repr(cia_z) + " order by conse"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      unids_z = 0
      ren_z = 0
      impcosto_z = 0
      iva_z = 0
      descri_z = ""
      self.encab()
      for record in result:
        self.nlineas_z = self.nlineas_z + 1
        if self.nlineas_z > utils.LINEAS_X_PAG:
           self.salto_pag()
        #End if
        codigo_z = record[5]
        recemi_z   = record[2]
        prvta_z  = record[21]
        folent_z = str(record[9])
        folsal_z = str(record[8])
        unids_z  = int(record[10])
        costou_z  = record[11]
        idconcep_z = record[16]
        entcan_z = record[23]
        siono_z  = record[7]
        serie_z  = record[6]
        #print codigo_z, costou_z
        mub_z = 0.0
        if codigo_z == "AUXILIAR":
           descri_z   = def_tablas.busca_dato(mydb, idconcep_z, \
              def_tablas.CONCEPTOS)
        else:
           sqlinv_z = "select codigo, descri, costos, coston, piva, precio from inven "
           sqlinv_z = sqlinv_z + " where codigo = '" + codigo_z + "' "
           sqlinv_z = sqlinv_z + " and cia = " + str(cia_z)
           cursorinv = mydb.cursor()
           cursorinv.execute(sqlinv_z)
           resultinv = cursorinv.fetchone()
           if resultinv <> None:
              descri_z   = resultinv[1]
              costo_z    = resultinv[3]
              precio_z   = resultinv[5]
              if precio_z <> 0:
                 mub_z = ( 1 - ( costo_z / precio_z  ) ) * 100
              #End If
           #End if
        #End If
        impcosto_z = impcosto_z + record[11]
        iva_z = iva_z + record[11] * record[12] / 100
        self.arch_z.write(self.subrayado_on)
        self.arch_z.write(descri_z.ljust(30)+"|")
        self.arch_z.write("  " + str(int(unids_z)).rjust(4) + "  |")
        self.arch_z.write(utils.currency(costou_z).rjust(12)+"|")
        self.arch_z.write(utils.currency(mub_z).rjust(5)+"|")
        self.arch_z.write("".ljust(20)+"|")
        self.arch_z.write(self.subrayado_off)
        self.arch_z.write("\n")
      #Fin de For
      total_z = impcosto_z + iva_z
      self.arch_z.write("Importe".rjust(44) + utils.currency(impcosto_z).rjust(12) + "\n")
      self.arch_z.write("Iva    ".rjust(44) + utils.currency(iva_z).rjust(12) + "\n")
      self.arch_z.write("Total  ".rjust(44) + utils.currency(total_z).rjust(12) + "\n")
      self.arch_z.write("Plazo " + entradas['facpro'] + "\n")
      self.arch_z.write(self.subrayado_off + "\n")
      sql_z = "select fecha, observs from observent "
      sql_z = sql_z + " where tipo = '" + self.tipent_z + "' "
      sql_z = sql_z + " and alm = '" + alm_z + "' "
      sql_z = sql_z + " and numero = " + utils.IntToStr(numero_z)
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      sql_z = sql_z + " order by fecha, conse"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result_z = cursor.fetchall()
      for record in result_z:
          self.nlineas_z = self.nlineas_z + 1
          if self.nlineas_z > utils.LINEAS_X_PAG:
             self.salto_pag()
          #End if
          self.arch_z.write(self.subrayado_on + record[1].ljust(70)+ self.subrayado_off + "\n")
      #Fin de For
      self.arch_z.write("Elaboro:_____ __________________\n")
      self.arch_z.write("Almacen:________________ Tesoreria:________________ ACL:________________\n")
      self.arch_z.close()
      visor = utils.visor_editor()
      resp_z = visor.ejecuta(miarchivo_z)

  def salto_pag(self):
      self.arch_z.write(def_tablas.font(mydb, 1, "FORM-FEED FF"))
      self.pag_z = self.pag_z + 1
      self.encab()

  def encab(self):
      self.condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      self.condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      self.subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      self.subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")
      hora_z = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
      self.arch_z.write(cias['razon'].center(80) + "\n")
      self.arch_z.write(self.condensado_on + "capped " + self.condensado_off + \
        (hora_z + " " + cias['dir']).center(70) + "\n")
      self.arch_z.write(("Impresion de Pedidos Pag:" + str(self.pag_z)).center(80) + "\n")
      self.arch_z.write("Numero:" + self.tipent_z + str(entradas['numero']).rjust(6))
      self.arch_z.write(" Periodo: " + entradas['alm'])
      self.arch_z.write(" Fecha: " + entradas['fecha'].strftime('%d/%m/%Y') + "\n")
      nombre_z = ""
      contacto_z = def_tablas.busca_dato(mydb, entradas['perenvrec'], def_tablas.CONCEPTOS)
      if self.tipent_z == "B":
         nombre_z = def_tablas.busca_nombre(mydb, entradas['prove'], cia_z, \
            def_tablas.PROVEEDOR)
         self.arch_z.write(" Proveedor: " + nombre_z + "\n")
      elif self.tipent_z == "G":
         nombre_z = def_tablas.busca_nombre(mydb, entradas['prove'], cia_z, \
            def_tablas.MAYORIS)
         self.arch_z.write(" Cliente: " + nombre_z + "\n")
      #End if
      self.arch_z.write("Contacto: " + contacto_z + "\n")
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("Descripcion".ljust(30)+"|")
      self.arch_z.write("Cantidad".rjust(6)+"|")
      self.arch_z.write("Costo S/Iva".rjust(12)+"|")
      self.arch_z.write("M.U.B".rjust(5)+"|")
      self.arch_z.write("Fecha Recibe".ljust(20)+"|")
      self.arch_z.write(self.subrayado_off)
      self.arch_z.write("\n")
      self.nlineas_z = self.nlineas_z = 7
#Fin de Encab()

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
      sql_z = "select tipo, alm, numero, fecha, prove, perenvrec, facpro, "
      sql_z = sql_z + " importe, iva, total from entradas "
      sql_z = sql_z + " where tipo = '" + self.tipent_z + "' "
      sql_z = sql_z + " and alm = '" + alm_z + "' "
      sql_z = sql_z + " and numero = "  + repr(numero_z) + " and cia= " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         entradas['tipo']       = self.tipent_z
         entradas['alm']        = alm_z
         entradas['numero']     = numero_z
         entradas['fecha']      = record[3]
         entradas['prove']      = record[4]
         entradas['perenvrec']  = record[5]
         entradas['facpro']     = record[6]
         entradas['importe']    = record[7]
         entradas['iva']        = record[8]
         entradas['total']      = record[7] + record[8]
         resp_z = True
      else:
         resp_z = False
      return ( resp_z)

  def despliega_datos(self):
      alm_z = entradas['alm'];
      numero_z = entradas['numero']
      self.busca_alm(alm_z)
      self.wTree.get_widget("edt_numero").set_text(str(numero_z))
      self.wTree.get_widget("edt_fecha").set_text(entradas['fecha'].strftime('%d/%m/%Y'))
      self.wTree.get_widget("edt_plazo").set_text(entradas['facpro'])
      prove_z = entradas['prove']
      self.wTree.get_widget("edt_almrec").set_text(prove_z)
      nombre_z = "SIN NOMBRE :" + self.tipent_z + ":"
      if self.tipent_z == "B":
         #Es pedido de Proveedor, hayq que buscar el nombre del proveedor
         nombre_z = def_tablas.busca_nombre(mydb, prove_z, cia_z,\
                def_tablas.PROVEEDOR)
      elif self.tipent_z == "G":
         #Es pedido de Proveedor, hayq que buscar el nombre del proveedor
         nombre_z = def_tablas.busca_nombre(mydb, prove_z, cia_z,\
                def_tablas.MAYORIS)
      #Fin de if
      self.wTree.get_widget("edt_nomalmrec").set_text(nombre_z)
      contacto_z   = def_tablas.busca_dato(mydb, entradas['perenvrec'], \
                def_tablas.CONCEPTOS)
      self.wTree.get_widget("edt_contacto").set_text(contacto_z)
      self.despliega_totales()
      self.lista_renglones(alm_z, numero_z)

  def despliega_totales(self):
      importe_z = utils.currency(entradas['importe']);
      iva_z = utils.currency(entradas['iva']);
      total_z = utils.currency(entradas['total']);
      self.wTree.get_widget("edt_importe").set_text(importe_z)
      self.wTree.get_widget("edt_iva").set_text(iva_z)
      self.wTree.get_widget("edt_total").set_text(total_z)

  def lista_renglones(self, alm_z='', numero_z=0):
      self.lst_renentra.clear()
      sql_z = "select a.tipo,alm,recemi,numero,codinv,serie,folent,importe,costou,siono,"
      sql_z = sql_z + "persenvrec,vend,poblac,tipago,costou,status,conse,unids"
      sql_z = sql_z + " from renentra a"
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + entradas['alm'] + "' and numero = "
      sql_z = sql_z + str(entradas['numero']) + " and a.cia = " + str(cia_z)
      sql_z = sql_z + " order by conse"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      # get and display one row at a time
      for record in result:
          renentra['tipo']        = record[0]
          renentra['alm']         = record[1]
          renentra['recemi']      = record[2]
          renentra['numero']      = record[3]
          renentra['codinv']      = record[4]
          renentra['serie']       = record[5]
          renentra['folent']      = record[6]
          renentra['importe']     = record[7]
          renentra['costou']      = record[8]
          renentra['siono']       = record[9]
          renentra['persenvrec']  = record[10]
          renentra['vend']        = record[11]
          renentra['poblac']      = record[12]
          renentra['tipago']      = record[13]
          renentra['costou']      = record[14]
          renentra['status']      = record[15]
          renentra['conse']       = record[16]
          renentra['unids']       = record[17]
          codigo_z = renentra['codinv']
          if codigo_z == "AUXILIAR":
             descri_z   = def_tablas.busca_dato(mydb, renentra['persenvrec'], \
                def_tablas.CONCEPTOS)
          else:
             descri_z   = def_tablas.busca_nombre(mydb, codigo_z, cia_z,\
                def_tablas.INVEN)
          #End If
          costou_z = utils.currency(renentra['costou'])
          importe_z = utils.currency(renentra['importe'])
          self.lst_renentra.append([ int(renentra['unids']), \
            renentra['codinv'], descri_z, costou_z, importe_z,  renentra['conse'] ])

  def ren_seleccionado(self, alm_z='', numero_z=0, tipo_z=0):
      colconse_z = 5
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
      sql_z = sql_z + "a.status,a.persenvrec,a.cia,a.vend,a.poblac,a.tipago,a.prvta,a.entosal,a.entcan"
      sql_z = sql_z + " from renentra a "
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + alm_z + "' and a.numero = " + repr(numero_z) 
      sql_z = sql_z + " and conse = " + repr(conse_z) + " and a.cia = " + repr(cia_z)
      codigo_z = ''
      descri_z = ''
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
      codigo_z = renentra['codinv']
      if codigo_z == "AUXILIAR":
         descri_z   = def_tablas.busca_dato(mydb, renentra['persenvrec'], \
            def_tablas.CONCEPTOS)
      else:
            descri_z   = def_tablas.busca_nombre(mydb, codigo_z, cia_z,\
            def_tablas.INVEN)
      #End If
      costou_z               = utils.currency(renentra['costou'])
      importe_z              = utils.currency(renentra['importe'])
      canti_z                = str(int((renentra['unids'])))
      self.wTree.get_widget("edt_codigo").set_text(codigo_z)
      self.wTree.get_widget("edt_descri").set_text(descri_z)
      self.wTree.get_widget("edt_canti").set_text(canti_z)
      self.wTree.get_widget("edt_costou").set_text(costou_z)

  def limpia_campos(self):
      campos_z = [ "edt_almacen", "edt_numero", "edt_fecha", "edt_importe",
        "edt_iva", "edt_total", "edt_almrec", "edt_nomalmrec", "edt_contacto",
        "edt_plazo", "edt_codigo", "edt_descri", "edt_canti", "edt_costou" ]
      
      for micampo_z in campos_z:
          self.wTree.get_widget(micampo_z).set_text('')
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
      #self.wTree.get_widget("edt_nomcli").set_editable(modo)
      #self.wTree.get_widget("edt_vend").set_editable(modo)
      #self.wTree.get_widget("edt_poblac").set_editable(modo)
      #self.wTree.get_widget("edt_tipago").set_editable(modo)
      #self.wTree.get_widget("edt_preciovta").set_editable(modo)
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

# Fin de Clase Captrasp

if __name__ == "__main__":
   hwg = Capped()
   hwg.wTree.get_widget("win_capped").connect("destroy", gtk.main_quit )
   gtk.main()

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    for option, argument in opts:
        if option in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        else:
            tipent_z = option
    #Fin de For

    #self.wTree.get_widget("win_capped").connect("destroy", gtk.main_quit )
    hwg = Capped()
    gtk.main()
    return 0
