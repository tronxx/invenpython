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
#
    hbox = gtk.HBox()
    label = gtk.Label("De la Situacion:")
    hbox.pack_start(label, False, True)
    label.show()
    self.edt_prsit = gtk.Entry()
    hbox.pack_start(self.edt_prsit, True, True)
    self.edt_prsit.show()
    hbox.show()
    vbox_main.pack_start(hbox, True, True)
    vbox_main.show()
#
    hbox = gtk.HBox()
    label = gtk.Label("A la Situacion:  ")
    hbox.pack_start(label, False, True)
    label.show()
    self.edt_ulsit = gtk.Entry()
    hbox.pack_start(self.edt_ulsit, True, True)
    self.edt_ulsit.show()
    hbox.show()
    vbox_main.pack_start(hbox, True, True)
    vbox_main.show()

#
    hbox_options = gtk.HBox()
    frame = gtk.Frame("Mercancia:")
    hbox = gtk.VBox()
    self.rbtn_canceltot = gtk.RadioButton(None, "Total")
    hbox.pack_start(self.rbtn_canceltot, True, True)
    self.rbtn_canceltot.show()
    self.rbtn_cancelsi = gtk.RadioButton(self.rbtn_canceltot, "Cancelacion")
    hbox.pack_start(self.rbtn_cancelsi, True, True)
    self.rbtn_cancelsi.show()
    self.rbtn_cancelno = gtk.RadioButton(self.rbtn_canceltot, "No Cancelacion")
    hbox.pack_start(self.rbtn_cancelno, True, True)
    self.rbtn_cancelno.show()
    hbox.show()
    frame.add(hbox)
    frame.show()
    hbox_options.pack_start(frame, True, True)
    hbox_options.show()
#
    frame = gtk.Frame("Status:")
    hbox = gtk.VBox()
    self.rbtn_vtatot = gtk.RadioButton(None, "Total")
    hbox.pack_start(self.rbtn_vtatot, True, True)
    self.rbtn_vtatot.show()
    hbox.show()
    self.rbtn_vtasi = gtk.RadioButton(self.rbtn_vtatot, "Si")
    hbox.pack_start(self.rbtn_vtasi, True, True)
    self.rbtn_vtasi.show()
    self.rbtn_vtano = gtk.RadioButton(self.rbtn_vtatot, "No")
    hbox.pack_start(self.rbtn_vtano, True, True)
    self.rbtn_vtano.show()
    frame.add(hbox)
    frame.show()
    hbox_options.pack_start(frame, True, True)
    hbox_options.show()
#
    frame = gtk.Frame("Reporte de:")
    hbox = gtk.VBox()
    self.rbtn_vtaneta = gtk.RadioButton(None, "Venta Neta")
    hbox.pack_start(self.rbtn_vtaneta, True, True)
    self.rbtn_vtaneta.show()
    hbox.show()
    self.rbtn_vtabru = gtk.RadioButton(self.rbtn_vtaneta, "Venta Bruta")
    hbox.pack_start(self.rbtn_vtabru, True, True)
    self.rbtn_vtabru.show()
    self.rbtn_vtacancel = gtk.RadioButton(self.rbtn_vtaneta, "Cancelaciones")
    hbox.pack_start(self.rbtn_vtacancel, True, True)
    self.rbtn_vtacancel.show()
    frame.add(hbox)
    frame.show()
    hbox_options.pack_start(frame, True, True)
    hbox_options.show()
