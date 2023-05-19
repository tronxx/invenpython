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
try:
  import MySQLdb
except:
  sys.exit(1)
import def_tablas
import utils
import datetime

global mydb
global cia_z
global mibd
global cias
global vendedor
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
PTOVTA = def_tablas.PTOVTA
LINEA = def_tablas.LINEA
CREDCON = def_tablas.CREDCON

class analisma:
  """Esta es una aplicación Alta Almacenes"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    self.gladefile = dirprogs_z + "reporte.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_aceptar_clicked": self.on_btn_aceptar_clicked, \
            "on_btn_cancel_clicked": self.on_btn_cancel_clicked, \
            "on_win_dialog_destroy_event": gtk.main_quit 
           }
    self.wTree.signal_autoconnect(dic)
    vbox_main = self.wTree.get_widget("vbox_main")
    
    global cias
    global cia_z
    global mydb
    cia_z = 1
    cias_lines = []
    basedato_z = []

    fh_cias = open('.cias.ini')
    for line in fh_cias.readlines():
        cias_lines.append(string.rstrip(line))
    cia_z = cias_lines[0]

    mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_dialog")
    miwin.set_title(cias['razon'] + " Analitico de Ventas")
    hoy_z = utils.SumaMeses(datetime.datetime.now(), -1)
    primerodemes_z = utils.PrimeroDeMes(hoy_z)
    self.wTree.get_widget("edt_fecini").set_text(primerodemes_z.strftime('%d/%m/%Y'))
    ultimodemes_z = utils.UltimoDeMes(primerodemes_z)
    self.wTree.get_widget("edt_fecfin").set_text(ultimodemes_z.strftime('%d/%m/%Y'))
    self.tipent_z = "E"
    
  def on_btn_aceptar_clicked(self, widget):
      self.fecini_z = utils.StrToDate(self.wTree.get_widget("edt_fecini").get_text())
      if self.fecini_z == -1:
         self.wTree.get_widget("edt_fecini").grab_focus()
      self.fecfin_z = utils.StrToDate(self.wTree.get_widget("edt_fecfin").get_text())
      if self.fecfin_z == -1:
         self.wTree.get_widget("edt_fecfin").grab_focus()
      self.inianu_z = utils.StrToDate("01-01-" + '%4d' % self.fecini_z.year)
      where_z = ""
      self.titmercan_z = "Mercancia Sin importar status de Cancelacion"
      self.titstatus_z = "Status 1 y 2"
      self.titvtabru_z = "Ventas Brutas "
      self.tittipovta_z = "Menudeo"
      tiposvta_z = []
      sql_z = "select a.prove,"
      sql_z = sql_z + "sum(b.costou*(b.piva/100+1)) as costo "
      sql_z = sql_z + "from entradas a "
      sql_z = sql_z + "join renentra b on a.tipo = b.tipo "
      sql_z = sql_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sql_z = sql_z + "where a.fecha between "
      sql_z = sql_z + "'" + self.inianu_z.strftime('%Y-%m-%d') + "' and "
      sql_z = sql_z + "'" + self.fecfin_z.strftime('%Y-%m-%d') + "' and "
      sql_z = sql_z + " a.cia = " + repr(cia_z) + " and a.tipo = '" + self.tipent_z + "'"
      sql_z = sql_z + " group by a.prove"

      sqlin3_z = "select b.siono, "
      sqlin3_z = sqlin3_z + "sum(b.costou*(b.piva/100+1)) as costo "
      sqlin3_z = sqlin3_z + "from entradas a "
      sqlin3_z = sqlin3_z + "join renentra b on a.tipo = b.tipo "
      sqlin3_z = sqlin3_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqlin3_z = sqlin3_z + "where a.fecha between "
      sqlin3_z = sqlin3_z + "'" + self.fecini_z.strftime('%Y-%m-%d') + "' and "
      sqlin3_z = sqlin3_z + "'" + self.fecfin_z.strftime('%Y-%m-%d') + "' and "
      sqlin3_z = sqlin3_z + " a.cia = " + repr(cia_z)
      sqlin3_z = sqlin3_z + " and a.tipo = '" + self.tipent_z + "' "

      self.pag_z = 1
      self.antlin_z = "-1"
      self.linea_z = ""
      self.antcrd_z = -1
      self.antptovta_z = "-1"
      band_z = ""
      self.arch_z = open("infent.tex", "w")
      self.antlinea_z = ""
      self.ptvta_z = ""
      self.mienc_z = "analitico"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      numrows = int(cursor.rowcount)
      ren_z = 0
      self.impcosxlin_z = 0
      self.impcosxcrd_z = 0
      self.impcosxptv_z = 0
      self.impcostot_z = 0
      result = cursor.fetchall()
      crdcon_z = ""
      totcomsi_z = 0
      totcomno_z = 0
      totcoman_z = 0
      misprove_z = []
      posan1_z = 0
      posan2_z = 0
      posmes1_z = 0
      posmes2_z = 0
      ren_z = 0
      maxcos01_z = 0
      maxcos02_z = 0
      maxcos03_z = 0
      maxcos04_z = 0
      for record in result:
        ii_z = 0
        prove_z = record[ii_z]
        ii_z = ii_z + 1
        costo_z = record[ii_z]
        nombre_z = def_tablas.busca_nombre(mydb, prove_z, cia_z, def_tablas.PROVEEDOR)[:30]
        sqlpro4_z = sqlin3_z + " and a.prove = '" + prove_z + "' "
        sqlpro4_z = sqlpro4_z + " group by b.siono "

        comprasi_z = 0
        comprano_z = 0
        cursor2 = mydb.cursor()
        cursor2.execute(sqlpro4_z)
        comprames = cursor2.fetchall()
        for compras in comprames:
            if compras[0] == "S":
               comprasi_z = compras[1]
            else:
               comprano_z = compras[1]
        misprove_z.append( [prove_z, comprasi_z, comprano_z, costo_z, 0, 0] )
        totcompra_z = comprasi_z + comprano_z
        if costo_z > maxcos01_z:
           maxcos01_z = costo_z
           posan1_z = ren_z
        if costo_z > maxcos02_z and costo_z < maxcos01_z:
           maxcos02_z = costo_z
           posan2_z = ren_z
        if totcompra_z > maxcos03_z:
           maxcos03_z = totcompra_z
           posmes1_z = ren_z
        if totcompra_z > maxcos04_z and totcompra_z < maxcos03_z:
           maxcos04_z = totcompra_z
           posmes2_z = ren_z
        ren_z = ren_z + 1

##----
      misprove_z[posan1_z][5] = 1
      misprove_z[posan2_z][5] = 2
      misprove_z[posmes1_z][4] = 1
      misprove_z[posmes2_z][4] = 2

      ren_z = 0
      for datosprove_z in misprove_z:
        ren_z = ren_z + 1
        costo_z = datosprove_z[3]
        prove_z = datosprove_z[0]
        nombre_z = def_tablas.busca_nombre(mydb, prove_z, cia_z, def_tablas.PROVEEDOR)[:30]
        comprasi_z = datosprove_z[1]
        comprano_z = datosprove_z[2]
        totcompra_z = comprasi_z + comprano_z
        totcomsi_z = totcomsi_z + comprasi_z
        totcomno_z = totcomno_z + comprano_z
        totcoman_z = totcoman_z + costo_z

        if band_z <> "S":
           self.encab()
           band_z = "S"
        self.arch_z.write("".ljust(6))
        if ren_z == numrows:
           self.arch_z.write(self.subrayado_on)
        self.arch_z.write("|" + prove_z.ljust(4)+"|")
        self.arch_z.write(nombre_z.ljust(30)+"|")
        if comprasi_z <> 0:
           strcomp_z = utils.currency(comprasi_z)
        else:
           strcomp_z = ""
        self.arch_z.write(strcomp_z.rjust(14)+"|")
        if comprano_z <> 0:
           strcomp_z = utils.currency(comprano_z)
        else:
           strcomp_z = ""
        self.arch_z.write(strcomp_z.rjust(14)+"|")
        self.arch_z.write(utils.currency(totcompra_z).rjust(14)+"|")
        pos_z = ""
        if datosprove_z[4] <> 0:
           pos_z = '%3d' % datosprove_z[4]
        self.arch_z.write(pos_z.rjust(3)+"|")
        self.arch_z.write(utils.currency(costo_z - totcompra_z).rjust(14)+"|")
        pos_z = ""
        if datosprove_z[5] <> 0:
           pos_z = '%3d' % datosprove_z[5]
        self.arch_z.write(pos_z.rjust(3)+"|")
        self.arch_z.write(utils.currency(costo_z).rjust(14)+"|")
        pos_z = ""
        if datosprove_z[5] <> 0:
           pos_z = '%3d' % datosprove_z[5]
        self.arch_z.write(pos_z.rjust(3)+"|")
        if ren_z == numrows:
           self.arch_z.write(self.subrayado_off)
        self.arch_z.write("\n")
        self.lineaspag_z = self.lineaspag_z + 1

      
      self.arch_z.write("".ljust(6)+ self.subrayado_on + "|Total General".ljust(36) + "|" )
      self.arch_z.write(utils.currency(totcomsi_z).rjust(14) + "|")
      self.arch_z.write(utils.currency(totcomno_z).rjust(14) + "|")
      self.arch_z.write(utils.currency(totcomsi_z + totcomno_z).rjust(14) + "|   |")
      self.arch_z.write(utils.currency(totcoman_z - totcomsi_z + totcomno_z).rjust(14) + "|   |")
      self.arch_z.write(utils.currency(totcoman_z).rjust(14) + "|   |")
      self.arch_z.write(self.subrayado_off + "\n\n")
      self.lineaspag_z = self.lineaspag_z + 2
      self.mienc_z = "tabla_x_linea"
      self.tabla_x_linea()
      self.arch_z.close()
      gtk.main_quit()

  def salto_pag(self):
      self.arch_z.write(def_tablas.font(mydb, 1, "FORM-FEED FF"))
      self.pag_z = self.pag_z + 1
      self.encab()

  def encab(self):
      self.arch_z.write(cias['razon'].center(80) + "\n")
      self.lineaspag_z = 1
      self.negritas_on = def_tablas.font(mydb, 1, "EMPHAIZED ON")
      self.negritas_off = def_tablas.font(mydb, 1, "EMPHAIZED OFF")
      self.condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      self.condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      self.subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      self.subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")
      self.elite = def_tablas.font(mydb, 1, "ELITE")
      hora_z = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
      self.lineaspag_z = self.lineaspag_z + 1
      self.arch_z.write(self.condensado_on + "infent " + self.condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      self.arch_z.write("Informe de Entradas del " + \
        self.fecini_z.strftime('%d/%m/%Y') + " Al " + \
        self.fecfin_z.strftime('%d/%m/%Y') + " Pag:" + \
        '%d' % self.pag_z + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
      if self.mienc_z == "tabla_x_linea_com":
         self.subenc_tab_x_linea_com()
      elif self.mienc_z == "tabla_x_linea_mes":
         self.subenc_tab_x_linea_mes()
      elif self.mienc_z == "analitico":
         self.subenc_analitico()

  def subenc_analitico(self):
      self.arch_z.write(self.condensado_on + "".ljust(6) )
      self.arch_z.write(utils.StringOf("_",125)+"\n")
      self.arch_z.write("".ljust(6) + self.subrayado_on)
      self.arch_z.write("|Provedor".ljust(35)+"|")
      self.arch_z.write("Compras Si".rjust(14) + "|" )
      self.arch_z.write("Compras No".rjust(14) + "|" )
      self.arch_z.write("Total Mensual".rjust(14) + "|POS|" )
      self.arch_z.write("Anual Compras".rjust(14) + "|POS|" )
      self.arch_z.write("Total General".rjust(14) + "|POS|" )
      self.arch_z.write(self.subrayado_off + "\n")
      self.lineaspag_z = self.lineaspag_z + 2

  def subenc0(self):
      self.arch_z.write("Punto de Venta:")
      nomptovt_z = def_tablas.busca_nombre(mydb, self.antptovta_z, cia_z, PTOVTA)
      self.arch_z.write(self.antptovta_z + " " + nomptovt_z + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
      #self.subenc1()

  def subenc1(self):
      self.arch_z.write("Linea:")
      nomlinea_z = def_tablas.busca_nombre(mydb, self.antlin_z, cia_z, LINEA)
      self.arch_z.write(self.antlin_z + " " + nomlinea_z + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
      if self.vtamen_z == "S":
         self.subenc2()

  def subenc2(self):
      nomcredcon_z = def_tablas.busca_dato(mydb, self.antcrd_z, CREDCON)
      self.arch_z.write(nomcredcon_z + "\n")
      self.lineaspag_z = self.lineaspag_z + 1

  def sub_credcon(self):
      self.arch_z.write("Subtotal Credito/Contado:".ljust(71))
      self.impcosxlin_z = self.impcosxlin_z + self.impcosxcrd_z 
      total_z = self.impcosxcrd_z 
      self.impcosxcrd_z=0
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.lineaspag_z = self.lineaspag_z + 1

  def sub_linea(self):
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("Subtotal esta Linea".ljust(44)+"|")
      unids_z = 0
      tothor_z = 0
      for ptovta_z in self.ptvta_z:
          unids_z = unids_z + ptovta_z[1]
          tothor_z = tothor_z + ptovta_z[2]
          cosstr_z = '%4.0f' % ptovta_z[1]
          self.arch_z.write(cosstr_z.rjust(4)+"|")
      cosstr_z = '%4.0f' % unids_z
      self.arch_z.write(cosstr_z+"|")
      self.arch_z.write(utils.currency(tothor_z).rjust(12)+"|")
      self.arch_z.write(self.subrayado_off+"\n")
      self.impcostot_z = self.impcostot_z + tothor_z
      self.lineaspag_z = self.lineaspag_z + 1

  def sub_ptovta(self):
      self.arch_z.write("Subtotal Punto de Venta".ljust(71))
      self.impcostot_z = self.impcostot_z + self.impcosxptv_z 
      total_z = self.impcosxptv_z 
      self.impcosxptv_z=0
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.lineaspag_z = self.lineaspag_z + 1

  def on_btn_cancel_clicked(self, widget):
      print "Presionaste Cancelar"
      gtk.main_quit()

  def tabla_x_linea(self):
      sqlin1_z = "select e.orden, c.linea, "
      sqlin1_z = sqlin1_z + "sum(b.costou*(b.piva/100+1)) "
      sqlin1_z = sqlin1_z + "from entradas a "
      sqlin1_z = sqlin1_z + "join renentra b on a.tipo = b.tipo "
      sqlin1_z = sqlin1_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqlin1_z = sqlin1_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqlin1_z = sqlin1_z + "join lineas e on c.linea = e.numero and c.cia = e.cia "
      sqlin1_z = sqlin1_z + "where a.fecha between "
      sqlin1_z = sqlin1_z + "'" + self.inianu_z.strftime('%Y-%m-%d') + "' and "
      sqlin1_z = sqlin1_z + "'" + self.fecfin_z.strftime('%Y-%m-%d') + "' and "
      sqlin1_z = sqlin1_z + " a.cia = " + repr(cia_z)
      sqlin1_z = sqlin1_z + " and a.tipo = '" + self.tipent_z + "' "
      sqlin1_z = sqlin1_z + " group by e.orden, c.linea"
      print sqlin1_z

      self.tipdev_z="R"
      sqlin2_z = "select c.linea, a.tipo, "
      sqlin2_z = sqlin2_z + "sum(b.costou*(b.piva/100+1)) "
      sqlin2_z = sqlin2_z + "from entradas a "
      sqlin2_z = sqlin2_z + "join renentra b on a.tipo = b.tipo "
      sqlin2_z = sqlin2_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqlin2_z = sqlin2_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqlin2_z = sqlin2_z + "where a.fecha between "
      sqlin2_z = sqlin2_z + "'" + self.fecini_z.strftime('%Y-%m-%d') + "' and "
      sqlin2_z = sqlin2_z + "'" + self.fecfin_z.strftime('%Y-%m-%d') + "' and "
      sqlin2_z = sqlin2_z + " a.cia = " + repr(cia_z)
      sqlin2_z = sqlin2_z + " and ( a.tipo = '" + self.tipent_z + "' "
      sqlin2_z = sqlin2_z + " or a.tipo = '" + self.tipdev_z + "') "

      cursor = mydb.cursor()
      cursor.execute(sqlin1_z)
      result = cursor.fetchall()
      self.mislineas_z=[]
      nrecs_z = 0
      totcosmes_z = 0
      totdevmes_z = 0
      totcosanu_z = 0
      totcosglo_z = 0
      totnetmes_z = 0
      for record in result:
          ii_z = 1
          linea_z = record[ii_z]
          ii_z = ii_z + 1
          costoan_z = record[ii_z]
          sqlin3_z = sqlin2_z + " and c.linea = '" + linea_z + "' group by c.linea, a.tipo"
          cursorlin = mydb.cursor()
          cursorlin.execute(sqlin3_z)
          resultlin = cursorlin.fetchall()
          cosmes_z = 0
          devmes_z = 0
          for reclin in resultlin:
              ii_z = 1
              tipo_z = reclin[ii_z]
              ii_z = ii_z + 1
              if tipo_z == self.tipdev_z:
                 devmes_z = reclin[ii_z]
              else:
                 cosmes_z = reclin[ii_z]
          totcosmes_z = totcosmes_z + cosmes_z
          totnetmes_z = totnetmes_z + cosmes_z - devmes_z
          totdevmes_z = totdevmes_z + devmes_z
          totcosanu_z = totcosanu_z + costoan_z - cosmes_z
          totcosglo_z = totcosglo_z + costoan_z
          self.mislineas_z.append([ linea_z, costoan_z, cosmes_z, devmes_z ] )

      nrecslin_z = len(self.mislineas_z)
      
      self.mienc_z = "tabla_x_linea_com"
      self.salto_pag()
      ii_z = 0
      for reclin_z in self.mislineas_z:
          ii_z = ii_z + 1
          if self.lineaspag_z  > utils.LINEAS_X_PAG:
             self.salto_pag()
          linea_z  = reclin_z[0]
          cosmes_z = reclin_z[2]
          cosglo_z = reclin_z[1]
          cosanu_z = cosglo_z - cosmes_z
          self.arch_z.write("".ljust(6))
          if ii_z == nrecslin_z:
             self.arch_z.write(self.subrayado_on)
          
          self.arch_z.write("|"+linea_z.ljust(5)+"|")
          self.arch_z.write(utils.currency(cosmes_z).rjust(14) + "|")
          self.arch_z.write(utils.Porcentaje(cosmes_z, totcosmes_z).rjust(5)+"|")
          self.arch_z.write(utils.currency(cosanu_z).rjust(14) + "|")
          self.arch_z.write(utils.Porcentaje(cosanu_z, totcosanu_z).rjust(5)+"|")
          self.arch_z.write(utils.currency(cosglo_z).rjust(14) + "|")
          self.arch_z.write(utils.Porcentaje(cosglo_z, totcosglo_z).rjust(5)+"|")
          if ii_z == nrecslin_z:
             self.arch_z.write(self.subrayado_off)
          self.arch_z.write("\n")
          self.lineaspag_z = self.lineaspag_z + 1

          if self.lineaspag_z + 3 > utils.LINEAS_X_PAG:
             self.salto_pag()
      self.arch_z.write("".ljust(6))
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("|Total|")
      self.arch_z.write(utils.currency(totcosmes_z).rjust(14)+"|100.0|")
      self.arch_z.write(utils.currency(totcosanu_z).rjust(14)+"|100.0|")
      self.arch_z.write(utils.currency(totcosglo_z).rjust(14)+"|100.0|")
      self.arch_z.write(self.subrayado_off+"\n\n")
      self.lineaspag_z = self.lineaspag_z + 2

#
      self.mienc_z = "tabla_x_linea_mes"
      if self.lineaspag_z + nrecslin_z + 1 >  utils.LINEAS_X_PAG:
         self.salto_pag()
      else:
         self.subenc_tab_x_linea_mes()
      
      ii_z = 0
      for reclin_z in self.mislineas_z:
          ii_z = ii_z + 1
          if self.lineaspag_z  > utils.LINEAS_X_PAG:
             self.salto_pag()
          linea_z  = reclin_z[0]
          cosmes_z = reclin_z[2]
          devmes_z = reclin_z[3]
          cosnet_z = cosmes_z - devmes_z
          self.arch_z.write("".ljust(11))
          if ii_z == nrecslin_z:
             self.arch_z.write(self.subrayado_on)
          
          self.arch_z.write("|"+linea_z.ljust(5)+"|")
          self.arch_z.write(utils.currency(cosmes_z).rjust(14) + "|")
          self.arch_z.write(utils.currency(devmes_z).rjust(14) + "|")
          self.arch_z.write(utils.currency(cosnet_z).rjust(14) + "|")
          self.arch_z.write(utils.Porcentaje(cosnet_z, totnetmes_z).rjust(5)+"|")
          if ii_z == nrecslin_z:
             self.arch_z.write(self.subrayado_off)
          self.arch_z.write("\n")
          self.lineaspag_z = self.lineaspag_z + 1

          if self.lineaspag_z + 3 > utils.LINEAS_X_PAG:
             self.salto_pag()
      cosnet_z = totcosmes_z - totdevmes_z
      self.arch_z.write("".ljust(11))
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("|Total|")
      self.arch_z.write(utils.currency(totcosmes_z).rjust(14)+"|")
      self.arch_z.write(utils.currency(totdevmes_z).rjust(14)+"|")
      self.arch_z.write(utils.currency(cosnet_z).rjust(14)+"|100.0|")
      self.arch_z.write(self.subrayado_off+"\n")


  def subenc_tab_x_linea_com(self):
      self.arch_z.write("".ljust(6)+utils.StringOf("_",70)+"\n")
      self.arch_z.write("".ljust(6)+self.subrayado_on+"|Linea|")
      self.arch_z.write("Compras Mes".rjust(14)+"|  %  |")
      self.arch_z.write("Compras Anual".rjust(14)+"|  %  |")
      self.arch_z.write("Compras Global".rjust(14)+"|  %  |")
      self.arch_z.write(self.subrayado_off +"\n")

  def subenc_tab_x_linea_mes(self):
      self.arch_z.write("".ljust(11)+utils.StringOf("_",58)+"\n")
      self.arch_z.write("".ljust(11)+self.subrayado_on+"|Linea|")
      self.arch_z.write("Compras Mes".rjust(14)+"|")
      self.arch_z.write("Devols Mes".rjust(14)+"|")
      self.arch_z.write("Compras Netas".rjust(14)+"|  %  |")
      self.arch_z.write(self.subrayado_off +"\n")


if __name__ == "__main__":
   hwg = analisma()
   gtk.main()

def main():

    gtk.main()
    return 0
