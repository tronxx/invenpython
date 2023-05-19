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
global ptovta
global businven_z
global prove

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
prove        = def_tablas.define_prove()
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

class Capentpro:
  """Esta es una aplicación Captura de Entradas Especiales"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.tipent_z="E"
    self.gladefile = dirprogs_z + "capentpro.glade"
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
            "on_btn_observs_clicked": self.on_btn_observs_clicked, \
            "on_btn_imprime_clicked": self.on_btn_imprime_clicked, \
            "on_edt_almacen_focus_out_event": self.on_edt_almacen_focus_out_event,\
            "on_edt_vend_focus_out_event": self.on_edt_vend_focus_out_event,\
            "on_edt_prove_focus_out_event": self.on_edt_prove_focus_out_event,\
            "on_edt_codigo_focus_out_event": self.on_edt_codigo_focus_out_event, \
            }
    self.wTree.get_widget("edt_almacen").connect("activate", self.on_edt_almacen_focus_out_event)
    self.wTree.get_widget("edt_codigo").connect("activate", self.on_edt_codigo_focus_out_event)
    self.wTree.get_widget("edt_numero").connect("activate", self.on_edt_numero_activate)

    campos_z = [ "edt_canti", "edt_importe", "edt_iva", "edt_total", \
      "edt_flete", "edt_ctofincom", "edt_ctofinpro", "edt_desxap", "edt_tasacfc", \
      "edt_tasacfp", "edt_grantot", "edt_numero" ]
    for micampo_z in campos_z:
        self.wTree.get_widget(micampo_z).set_property('xalign', 1)

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

    cias = def_tablas.busca_cia(mydb, cia_z)
    self.asigna_tipent("E")

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
    if self.tipent_z == "P":
       visibles_z = False
    elif self.tipent_z == "C": 
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

  def on_btn_observs_clicked(self, widget):
      alm_z    = self.wTree.get_widget("edt_almacen").get_text().upper()
      nomalm_z = self.wTree.get_widget("edt_nomalm").get_text().upper()
      numero_z = utils.StrToInt(self.wTree.get_widget("edt_numero").get_text())
      obsent_z = cap_obsent.Capobsent(alm_z, numero_z, self.tipent_z)
      resp_z = obsent_z.ejecuta()

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
      if entradas['status']=="C":
         utils.msgdlg("Entrada Cerrada")
         return -1
      resp_z = utils.yesnodlg("Seguro de Cerrar esta Entrada ?")
      if resp_z <> gtk.RESPONSE_OK:
         return -1
         
      alm_z = entradas['alm']
      numero_z = entradas['numero']      
      
      sql_z = "select conse from renentra where tipo = '" + self.tipent_z + "' "
      sql_z = sql_z + " and alm = '" + alm_z + "' and numero = " + utils.IntToStr(numero_z)
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      sql_z = sql_z + " and status = 'A'"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result_z = cursor.fetchall()
      for record in result_z:
          conse_z = record[0]
          self.despliega_renglon(alm_z, numero_z, conse_z)
          def_tablas.afecta_renentra(mydb, renentra, entradas)
      self.afecta_pagare(alm_z, numero_z)
      self.busca_entrada(alm_z, numero_z)
      self.despliega_datos()
         

  def afecta_pagare(self, alm_z, numero_z):
      prove_z = entradas['prove']
      #Primero borro las entradas de pagare que ya existan
      sql_z = "delete from entpag where prove = '" + entradas['prove'] + "' "
      sql_z = sql_z + " and numero = " + utils.IntToStr(entradas['numero'])
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      sql2_z = "delete from mventpag where prove = '" + entradas['prove'] + "' "
      sql2_z = sql2_z + " and entrada = " + utils.IntToStr(entradas['numero'])
      sql2_z = sql2_z + " and cia = " + utils.IntToStr(cia_z)
      sql2_z = sql2_z + " and tpmov = 'A'"
      planp_z = entradas['planp']
      planesp = def_tablas.busca_planp(mydb, planp_z, cia_z)
      letras_z = planesp['numlet']
      plazo_z = planesp['plazo']
      fletes_z = entradas['fletes']
      fecha_z = entradas['fecha']
      piva_z = 0.0
      if entradas['coniva'] == "S":
         piva_z = 15.0
      #Fin de If
      imppag_z = round(entradas['importe'] - ( entradas['fletes'] / ( piva_z / 100 + 1) ), 2)
      descxapag_z = round(entradas['desxap']  / ( piva_z / 100 + 1),2)
      ctofinent_z = round( ( entradas['ctofin'] + entradas['ctofincomp'] ) / ( piva_z / 100 + 1), 2)
      capital_z = imppag_z + ctofinent_z + descxapag_z
      ivapag_z = round(capital_z * ( piva_z / 100 ), 2)
      print "Entradas Coniva:", entradas['coniva'], ": Piva:", piva_z, " ivapag:", ivapag_z, " Capital:", capital_z
      ivacfcent_z = round ( ctofinent_z * ( piva_z / 100), 2)
      ivaint_z = 0.0
      totalint_z = 0.0
      
      def_tablas.start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      cursor2 = mydb.cursor()
      cursor2.execute(sql2_z)
      #Ahora voy a insertar los datos de los renglones de pagares
      numlet_z = planesp['numlet']
      fecprp_z = entradas['fechaprp']
      feculp_z = entradas['vence']
      nprpag_z = 1
      if planesp['ivadis'] <> "S" and planesp['letivasol'] == "S":
         numlet_z = numlet_z - 1
         if planesp['nletiva'] == 1 and planesp['letivaemp'] == "S":
            nprpag_z = 2
         #Fin de If
      #Fin de If
      if numlet_z <> 0:
         amort_z = capital_z / numlet_z
         cfc_z = ctofinent_z / numlet_z
         descxlet_z = entradas['desxap'] / numlet_z
         if planesp['fletedis'] == "S":
            fletexlet_z = fletes_z / numlet_z
         #Fin de if
      #Fin de if
      sdocap_z = capital_z
      totint_z = 0.0
      entpag = def_tablas.define_entpag()
      conse_z = def_tablas.busca_sigte(mydb, '', prove_z, numero_z, cia_z, def_tablas.MVENTPAG)
      for ii_z in range (1, numlet_z + 1):
          mventpag = def_tablas.define_mventpag()
          mventpag['prove'] = prove_z
          mventpag['entrada'] = numero_z
          mventpag['fecha'] = fecha_z
          mventpag['pagare'] = ii_z
          mventpag['conse'] = conse_z
          mventpag['tpmov'] = "A"
          mventpag['tipo2'] = "O"
          mventpag['concep'] = 0
          if planesp['dscxapdis'] == "S":
             mventpag['desxap'] = descxlet_z
          else:
             mventpag['desxap'] = 0.0
          if ii_z <= nprpag_z:
             mventpag['vence'] = fecprp_z
             if ii_z == 1 and planesp['dscxapdis'] <> "S":
                mventpag['desxap'] = entradas['desxap']
             #End if
          else:
             if ii_z == planesp['numlet']:
                mventpag['vence'] = feculp_z
             else:
               if planesp['letivaemp'] == "N" and ii_z > planesp['nletiva'] and planesp['letivasol'] == "S":
                  dias_z =  planesp['plazo'] * ( ii_z - 2 )
                  vence_z = fecprp_z + datetime.timedelta( dias_z )
                  mventpag['vence'] = vence_z
               else:
                  dias_z =  planesp['plazo'] * ( ii_z - 1 )
                  vence_z = fecprp_z + datetime.timedelta( dias_z )
                  mventpag['vence'] = vence_z
               #End if
             #End if
          #End if
          if planesp['ivadis'] == "S":
             mventpag['capital'] = amort_z
             mventpag['interes'] = round ( sdocap_z * entradas['taspro'] / 100, 4)
             totint_z = totint_z + mventpag['interes']
             sdocap_z = sdocap_z - amort_z
             mventpag['cfc'] = cfc_z
             mventpag['iva'] = round( mventpag['interes'] * entpag['poriva'] / 100 + (ivapag_z / numlet_z), 4)
             ivaint_z = round( ivaint_z + ( mventpag['interes'] * entpag['poriva'] / 100 ), 4)
             mventpag['saldo'] = mventpag['capital'] + mventpag['interes'] + mventpag['iva']
             if planesp['fletedis'] == "S":
                mventpag['capital'] = mventpag['capital'] + fletexlet_z
             #End if
          else:
             if planesp['letivasol'] == "S" and ii_z == planesp['nletiva']:
                mventpag['iva'] = ivapag_z
             else:
                mventpag['capital'] = amort_z
                mventpag['interes'] = round( sdocap_z * entradas['taspro'] / 100, 4)
                sdocap_z = sdocap_z - amort_z
                mventpag['cfc'] = cfc_z
                cosfc_z = cosfc_z - cfc_z
                ivaint_z = ivaint_z + round ( mventpag['interes'] * (planesp['pporiva'] / 100), 4 )
             #End if
             mventpag['saldo'] = mventpag['capital'] + mventpag['interes'] + mventpag['iva']
          #End if
          mventpag['cia'] = cia_z
          sql_z = def_tablas.insert_into_mventpag(mventpag)
          cursor = mydb.cursor()
          cursor.execute(sql_z)
          conse_z = conse_z + 1
      #Fin de Range
      entpag['prove'] = prove_z
      entpag['numero'] = numero_z
      entpag['fecha'] = fecha_z
      entpag['facpro'] = entradas['facpro']
      entpag['fecentra'] = entradas['fecha']
      entpag['tasacfc'] = entradas['tascomp']
      entpag['tasapro'] = entradas['taspro']
      entpag['poriva'] = piva_z
      entpag['importe'] = entradas['importe']
      entpag['descxap'] = descxapag_z
      entpag['ctofinent'] = ctofinent_z
      entpag['capital'] = capital_z
      entpag['letras'] = letras_z
      entpag['iva'] = ivapag_z
      entpag['ivacfcent'] = ivacfcent_z
      entpag['plazo'] = plazo_z
      entpag['planp'] = planp_z
      entpag['fletes_z'] = capital_z
      entpag['fecprp_z'] = entradas['fechaprp']
      entpag['feculp_z'] = entradas['vence']
      entpag['sdocap'] = capital_z
      entpag['cia'] = cia_z
      entpag['totalinter'] = totint_z
      entpag['ivaint'] = ivaint_z
      entpag['total'] = capital_z + entpag['iva'] + ivaint_z + totint_z + entpag['fletes']
      sql_z = def_tablas.insert_into_entpag(entpag)
      print "Insert into Entpag:\n", sql_z
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      cfpro_z = totint_z + ivaint_z
      sql_z = "update entradas set ctofin = " + repr(cfpro_z) + ","
      sql_z = sql_z + " status = 'C' "
      sql_z = sql_z + " where tipo = '" + self.tipent_z + "' "
      sql_z = sql_z + " and alm = '" + alm_z + "' "
      sql_z = sql_z + " and numero = " + utils.IntToStr(numero_z)
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      if planesp['fletedis'] == "N" and entpag['fletes'] <> 0:
         idconcep_z = def_tablas.busca_iddato(mydb, "FLETE", def_tablas.CONCEPTOS)
         mventpag = def_tablas.define_mventpag()
         mventpag['prove'] = prove_z
         mventpag['entrada'] = numero_z
         mventpag['fecha'] = fecha_z
         mventpag['pagare'] = ii_z
         mventpag['conse'] = conse_z
         mventpag['tpmov'] = "A"
         mventpag['tipo2'] = "O"
         mventpag['concep'] = idconcep_z
         mventpag['capital'] = entpag['fletes']
         mventpag['vence'] = entpag['fecha']
         mventpag['saldo'] = entpag['capital']
         mventpag['cia'] = cia_z
         sql_z = def_tablas.insert_into_mvenpag()
         cursor = mydb.cursor()
         cursor.execute(sql_z)
      #End if
      if planesp['ivadis'] <> "S":
         sql_z = "update mventpag set iva = " + repr(entpag['iva'] + entpag['ivaint'])
         sql_z = sql_z + ", saldo = saldo + " + repr(entpag['iva'] + entpag['ivaint'])
         sql_z = sql_z + " where prove = '" + prove_z + "' "
         sql_z = sql_z + " and entrada = " + utils.IntToStr(numero_z)
         sql_z = sql_z + " and pagare = " + utils.IntToStr(planesp['nletiva'])
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
         print "update mventpag:", sql_z
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         
      #End if
      def_tablas.commit_trans(mydb)

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
         costou_z = renentra['costou']
         piva_z  = renentra['piva']
         alm_z = entradas['alm']
         numero_z = entradas['numero']
         sql_z = "delete from renentra "
         sql_z = sql_z + " where tipo = '" + self.tipent_z + "' and alm = '"
         sql_z = sql_z + entradas['alm'] + "' and numero = "
         sql_z = sql_z + repr(entradas['numero']) + " and conse=" + repr(renentra['conse']) 
         sql_z = sql_z + " and cia = " + repr(cia_z) + " order by conse"
         
         def_tablas.start_trans(mydb)
         cursor = mydb.cursor()
         cursor.execute(sql_z)

         sql_z = "update entradas set importe = importe - " + repr(costou_z) + ","
         sql_z = sql_z + " iva = iva - " + repr(costou_z * piva_z / 100 ) + ","
         sql_z = sql_z + " total = total - " + repr(costou_z * (piva_z / 100 + 1) )
         sql_z = sql_z + " where tipo = '" + self.tipent_z + "' and alm = '" + alm_z + "' "
         sql_z = sql_z + " and numero = " + utils.IntToStr(numero_z) 
         sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
         
         cursor = mydb.cursor()
         cursor.execute(sql_z)

         def_tablas.commit_trans(mydb)
         self.busca_entrada(alm_z, numero_z)
         self.despliega_datos()

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

  def on_edt_prove_focus_out_event(self, widget, tipo=None):
      if estoyen_z <> def_tablas.ENTRADAS and modo_z <> NUEVO:
         return (-1)
      prove_z = widget.get_text().upper()
      if ( self.busca_prove(prove_z) == True):
         widget.set_text(prove['codigo'])

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

  def busca_prove(self, prove_z = ''):
      edt_prove  = self.wTree.get_widget("edt_prove")
      edt_nombre   = self.wTree.get_widget("edt_nompro")
      if prove_z == '':
         prove_z = edt_prove.get_text().upper()
         
      sql_z = "select codigo, nombre from proveedor where codigo = '" + prove_z + "' and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        prove['codigo']    = record[0]
        prove['nombre']  = record[1]
        edt_prove.set_text(prove['codigo'])
        edt_nombre.set_text(prove['nombre'])
        resp_z = True
      else:
        sql_z = "select codigo, nombre from proveedor where cia = " + repr(cia_z) + " order by codigo"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El Proveedor")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           prove['codigo']   = miresp_z[0]
           prove['nombre']  = miresp_z[1]
           edt_prove.set_text(prove['codigo'])
           edt_nombre.set_text(prove['nombre'])
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
      self.editable_onoff(True)
      self.wTree.get_widget("edt_prove").grab_focus()

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

      nomcli_z = ""
      vend_z = ""
      poblac_z = ""
      ptovta_z = ""
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
      if self.wTree.get_widget("chk_status").get_active() == True:
         siono_z = 'S'
         piva_z = inven['piva']
      else:
         siono_z = 'N'
         piva_z = 0
      entcan_z = 'N'
      folent_z = 0
      preciovta_z = 0
      npob_z   = 0
      ncli_z   = 0
      conse_z = def_tablas.busca_sigte(mydb, self.tipent_z, alm_z, numero_z, cia_z, def_tablas.RENENTRA)
      def_tablas.start_trans(mydb)
      for misfolios_z in folios_z:
        renentra['tipo'] = self.tipent_z
        renentra['alm'] = alm_z
        renentra['recemi'] = ptovta_z
        renentra['numero'] = numero_z
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
      iva_z = round(costou_z * canti_z * piva_z / 100, 4)
      sql_z = "update entradas set importe = importe + " + repr(costou_z * canti_z) + ","
      sql_z = sql_z + " iva = iva + " + repr(iva_z) + ","
      sql_z = sql_z + " total = total + " + repr(iva_z )
      sql_z = sql_z + " where tipo = '" + self.tipent_z + "' and alm = '" + alm_z + "' "
      sql_z = sql_z + " and numero = " + utils.IntToStr(numero_z) 
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
      
      cursor = mydb.cursor()
      cursor.execute(sql_z)

      def_tablas.commit_trans(mydb)
      self.busca_entrada(alm_z, numero_z)
      self.despliega_datos()
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
         utils.msgdlg("Fecha de Entrada Invalida:" + edt_fecha.get_text());
         edt_fecha.grab_focus()
         return (-1)
      ## -- End If
      fecprp_z = utils.StrToDate(self.wTree.get_widget("edt_fecprp").get_text())
      if ( fecprp_z == -1):
         utils.msgdlg("Fecha Invalida de Primer Pago:");
         self.wTree.get_widget("edt_fecprp").grab_focus()
         return (-1)
      ## -- End If
      feculp_z = utils.StrToDate(self.wTree.get_widget("edt_feculp").get_text())
      if ( feculp_z == -1):
         utils.msgdlg("Fecha Invalida de Ultimo Pago:");
         self.wTree.get_widget("edt_feculp").grab_focus()
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
      facpro_z = self.wTree.get_widget("edt_factura").get_text().upper()
      prove_z = self.wTree.get_widget("edt_prove").get_text().upper()
      if self.wTree.get_widget("chk_status").get_active() == True:
         siono_z = 'S'
      else:
         siono_z = 'N'
      planp_z = utils.StrToInt(self.wTree.get_widget("edt_planp").get_text())
      letras_z = utils.StrToInt(self.wTree.get_widget("edt_letras").get_text())
      ctofincom_z = utils.StrToFloat(self.wTree.get_widget("edt_ctofincom").get_text())
      ctofinpro_z = utils.StrToFloat(self.wTree.get_widget("edt_ctofinpro").get_text())
      fletes_z = utils.StrToFloat(self.wTree.get_widget("edt_flete").get_text())
      tascfc_z = utils.StrToFloat(self.wTree.get_widget("edt_tasacfc").get_text())
      tascfp_z = utils.StrToFloat(self.wTree.get_widget("edt_tasacfp").get_text())
      desxap_z = utils.StrToFloat(self.wTree.get_widget("edt_desxap").get_text())

      entradas['tipo']   = self.tipent_z
      entradas['alm']  = alm_z
      entradas['recemi']  = ''
      entradas['numero']  = numero_z
      entradas['facpro']  = facpro_z
      entradas['prove']  = prove_z
      entradas['perenvrec']  = 0
      entradas['status']  = 'A'
      entradas['coniva']  = siono_z
      entradas['fecha']  = fecha_z
      entradas['importe']  = 0
      entradas['iva']  = 0
      entradas['total']  = 0
      entradas['vence']  = feculp_z
      entradas['ctofin']  = ctofinpro_z
      entradas['tascomp']  = tascfc_z
      entradas['taspro']  = tascfp_z
      entradas['fechafac']  = fecha_z
      entradas['letras']  = letras_z
      entradas['plazocfp']  = 0
      entradas['fletes']  = fletes_z
      entradas['desxap']  = desxap_z
      entradas['fechaprp']  = fecprp_z
      entradas['ctofincomp']  = ctofincom_z
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
      antcod_z = ""
      self.despliega_datos()
      self.pag_z = 1
      self.nlineas_z = 0
      miarchivo_z = "capentpro.tex"
      self.arch_z = open(miarchivo_z, "w")
      self.arch_z.write(cias['razon'].center(80) + "\n")
      self.condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      self.elite = def_tablas.font(mydb, 1, "ELITE")
      self.condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      self.subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      self.subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")
      prove_z      = entradas['prove']
      impfletes_z  = entradas['fletes']
      desxap_z     = entradas['desxap']
      ctofincomp_z = entradas['ctofincomp']
      ctofinprov_z = entradas['ctofin']
      self.encab()
      sql_z = "select a.tipo,a.alm,a.recemi,a.numero,a.conse,a.codinv,a.serie,"
      sql_z = sql_z + "a.siono,a.folsal,a.folent,a.unids,a.costou,a.piva,a.importe,a.cantmueve,"
      sql_z = sql_z + "a.status,a.persenvrec,a.cia,a.vend,a.poblac,a.tipago,b.precio,a.entosal,a.entcan,"
      sql_z = sql_z + "b.descri, b.piva"
      sql_z = sql_z + " from renentra a"
      sql_z = sql_z + " join inven b on a.codinv = b.codigo and a.cia = b.cia"
      sql_z = sql_z + " where a.tipo = '" + self.tipent_z + "' and alm = '"
      sql_z = sql_z + entradas['alm'] + "' and a.numero = " + repr(entradas['numero']) 
      sql_z = sql_z + " and a.cia = " + repr(cia_z) + " order by conse"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      ren_z = 0
      impcosto_z = 0
      iva_z = 0
      artcod_z = 0
      costocod_z = 0
      primero_z = "S"
      for record in result:
          ren_z = ren_z + 1
          ptovta_z = record[2]
          codigo_z = record[5]
          vend_z   = record[18]
          prvta_z  = record[21]
          descri_z = record[24]
          piva_z   = record[25]
          folent_z = '%5d' % record[9]
          if antcod_z <> codigo_z and primero_z <> "S":
             self.arch_z.write(self.subrayado_on)
             self.arch_z.write("Total de Este Articulo:".ljust(31)+codigo_z.ljust(13)+":")
             self.arch_z.write(utils.IntToStr(artcod_z).rjust(5) + " ")
             self.arch_z.write(utils.currency(costocod_z).rjust(12))
             self.arch_z.write("".ljust(32))
             self.arch_z.write(self.subrayado_off + "\n")
             costocod_z = 0
             artcod_z = 0
             antcod_z = codigo_z
          #End if
          primero_z = "N"
          if artcod_z == 0:
             antcod_z = codigo_z
             gpodiary_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_GPODIARY)
             gpoartdesp_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_ARTDESP)
             descrilar_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_DESCRILAR)
          #End if
          entcan_z = record[23]
          siono_z  = record[7]
          serie_z  = record[6]
          costou_z = record[11]
          costocod_z = costocod_z + costou_z
          costoneto_z = costou_z * ( piva_z / 100 + 1)
          impcosto_z = impcosto_z + costou_z
          iva_z = iva_z + costou_z * record[12] / 100
          if prvta_z <> 0:
            mub_z = 100 * (1 -(costoneto_z / prvta_z ) )
          else:
            mub_z = -100
          #End If
          if self.nlineas_z > utils.LINEAS_X_PAG:
             self.salto_pag()
          #End if
          self.arch_z.write(codigo_z.ljust(13)+"|")
          self.arch_z.write(descri_z.ljust(30)+"|")
          self.arch_z.write(folent_z.rjust(5)+"|")
          self.arch_z.write(utils.currency(costou_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(costoneto_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(prvta_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(mub_z).rjust(5)+"|")
          if artcod_z == 0:
             self.arch_z.write(gpodiary_z.ljust(10)+"|")
             self.arch_z.write(gpoartdesp_z.ljust(10)+"|")
          #End if
          self.arch_z.write("\n")
          self.nlineas_z = self.nlineas_z + 1
          if artcod_z == 0:
             self.arch_z.write("".ljust(13)+"|" + descrilar_z + "\n")
             antcod_z = codigo_z
             self.nlineas_z = self.nlineas_z + 1
          #End if
          artcod_z = artcod_z + 1
      #End For
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("Total de Este Articulo:".ljust(31)+codigo_z.ljust(13)+":")
      self.arch_z.write(utils.IntToStr(artcod_z).rjust(5) + " ")
      self.arch_z.write(utils.currency(costocod_z).rjust(12))
      self.arch_z.write("".ljust(32))
      self.arch_z.write(self.subrayado_off + "\n")
      self.nlineas_z = self.nlineas_z + 1
      
      total_z = impcosto_z + iva_z
      grantot_z = total_z - impfletes_z + ctofincomp_z + ctofinprov_z + desxap_z
      self.nlineas_z = self.nlineas_z + 1
      if self.nlineas_z > utils.LINEAS_X_PAG - 4:
         self.salto_pag()
      #End if
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("Importe:" + utils.currency(impcosto_z).ljust(12) + "|")
      self.arch_z.write("Iva    :" + utils.currency(iva_z).ljust(12) + "|")
      self.arch_z.write("Total  :" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.arch_z.write("Fletes          :" + utils.currency(impfletes_z).rjust(12) + " ")
      self.arch_z.write("Descto x Aplicar:" + utils.currency(desxap_z).rjust(12) + " ")
      self.arch_z.write("\n")
      self.arch_z.write("Cto.Fin.Compra  :" + utils.currency(ctofincomp_z).rjust(12) + " ")
      self.arch_z.write("Cto.Fin.Prove   :" + utils.currency(ctofinprov_z).rjust(12) + " ")
      self.arch_z.write("\n")
      self.arch_z.write("Gran Total      :" + utils.currency(grantot_z).rjust(12))
      self.arch_z.write("\n")
      self.arch_z.write(self.condensado_off + self.elite)
      sql_z = "select fecha, pagare, vence, cfc, capital, interes, iva, desxap, saldo "
      sql_z = sql_z + " from mventpag where prove = '" + prove_z + "' "
      sql_z = sql_z + " and entrada = " + utils.IntToStr(numero_z) + "  "
      sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z) + "  order by pagare"
      self.arch_z.write(self.subrayado_on+"Lta|")
      self.arch_z.write("Vence".center(10)+"|")
      self.arch_z.write("Costo F.Comp".rjust(12)+"|")
      self.arch_z.write("Capital".rjust(12)+"|")
      self.arch_z.write("Interes".rjust(12)+"|")
      self.arch_z.write("I.V.A.".rjust(12)+"|")
      self.arch_z.write("DescxAplicar".rjust(12)+"|")
      self.arch_z.write("Saldo".rjust(12)+self.subrayado_off+"\n")
      self.nlineas_z = self.nlineas_z + 1
      total_z = 0
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result_z = cursor.fetchall()
      for record in result_z:
          ii_z = 0
          fecha_z  = record[ii_z]
          ii_z = ii_z + 1
          pagare_z = record[ii_z]
          ii_z = ii_z + 1
          vence_z = record[ii_z]
          ii_z = ii_z + 1
          cfc_z  = record[ii_z]
          ii_z = ii_z + 1
          capital_z = record[ii_z]
          ii_z = ii_z + 1
          interes_z = record[ii_z]
          ii_z = ii_z + 1
          iva_z = record[ii_z]
          ii_z = ii_z + 1
          desxap_z = record[ii_z]
          ii_z = ii_z + 1
          self.nlineas_z = self.nlineas_z + 1
          if self.nlineas_z > utils.LINEAS_X_PAG:
             self.salto_pag()
          #End if
          saldo_z = record[ii_z]
          self.arch_z.write(utils.IntToStr(pagare_z).rjust(3)+"|")
          self.arch_z.write(vence_z.strftime('%d/%m/%Y')+"|")
          self.arch_z.write(utils.currency(cfc_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(capital_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(interes_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(iva_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(desxap_z).rjust(12)+"|")
          self.arch_z.write(utils.currency(saldo_z).rjust(12)+"|\n")
          self.nlineas_z = self.nlineas_z + 1
          total_z = total_z + saldo_z
      #End For
      self.arch_z.write(self.subrayado_on+"".ljust(74)+"Total:"+utils.currency(total_z).rjust(12)+self.subrayado_off+"\n")
      self.arch_z.write("Vencimiento:\n" + entradas['vence'].strftime('%d/%m/%Y') + "\n")
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
          self.arch_z.write(record[1]+"\n")
      #Fin de For
      self.arch_z.close()
      visor = utils.visor_editor()
      resp_z = visor.ejecuta(miarchivo_z)

  def salto_pag(self):
      self.arch_z.write(def_tablas.font(mydb, 1, "FORM-FEED FF"))
      self.pag_z = self.pag_z + 1
      self.encab()

  def encab(self):
      nompro_z = def_tablas.busca_nombre(mydb, entradas['prove'], cia_z, def_tablas.PROVEEDOR)
      nomplan_z = def_tablas.busca_nombre(mydb, entradas['planp'], cia_z, def_tablas.PLANESP)
      hora_z = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
      self.arch_z.write(self.condensado_on + "capentes " + self.condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      self.arch_z.write(("Impresion de " + def_tablas.tipoentra(self.tipent_z)[2] + " Pag:" + '%d' % self.pag_z).center(80) + "\n")
      self.arch_z.write("Numero:" + self.tipent_z + "%6d" % entradas['numero'])
      self.arch_z.write(" Almacen: " + entradas['alm'] + " " + almacen['nombre'])
      self.arch_z.write(" Fecha: " + entradas['fecha'].strftime('%d/%m/%Y') + "\n")
      self.arch_z.write("Proveedor:" + entradas['prove'] + " " + nompro_z + "\n")
      self.arch_z.write("Plan de Pago:" + utils.IntToStr(entradas['planp']) + " " + nomplan_z)
      self.arch_z.write(" Letras:" + utils.IntToStr(entradas['letras']))
      self.arch_z.write(" Factura:" + entradas['facpro'] + "\n")
      self.arch_z.write("% Costo Fin. Compra:" + utils.currency(entradas['tascomp']))
      self.arch_z.write(" % Costo Fin. Proveedor:" + utils.currency(entradas['taspro']) + "\n")
      
      self.arch_z.write(self.condensado_on)
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("Codigo".ljust(13)+"|")
      self.arch_z.write("Descripcion".ljust(30)+"|")
      self.arch_z.write("Folio".rjust(5)+"|")
      self.arch_z.write("Costo Unit".rjust(12)+"|")
      self.arch_z.write("Costo Neto".rjust(12)+"|")
      self.arch_z.write("Precio Lista".rjust(12)+"|")
      self.arch_z.write("%Marg".rjust(5)+"|")
      self.arch_z.write("Gpo.Diary".ljust(10)+"|")
      self.arch_z.write("Gpo.Art.Despl".ljust(10)+"|")
      self.arch_z.write(self.subrayado_off)
      self.arch_z.write("\n")
      self.nlineas_z = 7
  

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
      sql_z = "select tipo, alm, numero, fecha, prove, planp, letras, importe, iva, total, "
      sql_z = sql_z + " fletes, ctofincomp, ctofin, fechaprp, vence, facpro, "
      sql_z = sql_z + " desxap, coniva, status, tascomp, taspro "
      sql_z = sql_z + " from entradas where "
      sql_z = sql_z + " tipo = '" + self.tipent_z + "' and alm = '" + alm_z + "' and numero = "  + repr(numero_z) + " and cia= " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         entradas['tipo']   = self.tipent_z
         entradas['alm']  = alm_z
         entradas['numero']  = numero_z
         ii_z = 3
         entradas['fecha']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['prove']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['planp']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['letras']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['importe']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['iva']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['total']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['fletes']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['ctofincomp']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['ctofin']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['fechaprp']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['vence']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['facpro']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['desxap']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['coniva']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['status']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['tascomp']  = record[ii_z]
         ii_z = ii_z + 1
         entradas['taspro']  = record[ii_z]
         ii_z = ii_z + 1
         resp_z = True
      else:
         resp_z = False
      return ( resp_z)

  def despliega_datos(self):
      alm_z = entradas['alm'];
      numero_z = entradas['numero']
      entradas['total']  = entradas['importe'] + entradas['iva'] 
      self.busca_alm(alm_z)
      nompro_z = def_tablas.busca_nombre(mydb, entradas['prove'], cia_z, def_tablas.PROVEEDOR)
      nomplan_z = def_tablas.busca_nombre(mydb, entradas['planp'], cia_z, def_tablas.PLANESP)
      self.wTree.get_widget("edt_numero").set_text(utils.IntToStr(numero_z))
      self.wTree.get_widget("edt_fecha").set_text(entradas['fecha'].strftime('%d/%m/%Y'))
      self.wTree.get_widget("edt_prove").set_text(entradas['prove'])
      self.wTree.get_widget("edt_nompro").set_text(nompro_z)
      self.wTree.get_widget("edt_planp").set_text(utils.IntToStr(entradas['planp']))
      self.wTree.get_widget("edt_descriplan").set_text(nomplan_z)
      self.wTree.get_widget("edt_letras").set_text(utils.IntToStr(entradas['letras']))
      self.wTree.get_widget("edt_importe").set_text(utils.currency(entradas['importe']))
      self.wTree.get_widget("edt_iva").set_text(utils.currency(entradas['iva']))
      self.wTree.get_widget("edt_total").set_text(utils.currency(entradas['total']))
      self.wTree.get_widget("edt_flete").set_text(utils.currency(entradas['fletes']))
      self.wTree.get_widget("edt_ctofincom").set_text(utils.currency(entradas['ctofincomp']))
      self.wTree.get_widget("edt_ctofinpro").set_text(utils.currency(entradas['ctofin']))
      self.wTree.get_widget("edt_desxap").set_text(utils.currency(entradas['desxap']))
      self.wTree.get_widget("edt_fecprp").set_text(entradas['fechaprp'].strftime('%d/%m/%Y'))
      self.wTree.get_widget("edt_feculp").set_text(entradas['vence'].strftime('%d/%m/%Y'))
      self.wTree.get_widget("edt_factura").set_text(entradas['facpro'])
      self.wTree.get_widget("edt_tasacfc").set_text(utils.currency(entradas['tascomp']))
      self.wTree.get_widget("edt_tasacfp").set_text(utils.currency(entradas['taspro']))
      self.wTree.get_widget("chk_status").set_active(entradas['coniva'] == 'S')
      gtotent_z=entradas['total']+entradas['ctofin']+entradas['ctofincomp']-entradas['fletes']+entradas['desxap']
      self.wTree.get_widget("edt_grantot").set_text(utils.currency(gtotent_z))
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
      result = cursor.fetchall()
      numrows = len(result)
      # get and display one row at a time
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
          #nomcli_z               = def_tablas.busca_dato(mydb, renentra['persenvrec'], CONCEPTOS)
          costou_z               = utils.currency(renentra['costou'])
          #if self.tipent_z in "C":
          #   poblac_z               = def_tablas.busca_dato(mydb, renentra['poblac'], POBLACIONES)
          #   nomvnd_z               = def_tablas.busca_nombre(mydb, renentra['vend'], cia_z, VENDEDOR)
          #   nomptovt_z             = def_tablas.busca_nombre(mydb, renentra['recemi'], cia_z, PTOVTA)
      
      self.wTree.get_widget("edt_codigo").set_text(renentra['codinv'])
      self.wTree.get_widget("edt_descri").set_text(descri_z)
      #self.wTree.get_widget("edt_nomcli").set_text(nomcli_z)
      #self.wTree.get_widget("edt_preciovta").set_text(costou_z)
      #self.wTree.get_widget("chk_sino").set_active(renentra['siono'] == 'S')
      #self.wTree.get_widget("chk_cancel").set_active(renentra['entcan'] == 'S')
      #if self.tipent_z in "C":
      #   self.wTree.get_widget("edt_vend").set_text(renentra['vend'])
      #   self.wTree.get_widget("edt_nomvnd").set_text(nomvnd_z)
      #   self.wTree.get_widget("edt_poblac").set_text(poblac_z)
      #   self.wTree.get_widget("edt_ptovta").set_text(renentra['recemi'])
      #   self.wTree.get_widget("edt_nomptovt").set_text(nomptovt_z)

  def limpia_campos(self):
      self.wTree.get_widget("edt_codigo").set_text('')
      self.wTree.get_widget("edt_descri").set_text('')
      #self.wTree.get_widget("edt_nomcli").set_text('')
      #self.wTree.get_widget("edt_tipago").set_text('')
      #self.wTree.get_widget("edt_preciovta").set_text('')
      #self.wTree.get_widget("chk_sino").set_active(False)
      #self.wTree.get_widget("chk_cancel").set_active(False)
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


if __name__ == "__main__":
   hwg = Capentpro()
   gtk.main()

def main():

    gtk.main()
    return 0
