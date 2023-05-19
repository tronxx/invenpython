#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Acumulado de ventas x Poblaci�n
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
import datetime

global mydb
global cia_z
global mibd
global cias
global inven
global exist
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

class analisma:
  """Esta es una aplicaci�n Alta Almacenes"""
       
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
    self.wTree.get_widget("win_dialog").connect("destroy", gtk.main_quit )
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
    cia_z = utils.StrToInt(cias_lines[0])

    dsn_z = "dsn="+mibd['base']+";uid="+mibd['user']+";pwd="+mibd['password']
    if mibd['tipobd'] == "MYSQL":
       mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])
    elif mibd['tipobd'] == "ODBC":
       mydb = pyodbc.connect(dsn_z)
    cias = def_tablas.busca_cia(mydb, cia_z)

    miwin = self.wTree.get_widget("win_dialog")
    mitable = self.wTree.get_widget("table1")
    self.lbl_tdaini = gtk.Label("Codigo Inicial")
    mitable.attach(self.lbl_tdaini, 0, 1, 2, 3)
    self.lbl_tdaini.show()
    self.edt_tdaini = gtk.Entry();
    mitable.attach(self.edt_tdaini, 1, 2, 2, 3)
    self.edt_tdaini.show()

    self.lbl_tdafin = gtk.Label("Codigo Final");
    mitable.attach(self.lbl_tdafin, 0, 1, 3, 4)
    self.lbl_tdafin.show()
    self.edt_tdafin = gtk.Entry();
    mitable.attach(self.edt_tdafin, 1, 2, 3, 4)
    self.edt_tdafin.show()

    miwin.set_title(cias['razon'] + " Acumulado de Poblaciones")
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
 
      self.where_z = where_z
      sql_z = "select a.codigo, a.descri, a.precio, a.piva, a.empaqe, a.cod2, a.linea";
      sql_z = sql_z + " from inven a ";
      sql_z = sql_z + " where a.empaqe <> 'DESCONT' and a.empaqe <> 'REMATE' ";
      sql_z = sql_z + " and a.cia = " + repr(cia_z);
      sql_z = sql_z + " and a.existes + a.existen > 0";
      sql_z = sql_z + " order by a.linea, a.cod2, a.codigo";
      print sql_z;
      colcodigo_z = 0;
      coldescri_z = 1;
      colprecio_z = 2;
      coldpiva_z  = 3;
      colsituac_z = 4;
      colgrupo_z  = 5;
      collinea_z  = 6;

      self.pag_z = 1
      self.antlin_z = "-1"
      self.linea_z = ""
      self.antcrd_z = -1
      self.antptovta_z = "-1"
      band_z = ""
      self.arch_z = open("catinv.json", "w")
      self.arch_z.write("[\n");
      self.antlinea_z = ""
      self.ptvta_z = ""
      self.mienc_z = 2
      self.lineaspag_z = 0;
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
      comillas_z = "\"";
      for record in result:
        ren_z = ren_z + 1;
        linea_z  = record[collinea_z];
        codigo_z = record[colcodigo_z];
        descri_z = record[coldescri_z];
        situac_z = record[colsituac_z];
        grupo_z  = record[colgrupo_z];
        precio_z  = record[colprecio_z];
        pdsc_z = self.busca_descto(linea_z);
        precstr_z  = "%0.2f" % ( precio_z * (1 - pdsc_z / 100) );
        marca_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_MARCAS)
        descrilar_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_DESCRILAR)
        descri_z = descri_z.replace("\"", " Pulg");
        descrilar_z = descrilar_z.replace("\"", " Pulg");
        descricomp_z = self.busca_caracteristicas(codigo_z, linea_z);
        numerofotos_z = self.busca_numero_de_fotos(codigo_z, linea_z);
        miexistencia_z = self.busca_existencias(codigo_z);
        
        if ren_z > 1:
        	self.arch_z.write(",\n");
        #End if

        self.arch_z.write("{ ");
        self.arch_z.write(comillas_z + "linea" + comillas_z + ":" + comillas_z + linea_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "grupo" + comillas_z + ":" + comillas_z + grupo_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "marca" + comillas_z + ":" + comillas_z + marca_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "dcorta" + comillas_z + ":" + comillas_z + descri_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "dlarga" + comillas_z + ":" + comillas_z + descrilar_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "dcomp" + comillas_z + ":" + comillas_z + descricomp_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "codigo" + comillas_z + ":" + comillas_z + codigo_z + comillas_z + ",");
        self.arch_z.write(comillas_z + "precio" + comillas_z + ":" + precstr_z + ",");
        self.arch_z.write(comillas_z + "existe" + comillas_z + ":" + miexistencia_z + ",");
        self.arch_z.write(comillas_z + "imagen" + comillas_z + ":" + str(numerofotos_z) );
        self.arch_z.write("}");
        self.lineaspag_z = self.lineaspag_z + 1

      
      #if self.vtamen_z == "S":
      #   self.sub_credcon()
      #self.sub_linea()
      #self.sub_ptovta()
      #total_z = self.impcostot_z
      #self.arch_z.write("Total General".ljust(59))
      #self.arch_z.write(self.subrayado_on + "|" + utils.currency(total_z).rjust(12) + "|")
      #self.arch_z.write(self.subrayado_off + "\n\n")
      #self.lineaspag_z = self.lineaspag_z + 2
      self.arch_z.write("\n]\n");
      self.mienc_z = 2
      self.arch_z.close()
      gtk.main_quit()

  def salto_pag(self):
      self.arch_z.write(def_tablas.font(mydb, 1, "FORM-FEED FF"))
      self.pag_z = self.pag_z + 1
      self.encab()


  def busca_caracteristicas(self, codigo_z, linea_z):
  	  pathlin_z = "html" + os.sep + linea_z;
  	  miscarac_z = "";
  	  nomarchcar_z = pathlin_z + os.sep + codigo_z + "_car.txt"
  	  if os.path.isfile(nomarchcar_z):
           farchcar_z = open(nomarchcar_z)
           for lineatext_z in farchcar_z.readlines():
           	   if miscarac_z <> "":
           	   	  miscarac_z = miscarac_z + "\\n"
           	   #End if 
           	   lineatext_z = lineatext_z.replace("\"", " Pulg")
           	   miscarac_z = miscarac_z + lineatext_z.strip("\n\r")
           #End for
           farchcar_z.close()
      #End if
  	  return (miscarac_z);

  def busca_numero_de_fotos(self, codigo_z, linea_z):
  	  pathlin_z = "html" + os.sep + "fotos" + os.sep + linea_z;
  	  numerofotos_z = 0;
  	  ii_z = 0;
  	  for ii_z in range (1,10):
  	     nomarchfoto_z = pathlin_z + os.sep + codigo_z + "_" + str(ii_z) + ".jpg"
  	     if os.path.isfile(nomarchfoto_z):
  	     	  numerofotos_z = numerofotos_z + 1;
         #End if
      #end for
  	  return (numerofotos_z);

  def busca_existencias(self, codigo_z):
  	  sql_z = "select alm, (existes + existen) as existencia from exist where codigo = '" + codigo_z + "' and existes + existen > 0 and cia = " + str(cia_z)
  	  numerofotos_z = 0;
  	  ii_z = 0;
  	  colalm_z = 0;
  	  colexist_z = 1;
  	  comillas_z = "\""
  	  cursor = mydb.cursor()
  	  cursor.execute(sql_z)
  	  result = cursor.fetchall()
  	  misexistencias_z = "[ {"
  	  for record in result:
  	  	alm_z = record[colalm_z]
  	  	exist_z = record[colexist_z]
  	  	if ii_z <> 0:
  	  		misexistencias_z = misexistencias_z + ","
  	  	#End if
  	  	ii_z = ii_z + 1
  	  	strexi_z = "%0.0f" % exist_z;
  	  	misexistencias_z = misexistencias_z + comillas_z + alm_z + comillas_z + ":"
  	  	misexistencias_z = misexistencias_z + strexi_z
  	  #End for
  	  misexistencias_z = misexistencias_z + "} ]";
  	  return (misexistencias_z);

  def busca_descto(self, linea_z):
  	  sql_z = "select b.obser from obslin b where b.linea = '" + linea_z + "' and obser like '%CONTADO%' and moe = 'M' and cia = " + str(cia_z)
  	  pdsc_z = 0;
  	  colobser_z = 0;
  	  cursor = mydb.cursor()
  	  cursor.execute(sql_z)
  	  result = cursor.fetchall()
  	  for record in result:
  	  	observ_z = record[colobser_z]
  	  #End for
  	  posini_z = observ_z.find("%")
  	  strtasa_z = observ_z[posini_z-2:posini_z]
  	  #print linea_z, " Tasa ", strtasa_z, " Posini:", posini_z, " Obser", observ_z, " A:", observ_z[posini_z-2:posini_z]
  	  pdsc_z = utils.ValFloat(strtasa_z)
  	  return (pdsc_z);


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
      self.arch_z.write(self.condensado_on + "catinvjson " + self.condensado_off + (hora_z + " " + cias['dir']).center(70) + "\n")
      self.arch_z.write(("Catalogo de Inven en Json Pag:" + '%d' % self.pag_z).center(80) + "\n")
      self.lineaspag_z = self.lineaspag_z + 1
#      self.arch_z.write(self.negritas_on)
#      self.arch_z.write(("De:" + self.alm_z + " " + nombrealm_z + " Del "+ self.fecini_z.strftime('%d/%m/%Y') + " Al " + self.fecfin_z.strftime('%d/%m/%Y') ).center(80))
#      self.arch_z.write(self.negritas_off + "\n")
#      self.lineaspag_z = self.lineaspag_z + 1
      self.arch_z.write(self.negritas_on + self.titmercan_z + self.negritas_off + "\n")

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