#
    frame = gtk.Frame("Movimientos de:")
    hbox = gtk.VBox()
    self.rbtn_vtamen = gtk.RadioButton(None, "Menudeo")
    hbox.pack_start(self.rbtn_vtamen, True, True)
    self.rbtn_vtamen.show()
    hbox.show()
    self.rbtn_vtafon = gtk.RadioButton(self.rbtn_vtamen, "Fonacot")
    hbox.pack_start(self.rbtn_vtafon, True, True)
    self.rbtn_vtafon.show()
    self.rbtn_vtafid = gtk.RadioButton(self.rbtn_vtamen, "Fide")
    hbox.pack_start(self.rbtn_vtafid, True, True)
    self.rbtn_vtafid.show()
    self.rbtn_vtaime = gtk.RadioButton(self.rbtn_vtamen, "Imevi")
    hbox.pack_start(self.rbtn_vtaime, True, True)
    self.rbtn_vtaime.show()
    self.rbtn_vtamtot = gtk.RadioButton(self.rbtn_vtamen, "Total")
    hbox.pack_start(self.rbtn_vtamtot, True, True)
    self.rbtn_vtamtot.show()
    frame.add(hbox)
    frame.show()
    hbox_options.pack_start(frame, True, True)
    hbox_options.show()

    vbox_main.pack_start(hbox_options, True, True)
    vbox_main.show()
    
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
    
  def on_btn_aceptar_clicked(self, widget):
      self.fecini_z = utils.StrToDate(self.wTree.get_widget("edt_fecini").get_text())
      if self.fecini_z == -1:
         self.wTree.get_widget("edt_fecini").grab_focus()
      self.fecfin_z = utils.StrToDate(self.wTree.get_widget("edt_fecfin").get_text())
      if self.fecfin_z == -1:
         self.wTree.get_widget("edt_fecfin").grab_focus()
      where_z = ""
      self.titmercan_z = "Mercancia Sin importar status de Cancelacion"
      self.titstatus_z = "Status 1 y 2"
      self.titvtabru_z = "Ventas Brutas "
      self.tittipovta_z = "Menudeo"
      tiposvta_z = []
      if self.rbtn_cancelsi.get_active() == True:
         where_z = where_z  + " and b.entcan = 'S' "
         self.titmercan_z = "Mercancia de Cancelacion"
      if self.rbtn_cancelno.get_active() == True:
         where_z = where_z  + " and b.entcan = 'N' "
         self.titmercan_z = "Mercancia No de Cancelacion"
      if self.rbtn_vtasi.get_active() == True:
         where_z = where_z + " and siono = 'S' "
         self.titstatus_z = "Status 1"
      if self.rbtn_vtano.get_active() == True:
         where_z = where_z + " and siono = 'N' "
         self.titstatus_z = "Status 2"
      if self.rbtn_vtabru.get_active() == True:
         self.vtabru_z = "V"
         self.titvtabru_z = "Ventas Brutas "
      if self.rbtn_vtaneta.get_active() == True:
         self.vtabru_z = "N"
         self.titvtabru_z = "Ventas Netas "
      if self.rbtn_vtacancel.get_active() == True:
         self.vtabru_z = "C"
         self.titvtabru_z = "Cancelaciones"
      self.vtamen_z = "N"
      if self.rbtn_vtamtot.get_active()== True:
         self.tipovta_z = "T"
         self.titvtabru_z = self.titvtabru_z + " Menudeo, Fonacot, Fide"
      if self.rbtn_vtamen.get_active()== True:
         self.tipovta_z = "M"
         self.vtamen_z = "N"
         self.titvtabru_z = self.titvtabru_z + " Menudeo"
      if self.rbtn_vtafon.get_active()== True:
         self.tipovta_z = "F"
         self.titvtabru_z = self.titvtabru_z + " Fonacot"
      if self.rbtn_vtafid.get_active() == True:
         self.tipovta_z = "I"
         self.titvtabru_z = self.titvtabru_z + " Fide"
      if self.tipovta_z == "M" or self.tipovta_z == "T":
         if self.vtabru_z == "N" or self.vtabru_z == "V":
            tiposvta_z.append(["V", 1])
         if self.vtabru_z == "N" or self.vtabru_z == "C":
            tiposvta_z.append(["C", -1])
      if self.tipovta_z == "F" or self.tipovta_z == "T":
         if self.vtabru_z == "N" or self.vtabru_z == "V":
            tiposvta_z.append(["F", 1])
         if self.vtabru_z == "N" or self.vtabru_z == "C":
            tiposvta_z.append(["O", -1])
      if self.tipovta_z == "I" or self.tipovta_z == "T":
         if self.vtabru_z == "N" or self.vtabru_z == "V":
            tiposvta_z.append(["H", 1])
         if self.vtabru_z == "N" or self.vtabru_z == "C":
            tiposvta_z.append(["J", -1])
      self.prsit_z = self.edt_prsit.get_text().upper()
      self.ulsit_z = self.edt_ulsit.get_text().upper()
      where_z = where_z + " and c.empaqe between '" + self.prsit_z + "' and '" + self.ulsit_z + "' "
      sql1_z = "delete from inv_tmpvtatmp"
      cursor = mydb.cursor()
      cursor.execute(sql1_z)
      sql1_z = "insert into inv_tmpvtatmp ( idtpvtatmp, idtarea, idtipovta, factor, tiposal) "
      ii_z = 0
      for dato in tiposvta_z:
         sql2_z = sql1_z + " values ( " + utils.IntToStr(ii_z) + ", 0, 0, "
         sql2_z = sql2_z + utils.IntToStr(dato[1]) + ", '" + dato[0] + "') "
         print sql2_z
         cursor = mydb.cursor()
         cursor.execute(sql2_z)
         ii_z = ii_z + 1

      self.where_z = where_z
      sql_z = "select e.orden, c.linea, b.codinv, c.descri, c.empaqe, "
      sql_z = sql_z + " (b.unids * d.factor) as unids, "
      sql_z = sql_z + "(b.costou*(b.piva/100+1)*d.factor) as costou "
      sql_z = sql_z + "from inv_tmpvtatmp d "
      sql_z = sql_z + "join entradas a on d.tiposal = a.tipo "
      sql_z = sql_z + "join renentra b on a.tipo = b.tipo "
      sql_z = sql_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sql_z = sql_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sql_z = sql_z + "join lineas e on c.linea = e.numero and c.cia = e.cia "
      sql_z = sql_z + "where a.fecha between "
      sql_z = sql_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sql_z = sql_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sql_z = sql_z + " a.cia = " + repr(cia_z)
      sql_z = sql_z + where_z
      sql_z = sql_z + " group by e.orden, c.linea, b.codinv"

      sqlin3_z = "select "
      sqlin3_z = sqlin3_z + "sum(b.unids*d.factor) as unids, "
      sqlin3_z = sqlin3_z + "sum(b.costou*(b.piva/100+1)*d.factor) as costo "
      sqlin3_z = sqlin3_z + "from inv_tmpvtatmp d "
      sqlin3_z = sqlin3_z + "join entradas a on d.tiposal = a.tipo "
      sqlin3_z = sqlin3_z + "join renentra b on a.tipo = b.tipo "
      sqlin3_z = sqlin3_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqlin3_z = sqlin3_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqlin3_z = sqlin3_z + "where a.fecha between "
      sqlin3_z = sqlin3_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sqlin3_z = sqlin3_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sqlin3_z = sqlin3_z + " a.cia = " + repr(cia_z)
      sqlin3_z = sqlin3_z + self.where_z

      self.pag_z = 1
      self.antlin_z = "-1"
      self.linea_z = ""
      self.antcrd_z = -1
      self.antptovta_z = "-1"
      band_z = ""
      self.arch_z = open("analifon.tex", "w")
      self.antlinea_z = ""
      self.ptvta_z = ""
      self.mienc_z = 2
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
      for record in result:
        ren_z = ren_z + 1
        ii_z = 1
        linea_z = record[ii_z]
        ii_z = ii_z + 1
        codigo_z = record[ii_z]
        ii_z = ii_z + 1
        descri_z = record[ii_z]
        ii_z = ii_z + 1
        situac_z = record[ii_z]
        ii_z = ii_z + 1
        canti_z = record[ii_z]
        ii_z = ii_z + 1
        costo_z = record[ii_z]
        if band_z <> "S":
           self.antlinea_z = linea_z
           band_z = "S"
           self.busca_ptosvta(self.antlinea_z)
           self.encab()
        else:
           if self.antlinea_z <> linea_z:
              self.sub_linea()
              self.arch_z.write("\n")
              self.lineaspag_z = self.lineaspag_z + 1
              self.antlinea_z = linea_z
              self.busca_ptosvta(self.antlinea_z)
              if self.lineaspag_z + 3 > utils.LINEAS_X_PAG:
                 self.salto_pag()
              else:
                 self.subenc_analitico()
              
        self.impcosxlin_z = self.impcosxlin_z + costo_z
        if ren_z == numrows:
           self.arch_z.write(self.subrayado_on)
        self.arch_z.write(codigo_z.ljust(13)+"|")
        self.arch_z.write(descri_z.ljust(30)+"|")
        tothor_z = 0
        unids_z = 0
        for ptovta_z in self.ptvta_z:
            sqlin4_z = sqlin3_z + " and b.recemi = '" + ptovta_z[0] + "' "
            sqlin4_z = sqlin4_z + " and c.codigo = '" + codigo_z + "' "
            #print "sqlin4:", sqlin4_z
            totptvt_z = ptovta_z[1]
            cursor2 = mydb.cursor()
            cursor2.execute(sqlin4_z)
            coslinxpt_z = 0
            unidsxpt_z = 0
            result2 = cursor2.fetchall()
            for record2 in result2:
                #print "Record2[0]:",record2[0], ": Record2[1]:",record2[1]

                unidsxpt_z = unidsxpt_z + utils.ValFloat(record2[0])
                coslinxpt_z = coslinxpt_z + utils.ValFloat(record2[1])
            if unidsxpt_z <> 0:
               cosstr_z = '%4.0f' % unidsxpt_z
            else:
               cosstr_z = ""
            tothor_z = tothor_z + coslinxpt_z
            unids_z = unids_z + unidsxpt_z
            self.arch_z.write(cosstr_z.rjust(4)+"|")
        cosstr_z = '%4.0f' % unids_z
        self.arch_z.write(cosstr_z+"|")
        self.arch_z.write(utils.currency(tothor_z).rjust(12)+"|")
        self.arch_z.write(situac_z.ljust(10)+"|")
        if ren_z == numrows:
           self.arch_z.write(self.subrayado_off)
        self.arch_z.write("\n")
        self.lineaspag_z = self.lineaspag_z + 1

      
      #if self.vtamen_z == "S":
      #   self.sub_credcon()
      self.sub_linea()
      #self.sub_ptovta()
      total_z = self.impcostot_z
      self.arch_z.write("Total General".ljust(59))
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n\n")
      self.lineaspag_z = self.lineaspag_z + 2
      self.mienc_z = 2
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
      self.arch_z.write(self.condensado_on + "repcvta " + self.condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      self.arch_z.write(("Impresion de Reporte de Costo de Ventas Pag:" + '%d' % self.pag_z).center(80) + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
#      self.arch_z.write(self.negritas_on)
#      self.arch_z.write(("De:" + self.alm_z + " " + nombrealm_z + " Del "+ self.fecini_z.strftime('%d/%m/%Y') + " Al " + self.fecfin_z.strftime('%d/%m/%Y') ).center(80))
#      self.arch_z.write(self.negritas_off + "\n")
#      self.lineaspag_z = self.lineaspag_z + 1
      self.arch_z.write(self.negritas_on + self.titmercan_z + self.negritas_off + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
      self.arch_z.write(self.negritas_on + self.titvtabru_z + " " + self.titstatus_z + self.negritas_off + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
      self.arch_z.write(self.negritas_on + "De la Situacion" + self.prsit_z + " A la Situacion " + self.ulsit_z + self.negritas_off + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
      if self.mienc_z == 1:
         self.subenc_tab_x_linea()
      elif self.mienc_z == 2:
         self.subenc_analitico()

  def subenc_analitico(self):
      nombre_z = def_tablas.busca_nombre(mydb, self.antlinea_z, cia_z, def_tablas.LINEA)
      self.arch_z.write(self.condensado_off + self.negritas_on + "Linea:" + \
      self.antlinea_z + " " + nombre_z + self.negritas_off + "\n")
      if len(self.ptvta_z) > 4:
         font_on = self.condensado_on
      elif len(self.ptvta_z) > 2:
         font_on = self.elite
      else:
         font_on = self.condensado_off
      self.arch_z.write(font_on + self.subrayado_on)
      self.arch_z.write("Codigo".ljust(13)+"|"+"Descripcion".ljust(30)+"|")
      for ptovta_z in self.ptvta_z:
          self.arch_z.write(ptovta_z[0].ljust(4)+"|")
      self.arch_z.write("Tot.|" + "Costo Total".rjust(12) + "|" + "Situacion".ljust(10))
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

  def busca_ptosvta(self, linea_z):
      sqlin2_z = "select b.recemi, sum(unids*d.factor) as canti, sum(b.costou*(b.piva/100+1)*d.factor) "
      sqlin2_z = sqlin2_z + "from inv_tmpvtatmp d "
      sqlin2_z = sqlin2_z + "join entradas a on d.tiposal = a.tipo "
      sqlin2_z = sqlin2_z + "join renentra b on a.tipo = b.tipo "
      sqlin2_z = sqlin2_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqlin2_z = sqlin2_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqlin2_z = sqlin2_z + "where a.fecha between "
      sqlin2_z = sqlin2_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sqlin2_z = sqlin2_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sqlin2_z = sqlin2_z + " a.cia = " + repr(cia_z)
      sqlin2_z = sqlin2_z + " and c.linea = '" + linea_z + "' "
      sqlin2_z = sqlin2_z + self.where_z
      sqlin2_z = sqlin2_z + " group by b.recemi"
      print sqlin2_z

      cursor = mydb.cursor()
      cursor.execute(sqlin2_z)
      result = cursor.fetchall()
      self.ptvta_z=[]
      for record in result:
          self.ptvta_z.append([ record[0], record[1], record[2] ] )
# Fin de Busca puntos de Venta

  def tabla_x_linea(self):
      sqlin1_z = "select e.orden, c.linea, "
      sqlin1_z = sqlin1_z + "sum(b.costou*(b.piva/100+1)*d.factor) "
      sqlin1_z = sqlin1_z + "from inv_tmpvtatmp d "
      sqlin1_z = sqlin1_z + "join entradas a on d.tiposal = a.tipo "
      sqlin1_z = sqlin1_z + "join renentra b on a.tipo = b.tipo "
      sqlin1_z = sqlin1_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqlin1_z = sqlin1_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqlin1_z = sqlin1_z + "join lineas e on c.linea = e.numero and c.cia = e.cia "
      sqlin1_z = sqlin1_z + "where a.fecha between "
      sqlin1_z = sqlin1_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sqlin1_z = sqlin1_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sqlin1_z = sqlin1_z + " a.cia = " + repr(cia_z)
      sqlin1_z = sqlin1_z + self.where_z
      sqlin1_z = sqlin1_z + " group by e.orden, c.linea"
      print sqlin1_z

      sqptvt_z = "select b.recemi, "
      sqptvt_z = sqptvt_z + "sum(b.costou*(b.piva/100+1)*d.factor) "
      sqptvt_z = sqptvt_z + "from inv_tmpvtatmp d "
      sqptvt_z = sqptvt_z + "join entradas a on d.tiposal = a.tipo "
      sqptvt_z = sqptvt_z + "join renentra b on a.tipo = b.tipo "
      sqptvt_z = sqptvt_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqptvt_z = sqptvt_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqptvt_z = sqptvt_z + "where a.fecha between "
      sqptvt_z = sqptvt_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sqptvt_z = sqptvt_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sqptvt_z = sqptvt_z + " a.cia = " + repr(cia_z)
      sqptvt_z = sqptvt_z + self.where_z
      sqptvt_z = sqptvt_z + " group by b.recemi"

      sqsituac_z = "select c.empaqe, "
      sqsituac_z = sqsituac_z + "sum(b.costou*(b.piva/100+1)*d.factor) "
      sqsituac_z = sqsituac_z + "from inv_tmpvtatmp d "
      sqsituac_z = sqsituac_z + "join entradas a on d.tiposal = a.tipo "
      sqsituac_z = sqsituac_z + "join renentra b on a.tipo = b.tipo "
      sqsituac_z = sqsituac_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sqsituac_z = sqsituac_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sqsituac_z = sqsituac_z + "where a.fecha between "
      sqsituac_z = sqsituac_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sqsituac_z = sqsituac_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sqsituac_z = sqsituac_z + " a.cia = " + repr(cia_z)
      sqsituac_z = sqsituac_z + self.where_z
      sqsituac_z = sqsituac_z + " group by c.empaqe"

      cursor = mydb.cursor()
      cursor.execute(sqlin1_z)
      result = cursor.fetchall()
      self.mislineas_z=[]
      nrecs_z = 0
      for record in result:
          self.mislineas_z.append([ record[1], record[2] ] )

      print "Puntos de Venta:\n", sqptvt_z
      cursor = mydb.cursor()
      cursor.execute(sqptvt_z)
      result = cursor.fetchall()
      self.misptovta_z=[]
      nrecs_z = 0
      for record in result:
          self.misptovta_z.append([ record[0], record[1] ] )

      print "Situaciones:\n", sqsituac_z
      cursor = mydb.cursor()
      cursor.execute(sqsituac_z)
      result = cursor.fetchall()
      self.missituac_z=[]
      nrecs_z = 0
      for record in result:
          self.missituac_z.append([ record[0], record[1] ] )

      maxrec_z = 0
      nrecslin_z = len(self.mislineas_z)
      if nrecslin_z > maxrec_z:
         maxrec_z = nrecslin_z
      nrecspvt_z = len(self.misptovta_z)
      if nrecspvt_z > maxrec_z:
         maxrec_z = nrecspvt_z
      nrecssit_z = len(self.missituac_z)
      if nrecssit_z > maxrec_z:
         maxrec_z = nrecssit_z
         
      self.mienc_z = 1
      if self.lineaspag_z + maxrec_z + 1 >  utils.LINEAS_X_PAG:
         self.salto_pag()
      else:
         self.subenc_tab_x_linea()

      totcossit_z = 0
      totcoslin_z = 0
      totcospvt_z = 0
      for ii_z in range (maxrec_z):
          if ii_z < nrecssit_z:
             cossit_z = utils.currency(self.missituac_z[ii_z][1])
             totcossit_z = totcossit_z + self.missituac_z[ii_z][1]
             situac_z = self.missituac_z[ii_z][0]
          else:
             cossit_z = ""
             situac_z = ""
          if ii_z < nrecslin_z:
             coslin_z = utils.currency(self.mislineas_z[ii_z][1])
             totcoslin_z = totcoslin_z + self.mislineas_z[ii_z][1]
             linea_z = self.mislineas_z[ii_z][0]
          else:
             coslin_z = ""
             linea_z = ""
          if ii_z < nrecspvt_z:
             cospvt_z = utils.currency(self.misptovta_z[ii_z][1])
             totcospvt_z = totcospvt_z + self.misptovta_z[ii_z][1]
             ptovta_z = self.misptovta_z[ii_z][0]
          else:
             cospvt_z = ""
             ptovta_z = ""
             
          if self.lineaspag_z  > utils.LINEAS_X_PAG:
             self.salto_pag()
          self.arch_z.write("".ljust(14))
          if ii_z == maxrec_z - 1:
             self.arch_z.write(self.subrayado_on)
          self.arch_z.write(situac_z.ljust(10)+ " "+ cossit_z.rjust(12) + "|")
          self.arch_z.write(linea_z.ljust(5)+ " "+ coslin_z.rjust(12) + "|")
          self.arch_z.write(ptovta_z.ljust(4)+ " "+ cospvt_z.rjust(12) + "|")
          if ii_z == maxrec_z - 1:
             self.arch_z.write(self.subrayado_off)
          self.arch_z.write("\n")
          self.lineaspag_z = self.lineaspag_z + 1

          if self.lineaspag_z + 3 > utils.LINEAS_X_PAG:
             self.salto_pag()
      self.arch_z.write("".ljust(14))
      self.arch_z.write(utils.currency(totcossit_z).rjust(23)+"|")
      self.arch_z.write(utils.currency(totcoslin_z).rjust(18)+"|")
      self.arch_z.write(utils.currency(totcospvt_z).rjust(17)+"|\n")


  def subenc_tab_x_linea(self):
      self.arch_z.write("".ljust(14))
      self.arch_z.write(self.subrayado_on+"Situacion".ljust(10)+" "+"Costo".rjust(12)+"|")
      self.arch_z.write("Linea "+"Costo".rjust(12)+"|")
      self.arch_z.write("Pvta "+"Costo".rjust(12)+"|" + self.subrayado_off +"\n")

if __name__ == "__main__":
   hwg = analisma()
   gtk.main()

def main():

    gtk.main()
    return 0
