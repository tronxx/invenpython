#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Manto  de Vendedores DRBR 26-May-2007
import sys
import types
import string, os
try:
  import pygtk
  import gobject
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
import Numeral
import datetime
platform = sys.platform 

global mydb
global cia_z
global mibd
global cias
global vendedor
global almacen
global businven_z

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
CREDCON      = def_tablas.CREDCON
MAYORIS      = def_tablas.MAYORIS

modo_z       = 0
businven_z   = False
estoyren_z   = 0
estoyen_z    = def_tablas.ENTRADAS
mibd = def_tablas.lee_basedato_ini()
cias = def_tablas.define_cias()
vendedor = def_tablas.define_vendedor()
mayoris = def_tablas.define_mayoris()
almacen  = def_tablas.define_ptovta()
ptovta   = def_tablas.define_almacen()
entradas = def_tablas.define_entradas()
renentra = def_tablas.define_renentra()
inven    = def_tablas.define_inven()
facturma = def_tablas.define_facturma()
renfacma = def_tablas.define_renfacma()

dirprogs_z = ".." + os.sep + "altaalm" + os.sep
selfolios_z = "N"

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

class Hazfacma:
  """Esta es una aplicación Captura de Facturas Mayoreo"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "hazfacma.glade"
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
            "on_btn_seriesren_clicked": self.on_btn_seriesren_clicked, \
            "on_btn_borraren_clicked": self.on_btn_borraren_clicked, \
            "on_btn_primero_clicked": self.on_btn_primero_clicked, \
            "on_btn_anter_clicked": self.on_btn_anter_clicked, \
            "on_btn_sigte_clicked": self.on_btn_sigte_clicked, \
            "on_btn_ultimo_clicked": self.on_btn_ultimo_clicked, \
            "on_btn_imprime_clicked": self.on_btn_imprime_clicked, \
            "on_edt_codigo_focus_out_event": self.on_edt_codigo_focus_out_event, \
            "on_edt_fecha_focus_out_event": self.on_edt_fecha_focus_out_event, \
            "on_edt_mayoris_focus_out_event": self.on_edt_mayoris_focus_out_event, \
            "on_edt_numero_activate": self.on_edt_numero_activate
            }
    self.wTree.signal_autoconnect(dic)
    self.wTree.get_widget("edt_codigo").connect("activate", self.on_edt_codigo_focus_out_event)
    self.wTree.get_widget("edt_fecha").connect("focus_out_event", self.on_edt_fecha_focus_out_event)
    self.wTree.get_widget("edt_pagos").connect("focus_out_event", self.on_edt_fecha_focus_out_event)
    self.wTree.get_widget("edt_plazo").connect("focus_out_event", self.on_edt_fecha_focus_out_event)
    self.wTree.get_widget("edt_pagos").connect("activate", self.on_edt_fecha_focus_out_event)
    self.wTree.get_widget("edt_plazo").connect("activate", self.on_edt_fecha_focus_out_event)
    camposnum_z = [ "edt_preciovta", "edt_canti", "edt_importe", "edt_descto", \
      "edt_iva", "edt_total" ]
    for micamponum_z in camposnum_z:
        self.wTree.get_widget(micamponum_z).set_property('xalign', 1)
    #End For
    #self.wTree.get_widget("win_hazfacma").connect("destroy", gtk.main_quit )
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
    dsn_z = "dsn="+mibd['base']+";uid="+mibd['user']+";pwd="+mibd['password']
    if mibd['tipobd'] == "MYSQL":
       mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
    elif mibd['tipobd'] == "ODBC":
       mydb = pyodbc.connect(dsn_z)

    cias = def_tablas.busca_cia(mydb, cia_z)

    self.editable_onoff(False)
    self.activa_aceptar_cancelar(False)
    self.activa_renglones(False)
    self.lst_renentra = gtk.ListStore(str, str, str, str, str, int)
    grd_renentra = self.wTree.get_widget("grd_renentra")
    grd_renentra.set_model(self.lst_renentra)
    columnas_z = [ "Codigo", "Descripcion", "Cantidad", "Precio U.", "Total" ]
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
    
    self.wTree.get_widget("edt_preciovta").set_property('xalign', 1)
    self.wTree.get_widget("edt_canti").set_property('xalign', 1)
    #edt_alm = self.wTree.get_widget("edt_almacen")
    #edt_alm.connect("activate", self.on_edt_almacen_focus_out_event)
    self.wTree.get_widget("edt_codigo").connect("activate", self.on_edt_codigo_focus_out_event)
    self.wTree.get_widget("edt_mayoris").connect("activate", self.on_edt_mayoris_focus_out_event)
    estoyen_z = def_tablas.ENTRADAS
    self.asigna_tipent("S")

  def asigna_tipent(self, tipo_z):
    self.tipent_z = tipo_z
    miwin = self.wTree.get_widget("win_hazfacma")
    miwin.set_title(cias['razon'] + " Captura de Facturas Mayoreo")
    self.tipospago_z = []
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
      alm_z   = "self.wTree.get_widget(edt_almacen).get_text().upper()"
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == False ):
         utils.msgdlg("No existe la Factura " + repr(numero_z));
         return (-1)
      ## -- End If
      self.despliega_datos()

  def on_btn_renglones_clicked(self, widget):
      global estoyen_z
      global estoyren_z
      alm_z   = "self.wTree.get_widget(edt_almacen).get_text().upper()"
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == False ):
         utils.msgdlg("No existe la Factura " + repr(numero_z));
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
      numero_z = facturma['num']
      if facturma['status'] == "C":
         utils.msgdlg("Factura Cerrada, No puede afectar")
         return (-1)
      #End if
      resp_z = utils.yesnodlg("Seguro de Cerrar esta Factura ?")
      if resp_z <> gtk.RESPONSE_OK:
         utils.msgdlg("No Se cierra la Factura")
         return (-1)
      #End if
      if facturma['mayomen'] == "Y":
         self.haz_pagares()
         self.agre_edomay()
      #End If
      sql2_z = "update facturma set status = 'C' "
      sql2_z = sql2_z + " where num = " + utils.IntToStr(numero_z)
      sql2_z = sql2_z + " and cia = " + utils.IntToStr(cia_z)
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql2_z)
      def_tablas.commit_trans(mydb)
  #End Cierra Facturas 

  def haz_pagares(self):
      factura_z = facturma['num']
      mayoris_z = facturma['mayoris']
      importe_z = facturma['total']
      npagos_z = facturma['npagos']
      fecha_z = facturma['fecha']
      vencefac_z = facturma['fecha']
      tipago_z = facturma['tipago']
      if npagos_z == 1:
         impxpag_z = importe_z
         impulpag_z = importe_z
      else:
         impxpag_z = round(importe_z / npagos_z, 2)
         impulpag_z = round(importe_z - ( impxpag_z * (npagos_z - 1)), 2)
      #End If
      idmov_z = def_tablas.busca_sigte(mydb, '', '', 0, cia_z, def_tablas.MOVMAY)
      conse_z = 1
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      for letra_z in range (npagos_z):
          letra_z = letra_z + 1
          if letra_z == 1:
             vence_z = vencefac_z
          else:
             if plazo_z == 30:
                vence_z = utils.SumaMeses(vencefac_z, letra_z)
             else:
                vence_z = vencefac_z + datetime.timedelta( dias_z * letra_z)
             #End If
          #End If
          concep_z = "Factura " + str(factura_z).rjust(6) + " Pagare " + str(letra_z)
          if letra_z == npagos_z:
             impxpag_z = impulpag_z
          #End if
          movmay = def_tablas.define_movmay()
          movmay['mayoris']  = mayoris_z
          movmay['docto']    = factura_z
          movmay['pagare']   = letra_z
          movmay['conse']    = conse_z
          movmay['fecha']    = fecha_z
          movmay['vence']    = vence_z
          movmay['concep']   = concep_z
          movmay['coa']      = "C"
          movmay['importe']  = impxpag_z
          movmay['saldo']    = impxpag_z
          movmay['cia']      = cia_z
          movmay['tipago']   = tipago_z
          movmay['idconcep'] = 0
          movmay['fecsal']   = fecha_z
          movmay['idmov']    = idmov_z
          sql_z = def_tablas.insert_into_movmay(movmay)
          #print sql_z
          cursor.execute(sql_z)
          idmov_z = idmov_z + 1
          conse_z = conse_z + 1
          
      #End For
      def_tablas.commit_trans(mydb)
  #Fin de haz_pagares

  def agre_edomay(self):
      factura_z = facturma['num']
      mayoris_z = facturma['mayoris']
      importe_z = facturma['total']
      fecha_z = utils.UltimoDeMes(facturma['fecha'])
      sql_z = "select * from edomay where mayoris= '" + mayoris_z + "'"
      sql_z = sql_z + " and fecha ='" + fecha_z.strftime('%Y-%m-%d') + "'"
      sql_z = sql_z + " and cia =" + utils.IntToStr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result_z = cursor.fetchone()
      if result_z <> None:
         edomay = def_tablas.define_edomay()
         edomay['fecha'] = fecha_z
         edomay['mayoris']=mayoris_z
         edomay['compras']=importe_z
         edomay['sdofin']=importe_z
         sql_z = def_tablas.insert_into_edomay(edomay)
      else:
         sql_z = "update edomay set compras = compras + " + str(importe_z) + " , "
         sql_z = sql_z + " sdofin = sdofin + " + str(importe_z)
         sql_z = sql_z + " where  mayoris= '" + mayoris_z + "'"
         sql_z = sql_z + " and fecha ='" + fecha_z.strftime('%Y-%m-%d') + "'"
         sql_z = sql_z + " and cia =" + utils.IntToStr(cia_z)
      #End if
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
  #Fin de agre_edomay
      
  def on_edt_almacen_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.ENTRADAS:
         return (-1)
      edt_almacen  = widget
      if self.busca_alm(edt_almacen.get_text().upper()) == True:
         edt_almacen.set_text(almacen['clave'])

  def on_edt_ptovta_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA:
         return (-1)
      edt_almacen  = widget
      if self.busca_ptovta(edt_almacen.get_text().upper()) == True:
         edt_almacen.set_text(ptovta['clave'])

  def on_btn_nuevoren_clicked(self, widget):
      global modo_z
      if facturma['status'] == "C":
         utils.msgdlg("Factura Cerrada, No puede afectar")
         return (-1)
      modo_z = NUEVOREN
      self.renglon_editable_onoff(True)
      self.activa_aceptar_cancelar(True)
      self.wTree.get_widget("edt_canti").set_text("1")
      self.wTree.get_widget("edt_codigo").grab_focus()

  def on_btn_borraren_clicked(self, widget):
      if estoyen_z <> def_tablas.RENENTRA:
         return (-1)
      if facturma['status'] == "C":
         utils.msgdlg("Factura Cerrada, No puede afectar")
         return (-1)
      resp_z = utils.yesnodlg("Seguro de Eliminar este Renglon ?")
      if resp_z == gtk.RESPONSE_OK:
         numero_z = facturma['num']
         importe_z = renfacma['importe']
         descu_z = renfacma['descu']
         iva_z = renfacma['iva']
         total_z = renfacma['total']
         facturma['importe'] = facturma['importe'] - importe_z
         facturma['descu'] = facturma['descu'] - descu_z
         facturma['neto'] = facturma['neto'] - importe_z - descu_z
         facturma['iva'] = facturma['iva'] - iva_z
         facturma['total'] = facturma['total'] - total_z

         sql_z = "delete from renfacma "
         sql_z = sql_z + " where factur = "
         sql_z = sql_z + utils.IntToStr(numero_z) 
         sql_z = sql_z + " and consec=" + utils.IntToStr(renfacma['consec']) 
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
         sql2_z = " update facturma set importe = importe - " + str(importe_z) + ", "
         sql2_z = sql2_z + " descu = descu - " + str(descu_z) + ", "
         sql2_z = sql2_z + " neto = neto - " + str(importe_z - descu_z) + ", "
         sql2_z = sql2_z + " iva = iva - " + str(iva_z) + ", "
         sql2_z = sql2_z + " total = total - " + str(total_z)
         sql2_z = sql2_z + " where num = " + utils.IntToStr(numero_z)
         sql2_z = sql2_z + " and cia = " + utils.IntToStr(cia_z)

         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         cursor.execute(sql2_z)
         def_tablas.commit_trans(mydb)
         self.despliega_totales()
         self.lista_renglones()

  def on_edt_codigo_focus_out_event(self, widget, tipo=None):
      #utils.msgdlg("Estoy en edt_codigo_focus_out")
      global businven_z
      if businven_z == True:
         #utils.msgdlg("businven_z = True")
         return(-1)
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         #utils.msgdlg("estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN")
         return (-1)
      widget.set_text(widget.get_text().upper())
      codigo_z = widget.get_text()
      if codigo_z <> "AUXILIAR":
         if ( self.busca_inv(codigo_z) == True):
            self.despliega_codigo()
         #End If
         self.wTree.get_widget("edt_descri").set_editable = False
         self.wTree.get_widget("edt_canti").grab_focus()
      else:
      #  Es aux, hay que hacer editable la descripcion
         self.wTree.get_widget("edt_descri").set_editable = True
      #End If
      businven_z = False

  def despliega_codigo(self):
      empaqe_z = inven['empaqe']
      costosi_z = inven['costos']
      preciomds_z = inven['precio']
      piva_z = inven['piva']
      preciomay_z = utils.calcu_preciomay(empaqe_z, costosi_z, preciomds_z, piva_z)
      self.wTree.get_widget("edt_codigo").set_text(inven['codigo'])
      self.wTree.get_widget("edt_descri").set_text(inven['descri'])
      self.wTree.get_widget("edt_preciovta").set_text(str(preciomay_z))
  #Fin Despliega_datos()

  def on_edt_fecha_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.ENTRADAS and modo_z <> NUEVO:
         return (-1)
      #End If
      fecha_z = utils.StrToDate(self.wTree.get_widget("edt_fecha").get_text())
      pagos_z = utils.StrToInt(self.wTree.get_widget("edt_pagos").get_text())
      plazo_z = utils.StrToInt(self.wTree.get_widget("edt_plazo").get_text())
      if plazo_z == 30:
         vence_z = utils.SumaMeses(fecha_z, pagos_z)
      else:
         vence_z = fecha_z + datetime.timedelta( plazo_z * pagos_z)
      #End If
      self.wTree.get_widget("edt_vence").set_text(utils.DateToStr(vence_z))
  #Fin on_edt_fecha_focus_out_event


  def on_edt_mayoris_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.ENTRADAS and modo_z <> NUEVO and modo_z <> MODIFICA:
         return (-1)
      mayoris_z = widget.get_text().upper()
      if ( self.busca_mayoris(mayoris_z) == True):
         widget.set_text(mayoris['codigo'])

  def on_edt_nomcli_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
      widget.set_text(widget.get_text().upper())
        
  def on_edt_preciovta_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.RENENTRA and modo_z <> NUEVOREN:
         return (-1)
  
  def on_btn_nuevo_clicked(self, widget):
      global modo_z
      modo_z = NUEVO
      alm_z = ""
      self.limpia_campos()
      edt_numero  = self.wTree.get_widget("edt_numero")
      edt_fecha  = self.wTree.get_widget("edt_fecha")
      self.editable_onoff(True)
      self.activa_aceptar_cancelar(True)
      numero_z = def_tablas.busca_sigte(mydb, self.tipent_z, alm_z, 0, cia_z, def_tablas.FACTURMA)
      edt_numero.set_text(utils.IntToStr(numero_z))
      edt_fecha.set_text(datetime.date.today().strftime('%d/%m/%Y'))
      edt_numero.grab_focus()

  def busca_mayoris(self, mayoris_z = ''):
      edt_vend  = self.wTree.get_widget("edt_mayoris")
      edt_nombre   = self.wTree.get_widget("edt_nommay")
      if mayoris_z == '':
         mayoris_z = edt_vend.get_text().upper()
      resp_z = self.busca_codmay(mayoris_z)
      if resp_z <> True:
        sql_z = "select codigo, nombre from mayoris "
        sql_z = sql_z + " where cia = " + utils.IntToStr(cia_z) + " order by codigo"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El Mayorista")
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
         self.wTree.get_widget("edt_mayoris").set_text(mayoris['codigo'])
         self.wTree.get_widget("edt_nommay").set_text(mayoris['nombre'])
         self.wTree.get_widget("edt_dircli").set_text(mayoris['direc'])
         self.wTree.get_widget("edt_rfc").set_text(mayoris['rfc'])
      #End If
      return (resp_z)

  def busca_codmay(self, mayoris_z=''):
      resp_z = False
      sql_z = "select codigo, nombre, direc, ciu, rfc, nompag1, \
      nompag2, dirpag1, dirpag2, nombre2, ciupag from mayoris "
      sql_z = sql_z + " where codigo = '" + mayoris_z + "'"
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         mayoris['codigo']  = record[0]
         mayoris['nombre']  = record[1]
         mayoris['direc']   = record[2]
         mayoris['ciu']     = record[3]
         mayoris['rfc']     = record[4]
         mayoris['nompag1']     = record[5]
         mayoris['nompag2']     = record[6]
         mayoris['dirpag1']     = record[7]
         mayoris['dirpag2']     = record[8]
         mayoris['ciupag']      = record[9]
         mayoris['nombre2']     = record[10]
         resp_z = True
      return (resp_z)
  #Fin de busca_codmay()

  def busca_inv(self, codigo_z = ''):
      global businven_z
      businven_z = True
      resp_z = False
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      if codigo_z == '':
         codigo_z = edt_codigo.get_text().upper()
      #Fin de If
      resp_z = self.busca_codigo(codigo_z)
      if resp_z == False:
         sql_z = "select codigo, descri, tipo "
         sql_z = sql_z + "from inven where codigo like '" + codigo_z + "%'"
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z) + " order by codigo"
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         result_z = cursor.fetchall()
         datosbuscados_z = utils.busca_datos(result_z, "Codigo:Descripcion:Tipo", "Seleccione El Articulo")

         miresp_z = datosbuscados_z.split(":")
         resp_z = utils.StrToInt(miresp_z[-1])
         if resp_z == gtk.RESPONSE_OK:
            resp_z = self.busca_codigo(miresp_z[0])
         else:
            resp_z = False
         #endif
      #endif
      businven_z = False
      if resp_z == True:
         self.despliega_codigo()
      #Fin de if
      return (resp_z)

  def busca_codigo(self, codigo_z = ''):
      resp_z = False
      sql_z = "select codigo, descri, tipo, costos, coston, piva, precio "
      sql_z = sql_z + " from inven where codigo = '" + codigo_z +"' "
      sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
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
        inven['precio']    = record[6]
        resp_z = True
      #End if
      return (resp_z)
  #Fin de busca_codigo

  def on_btn_modif_clicked(self, widget):
      global modo_z
      alm_z = ""
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      resp_z = self.busca_entrada( alm_z, numero_z)
      if resp_z <> True:
         utils.msgdlg("No existe esa Factura");
         edt_numero.grab_focus()
         return (-1)
         ## -- End If
      #End if
      modo_z = MODIFICA
      edt_nombre = self.wTree.get_widget("edt_nommay")
      self.editable_onoff(True)
      self.activa_aceptar_cancelar(True)
      edt_nombre.grab_focus()

  def on_btn_borra_clicked(self, widget):
      global modo_z
      modo_z = BORRAR
      if facturma['status'] == "C":
         utils.msgdlg("Factura Cerrada, No puede eliminar")
         return (-1)
      resp_z = utils.yesnodlg("Seguro de Eliminar esta Factura completa ?")
      if resp_z == gtk.RESPONSE_OK:
         def_tablas.borra_facturma(mydb, facturma['num'], cia_z)
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

  def on_btn_seriesren_clicked(self, widget):
      canti_z = utils.StrToInt(self.wTree.get_widget("edt_canti").get_text())
      if facturma['status'] == "C":
         editable_z = "N"
      else:
         editable_z = "S"
      #End If
      sql_z = "select serie from seriefacma where factur = " + str(facturma['num'])
      sql_z = sql_z + " and renglon = " + str(renfacma['consec']) + " order by serie"
      series_z = []
      #print sql_z
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      ii_z = 0
      for record in result:
          ii_z = ii_z + 1
          series_z.append([ii_z, record[0], editable_z])
      #End for
      pide_series = utils.pide_series_mayoreo("No:Serie:Editable", "Proporcione las Series", series_z, editable_z, canti_z)
      resp_z = pide_series.ejecuta()
      #-- Si llego hasta aqui es que ha proporcionado las Series
      #print resp_z
      if resp_z[0][1] <> gtk.RESPONSE_OK:
         return (-1)
      #End If
      series_z = resp_z[0][0]
      sql_z = "delete from seriefacma where factur = " + str(facturma['num'])
      sql_z = sql_z + " and renglon = " + str(renfacma['consec'])
      #print sql_z
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      ii_z = 1
      for miserie_z in series_z:
          sql_z = "insert into seriefacma (factur,renglon,consec,codinv,serie,cia) "
          sql_z = sql_z + " values ( " + str(facturma['num']) + ", "
          sql_z = sql_z + str(renfacma['consec']) + ", " + str(ii_z) + ", "
          sql_z = sql_z + "'" + renfacma['codigo'] + "', '" + miserie_z[1] + "', "
          sql_z = sql_z + str(cia_z) + ")"
          ii_z = ii_z + 1
          #print sql_z
          cursor.execute(sql_z)
      #End For
      def_tablas.commit_trans(mydb)
  #FIn de on_btn_seriesren_clicked(self, widget):

  def agrega_nuevo_ren(self):
      numero_z = facturma['num']
      alm_z = ''
      descri_z = self.wTree.get_widget("edt_descri").get_text().upper()
      codigo_z = self.wTree.get_widget("edt_codigo").get_text().upper()
      costo_z = 0
      piva_z = 15
      pdsc_z = 0
      if codigo_z <> "AUXILIAR":
         if  self.busca_codigo(codigo_z) == False:
             utils.msgdlg("No tiene un articulo valido...")
             self.wTree.get_widget("edt_codigo").grab_focus()
             return ( -1)
         #End If
         costo_z = inven['costos']
         piva_z = inven['piva']
      #End If
      canti_z = utils.StrToInt(self.wTree.get_widget("edt_canti").get_text())
      preciovta_z = utils.StrToFloat(self.wTree.get_widget("edt_preciovta").get_text())
      conse_z = def_tablas.busca_sigte(mydb, self.tipent_z, alm_z, numero_z, cia_z, def_tablas.RENFACMA)
      importe_z = preciovta_z * canti_z
      descu_z = importe_z * pdsc_z
      iva_z = round( importe_z * piva_z / 100, 2)
      total_z = importe_z + iva_z
      renfacma = def_tablas.define_renfacma()
      renfacma['factur']= numero_z
      renfacma['consec']= conse_z
      renfacma['codigo']= codigo_z
      renfacma['descri']= descri_z
      renfacma['unids']= canti_z
      renfacma['preciou']= preciovta_z
      renfacma['importe']= importe_z
      renfacma['pordsc']= pdsc_z
      renfacma['descu']= descu_z
      renfacma['poriva']= piva_z
      renfacma['iva']= iva_z
      renfacma['total']= total_z
      renfacma['costou']= costo_z
      renfacma['cia']= cia_z
      facturma['importe'] = facturma['importe'] + importe_z
      facturma['descu'] = facturma['descu'] + descu_z
      facturma['neto'] = facturma['neto'] + importe_z - descu_z
      facturma['iva'] = facturma['iva'] + iva_z
      facturma['total'] = facturma['total'] + total_z
      
      sql_z = def_tablas.insert_into_renfacma(renfacma)
      sql2_z = " update facturma set importe = importe + " + str(importe_z) + ", "
      sql2_z = sql2_z + " descu = descu + " + str(descu_z) + ", "
      sql2_z = sql2_z + " neto = neto + " + str(importe_z - descu_z) + ", "
      sql2_z = sql2_z + " iva = iva + " + str(iva_z) + ", "
      sql2_z = sql2_z + " total = total + " + str(total_z)
      sql2_z = sql2_z + " where num = " + utils.IntToStr(numero_z)
      sql2_z = sql2_z + " and cia = " + utils.IntToStr(cia_z)
      #print "sql:", sql_z
      #print "sql2:", sql2_z
      
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      cursor.execute(sql2_z)
      def_tablas.commit_trans(mydb)
      self.despliega_totales()
      self.lista_renglones(alm_z, numero_z)
      self.renglon_editable_onoff(False)
      self.activa_aceptar_cancelar(False)

  def nueva_modif_entradas(self):
      global modo_z
      sql_z = ''
      edt_fecha    = self.wTree.get_widget("edt_fecha")
      edt_numero   = self.wTree.get_widget("edt_numero")
      fecha_z = utils.StrToDate(edt_fecha.get_text())
      if ( fecha_z == -1):
         utils.msgdlg("Fecha Invalida:" + edt_fecha.get_text());
         edt_fecha.grab_focus()
         return (-1)
      ## -- End If
      vence_z = utils.StrToDate(self.wTree.get_widget("edt_vence").get_text())
      if ( vence_z == -1):
         utils.msgdlg("Vencimiento Invalido:" + self.wTree.get_widget("edt_vence").get_text());
         self.wTree.get_widget("edt_vence").grab_focus()
         return (-1)
      ## -- End If
      alm_z = ""
      numero_z = utils.StrToInt(edt_numero.get_text())
      if modo_z == NUEVO:
         resp_z = self.busca_entrada( alm_z, numero_z)
         if resp_z == True:
            utils.msgdlg("Ya existe esa Factura");
            edt_numero.grab_focus()
            return (-1)
         ## -- End If
      #End if
      mayoris_z = self.wTree.get_widget("edt_mayoris").get_text().upper()
      if ( self.busca_codmay(mayoris_z) <> True):
          utils.msgdlg("Mayorista Inexistente");
          self.wTree.get_widget("edt_mayoris").grab_focus()
          return (-1)
      ## -- End If
      npagos_z = utils.StrToInt(self.wTree.get_widget("edt_pagos").get_text())
      plazo_z = utils.StrToInt(self.wTree.get_widget("edt_plazo").get_text())
      pdsc_z = utils.StrToFloat(self.wTree.get_widget("edt_pdsc").get_text())
      nomcli_z = self.wTree.get_widget("edt_nommay").get_text().upper()
      dir_z = self.wTree.get_widget("edt_dircli").get_text().upper()
      rfc_z = self.wTree.get_widget("edt_rfc").get_text().upper()
      refer_z = self.wTree.get_widget("edt_refer").get_text().upper()
      mayomen_z = self.wTree.get_widget("edt_maymen").get_text().upper()
      tipago_z = self.wTree.get_widget("edt_intmer").get_text().upper()
      if mayomen_z not in ["M", "Y"]:
          utils.msgdlg("Debe Selecionar Menudeo o maYoreo M/Y");
          self.wTree.get_widget("edt_maymen").grab_focus()
          return (-1)
      ## -- End If
      if tipago_z not in ["M", "I", "O"]:
          utils.msgdlg("Debe Selecionar Mercancia Interes o mOratios M/I/O");
          self.wTree.get_widget("edt_intmer").grab_focus()
          return (-1)
      ## -- End If
      facturma['num'] = numero_z
      facturma['mayoris'] = mayoris_z
      facturma['refer'] = refer_z
      facturma['nomay'] = nomcli_z
      facturma['dir'] = dir_z
      facturma['rfc'] = rfc_z
      facturma['status'] = "A"
      facturma['fecha'] = fecha_z
      facturma['vence'] = vence_z
      facturma['cia'] = cia_z
      facturma['npagos'] = npagos_z
      facturma['plazo'] = plazo_z
      facturma['tipago'] = tipago_z
      facturma['pdsc'] = pdsc_z
      facturma['mayomen'] = mayomen_z

      if modo_z == NUEVO:
         facturma['importe'] = 0
         facturma['descu'] = 0
         facturma['neto'] = 0
         facturma['iva'] = 0
         facturma['total'] = 0
         sql_z = def_tablas.insert_into_facturma(facturma)
      else:
         sql_z = "update facturma set "
         sql_z = sql_z + "mayoris = '" + mayoris_z + "', "
         sql_z = sql_z + "refer = '" + refer_z + "', "
         sql_z = sql_z + "nomay = '" + nomcli_z + "', "
         sql_z = sql_z + "dir = '" + dir_z + "', "
         sql_z = sql_z + "rfc = '" + rfc_z + "', "
         sql_z = sql_z + "fecha = '" + fecha_z.strftime('%Y-%m-%d') + "', "
         sql_z = sql_z + "vence = '" + vence_z.strftime('%Y-%m-%d') + "', "
         sql_z = sql_z + "npagos = '" + str(npagos_z) + "', "
         sql_z = sql_z + "plazo = '" + str(plazo_z) + "', "
         sql_z = sql_z + "tipago = '" + tipago_z + "', "
         sql_z = sql_z + "pdsc = " + str(pdsc_z) + ", "
         sql_z = sql_z + "mayomen = '" + mayomen_z + "' "
         sql_z = sql_z + " where num = " + utils.IntToStr(numero_z)
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      #Fin de If
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      #print sql_z
      cursor.execute(sql_z)
      def_tablas.commit_trans(mydb)
      self.busca_entrada( alm_z, numero_z)
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
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      alm_z = ''
      nommay_z = facturma['nomay']
      nommay2_z = mayoris['nombre2']
      fecha_z = facturma['fecha']
      npagos_z = facturma['npagos']
      ciumay_z = mayoris['ciu']
      resp_z = self.busca_entrada( alm_z, numero_z)
      if ( resp_z == False ):
         utils.msgdlg("No existe la Factura " + repr(numero_z));
         return (-1)
      ## -- End If
      self.despliega_datos()
      if facturma['status'] <> "C":
         utils.msgdlg("Esta Factura no esta cerrada " + repr(numero_z));
         return (-1)
      ## -- End If
      pag_z = 1
      miarchivo_z = "hazfacma.tex"
      arch_z = open(miarchivo_z, "w")
      reset_imp = def_tablas.font(mydb, 1, "RESET")
      font_pica = def_tablas.font(mydb, 1, "PICA-PITCH")
      condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      emphized_on = def_tablas.font(mydb, 1, "EMPHAIZED ON")
      emphized_off = def_tablas.font(mydb, 1, "EMPHAIZED OFF")
      subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")
      arch_z.write(reset_imp + font_pica + "".ljust(60) + utils.IntToStr(facturma['num']).rjust(6) +"\n" )
      arch_z.write("".ljust(10) + condensado_on + nommay_z.ljust(50) + condensado_off )
      arch_z.write("".ljust(10) + facturma['rfc'].ljust(15) + "\n")
      arch_z.write("".ljust(10) + condensado_on + nommay2_z.ljust(50) + condensado_off + "\n" )
      arch_z.write("".ljust(12) + facturma['dir'] + " " + ciumay_z + "\n\n\n\n\n")

      campos_z = [ "factur", "consec", "codigo", "descri", "unids", "preciou", "importe" ]
      sql_z = "select "
      ii_z = 0
      for micampo_z in campos_z:
          if ii_z > 0:
             sql_z = sql_z + ","
          #End if
          sql_z = sql_z + micampo_z
          ii_z = ii_z + 1
      sql_z = sql_z + " from renfacma "
      sql_z = sql_z + " where factur = " + utils.IntToStr(numero_z)
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      sql_z = sql_z + " order by consec"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      ren_z = 0
      impcosto_z = 0
      iva_z = 0
      for record in result:
        ren_z = ren_z + 1
        codigo_z   = record[2]
        descri_z   = record[3]
        unids_z    = record[4]
        prvta_z    = record[5]
        importe_z  = record[6]
        arch_z.write(str(int(unids_z)).rjust(7)+ "".ljust(6))
        arch_z.write(descri_z.ljust(40))
        arch_z.write(utils.currency(prvta_z).rjust(9) + " ")
        arch_z.write(utils.currency(importe_z).rjust(13))
        arch_z.write("\n")
      for ii_z in range ( 28 - ren_z):
          arch_z.write("\n")
      #End For
      arch_z.write(emphized_on + "".ljust(10) + "SOMOS COMPRADORES DE TERCERA MANO" + emphized_off + "\n" )
      neto_z = facturma['total'] - facturma['iva']
      if facturma['descu'] <> 0:
         arch_z.write("".ljust(44) + "Importe".rjust(20) + utils.currency(facturma['importe']).rjust(13) + "\n" )
         arch_z.write("".ljust(44) + "Descuento".rjust(20) + utils.currency(facturma['descu']).rjust(13) + "\n" )
      else:
         arch_z.write("\n\n")
      #Fin de If
      arch_z.write("\n")
      enletras_z = self.numeros_a_pesos(facturma['total'])
      arch_z.write("".ljust(64) + utils.currency(neto_z).rjust(13) + "\n" )
      arch_z.write("".ljust(64) + utils.currency(facturma['iva']).rjust(13) + "\n" )
      arch_z.write("".ljust(12) + condensado_on + enletras_z + condensado_off + "\n" )
      arch_z.write("".ljust(64) + utils.currency(facturma['total']).rjust(13) + "\n\n" )
      if facturma['npagos'] > 1:
        arch_z.write("".ljust(14) + "Esta Factura sera pagada en "  + str(facturma['npagos']) + " Exhibiciones") 
      else:
        arch_z.write("".ljust(14) + "Esta Factura sera pagada en una sola Exhibicion") 
      #End if
      arch_z.write("\n") 
      arch_z.write("".ljust(14) + "Efectos fiscales al pago\n") 
      arch_z.write("".ljust(32) + str(fecha_z.day) + utils.NombreMes(fecha_z).center(17) + str(fecha_z.year).rjust(25) + "\n") 
      arch_z.close()
      visor = utils.visor_editor()
      resp_z = visor.ejecuta(miarchivo_z)
      resp_z = utils.piderangosdlg("Desea Imprimir los Pagares ? ", 0, "Pagare Inicial", 1, "Pagare Final", npagos_z)
      if resp_z[0] == gtk.RESPONSE_OK:
         self.imprime_pagares(resp_z[1], resp_z[2])
      #End If
      resp_z = utils.yesnodlg("Desea Imprimir la lista de Precios Sugerida ?")
      if resp_z == gtk.RESPONSE_OK:
         self.lista_precios()
      #End if
  #Fin de on_btn_imprime

  def imprime_pagares(self, ini_z, fin_z):
      npagos_z = facturma['npagos']
      fecha_z = facturma['fecha']
      mayoris_z = facturma['mayoris']
      factur_z = facturma['num']
      nompag1_z = mayoris['nompag1']
      nompag2_z = mayoris['nompag2']
      dirpag1_z = mayoris['dirpag1']
      dirpag2_z = mayoris['dirpag2']
      ciupag_z  = mayoris['ciupag']
      if ciupag_z == None:
         ciupag_z = ""
      #End if
      prpagare_z = ini_z
      ulpagare_z = fin_z
      miarchivo_z = "hazfacma.tex"
      arch_z = open(miarchivo_z, "w")
      reset_imp = def_tablas.font(mydb, 1, "RESET")
      font_pica = def_tablas.font(mydb, 1, "PICA-PITCH")
      font_elite = def_tablas.font(mydb, 1, "ELITE")
      condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      emphized_on = def_tablas.font(mydb, 1, "EMPHAIZED ON")
      emphized_off = def_tablas.font(mydb, 1, "EMPHAIZED OFF")
      subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")


      sql_z = "select pagare, fecha, vence, importe from movmay2 "
      sql_z = sql_z + "where docto = " + str(factur_z) 
      sql_z = sql_z + " and pagare between " + str(prpagare_z) + " and " + str(ulpagare_z)
      sql_z = sql_z + " and cia= " + str(cia_z) 
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result_z = cursor.fetchall()
      for record in result_z:
          vence_z = record[2]
          importe_z = record[3]
          arch_z.write(reset_imp + font_pica + "".ljust(4) + "MERIDA\n\n\n\n\n")
          arch_z.write(str(fecha_z.day).rjust(2) + utils.NombreMes(fecha_z).center(12) + str(fecha_z.year).rjust(4) )
          arch_z.write( str(factur_z).rjust(6) + str(record[0]).rjust(2) + "/")
          arch_z.write( str(npagos_z).rjust(2))
          arch_z.write( "".ljust(4) + str(vence_z.day).rjust(2) + utils.NombreMes(fecha_z).center(12) + str(fecha_z.year).rjust(4) )
          arch_z.write( "$".rjust(4) + utils.currency(importe_z)+"\n\n")
          arch_z.write( emphized_on + "  " + font_elite + self.numeros_a_pesos(importe_z)+ font_pica + emphized_off +  "\n")
          arch_z.write( "4%".rjust(75) + font_elite + "\n\n\n\n")
          arch_z.write( "".ljust(15) + nompag1_z.ljust(40) + "\n")
          arch_z.write( "".ljust(15) + nompag2_z.ljust(40) + "\n")
          arch_z.write( "".ljust(15) + dirpag1_z.ljust(40) + "\n")
          arch_z.write( "".ljust(15) + dirpag2_z.ljust(40) + "\n")
          arch_z.write( "".ljust(15) + ciupag_z.ljust(40) + "\n")
          for ii_z in range(9):
              arch_z.write("\n")
          #Fin de For
      #End for
      arch_z.close()
      visor = utils.visor_editor()
      resp_z = visor.ejecuta(miarchivo_z)
  #Fin de imprime_pagares
  
  def lista_precios(self):
      factur_z = facturma['num']
      miarchivo_z = "hazfacma.tex"
      arch_z = open(miarchivo_z, "w")
      sql_z = "select a.codigo, a.descri, a.preciou * (poriva / 100 + 1), b.precio "
      sql_z = sql_z + " from renfacma a join inven b on a.codigo = b.codigo "
      sql_z = sql_z + " and a.cia = b.cia where a.factur = " + str(factur_z)
      sql_z = sql_z + " and a.cia = " + str(cia_z)
      reset_imp = def_tablas.font(mydb, 1, "RESET")
      font_pica = def_tablas.font(mydb, 1, "PICA-PITCH")
      font_elite = def_tablas.font(mydb, 1, "ELITE")
      condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      emphized_on = def_tablas.font(mydb, 1, "EMPHAIZED ON")
      emphized_off = def_tablas.font(mydb, 1, "EMPHAIZED OFF")
      subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")

      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result_z = cursor.fetchall()
      arch_z.write(cias['razon'].center(80) + "\n")
      hora_z = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
      arch_z.write(condensado_on + "hazfacma " + condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      arch_z.write(("Lista de Precios Sugeridos").center(80) + "\n")
      arch_z.write("Descripcion".ljust(30) + " " + "Facturacion".rjust(12) + " " + "Precio Sugerido" + "\n")
      for record in result_z:
          descri_z = record[1]
          costou_z = record[2]
          precio_z = record[3]
          arch_z.write(descri_z.ljust(30) + " " + utils.currency(costou_z).rjust(12) + " " \
             + utils.currency(precio_z).rjust(14) + "\n")
      #End for
      arch_z.close()
      visor = utils.visor_editor()
      resp_z = visor.ejecuta(miarchivo_z)
  #Fin de lista_precios

  def numeros_a_pesos(self, importe_z):
      totint_z = int(importe_z)
      cents_z = ( importe_z - totint_z )
      strcents_z = str( int ( round(cents_z * 100,2) ))
      enletras_z = "(Son : " + Numeral.numerals(totint_z, 0) + " Pesos " + strcents_z + "/100 M.N)"
      return (enletras_z)
  #Fin de numeros_a_pesos()  

  def mueve_entrada(self, hacia_z, alm_z=''):
      global mydb
      global cia_z
      cursor = mydb.cursor()
      #edt_almacen  = self.wTree.get_widget("edt_almacen")
      edt_numero  = self.wTree.get_widget("edt_numero")
      #if self.busca_alm(edt_almacen.get_text().upper()) <> True:
      #   utils.msgdlg("Debe seleccionar un Almacen");
      #   return (-1)
      ## -- End If
      #alm_z   = edt_almacen.get_text().upper()
      numero_z = utils.StrToInt(edt_numero.get_text())
      where_z = " from facturma where cia = " + utils.IntToStr(cia_z)
      if hacia_z == 'P':
        sql_z = "select min(num) "
        sql2_z = ""
      elif hacia_z == 'U':
        sql_z = "select max(num) "
        sql2_z = ""
      elif hacia_z == 'A':
        sql_z = "select max(num) "
        sql2_z = " and num < " + utils.IntToStr(numero_z)
      elif hacia_z == 'S':
        sql_z = "select min(num) "
        sql2_z = " and num > " + utils.IntToStr(numero_z)
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
      campos_z = [ "num", "mayoris", "refer", "nomay", "dir", "rfc", "status", \
        "fecha", "vence", "importe", "descu", "neto", "iva", "total", "cia", \
        "npagos", "plazo", "tipago", "pdsc", "mayomen" ]
      sql_z = "select "
      ii_z = 0
      for micampo_z in campos_z:
         if ii_z > 0:
            sql_z = sql_z + ", "
         #End if
         sql_z = sql_z + micampo_z 
         ii_z = ii_z + 1
      sql_z = sql_z + " from facturma where "
      sql_z = sql_z + " num = "  + utils.IntToStr(numero_z) 
      sql_z = sql_z + " and cia= " + utils.IntToStr(cia_z)
      #print sql_z
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         ii_z = 0
         for micampo_z in campos_z:
             facturma[micampo_z]    = record[ii_z]
             ii_z = ii_z + 1
         resp_z = True
      else:
         resp_z = False
      return ( resp_z)

  def despliega_datos(self):
      numero_z = facturma['num']
      alm_z = ""
      mayoris_z = facturma['mayoris']
      self.busca_codmay(mayoris_z)
      self.wTree.get_widget("edt_numero").set_text(utils.IntToStr(numero_z))
      self.wTree.get_widget("edt_pagos").set_text(utils.IntToStr(facturma['npagos']))
      self.wTree.get_widget("edt_plazo").set_text(utils.IntToStr(facturma['plazo']))
      self.wTree.get_widget("edt_pdsc").set_text(utils.currency(facturma['pdsc']))
      self.wTree.get_widget("edt_fecha").set_text(utils.DateToStr(facturma['fecha']))
      self.wTree.get_widget("edt_vence").set_text(utils.DateToStr(facturma['vence']))
      self.wTree.get_widget("edt_mayoris").set_text(mayoris_z)
      self.wTree.get_widget("edt_nommay").set_text(facturma['nomay'])
      self.wTree.get_widget("edt_dircli").set_text(facturma['dir'])
      self.wTree.get_widget("edt_rfc").set_text(facturma['rfc'])
      self.wTree.get_widget("edt_refer").set_text(facturma['refer'])
      self.wTree.get_widget("edt_maymen").set_text(facturma['mayomen'])
      self.wTree.get_widget("edt_intmer").set_text(facturma['tipago'])
      self.despliega_totales()
      self.lista_renglones(alm_z, numero_z)

  def despliega_totales(self):
      self.wTree.get_widget("edt_importe").set_text(utils.currency(facturma['importe']))
      self.wTree.get_widget("edt_descto").set_text(utils.currency(facturma['descu']))
      self.wTree.get_widget("edt_iva").set_text(utils.currency(facturma['iva']))
      self.wTree.get_widget("edt_total").set_text(utils.currency(facturma['total']))
  #Fin de despleiga_totales()

  def lista_renglones(self, alm_z='', numero_z=0):
      self.lst_renentra.clear()
      campos_z = [ "factur", "consec", "codigo", "descri", "unids", "preciou", "importe", \
         "pordsc", "descu", "poriva", "iva", "total", "costou", "cia" ]
      sql_z = "select "
      ii_z = 0
      for micampo_z in campos_z:
          if ii_z > 0:
             sql_z = sql_z + ","
          #End if
          sql_z = sql_z + micampo_z
          ii_z = ii_z + 1
      sql_z = sql_z + " from renfacma "
      sql_z = sql_z + " where factur = " + utils.IntToStr(facturma['num'])
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      sql_z = sql_z + " order by consec"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      # get and display one row at a time
      for record in result:
          ii_z = 0
          for micampo_z in campos_z:
              renfacma[micampo_z]    = record[ii_z]
              ii_z = ii_z + 1
          #End For
          preciou_z = utils.currency(renfacma['preciou'])
          importe_z = utils.currency(renfacma['importe'])
          unids_z = utils.currency(renfacma['unids'])
          self.lst_renentra.append([ renfacma['codigo'], renfacma['descri'], unids_z, preciou_z, importe_z, renfacma['consec'] ])

  def ren_seleccionado(self, alm_z='', numero_z=0, tipo_z=0):
      colconse_z = 5
      grd_renentra = self.wTree.get_widget("grd_renentra")
      selection = grd_renentra.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          conse_z = self.lst_renentra.get_value(selection_iter, colconse_z)
      self.despliega_renglon('', 0, conse_z)

  def despliega_renglon(self, alm_z='', numero_z=0, conse_z=0):
      campos_z = [ "factur", "consec", "codigo", "descri", "unids", "preciou", "importe", \
         "pordsc", "descu", "poriva", "iva", "total", "costou", "cia" ]
      sql_z = "select "
      ii_z = 0
      for micampo_z in campos_z:
          if ii_z > 0:
             sql_z = sql_z + ","
          #End if
          sql_z = sql_z + micampo_z
          ii_z = ii_z + 1
      sql_z = sql_z + " from renfacma "
      sql_z = sql_z + " where factur = " + utils.IntToStr(facturma['num'])
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      sql_z = sql_z + " and consec = " + utils.IntToStr(conse_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      # get and display one row at a time
      for record in result:
          ii_z = 0
          for micampo_z in campos_z:
              renfacma[micampo_z]    = record[ii_z]
              ii_z = ii_z + 1
          #End For
          preciou_z = utils.currency(renfacma['preciou'])
          unids_z = str(int((renfacma['unids'])))

      self.wTree.get_widget("edt_codigo").set_text(renfacma['codigo'])
      self.wTree.get_widget("edt_descri").set_text(renfacma['descri'])
      self.wTree.get_widget("edt_preciovta").set_text(preciou_z)
      self.wTree.get_widget("edt_canti").set_text(unids_z)
  #Fin de Despliega Renglon

  def limpia_campos(self):
      campos_z = [ "edt_numero", "edt_fecha", "edt_pagos", "edt_plazo", "edt_pdsc", \
      "edt_mayoris", "edt_nommay", "edt_dircli", "edt_rfc", "edt_refer", "edt_maymen", \
      "edt_intmer", "edt_importe", "edt_descto", "edt_iva", "edt_total", \
            "edt_codigo", "edt_descri", "edt_preciovta", "edt_canti" ]
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
      self.wTree.get_widget("edt_preciovta").set_editable(modo)
      self.wTree.get_widget("btn_nuevoren").set_child_visible(not(modo))
      self.wTree.get_widget("btn_borraren").set_child_visible(not(modo))
      self.wTree.get_widget("btn_seriesren").set_child_visible(not(modo))
      #btn_cierra.set_child_visible(not(modo))

  def activa_aceptar_cancelar(self, modo):
     self.wTree.get_widget("btn_aceptar").set_child_visible(modo)
     self.wTree.get_widget("btn_cancelar").set_child_visible(modo)
     self.wTree.get_widget("btn_entradas").set_child_visible(not(modo))

  def activa_renglones(self, modo):
      self.wTree.get_widget("btn_nuevoren").set_child_visible(modo)
      self.wTree.get_widget("btn_borraren").set_child_visible(modo)
      self.wTree.get_widget("btn_seriesren").set_child_visible(modo)
      self.wTree.get_widget("btn_entradas").set_child_visible(modo)
      #self.wTree.get_widget("edt_almacen").set_editable(not(modo))
      self.wTree.get_widget("edt_numero").set_editable(not(modo))
      self.wTree.get_widget("edt_fecha").set_editable(not(modo))

if __name__ == "__main__":
   hwg = Hazfacma()
   gtk.main()

def main():
    global mydb
    mibd = utils.lee_basedato_ini()
    mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])

    gtk.main()
    return 0
