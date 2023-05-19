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
    label = gtk.Label("Del Almacen:")
    hbox.pack_start(label, False, True)
    label.show()
    self.edt_almacen = gtk.Entry()
    hbox.pack_start(self.edt_almacen, True, True)
    self.edt_almacen.show()
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
#
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

# execute SQL statement
    mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])

    sql_z = "select * from ciasinv where cia = " + repr(cia_z)
    cias = def_tablas.busca_cia(mydb, cia_z)
    miwin = self.wTree.get_widget("win_dialog")
    miwin.set_title(cias['razon'] + " Analitico de Ventas")
    hoy_z = utils.SumaMeses(datetime.datetime.now(), -1)
    primerodemes_z = utils.PrimeroDeMes(hoy_z)
    self.wTree.get_widget("edt_fecini").set_text(primerodemes_z.strftime('%d/%m/%Y'))
    ultimodemes_z = utils.UltimoDeMes(primerodemes_z)
    self.wTree.get_widget("edt_fecfin").set_text(ultimodemes_z.strftime('%d/%m/%Y'))
    
  def on_btn_aceptar_clicked(self, widget):
      self.alm_z = self.edt_almacen.get_text().upper()
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
         
      sql_z = "select a.alm, b.recemi, c.linea, "
      if self.vtamen_z == "S":
         sql_z = sql_z + "b.folent, "
      sql_z = sql_z + "b.codinv, c.descri, sum(b.unids * d.factor), "
      sql_z = sql_z + "sum(b.costou*(b.piva/100+1)*d.factor) "
      sql_z = sql_z + "from inv_tmpvtatmp d "
      sql_z = sql_z + "join entradas a on d.tiposal = a.tipo "
      sql_z = sql_z + "join renentra b on a.tipo = b.tipo "
      sql_z = sql_z + "and a.numero = b.numero and a.alm = b.alm and a.cia = b.cia "
      sql_z = sql_z + "join inven c on b.codinv = c.codigo and b.cia = c.cia "
      sql_z = sql_z + "where a.fecha between "
      sql_z = sql_z + "'" + self.fecini_z.strftime('%Y/%m/%d') + "' and "
      sql_z = sql_z + "'" + self.fecfin_z.strftime('%Y/%m/%d') + "' and "
      sql_z = sql_z + " a.alm = '" + self.alm_z + "' and "
      sql_z = sql_z + " a.cia = " + repr(cia_z)
      sql_z = sql_z + where_z
      sql_z = sql_z + " group by a.alm, b.recemi, c.linea, "
      if self.vtamen_z == "S":
         sql_z = sql_z + "b.folent, "
      sql_z = sql_z + " b.codinv, c.descri"
      print sql_z

      self.pag_z = 1
      self.antlin_z = "-1"
      self.linea_z = ""
      self.antcrd_z = -1
      self.antptovta_z = "-1"
      band_z = ""
      self.arch_z = open("repcvta.tex", "w")
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
        ptovta_z = record[ii_z]
        ii_z = ii_z + 1
        linea_z = record[ii_z]
        ii_z = ii_z + 1
        if self.vtamen_z == "S":
          crdcon_z = record[ii_z]
          ii_z = ii_z + 1
        codigo_z = record[ii_z]
        ii_z = ii_z + 1
        descri_z = record[ii_z]
        ii_z = ii_z + 1
        canti_z = record[ii_z]
        ii_z = ii_z + 1
        costo_z = record[ii_z]
        costou_z = 0
        if canti_z <> 0:
           costou_z = costo_z / canti_z
        if band_z <> "S":
           self.antlin_z = linea_z
           self.antcrd_z = crdcon_z
           self.antptovta_z = ptovta_z
           band_z = "S"
           self.encab()
        else:
           if self.antptovta_z <> ptovta_z:
              if self.vtamen_z == "S":
                self.sub_credcon()
                
              self.sub_linea()
              self.sub_ptovta()
              self.arch_z.write("\n")
              self.lineas_z = self.lineas_z + 1
              self.antptovta_z = ptovta_z
              self.antlin_z = linea_z
              self.antcrd_z = crdcon_z
              self.subenc0()
           if self.antlin_z <> linea_z:
              if self.vtamen_z == "S":
                 self.sub_credcon()
              self.sub_linea()
              self.arch_z.write("\n")
              self.lineas_z = self.lineas_z + 1
              self.antlin_z = linea_z
              self.antcrd_z = crdcon_z
              self.subenc1()
           if self.vtamen_z == "S":
              if self.antcrd_z <> crdcon_z:
                 self.sub_credcon()
                 self.arch_z.write("\n")
                 self.lineas_z = self.lineas_z + 1
                 self.antcrd_z = crdcon_z
                 self.subenc2()
              
        if self.vtamen_z == "S":
           self.impcosxcrd_z = self.impcosxcrd_z + costo_z
        else:
           self.impcosxlin_z = self.impcosxlin_z + costo_z
        if self.lineas_z > utils.LINEAS_X_PAG:
           self.salto_pag()
           self.encab()
           
        if ren_z == numrows:
           self.arch_z.write(self.subrayado_on)
        self.arch_z.write(codigo_z.ljust(13)+"|")
        self.arch_z.write(descri_z.ljust(30)+"|")
        self.arch_z.write(('%5.0f' % canti_z).rjust(5)+"|")
        self.arch_z.write(utils.currency(costou_z).rjust(12)+"|")
        self.arch_z.write(utils.currency(costo_z).rjust(12)+"|")
        if ren_z == numrows:
           self.arch_z.write(self.subrayado_off)
        self.arch_z.write("\n")
        self.lineas_z = self.lineas_z + 1
      
      if self.vtamen_z == "S":
         self.sub_credcon()
      self.sub_linea()
      self.sub_ptovta()
      total_z = self.impcostot_z
      self.arch_z.write("Total General".ljust(63))
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.arch_z.close()

  def salto_pag(self):
      self.arch_z.write(def_tablas.font(mydb, 1, "FORM-FEED FF"))
      self.pag_z = self.pag_z + 1
      

  def encab(self):
      self.arch_z.write(cias['razon'].center(80) + "\n")
      self.lineas_z = 1
      self.negritas_on = def_tablas.font(mydb, 1, "EMPHAIZED ON")
      self.negritas_off = def_tablas.font(mydb, 1, "EMPHAIZED OFF")
      self.condensado_on = def_tablas.font(mydb, 1, "CONDENSADO_ON")
      self.condensado_off = def_tablas.font(mydb, 1, "CONDENSADO_OFF")
      self.subrayado_on = def_tablas.font(mydb, 1, "SUBRAYADO ON")
      self.subrayado_off = def_tablas.font(mydb, 1, "SUBRAYADO OFF")
      nombrealm_z = def_tablas.busca_nombre(mydb, self.alm_z, cia_z, def_tablas.ALMACEN)
      hora_z = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
      self.lineas_z = self.lineas_z + 1
      self.arch_z.write(self.condensado_on + "repcvta " + self.condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      self.arch_z.write(("Impresion de Reporte de Costo de Ventas Pag:" + '%d' % self.pag_z).center(80) + "\n")
      self.lineas_z = self.lineas_z + 1
      self.arch_z.write(self.negritas_on)
      self.arch_z.write(("De:" + self.alm_z + " " + nombrealm_z + " Del "+ self.fecini_z.strftime('%d/%m/%Y') + " Al " + self.fecfin_z.strftime('%d/%m/%Y') ).center(80))
      self.arch_z.write(self.negritas_off + "\n")
      self.lineas_z = self.lineas_z + 1
      self.arch_z.write(self.negritas_on + self.titmercan_z + self.negritas_off + "\n")
      self.lineas_z = self.lineas_z + 1
      self.arch_z.write(self.negritas_off + self.titvtabru_z + " " + self.titstatus_z + self.negritas_off + "\n")
      self.lineas_z = self.lineas_z + 1
      self.arch_z.write(self.condensado_on)
      self.arch_z.write(self.subrayado_on)
      self.arch_z.write("Codigo".ljust(13)+"|")
      self.arch_z.write("Descripcion".ljust(30)+"|")
      self.arch_z.write("Unids".rjust(5)+"|")
      self.arch_z.write("Costo Unit".rjust(12)+"|")
      self.arch_z.write("Costo Total".rjust(12))
      self.arch_z.write(self.subrayado_off)
      self.arch_z.write("\n")
      self.lineas_z = self.lineas_z + 1
      self.subenc0()

  def subenc0(self):
      self.arch_z.write("Punto de Venta:")
      nomptovt_z = def_tablas.busca_nombre(mydb, self.antptovta_z, cia_z, PTOVTA)
      self.arch_z.write(self.antptovta_z + " " + nomptovt_z + "\n")
      self.lineas_z = self.lineas_z + 1
      self.subenc1()

  def subenc1(self):
      self.arch_z.write("Linea:")
      nomlinea_z = def_tablas.busca_nombre(mydb, self.antlin_z, cia_z, LINEA)
      self.arch_z.write(self.antlin_z + " " + nomlinea_z + "\n")
      self.lineas_z = self.lineas_z + 1
      if self.vtamen_z == "S":
         self.subenc2()

  def subenc2(self):
      nomcredcon_z = def_tablas.busca_dato(mydb, self.antcrd_z, CREDCON)
      self.arch_z.write(nomcredcon_z + "\n")
      self.lineas_z = self.lineas_z + 1

  def sub_credcon(self):
      self.arch_z.write("Subtotal Credito/Contado:".ljust(63))
      self.impcosxlin_z = self.impcosxlin_z + self.impcosxcrd_z 
      total_z = self.impcosxcrd_z 
      self.impcosxcrd_z=0
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.lineas_z = self.lineas_z + 1

  def sub_linea(self):
      self.arch_z.write("Subtotal esta Linea".ljust(63))
      self.impcosxptv_z = self.impcosxptv_z + self.impcosxlin_z 
      total_z = self.impcosxlin_z 
      self.impcosxlin_z=0
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.lineas_z = self.lineas_z + 1

  def sub_ptovta(self):
      self.arch_z.write("Subtotal Punto de Venta".ljust(63))
      self.impcostot_z = self.impcostot_z + self.impcosxptv_z 
      total_z = self.impcosxptv_z 
      self.impcosxptv_z=0
      self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      self.arch_z.write(self.subrayado_off + "\n")
      self.lineas_z = self.lineas_z + 1

  def on_btn_cancel_clicked(self, widget):
      print "Presionaste Cancelar"
      gtk.main_quit()

if __name__ == "__main__":
   hwg = analisma()
   gtk.main()

def main():

    gtk.main()
    return 0
