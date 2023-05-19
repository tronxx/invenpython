#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import string, os
import json
try:
  import pygtk
  pygtk.require('2.0')
except:
  pass
try:
  import gtk
  import gtk.glade
except:
  print ("No tengo libreria gtk.glade");
  sys.exit(1)
import def_tablas
import utils
import datetime
import math

global mydb
global cia_z
global mibd
global cias
global almacen
global inven
global invulpre
global mimodo_z
platform = sys.platform 
#-- Define additional constants

EXIT            = 0
CONTINUE        = 1
NUEVO           = 1
MODIFICA        = 2
BORRAR          = 3
TAB_KARDEX      = 0
TAB_ESTADIS     = 1
TAB_EXIST       = 2
TAB_OBSERVS     = 3
TAB_DISPONIBLES = 4
TAB_BUSCASERIE  = 5

modo_z       = 0

CONCEPTOS    = def_tablas.CONCEPTOS

mibd = def_tablas.lee_basedato_ini()
cias = def_tablas.define_cias()
almacen = def_tablas.define_almacen()
inven = def_tablas.define_inven()
invulpre = def_tablas.define_invulpre()
dirprogs_z = ".." + os.sep + "altaalm" + os.sep
tipoagru_z = [ "GRUPO", "MARCA", "PROVEEDOR", "SITUACION", "CODIGO", "DIARY", "LINEA"]
tipoest_z = [ "SALIDAS ESPECIALES", "SALIDAS X VENTA", "ENTRADAS X CANCEL", \
             "ENTRADAS ESPECIALES", "SALIDAS MAYOREO", "ENTRADAS X COMPRA" ]
archsinfoto_z = []

if mibd['tipobd'] == "MYSQL":
   try:
     import MySQLdb
   except:
     sys.exit(1)
elif mibd['tipobd'] == "ODBC":
   try:
     import pyodbc
   except:
     print ("No puedo importar pyodbc");
     sys.exit(1)

class Altainv:
  """Esta es una aplicaci?n Alta Inventario"""
       
  def __init__(self):
       
    #Establecemos el archivo Glade
    
    self.gladefile = dirprogs_z + "altainv.glade"
    self.wTree = gtk.glade.XML(self.gladefile)
    dic = { "on_btn_primero_clicked": self.on_btn_primero_clicked, \
            "on_btn_sigte_clicked": self.on_btn_sigte_clicked, \
            "on_btn_anter_clicked": self.on_btn_anter_clicked, \
            "on_btn_ultimo_clicked": self.on_btn_ultimo_clicked, \
            "on_btn_nuevo_clicked": self.on_btn_nuevo_clicked, \
            "on_btn_modif_clicked": self.on_btn_modif_clicked, \
            "on_btn_borra_clicked": self.on_btn_borra_clicked, \
            "on_edt_codigo_activate": self.on_edt_codigo_activate, \
            "on_edt_almkdx_activate": self.on_edt_almkdx_activate, \
            "on_btn_okestadis_clicked": self.on_btn_okestadis_clicked, \
            "on_btn_okexist_clicked": self.on_btn_okexist_clicked, \
            "on_edt_agrupapor_activate": self.on_edt_agrupapor_activate, \
            "on_edt_tipoest_activate": self.on_edt_tipoest_activate, \
            "on_edt_exipor_activate": self.on_edt_exipor_activate, \
            "on_btn_buscaserie_clicked": self.on_btn_buscaserie_clicked, \
            "on_btn_catalogo_clicked": self.on_btn_catalogo_clicked, \
            #"on_btn_aceptar_clicked": self.on_btn_aceptar_clicked, \
            #"on_btn_cancelar_clicked": self.on_btn_cancelar_clicked
            }
    self.wTree.get_widget("edt_descri").connect("activate", self.catalogo_html)
            
    #                "on_win_altaalm_destroy": gtk.main_quit }
    campos_numericos_z = ["edt_costosi", "edt_costono", "edt_preciomds", \
    "edt_preciofide", "edt_min", "edt_max", "edt_piva", "edt_preciomay", \
    "edt_preciomayneto", "edt_mubmay", "edt_inicials", "edt_inicialn", \
    "edt_entcoms", "edt_entcomn", "edt_entcans", "edt_entesps", "edt_entespn", \
    "edt_totents", "edt_totentn", "edt_salvtas", "edt_salvtan", "edt_salfons", \
    "edt_salfonn", "edt_salesps", "edt_salespn", "edt_salmays", "edt_salmayn", \
    "edt_existes", "edt_existen"]
    for campo_z in campos_numericos_z:
      self.wTree.get_widget(campo_z).set_property('xalign', 1)

    self.wTree.signal_autoconnect(dic)
    global cias
    global almacen
    global cia_z
    global mydb
    self.inianu_z = utils.StrToDate("01/01/"+datetime.date.today().strftime('%Y'))
    self.hoy_z = datetime.date.today()
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

    miwin = self.wTree.get_widget("win_altainv")
    miwin.set_title(cias['razon'] + " Mantenimiento de Inventario")
    self.define_tabla_exist()
    self.define_tab_estadis()
    self.editable_onoff(False)
    self.define_tab_kardex()
    self.define_tab_observs()
    self.define_tab_disponibles()
    self.define_tab_busqserie()
    grd_kardex = self.wTree.get_widget("grd_kardex")
    grd_kardex.connect("row_activated", self.on_grd_kardex_activate)
    grd_exists = self.wTree.get_widget("grd_exists")
    grd_exists.connect("row_activated", self.on_grd_exists_activate)
    notebook=self.wTree.get_widget("notebook_principal")
    notebook.connect("switch_page", self.on_cambio_pagina_notebook)
    if mimodo_z == "AUTO":
      self.catalogo_html(self)
      sys.exit(1)
    #End IF
    if mimodo_z == "JSON":
      self.genera_archivo_JSON(self)
      sys.exit(1)
    #End IF
    if mimodo_z == "DESCRIS":
      self.genera_JSON_descripciones(self)
      sys.exit(1)
    #End IF
    if mimodo_z == "GRUPOS":
      self.genera_JSON_grupos(self)
      sys.exit(1)
    #End IF
    if mimodo_z == "LINEAS":
      self.genera_JSON_lineas(self)
      sys.exit(1)
    #End IF
    if mimodo_z == "OFERTAS":
      self.genera_JSON_ofertas(self)
      sys.exit(1)
    #End IF
       
    
  def define_tab_kardex(self):
    global cia_z
    grd_kardex = self.wTree.get_widget("grd_kardex")
    self.lst_kardex = gtk.ListStore(str, str, int, str, str, str, int, str, str, str, str, str, str)
    grd_kardex.set_model(self.lst_kardex)
    columns_z = ["Fecha", "E", "Entrada", "Viene de", "Fol.Viene", "Proveedor", "Folio", "Serie", "S", "F.Salida", "Recibe", "Fol.Rec", "Sale Para"]
    ii_z = 0
    for midato_z in columns_z:
      col = gtk.TreeViewColumn(midato_z)
      col.set_resizable(True)
      grd_kardex.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1

    #grd_kardex.connect("cursor-changed", self.ren_seleccionado)
    if platform in utils.grd_lines_soported:  
       grd_kardex.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
# --- Fin de define_tab_kardex(self) ------    

  def genera_archivo_JSON(self, widget):
      imprime_sin_exis_z = "NO"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"
      archimg_z = "";
      mifecha_z = datetime.date.today()
      strhoy_z = mifecha_z.strftime('%Y-%m-%d')


      sql_z = "select linea, b.codigo, b.descri, a.codigo, a.descri, precio, a.empaqe, "
      sql_z = sql_z + " cast(a.existes+a.existen as integer) as exist"
      sql_z = sql_z + " from inven a join inv_invhist c on a.codigo = c.codigo and a.cia = c.cia"
      sql_z = sql_z + " join inv_relinv d on c.idart = d.idart and d.idrel = " + str(def_tablas.REL_INVEN_GRUPOS_INTERNET)
      sql_z = sql_z + " join inv_gruposinternet b on d.iddato = b.idgrupo "
      if imprime_sin_exis_z == "NO" :
         sql_z = sql_z + " join movart e on e.codigo = a.codigo and e.cia = a.cia "
         sql_z = sql_z + " and almac not in ('BO', 'AG', 'SE') "
      #endif
      sql_z = sql_z + " where a.empaqe <> 'REMATE' " + " and a.cia = " + str(cia_z)
      sql_z = sql_z + " and a.empaqe <> 'PUBLICITAR'  and a.precio > 1 "
      sql_z = sql_z + " and ( a.existes+a.existen > 2)  "
      if imprime_sin_exis_z == "NO" :
         sql_z  = sql_z  + " and e.salio <> 'S'"
      #Fin If
      sql_z = sql_z + " group by linea, b.codigo, b.descri, a.codigo, a.descri, precio, a.empaqe, exist"
      print sql_z;
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      artsinfoto_z = []
      artconfoto_z = []
      ren_z = 0
      antcod_z = "-1"
      sigcod_z = ""
      antlinea_z = "-1"
      micatjson = [];
      archjson_z = "catalogo.json";
      #findice_z = open(archjson_z, "w")
      #findice_z.write("[\n");
      for record in result:
          ren_z = ren_z + 1
          linea_z = record[0]
          grupo_z = record[1]
          codigo_z = record[3]
          descri_z = record[4]
          precio_z = record[5]
          empaqe_z = record[6]
          exist_z  = record[7]
          
          siimprimir_z = "SI"
          sqlexist_z = "select count(*) as exist from movart where codigo = '"+codigo_z+"' and salio <> 'S' and cia=" + str(cia_z);
          sqlexist_z = sqlexist_z + " and almac not in ('BO', 'AG', 'SE') "



          if imprime_unicos_z == "NO" and ( empaqe_z.strip() == unico_z.strip() or empaqe_z.strip() == descontinuado_z.strip() ):
             cursor2 = mydb.cursor()
             cursor2.execute(sqlexist_z)
             result2_z = cursor2.fetchall()
             for record2 in result2_z:
                 exist_z = record2[0]

             if exist_z == 0 :
                siimprimir_z = "NO"
             #end if
          #end if
          if  siimprimir_z == "SI" :
            foto_z = "mdsapps.ddns.net/catalogo/html/fotos/" + linea_z + "/" + codigo_z + ".jpg";
            #descri_z = utils.elimina_car_esp(descri_z)
            #if ren_z > 1 : 
            #   findice_z.write(",\n");
            #

            if linea_z != antlinea_z:
               sqlobs_z = "select obser from obslin where linea = '" + linea_z + "' and obser like '%VENTAS%CONTADO%'"
               cursor3 = mydb.cursor()
               cursor3.execute(sqlobs_z)
               result3_z = cursor3.fetchall()
               miobscont_z = "0%"
               strdesc_z = "0"
               desctolin_z = 0
               for record3 in result3_z:
                   miobscont_z = record3[0]
               #End for
               inicia_z = miobscont_z.find("%")
               strdesc_z = miobscont_z[inicia_z - 2 : inicia_z]
               print "Linea:", linea_z, " Strdesc:", strdesc_z, " miobscont:", miobscont_z
               desctolin_z = utils.ValFloat(strdesc_z);
               antlinea_z = linea_z
            #End if
            enganche_z = precio_z /10;

            if desctolin_z > 0 :
                precio_z = precio_z * ( 1 - desctolin_z / 100 )
                precio_z = precio_z / 100;
                precio_z = math.ceil(precio_z) * 100
            #Fin de If

            ## Voy a Buscar las Ofertas Vigentes:
            ESTADO_CERRADO = 2
            sql_z = "";
            sql_z = sql_z + " select a.fecini, a.fecfin, b.precmds from inv_polofertas a "
            sql_z = sql_z + " join inv_renpolofertas b on a.idpolcampre = b.idpolcampre " 
            sql_z = sql_z + " join inv_invhist c on b.idart = c.idart " 
            sql_z = sql_z + " where a.tipo = 'O' and a.status = " + str(ESTADO_CERRADO)
            sql_z = sql_z + " and '" + strhoy_z + "' between  a.fecini and fecfin"
            sql_z = sql_z + " and a.cia = " + str(cia_z)
            sql_z = sql_z + " and c.codigo = '" + codigo_z + "'"
            sql_z = sql_z + " order by a.folio desc, b.idrenpolcampre"
            print sql_z;
            cursor = mydb.cursor()
            cursor.execute(sql_z)
            result4_z = cursor.fetchall()
            proferta_z = 0;
            fecini_z = "";
            fecfin_z = "";
            for record4 in result4_z:
                   fecini_z   = record4[0].strftime('%Y-%m-%d')
                   fecfin_z   = record4[1].strftime('%Y-%m-%d')
                   proferta_z = record4[2]
            #End for
            plazomax_z = self.busca_plazomax(codigo_z, precio_z);
            letras_z = 0;
            if(plazomax_z):
               letras_z = precio_z / plazomax_z;
            #End if
            esoferta_z = "N";
            if (proferta_z != 0):
               esoferta_z = "S";
            #End if

            miren_z = {
               "linea": linea_z,
               "grupo": grupo_z,
               "codigo": codigo_z,
               "descri": descri_z,
               "foto": foto_z,
               "existencia": str(exist_z),
               "precio": ("%.2f" % precio_z),
               "enganche": ("%.2f" % enganche_z),
               "numpagos": plazomax_z,
               "letra": ("%.2f" % letras_z),
               "oferta": esoferta_z,
               "preciooferta": ("%.2f" % proferta_z),
               "inioferta": fecini_z,
               "finoferta": fecfin_z
            };
            micatjson.append(miren_z);

            #findice_z.write("{");
            #findice_z.write('"linea":"' + linea_z + '",');
            #findice_z.write('"grupo":"' + grupo_z + '",');
            #findice_z.write('"codigo":"' + codigo_z + '",');
            #findice_z.write('"descri":"' + descri_z + '",');
            #findice_z.write('"foto":"' + foto_z + '",');
            #findice_z.write('"existencia":' +  str(exist_z) + ',');
            #findice_z.write('"precio":' +  ("%.2f" % precio_z) + ',');
            #findice_z.write('"preciooferta":' +  ("%.2f" % proferta_z) + ',');
            #findice_z.write('"inioferta":"' +  fecini_z  + '",');
            #findice_z.write('"finoferta":"' +  fecfin_z  + '"');
            #findice_z.write('}');
            ren_z = ren_z + 1
          ##End if
      #End For
      #findice_z.write("\n]\n");
      #findice_z.close();
      with open(archjson_z, "w") as outfile:
         json.dump(micatjson, outfile, indent=4)

      self.genera_JSON_descripciones(self)
      self.genera_JSON_grupos(self)
      self.genera_JSON_ofertas(self)

##-- Fin de Funcion genera JSON

  def genera_JSON_descripciones(self, widget):
      imprime_sin_exis_z = "NO"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"
      archimg_z = "";

      sql_z = "select a.codigo, a.descri from inven a "
      sql_z = sql_z + " where a.empaqe <> 'REMATE' " + " and a.cia = " + str(cia_z)
      sql_z = sql_z + " order by a.codigo"
      print sql_z;
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      ren_z = 0
      antcod_z = "-1"
      sigcod_z = ""
      antlinea_z = "-1"
      archjson_z = "titulos.json";
      #findice_z = open(archjson_z, "w")
      #findice_z.write("[\n");
      catalogodescri_z = []
      nartic_z = 1;
      for record in result:
          ren_z = ren_z + 1
          codigo_z = record[0]
          descri_z = record[1]
          titulo_z = ""
          descripciones_z = []
          cursor2 = mydb.cursor()
          sqldescri_z = "select tipo, observs from observent where codigo = '" + codigo_z + "'"
          sqldescri_z = sqldescri_z + "and alm = '' and (tipo = 'T' or tipo = 'D') order by tipo, conse"
          cursor2.execute(sqldescri_z)
          result2_z = cursor2.fetchall()
          for record2 in result2_z:
                 tipo_z = record2[0]
                 obs_z = record2[1]
                 #obs_z = utils.elimina_car_esp(obs_z)
                 if tipo_z == "T":
                    titulo_z = obs_z
                 else:
                    descripciones_z.append(obs_z)
                 ##end if
          ##End For
          #if nartic_z > 1 : 
          #          findice_z.write(",\n");
          #End if
          miren_z = {
            "codigo": codigo_z,
            "titulo": titulo_z,
            "descripcion": descripciones_z
          }
          catalogodescri_z.append(miren_z);
          #findice_z.write("{");
          #findice_z.write('"codigo":"' + codigo_z + '",');
          #findice_z.write('"titulo":"' + titulo_z + '",');
          #findice_z.write('"descripcion":[');
          #ndescri_z = 1;
          #for midescrilin_z in descripciones_z:
          #    if ndescri_z > 1 : 
          #          findice_z.write(",\n");
          #    #End if

          #    findice_z.write('"' + midescrilin_z + '"');
          #    ndescri_z = ndescri_z + 1
          #End For
          #findice_z.write(']');
          #findice_z.write('}');
          nartic_z = nartic_z + 1
      #End For
      #findice_z.write("\n]\n");
      #findice_z.close();
      with open(archjson_z, "w") as outfile:
         json.dump(catalogodescri_z, outfile, indent=4)


  def genera_JSON_grupos(self, widget):
      imprime_sin_exis_z = "NO"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"
      archimg_z = "";

      sql_z = "select a.codigo, a.descri from inv_gruposinternet a "
      sql_z = sql_z + " where  a.cia = " + str(cia_z)
      sql_z = sql_z + " order by a.codigo"
      print sql_z;
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      ren_z = 0
      antcod_z = "-1"
      sigcod_z = ""
      antlinea_z = "-1"
      archjson_z = "grupos.json";
      #findice_z = open(archjson_z, "w")
      #findice_z.write("[\n");
      micatjson = []
      nartic_z = 1;
      for record in result:
          ren_z = ren_z + 1
          codigo_z = record[0]
          descri_z = record[1]
          miren_z = {
            "codigo": codigo_z,
            "descri": descri_z
          }
          micatjson.append(miren_z);
       #   descri_z = utils.elimina_car_esp(descri_z)
      #    if nartic_z > 1 : 
      #              findice_z.write(",\n");
          #End if
      #    findice_z.write("{");
      #    findice_z.write('"codigo":"' + codigo_z + '",');
      #    findice_z.write('"dscri":"' + descri_z + '"');
      #    findice_z.write('}');
      #    nartic_z = nartic_z + 1
      #End For
      #findice_z.write("\n]\n");
      #findice_z.close();
      with open(archjson_z, "w") as outfile:
         json.dump(micatjson, outfile, indent=4)
   #End def_genera_grupos

  def genera_JSON_ofertas(self, widget):
      imprime_sin_exis_z = "NO"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"
      archimg_z = "";
      ESTADO_CERRADO = 2;
      mifecha_z = datetime.date.today()
      strhoy_z = mifecha_z.strftime('%Y-%m-%d')
      sql_z = "";
      sql_z = sql_z + " select f.codigo, f.linea, e.codigo as grupo, a.fecini, a.fecfin, b.precmds from inv_polofertas a "
      sql_z = sql_z + " join inv_renpolofertas b on a.idpolcampre = b.idpolcampre " 
      sql_z = sql_z + " join inv_invhist c on b.idart = c.idart " 
      sql_z = sql_z + " join inven f on c.codigo = f.codigo " 
      sql_z = sql_z + " join inv_relinv d on c.idart = d.idart and d.idrel = " + str(def_tablas.REL_INVEN_GRUPOS_INTERNET)
      sql_z = sql_z + " join inv_gruposinternet e on d.iddato = e.idgrupo "
      sql_z = sql_z + " where a.tipo = 'O' and a.status = " + str(ESTADO_CERRADO)
      sql_z = sql_z + " and '" + strhoy_z + "' between  a.fecini and fecfin"
      sql_z = sql_z + " and a.cia = " + str(cia_z)
      sql_z = sql_z + " order by f.codigo.e.codigo, folio desc, b.idrenpolcampre"

      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      ren_z = 0
      codigo_z = "";
      linea_z = "";
      grupo_z = "";
      fecini_z = "";
      fecfin_z = "";
      proferta_z = 0;
      archjson_z = "ofertas.json";
      #findice_z = open(archjson_z, "w")
      #findice_z.write("[\n");
      micatjson = []
      nartic_z = 1;
      for record in result:
          ren_z = ren_z + 1;
          codigo_z = record[0];
          linea_z = record[1];
          grupo_z = record[2];
          fecini_z = record[3].strftime('%Y-%m-%d');
          fecfin_z = record[4].strftime('%Y-%m-%d');
          proferta_z = record[5];
          miren_z = {
            "codigo": codigo_z,
            "grupo": grupo_z,
            "linea": linea_z,
            "inioferta": fecini_z,
            "finoferta": fecfin_z,
            "preciooferta": ("%.2f" % proferta_z)
          }
          micatjson.append(miren_z);
       #   descri_z = utils.elimina_car_esp(descri_z)
      #    if nartic_z > 1 : 
      #              findice_z.write(",\n");
          #End if
      #    findice_z.write("{");
      #    findice_z.write('"codigo":"' + codigo_z + '",');
      #    findice_z.write('"dscri":"' + descri_z + '"');
      #    findice_z.write('}');
      #    nartic_z = nartic_z + 1
      #End For
      #findice_z.write("\n]\n");
      #findice_z.close();
      with open(archjson_z, "w") as outfile:
         json.dump(micatjson, outfile, indent=4)
   #End def genera_JSON_ofertas

  def genera_JSON_lineas(self, widget):
      imprime_sin_exis_z = "NO"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"
      archimg_z = "";
      jsonlineas_z = [];

      sql_z = "select a.linea, a.descri from inv_lineas a "
      sql_z = sql_z + " where  a.cia = " + str(cia_z)
      sql_z = sql_z + " order by a.linea"
      print sql_z;
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      ren_z = 0
      antcod_z = "-1"
      sigcod_z = ""
      antlinea_z = "-1"
      archjson_z = "lineas.json";
      findice_z = open(archjson_z, "w")
      findice_z.write("[\n");
      catalogodescri_z = []
      nartic_z = 1;
      for record in result:
          ren_z = ren_z + 1
          codigo_z = record[0]
          descri_z = record[1]
          descri_z = utils.elimina_car_esp(descri_z)
          if nartic_z > 1 : 
                    findice_z.write(",\n");
          #End if
          findice_z.write("{");
          findice_z.write('"codigo":"' + codigo_z + '",');
          findice_z.write('"descri":"' + descri_z + '"');
          findice_z.write('}');
          jsonlineas_z.append (
            {"codigo": codigo_z,
             "descri": descri_z
            }
          )
          nartic_z = nartic_z + 1
      #End For
      findice_z.write("\n]\n");
      findice_z.close();
      with open("lineas2.json", "w") as outfile:
            json.dump(jsonlineas_z, outfile);


  def catalogo_html(self, widget):
      if mimodo_z <> "AUTO" :
      	resp_z = utils.yesnodlg("Seguro de Crear el catalogo V.3 ?")
      	if resp_z <> gtk.RESPONSE_OK:
         	return
      	#End if
      #End if
      imprime_sin_exis_z = "SI"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"

      indice_z = "html" + os.sep + "lineas.html"
      antlin_z = "-1"
      antgpo_z = "-1"
      sqllin_z = "select linea, count(*) "
      sqllin_z  = sqllin_z + " from inven a join inv_invhist c on a.codigo = c.codigo and a.cia = c.cia"
      sqllin_z  = sqllin_z + " join inv_relinv d on c.idart = d.idart and d.idrel = " + str(def_tablas.REL_INVEN_ARTDESP)
      sqllin_z  = sqllin_z + " join inv_grupos b on d.iddato = b.idgrupo "
      if imprime_sin_exis_z == "NO" :
        sqllin_z  = sqllin_z + " join movart e on e.codigo = a.codigo and e.cia = a.cia "
      ##End if
      sqllin_z  = sqllin_z + " where a.empaqe <> 'REMATE' and a.cia = " + str(cia_z) 
      if imprime_sin_exis_z == "NO" :
         sqllin_z  = sqllin_z  + " and e.salio <> 'S'"
      #Fin If
      sqllin_z  = sqllin_z + " group by linea"

      fultact_z = open("html" +  os.sep + "ultima_actualizacion.txt", "w");
      fultact_z.write(datetime.date.today().strftime('%Y%m%d')+ "\n");
      fultact_z.close();
      
      findice_z = open(indice_z, "w")
      findice_z.write("<html>\n")
      findice_z.write("<head>\n")
      findice_z.write("<script language=\"JavaScript\" type=\"text/javascript\">\n");
      findice_z.write("<!--\n");
      findice_z.write("function PopWindow()\n");
      findice_z.write("{\n");
      findice_z.write("window.open('mds/tabla_venta.html','Amortizacion',\n");
      findice_z.write("'width=800,height=300,menubar=no,scrollbars=yes,toolbar=no,location=no,directories=no,resizable=yes,top=0,left=0');\n");
      findice_z.write("}\n");
      findice_z.write("//-->\n");
      findice_z.write("</script>\n");
      findice_z.write("<script src=\"../calcuprecios/utils.js\"></script>\n");
      findice_z.write("<title>Catalogo de Articulos</title>\n")
      findice_z.write("</head>\n")
      findice_z.write("<center><IMG ALT=\"Diaz y Solis\" SRC=\"fotos/mds/logo2.jpg\" WIDTH=\"100%\" /></center>\n")
      findice_z.write("<label id=\"lbl_zona\">Zona</label><br>\n");
      findice_z.write("Catalogo de Lineas\n")
      findice_z.write("<ul>\n")
      cursor = mydb.cursor()
      cursor.execute(sqllin_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      ren_z = 0
      antcod_z = "-1"
      for record in result:
          ren_z = ren_z + 1
          linea_z = record[0]
          findice_z.write("<li> <A HREF=\"" + linea_z + "/" + linea_z + ".html" + "\" TARGET=\"principal\"> " + linea_z + " </A>\n")
          self.genera_archivo_linea(linea_z);
      #End For
      # Genero la tabla de codigos sin foto
      findice_z.write("<li> <A HREF=\"" + "artsinfoto" + "/" + "artsinfoto" + ".html" + "\" TARGET=\"principal\"> " + "Articulos Sin Foto" + " </A>\n")
      pathlin_z = "html" + os.sep + "artsinfoto"
      nomarchlin_z = pathlin_z + os.sep + "artsinfoto" + ".html"
      self.comprobar_directorio(pathlin_z)
      farchlin_z = open(nomarchlin_z, "w")
      farchlin_z.write("<html>\n")
      farchlin_z.write("<body>\n")
      farchlin_z.write("<table border=1>\n")
      farchlin_z.write("<tr><th>Linea</th><th>Codigo</th><th>Descripcion</th><th>Archivo</th><tr>\n")
      for articulo_z in archsinfoto_z:
          farchlin_z.write("<tr><td>" + articulo_z[2] + "</td><td>" + articulo_z[0] + "</td><td>"+ articulo_z[1] + "</td><td>"+ articulo_z[3] + "</td></tr>\n")
      #End for
      findice_z.write("</ul>\n");
      findice_z.write("<form><input type=\"button\" value=\"Calcular Precios\" onClick=\"JavaScript:PopWindow()\"></form>\n");
      findice_z.write("<form name=\"selzona\" method=\"GET\" action=\"seleczona.html\"  TARGET=\"principal\"><input type=\"submit\" value=\"Definir Zona\" ></form>\n");

      findice_z.write("Fecha:" + datetime.date.today().strftime('%d-%m-%Y'));
      findice_z.write("<p><a href=\"../manualescartera/manuales/manual_p_vender_tiempo_aire.pdf\" target=\"nuevo\" > Manual Ventas TA</a></p>");
      findice_z.write("<p><a href=\"../manualescartera/manuales/formato_ventas_ta.pdf\" target=\"nuevo\" > Formato Ventas TA</a></p>");
      findice_z.write("<p>Venta de Tiempo Aire<br><a href=\"http://ventas.tecnopay.com\" target=\"nuevo\" > <img src=\"fotos/logo_mds/logota.jpg\" alt=\"Venta de Tiempo Aire\"></a></p>");
      findice_z.write("<p>Manuales de Cartera<br><a href=\"http://mdsapps.ddns.net/catalogo/manualescartera/\" target=\"nuevo\" > <img src=\"manuales/img/manual.jpg\" alt=\"Manuales de Cartera\"></a></p>");
      findice_z.write("<script src=\"../cotizacion/utils.js\"></script>");

      findice_z.write("</body>\n")
      findice_z.write("</html>\n")

      if mimodo_z <> "AUTO" :
      	utils.msgdlg("Catalogo Generado");
      #End if

# --Fin de generar cat?logo
          
          
  def genera_archivo_linea(self, linea_z):
      self.corrige_extensiones(linea_z)
      imprime_sin_exis_z = "SI"
      imprime_descontinuados_z = "NO"
      descontinuado_z = "DESCONT"
      imprime_unicos_z = "NO"
      unico_z = "UNICO"
      archimg_z = "";

      sql_z = "select linea, b.codigo, b.descri, a.codigo, a.descri, precio, a.empaqe, "
      sql_z = sql_z + " cast(a.existes+a.existen as integer) as exist"
      sql_z = sql_z + " from inven a join inv_invhist c on a.codigo = c.codigo and a.cia = c.cia"
      sql_z = sql_z + " join inv_relinv d on c.idart = d.idart and d.idrel = " + str(def_tablas.REL_INVEN_ARTDESP)
      sql_z = sql_z + " join inv_grupos b on d.iddato = b.idgrupo "
      if imprime_sin_exis_z == "NO" :
         sql_z = sql_z + " join movart e on e.codigo = a.codigo and e.cia = a.cia "
         sql_z = sql_z + " and almac not in ('BO', 'AG', 'SE') "
      #endif
      sql_z = sql_z + " where a.linea = '" + linea_z + "' and a.empaqe <> 'REMATE' " + " and a.cia = " + str(cia_z)
      if imprime_sin_exis_z == "NO" :
         sql_z  = sql_z  + " and e.salio <> 'S'"
      #Fin If
      sql_z = sql_z + " group by linea, b.codigo, b.descri, a.codigo, a.descri, precio, a.empaqe, exist"
      print sql_z;
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      cuantos_z = len(result)
      artsinfoto_z = []
      artconfoto_z = []
      ren_z = 0
      antcod_z = "-1"
      sigcod_z = ""
      pathlin_z = "html" + os.sep + linea_z
      for record in result:
          ren_z = ren_z + 1
          grupo_z = record[2]
          codigo_z = record[3]
          descri_z = record[4]
          precio_z = record[5]
          empaqe_z = record[6]
          exist_z  = record[7]
          siimprimir_z = "SI"
          sqlexist_z = "select count(*) as exist from movart where codigo = '"+codigo_z+"' and salio <> 'S' and cia=" + str(cia_z);
          sqlexist_z = sqlexist_z + " and almac not in ('BO', 'AG', 'SE') "

          if imprime_unicos_z == "NO" and ( empaqe_z.strip() == unico_z.strip() or empaqe_z.strip() == descontinuado_z.strip() ):
             cursor2 = mydb.cursor()
             cursor2.execute(sqlexist_z)
             result2_z = cursor2.fetchall()
             for record2 in result2_z:
                 exist_z = record2[0]

             if exist_z == 0 :
                siimprimir_z = "NO"
             #end if
          #end if

          #print codigo_z, empaqe_z, descri_z, "Se imprime:", siimprimir_z, unico_z, descontinuado_z, exist_z

          if siimprimir_z == "SI" :
            codigo_z = utils.elimina_car_esp(codigo_z)
            archimg_z = "html" + os.sep + "fotos" + os.sep + linea_z + os.sep + codigo_z + ".jpg"
            print("Leyendo:" + linea_z + ":" + codigo_z + ":" + descri_z + "\n");
            if os.path.isfile(archimg_z) == False:
               archsinfoto_z.append([codigo_z, descri_z, linea_z, archimg_z])
               artsinfoto_z.append([grupo_z, codigo_z, descri_z, precio_z, exist_z])
            else:
               artconfoto_z.append([grupo_z, codigo_z, descri_z, precio_z, exist_z])
            #End if
          #End if
      #Fin de For
      # Ahora recorro la lista de los archivos con Foto
      antcod_z = "-1";
      self.comprobar_directorio("html")
      pathlin_z = "html" + os.sep + linea_z
      nomarchlin_z = pathlin_z + os.sep + linea_z + ".html"
      self.comprobar_directorio(pathlin_z)
      farchlin_z = open(nomarchlin_z, "w")
      farchlin_z.write("<html><body>\n")
      antgpo_z = "-1"
      antcod_z = "-1"
      ren_z = 0;
      cuantos_z = len(artconfoto_z)
      for miart_z in artconfoto_z:
          ren_z = ren_z + 1
          grupo_z  = miart_z[0];
          codigo_z = miart_z[1];
          descri_z = miart_z[2];
          precio_z = miart_z[3];
          exist_z  = miart_z[4];
          if ren_z < cuantos_z:
             sigcod_z = artconfoto_z[ren_z][1]
          else:
             if len(artsinfoto_z) > 0:
                sigcod_z = artsinfoto_z[0][1]
             #End if
          #End if
          sigcod_z = utils.elimina_car_esp(sigcod_z)

          if antgpo_z == "-1":
            farchlin_z.write("<ul>\n")
            antgpo_z = grupo_z;
            farchlin_z.write("<li>" + grupo_z )
            farchlin_z.write("<ul>\n")
          #End if
          if  grupo_z <> antgpo_z:
            antgpo_z = grupo_z;
            farchlin_z.write("</ul>\n")
            farchlin_z.write("<li>" + grupo_z )
            farchlin_z.write("<ul>\n")
          #End if
          farchlin_z.write("<li> <A HREF=\"" + codigo_z + ".html\" TARGET=\"principal\">")
          codimg_z = utils.elimina_car_esp(codigo_z);
          nomarchjpg_z = ".." + "/" + "fotos" + "/" + linea_z + "/" + codimg_z + ".jpg" 
          tumb_z = "<img src=\"" + nomarchjpg_z + "\" width=\"100\" height =\"100\">";

          farchlin_z.write(descri_z + " Existencia: " + str(exist_z) + "<br>" + tumb_z + "</A> " +  "\n");
          self.genera_arch_cod_html(codigo_z, sigcod_z, antcod_z, descri_z, pathlin_z, linea_z, linea_z, precio_z);
          antcod_z = codigo_z
      #End de For
      ren_z = 0;
      cuantos_z = len(artsinfoto_z)
      for miart_z in artsinfoto_z:
          ren_z = ren_z + 1
          grupo_z  = miart_z[0];
          codigo_z = miart_z[1];
          descri_z = miart_z[2];
          precio_z = miart_z[3];
          exist_z  = miart_z[4];
          if ren_z < cuantos_z:
             sigcod_z = artsinfoto_z[ren_z][1]
             sigcod_z = utils.elimina_car_esp(sigcod_z)
          #End if
          
          if antgpo_z == "-1":
            farchlin_z.write("<ul>\n")
            antgpo_z = grupo_z;
            farchlin_z.write("<li>" + grupo_z )
            farchlin_z.write("<ul>\n")
          #End if
          if  grupo_z <> antgpo_z:
            antgpo_z = grupo_z;
            farchlin_z.write("</ul>\n")
            farchlin_z.write("<li>" + grupo_z )
            farchlin_z.write("<ul>\n")
          #End if
          farchlin_z.write("<li> <A HREF=\"" + codigo_z + ".html\" TARGET=\"principal\">")
          farchlin_z.write(descri_z + "</A> " + " Existencia: " + str(exist_z) + "\n")
          self.genera_arch_cod_html(codigo_z, sigcod_z, antcod_z, descri_z, pathlin_z, linea_z, linea_z, precio_z)
          antcod_z = codigo_z
      #End de For
          
      # farchlin_z.write("<li> <A HREF=\"" + "AUX1" + ".html\" TARGET=\"principal\">")
      # farchlin_z.write("AUXILIAR1" + "</A>\n");
      # self.genera_arch_cod_html("AUX1", "AUX2", antcod_z, "AUXILIAR 1", pathlin_z, linea_z, linea_z, 0)
      # farchlin_z.write("<li> <A HREF=\"" + "AUX2" + ".html\" TARGET=\"principal\">")
      # farchlin_z.write("AUXILIAR2" + "</A>\n");
      # self.genera_arch_cod_html("AUX2", "AUX3", "AUX1", "AUXILIAR2", pathlin_z, linea_z, linea_z, 0)
      # farchlin_z.write("<li> <A HREF=\"" + "AUX3" + ".html\" TARGET=\"principal\">")
      # farchlin_z.write("AUXILIAR3" + "</A>\n");
      # self.genera_arch_cod_html("AUX3", "AUX4", "AUX2", "AUXILIAR3" , pathlin_z, linea_z, linea_z, 0)
      # farchlin_z.write("<li> <A HREF=\"" + "AUX4" + ".html\" TARGET=\"principal\">")
      # farchlin_z.write("AUXILIAR4" + "</A>\n");
      # self.genera_arch_cod_html("AUX4", "AUX5", "AUX3", "AUXILIAR4" , pathlin_z, linea_z, linea_z, 0)
      # farchlin_z.write("<li> <A HREF=\"" + "AUX5" + ".html\" TARGET=\"principal\">")
      # farchlin_z.write("AUXILIAR5" + "</A>\n");
      # self.genera_arch_cod_html("AUX5", "-1", "AUX4", "AUXILIAR5" , pathlin_z, linea_z, linea_z, 0)
      farchlin_z.write("</ul>\n")
      #End If
      farchlin_z.write("</ul>\n")
      farchlin_z.write("</body>\n")
      farchlin_z.write("</html>\n")
      farchlin_z.close()


# --- Fin de define_catalogo_html(self) ------    

# --- Funcion que sirve para corregir las extensiones de los archivos de JPG a jpg
  def corrige_extensiones(self, linea_z):
      directorio_z =  "html" + os.sep + "fotos" + os.sep + linea_z
      for filename in os.listdir(directorio_z):
          extension_z = filename[-3:]
          if extension_z == "JPG":
             nvofilename_z = "html" + os.sep + "fotos" + os.sep + linea_z + os.sep + filename[0:-3] + "jpg"
             oldfilename_z = "html" + os.sep + "fotos" + os.sep + linea_z + os.sep + filename
             print("Renombrando:" + oldfilename_z + " -> " + nvofilename_z)
             os.rename(oldfilename_z, nvofilename_z)
          #End if
      #End for
# --- Fin Funcion que sirve para corregir las extensiones de los archivos de JPG a jpg
    

# --- Define crear_directorio -----
  def comprobar_directorio(self, directorio_z):
      if os.path.isdir(directorio_z) == False:
         if os.path.isfile(directorio_z):
            os.remove(directorio_z)
         #End if
         os.mkdir(directorio_z)
      #End if
# Fin de Define crear_directorio -----

# --- Define archivo html x codigo -----
  def genera_arch_cod_html(self, codigo_z, sigcod_z, antcod_z, descri_z, pathlin_z, linea_z, siglin_z, precio_z):
          misep_z = "/"
          plazomax_z = self.busca_plazomax(codigo_z, precio_z)
          
          nomarchcod_z = pathlin_z + misep_z + codigo_z + ".html"
          nomarchcar_z = pathlin_z + misep_z + codigo_z + "_car.txt"
          nomarchimg_z = ".." + misep_z + "fotos" + misep_z + linea_z + misep_z + codigo_z
          
          farchcod_z = open(nomarchcod_z, "w")
          farchcod_z.write("<html>\n")
          farchcod_z.write("<body>\n")
          farchcod_z.write("<FORM name=\"guideform\" action=\"../../cotizacion/cotizador.php\" method=\"GET\" >")
          farchcod_z.write("<INPUT type=\"button\" name=\"anter\" value=\"Anterior\" onClick=\"window.location=\'")
          if antcod_z == "-1" :
             farchcod_z.write(sigcod_z)
          else:
             farchcod_z.write(antcod_z)
          #Else
          farchcod_z.write(".html\'\">")
          antcod_z = codigo_z
          if siglin_z == linea_z:
             farchcod_z.write("<INPUT type=\"button\" name=\"sigte\" value=\"Siguiente\" onClick=\"window.location=\'" +
             sigcod_z + ".html\'\">")
          #End if
          farchcod_z.write("\n<INPUT type=\"submit\" name=\"cotizar\" value=\"Cotizar\" >\n")
          
          modo_z = self.wTree.get_widget("edt_fecalta").get_text().upper()
          tasa_z = self.wTree.get_widget("edt_situac").get_text()
          descto_z = utils.ValFloat(tasa_z)
          if modo_z == "CAT_TRON":
            strprecio_z = "Precio: $" + utils.currency(precio_z * (1 - descto_z / 100) )
          else:
            strprecio_z = " P:" + utils.canticodif(precio_z)
          #End if
          descri_z = utils.elimina_car_esp(descri_z)
          farchcod_z.write("<input type = \"hidden\" name=\"codigo\" value=\"" + codigo_z + "\" > \n")
          farchcod_z.write("<input type = \"hidden\" name=\"descri\" value=\"" + descri_z + "\" > \n")
          farchcod_z.write("<input type = \"hidden\" name=\"linea\" value=\"" + linea_z + "\" > \n")
          farchcod_z.write("<input type = \"hidden\" name=\"precio\" value=\"" + ("%.2f" % precio_z) + "\" > \n")
          farchcod_z.write("<input type = \"hidden\" name=\"pzomax\" value=\"" + repr(plazomax_z) + "\" > \n")
          farchcod_z.write("</form>\n")
          farchcod_z.write("<table>\n")
          farchcod_z.write("<tr><td valign=\"top\">" )
          farchcod_z.write("<a href=\"" + nomarchimg_z + ".jpg\" target=\"new\" >" )
          farchcod_z.write(codigo_z + " " + descri_z + " <br> " + strprecio_z + "<br><img src=\"" + nomarchimg_z + ".jpg\" ")
          farchcod_z.write(" WIDTH=\"320\"" )
          farchcod_z.write(" ALT=\"" + descri_z + "\"></a>\n")
          if os.path.isfile(nomarchcar_z):
             farchcar_z = open(nomarchcar_z)
             farchcod_z.write("</td><td valign=\"top\" ><pre>\n")
             for line in farchcar_z.readlines():
                 farchcod_z.write(" " + line)
             #End for
             farchcod_z.write("</pre>\n")
             farchcar_z.close()
          #End if

          farchcod_z.write("</td></tr>\n")
          ## --> Ahora voy a poner las existencias <-- 
          sql_z = "select alm, existes + existen from exist where codigo = '" + codigo_z + "'"
          sql_z = sql_z + " and cia = " + repr(cia_z)
          sql_z = sql_z + " and alm not in ('BO', 'AG', 'SE') "
          cursor = mydb.cursor()
          cursor.execute(sql_z)
          result = cursor.fetchall()
          miscolores_z = self.busca_colores(codigo_z)
          totex_z = 0
          farchcod_z.write("<tr><td>Existencias<br>\n")
          farchcod_z.write("<table border=\"1\">\n")
          farchcod_z.write("<tr>\n")
          for record in result:
              if record[1] <> 0:
                 farchcod_z.write("<td>")
                 farchcod_z.write(record[0])
                 farchcod_z.write("</td>")
              #End if
          #End for
          farchcod_z.write("<td>Total</td>")
          farchcod_z.write("</tr>\n")
          farchcod_z.write("<tr>\n")
          totexi_z = 0
          for record in result:
              if record[1] <> 0:
                 farchcod_z.write("<td>")
                 farchcod_z.write(repr(int(record[1])) + " ")
                 primero_z = "<br>Colores:<br>"
                 for micolor_z in miscolores_z:
                    if micolor_z[0] == record [0]:
                       farchcod_z.write(primero_z + micolor_z[2] + ":")
                       farchcod_z.write(repr(int(micolor_z[3])))
                       primero_z = "<br> "

                 totexi_z = totexi_z + int(record[1])
                 farchcod_z.write("</td>")
              #End if
          #End for
          farchcod_z.write("<td>" + repr (int(totexi_z)) + "</td>")
          farchcod_z.write("</tr>\n")
          farchcod_z.write("</table>\n")
          
          farchcod_z.write("</table>\n")
          farchcod_z.write("<table>\n")
          farchcod_z.write("<tr>\n")
          for ii_z in range (1, 10):
              nomarchjpg1_z = "html" + os.sep + "fotos" + os.sep + linea_z + os.sep + codigo_z + "_" + str(ii_z) + ".jpg"
              nomarchjpg_z = ".." + "/" + "fotos" + "/" + linea_z + "/" + codigo_z + "_" + str(ii_z) + ".jpg" 
              if os.path.isfile(nomarchjpg1_z):
                 farchcod_z.write("<td><img src=\"" + nomarchjpg_z + "\" ")
                 farchcod_z.write(" WIDTH=88 HEIGHT=88 ")
                 farchcod_z.write(" onclick=\"this.src=\'" + nomarchjpg_z + "\' ")
                 farchcod_z.write(" ; this.height=400;this.width=300\" ")
                 farchcod_z.write(" ondblclick=\"this.src=\'" + nomarchjpg_z + "\' ")
                 farchcod_z.write(" ; this.height=88;this.width=88\">" )
                 farchcod_z.write(" </td>\n")
              #End if
          #End for
#          farchcod_z.write("<iframe width=100% src=\"" + codigo_z + "_car.html\" </iframe>")
          farchcod_z.write("</tr>\n</table>\n")
#          tablavta = open("html"+os.sep+"mds"+os.sep+"tablavta.txt")
#          for line in tablavta.readlines():
#              farchcod_z.write(line+"\n");
#          #End for

          farchcod_z.write("</body>\n")
          farchcod_z.write("</html>\n")
          farchcod_z.close()
    
# --- Fin Define archivo html x codigo -----

# --- Define Buscar Colores -----
  def  busca_colores(self, codigo_z):
     global cia_z
     sibuscar_z = "NO"
     sql_z = "select tipo, linea from inven where codigo = '" + codigo_z + "'"
     sql_z = sql_z + " and cia = " + repr(cia_z)
     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchone()
     linea_z = result[1]
     if result[0] <> "ALF":
        result = []
     else:
        if linea_z <> "MOTO":
            sql_z = "select c.codigo from inv_invhist a ";
            sql_z = sql_z + " join inv_relinv b on a.idart = b.idart and b.idrel = " + str(def_tablas.REL_INVEN_ARTDESP)
            sql_z = sql_z + " join inv_grupos d on b.iddato = d.idgrupo join inv_servicios c on d.idgrupo = c.idart"
            sql_z = sql_z + " where a.codigo = '" + codigo_z + "'"
            sql_z = sql_z + " and a.cia = " + repr(cia_z)
            sql_z = sql_z + " and c.tipo = " + str(def_tablas.TIPO_INV_SERVICIO_SERIESAUMENTADAS)
            cursor = mydb.cursor()
            cursor.execute(sql_z)
            result = cursor.fetchall()
            for record in result:
               sibuscar_z = "SI"
            #End for
        else:
            sibuscar_z = "SI"
        #End if
        

        if sibuscar_z <> "SI":
           sql_z = "select almac, b.codigo, b.descri, "
           sql_z = sql_z + " count(*) from movart a"
           sql_z = sql_z + " join inv_colores b on substring(serie, length(serie) - 1, 2) = b.codigo"
           sql_z = sql_z + " where a.codigo = '" + codigo_z + "' and salio <> 'S'"
           if linea_z <> "MOTO":
              sql_z = sql_z + " and serie like '--%' "
           #End if 
           sql_z = sql_z + " and a.cia =" + repr(cia_z)
           sql_z = sql_z + " and almac not in ('BO', 'AG', 'SE') "
           sql_z = sql_z + " group by almac, b.codigo, b.descri";
        else:
           sql_z = "select almac, b.codigo, b.descri, "
           sql_z = sql_z + " count(*) from movart a"
           sql_z = sql_z + " join inv_colores b on substring(serie, length(serie) - 1, 2) = b.codigo"
           sql_z = sql_z + " where a.codigo = '" + codigo_z + "' and salio <> 'S'"
           sql_z = sql_z + " and length(serie) > 2 and a.cia =" + repr(cia_z)
           sql_z = sql_z + " and almac not in ('BO', 'AG', 'SE') "
           sql_z = sql_z + " group by almac, b.codigo, b.descri";
        #End if 

        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result = cursor.fetchall()
     return (result)
     
# ----------- Fin de Funcion --------

# --- Define Buscar PLazoMax -----
  def  busca_plazomax(self, codigo_z, precio_z):
     global cia_z;
     miplazomax_z = 0;
     seguir_z = ""
     sibuscar_z = "NO";
     plazo_z = 0;
     plazomax_z = 0;
     grupo_z = "";
     sql_z = " select cod2 from inven c where c.codigo = '" + codigo_z + "'"
     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchall()
     for record in result:
         grupo_z = record[0];


     sql_z = "select plazomax from plazoscrd a join inv_invhist b on a.idlinea = b.idart"
     sql_z = sql_z + " where tipo= " + repr(def_tablas.TIPO_PLAZO_ARTICULO) + " and a.cia= " + repr(cia_z)
     sql_z = sql_z + " and b.codigo = '" + codigo_z + "'"
     ## print sql_z
     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchall()
     for record in result:
         seguir_z = "NO"
         plazomax_z = record[0];
         ## print ("busca_plazomax plazo x articulo")
         return(plazomax_z * 2);
     #End for
     ## --> No hay plazo por Codigo, lo busco por grupo con Prioridad
     sql_z = "select plazomax from plazoscrd a join inv_grupos b ";
     sql_z = sql_z + "on a.idlinea = b.idgrupo ";
     sql_z = sql_z + " where tipo= " + repr(def_tablas.TIPO_PLAZO_GRUPO_PRIORIDAD);
     sql_z = sql_z + " and a.cia= "  + repr(cia_z)
     sql_z = sql_z + " and b.codigo = '" + grupo_z + "'";

     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchall()
     for record in result:
         seguir_z = "NO"
         plazomax_z = record[0];
         ## print ("busca_plazomax plazo x grupo prioridad" + repr(plazomax_z))
         return(plazomax_z * 2)
     #End for
     sql_z = "select a.tipo, a.plazomax from inven b ";
     sql_z = sql_z + " join plazoscrd a on b.linea = a.linea and b.cia = a.cia";
     sql_z = sql_z + " where ( a.tipo= " + repr(def_tablas.TIPO_PLAZO_LINEA_PRIORIDAD);
     sql_z = sql_z + " or a.tipo = "  + repr(def_tablas.TIPO_PLAZO_LINEA_X_TABLA);
     sql_z = sql_z + " or a.tipo = "  + repr(def_tablas.TIPO_PLAZO_LINEA_X_GRUPO);
     sql_z = sql_z + " or a.tipo = "  + repr(def_tablas.TIPO_PLAZO_X_GRUPOX_TABLA);
     sql_z = sql_z + ") and b.cia= "  + repr(cia_z);
     sql_z = sql_z + " and b.codigo = '" + codigo_z + "'";
     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchall()
     for record in result:
         seguir_z = "NO"
         tipopzo_z = record[0];
         plazomax_z = record[1];
         if(tipopzo_z == def_tablas.TIPO_PLAZO_LINEA_PRIORIDAD):
            plazolin_z = plazomax_z;
            ## print ("busca_plazomax plazo x linea prioridad " + repr(plazomax_z))
            return(plazomax_z * 2);
     #End for
     sql_z = "select a.plazomax from plazoscrd a where ";
     sql_z = sql_z + " a.tipo = "  + repr(def_tablas.TIPO_PLAZO_PRECIO);
     sql_z = sql_z + " and a.cia= "  + repr(cia_z);
     sql_z = sql_z + "  and plistamax = ( ";
     sql_z = sql_z + " select min(plistamax) from plazoscrd c ";
     sql_z = sql_z + " where c.tipo = "  + repr(def_tablas.TIPO_PLAZO_PRECIO);
     sql_z = sql_z + " and c.plistamax >= " +  "%12.2f" % precio_z + ")"
     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchall()
     for record in result:
         seguir_z = "NO"
         if plazomax_z > record[0]:
            plazomax_z = record[0];
            ## print ("busca_plazomax plazo x linea precio")
     #End for
     sql_z = "select plazomax from plazoscrd a join inv_grupos b "
     sql_z += "on a.idlinea = b.idgrupo where "
     sql_z += " tipo= " + repr(def_tablas.TIPO_PLAZO_GRUPO);
     sql_z += " and a.cia= " + repr(cia_z)
     sql_z += " and b.codigo = '" + grupo_z + "'"

     cursor = mydb.cursor()
     cursor.execute(sql_z)
     result = cursor.fetchall()
     for record in result:
         seguir_z = "NO"
         if plazomax_z > record[0]:
            plazomax_z = record[0];
            ## print ("busca_plazomax plazo x grupo")
     #End for

     return (plazomax_z * 2);
     
# ----------- Fin de Funcion --------

  def define_tab_disponibles(self):
    global cia_z
    grd_dispo = self.wTree.get_widget("grd_disponibles")
    self.lst_disponibles = gtk.ListStore(str, str, str, int, str, str, str, int, str, str, str, str, str, str)
    grd_dispo.set_model(self.lst_disponibles)
    columns_z = ["Alm", "Fecha", "E", "Entrada", "Viene de", "Fol.Viene", "Proveedor", "Folio", "Serie", "S", "F.Salida", "Recibe", "Fol.Rec", "Sale Para"]
    ii_z = 0
    for midato_z in columns_z:
      col = gtk.TreeViewColumn(midato_z)
      col.set_resizable(True)
      grd_dispo.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1

    #grd_dispo.connect("cursor-changed", self.ren_seleccionado)
    if platform in utils.grd_lines_soported:  
       grd_dispo.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
# --- Fin de define_tab_disponibles(self) ------    

  def define_tab_busqserie(self):
    global cia_z
    grd_busqserie = self.wTree.get_widget("grd_busqserie")
    self.lst_busqserie = gtk.ListStore(str, str, str, int, str, str, str, int, str, str, str, str, str, str)
    grd_busqserie.set_model(self.lst_busqserie)
    columns_z = [
      "Alm", 
      "Fecha", 
      "E", 
      "Entrada", 
      "Viene de", 
      "Fol.Viene", 
      "Proveedor", 
      "Folio", 
      "Serie", 
      "S",
      "F.Salida",
      "Recibe",
      "Fol.Rec",
      "Sale Para"
    ]
    ii_z = 0
    for midato_z in columns_z:
      col = gtk.TreeViewColumn(midato_z)
      col.set_resizable(True)
      grd_busqserie.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1

    #grd_dispo.connect("cursor-changed", self.ren_seleccionado)
    if platform in utils.grd_lines_soported:  
       grd_busqserie.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
# --- Fin de define_tab_busqserie(self) ------    


  def define_tab_estadis(self):
    global cia_z
    grd_estadis = self.wTree.get_widget("grd_estadis")
    self.lst_estadis = gtk.ListStore(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    grd_estadis.set_model(self.lst_estadis)
    columns_z = ["Alm", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul",  "Ago",  "Sep",  "Oct",  "Nov",  "Dic", "Total", "Nombre" ]
    ii_z = 0
    for midato_z in columns_z:
      col = gtk.TreeViewColumn(midato_z)
      col.set_resizable(True)
      grd_estadis.append_column(col)
      cell = gtk.CellRendererText()
      col.pack_start(cell, False)
      col.set_attributes(cell, text=ii_z)
      ii_z = ii_z + 1
    if platform in utils.grd_lines_soported:  
       grd_estadis.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
# --- Fin de define_tab_estadis(self) ------    

  def define_tab_observs(self):
    global cia_z
    grd_observs = self.wTree.get_widget("grd_observs")
    self.lst_observs = gtk.ListStore(str, str)
    grd_observs.set_model(self.lst_observs)

    col01 = gtk.TreeViewColumn('Fecha')
    col02 = gtk.TreeViewColumn('Observaciones')
        
    grd_observs.append_column(col01)
    grd_observs.append_column(col02)
        
    # create a CellRenderers to render the data
    cell01 = gtk.CellRendererText()
    cell02 = gtk.CellRendererText()
        
    col01.pack_start(cell01, False)
    col02.pack_start(cell02, False)
        
    col01.set_attributes(cell01, text=0)
    col02.set_attributes(cell02, text=1)
    if platform in utils.grd_lines_soported:  
       grd_observs.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
# --- Fin de define_tab_observs(self) ------    


  def define_tabla_exist(self):
    global cia_z
    hbox_existe = self.wTree.get_widget("hbox_exist")
    grd_exists = self.wTree.get_widget("grd_exists")
    sql_z = "select clave from almacen where cia = " + repr(cia_z) 
    sql_z = sql_z + " order by ordiary, clave"
    cursor = mydb.cursor()
    cursor.execute(sql_z)

    result = cursor.fetchall()
    ii_z = 0
    self.edt_exis = []
    self.alm_exis = []
    self.alms_z = []
    self.alms_z.append(str)
    col = gtk.TreeViewColumn("Codigo")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    for record in result:
       cvealm_z = record[0]
       self.alm_exis.append(cvealm_z)
       self.alms_z.append(str)
       vbox1 = gtk.VBox()
       label1 = gtk.Label(cvealm_z)
       edt_exialm = gtk.Entry()
       edt_exialm .set_width_chars(4)
       edt_exialm .set_editable(False)
       self.edt_exis.append(edt_exialm)
       label1.show()
       vbox1.pack_start(label1, False, False, 0)
       vbox1.show()
       edt_exialm.show()
       vbox1.pack_start(edt_exialm, False, False, 0)
       vbox1.show()
       hbox_existe.pack_start(vbox1, False, False, 0)
       hbox_existe.show()
       col = gtk.TreeViewColumn(cvealm_z)
       col.set_resizable(True)
       grd_exists.append_column(col)    
       cell = gtk.CellRendererText()
       col.pack_start(cell, False)
       col.set_attributes(cell, text=ii_z)
       ii_z = ii_z + 1

    vbox1 = gtk.VBox()
    label1 = gtk.Label("Total")
    edt_exialm = gtk.Entry()
    edt_exialm .set_width_chars(4)
    edt_exialm .set_editable(False)
    self.edt_exis.append(edt_exialm)
    self.alm_exis.append("-TOTAL")
    label1.show()
    vbox1.pack_start(label1, False, False, 0)
    vbox1.show()
    edt_exialm.show()
    vbox1.pack_start(edt_exialm, False, False, 0)
    vbox1.show()
    hbox_existe.pack_start(vbox1, False, False, 0)
    hbox_existe.show()
    self.alms_z.append(str)
    col = gtk.TreeViewColumn("Total")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    self.alms_z.append(str)
    col = gtk.TreeViewColumn("Costo.U")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    self.alms_z.append(str)
    col = gtk.TreeViewColumn("P.Lista")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    self.alms_z.append(int)
    col = gtk.TreeViewColumn("Max")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    self.alms_z.append(str)
    col = gtk.TreeViewColumn("MUB")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    self.alms_z.append(str)
    col = gtk.TreeViewColumn("Descripcion")
    grd_exists.append_column(col)
    cell = gtk.CellRendererText()
    col.pack_start(cell, False)
    col.set_attributes(cell, text=ii_z)
    ii_z = ii_z + 1
    self.lst_exists = gtk.ListStore(*[col for col in self.alms_z])
    grd_exists.set_model(self.lst_exists)
    if platform in utils.grd_lines_soported:  
       grd_exists.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

#--- Fin de Define Tabla Existencias ------------

  def on_btn_primero_clicked(self, widget):
      self.busca_vnd("P")

  def on_btn_anter_clicked(self, widget):
      self.busca_vnd("A", inven['codigo'])

  def on_btn_sigte_clicked(self, widget):
      self.busca_vnd("S", inven['codigo'])

  def on_btn_ultimo_clicked(self, widget):
      self.busca_vnd("U")

  def on_edt_codigo_activate(self, widget):
      self.busca_inv(widget.get_text().upper())

  def on_edt_almkdx_activate(self, widget):
      if self.busca_alm(widget.get_text().upper()) == True:
         widget.set_text(almacen['clave'])
      self.lst_kardex.clear()
      self.despliega_kardex()

  def busca_inv(self, codigo_z = ''):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      if codigo_z == '':
         codigo_z = edt_codigo.get_text().upper()
         
      sql_z = "select codigo, descri, tipo, costos, coston, piva from inven where codigo = '" + codigo_z + "' and cia=" + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows <> 0:
        record = record[0] ## Solo Espero un registro
        codigo_z    = record[0]
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
           codigo_z    = miresp_z[0]
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif
      if(resp_z == True):
         self.busca_vnd("D", codigo_z)

      return (resp_z)

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
      global modo_z
      modo_z = BORRAR
      codigo_z = almacen['clave']
      nombre_z = almacen['nombre']
      resp_z = utils.yesnodlg("Seguro de Eliminar este Almacen ?" + nombre_z)
      if resp_z == gtk.RESPONSE_OK:
         sql_z = "delete from almacen where clave='" + codigo_z + "' and cia= " + repr(cia_z)
         cursor = mydb.cursor()
         cursor.execute(sql_z)
         self.limpia_campos()
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
      edt_direc   = self.wTree.get_widget("edt_direc")
      edt_ordiary = self.wTree.get_widget("edt_ordiary")
      edt_exib    = self.wTree.get_widget("edt_exib")
      edt_zona    = self.wTree.get_widget("edt_zona")
      edt_ordtab  = self.wTree.get_widget("edt_ordtab")

      almacen['clave']   = edt_codigo.get_text().upper()
      almacen['nombre']  = edt_nombre.get_text().upper()
      almacen['direc']   = edt_direc.get_text().upper()
      almacen['cia']     = cia_z
      almacen['ordiary'] = def_tablas.StrToInt(edt_ordiary.get_text())
      almacen['exib']    = edt_exib.get_text()
      almacen['zona']    = edt_zona.get_text()
      almacen['ordtab']  = def_tablas.StrToInt(edt_ordtab.get_text())
      if modo_z == NUEVO:
         sql_z = "insert into almacen (clave,nombre,direc,sdoini,impent,impsal,sdofin,cia,ordiary,exib,zona,ordtabt) values ( "
         sql_z = sql_z + "'" + almacen['clave'] + "',"
         sql_z = sql_z + "'" + almacen['nombre'] + "',"
         sql_z = sql_z + "'" + almacen['direc'] + "',"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + "0,"
         sql_z = sql_z + repr(cia_z) + ","
         sql_z = sql_z + repr(almacen['ordiary']) + ","
         sql_z = sql_z + "'" + almacen['exib'] + "',"
         sql_z = sql_z + "'" + almacen['zona'] + "',"
         sql_z = sql_z + repr(almacen['ordtab']) + ")"
          
      elif modo_z == MODIFICA:
         sql_z = "update almacen set "
         sql_z = sql_z + "nombre = '" + almacen['nombre'] + "',"
         sql_z = sql_z + "direc = '" + almacen['direc'] + "',"
         sql_z = sql_z + "ordiary = " + repr(almacen['ordiary']) + ","
         sql_z = sql_z + "exib = '" + almacen['exib'] + "',"
         sql_z = sql_z + "zona = '" + almacen['zona'] + "',"
         sql_z = sql_z + "ordtabt = " + repr(almacen['ordtab'])
         sql_z = sql_z + " where clave = '" + almacen['clave'] + "'"
         sql_z = sql_z + " and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      print sql_z
      cursor.execute(sql_z)

  def on_edt_tipoest_activate(self, widget):
      self.toma_tipo_estadis()

  def on_edt_agrupapor_activate(self, widget):
      self.toma_grupo_estadis()

  def toma_grupo_estadis(self):
      agrupapor_z = self.wTree.get_widget("edt_agrupapor").get_text().upper()
      self.wTree.get_widget("edt_agrupapor").set_text(agrupapor_z)
      if not(agrupapor_z in tipoagru_z):
         datosbuscados_z = utils.busca_datos(tipoagru_z, "Conjunto", "Seleccione Como desea agrupar")
         miresp_z = datosbuscados_z.split(":")
         resp_z = utils.StrToInt(miresp_z[-1])
         if resp_z <> gtk.RESPONSE_OK:
           return (False)
         agrupapor_z   = miresp_z[0]
         self.wTree.get_widget("edt_agrupapor").set_text(agrupapor_z)
         if agrupapor_z == "GRUPO":
            codest_z = self.wTree.get_widget("edt_grupo").get_text()
         elif agrupapor_z == "MARCA":
            codest_z = self.wTree.get_widget("edt_marca").get_text()
         elif agrupapor_z == "SITUACION":
            codest_z = self.wTree.get_widget("edt_situac").get_text()
         elif agrupapor_z == "PROVEEDOR":
            codest_z = self.wTree.get_widget("edt_prove").get_text()
         elif agrupapor_z == "DIARY":
            codest_z = self.wTree.get_widget("edt_diary").get_text()
         elif agrupapor_z == "LINEA":
            codest_z = self.wTree.get_widget("edt_linea").get_text()
         elif agrupapor_z == "CODIGO":
            codest_z = self.wTree.get_widget("edt_codigo").get_text()
         self.wTree.get_widget("edt_codest").set_text(codest_z)

  def toma_nombre_estadis(self, estadi_z, clave_z):
      nombre_z = ""
      if (estadi_z == "SALIDAS ESPECIALES" ) or \
         (estadi_z == "ENTRADAS ESPECIALES" ) or \
         (estadi_z == "ENTRADAS X CANCEL" ) or \
         (estadi_z == "ENTRADAS X COMPRA" ):
         sql_z = "select nombre from almacen where clave = '" + clave_z + "' and cia=" + repr(cia_z)
      elif estadi_z == "SALIDAS X VENTA":
         sql_z = "select nombre from ptovta where clave = '" + clave_z + "' and cia=" + repr(cia_z)
      elif estadi_z == "SALIDAS MAYOREO":
         sql_z = "select nombre from mayoris where codigo = '" + clave_z + "' and cia=" + repr(cia_z)
      cursoralm = mydb.cursor()
      cursoralm.execute(sql_z)
      recalm = cursoralm.fetchall()
      numrows = len(recalm)
      if numrows <> 0:
         recalm = recalm[0] ## Solo Espero un registro
         nombre_z = recalm[0]
      # Fin de If
      return (nombre_z)


  def toma_tipo_estadis(self):
      estadi_z = self.wTree.get_widget("edt_tipoest").get_text().upper()
      self.wTree.get_widget("edt_tipoest").set_text(estadi_z)
      if not(estadi_z in tipoest_z):
         datosbuscados_z = utils.busca_datos(tipoest_z, "Tipo", "Seleccione Que estadistica desea")
         miresp_z = datosbuscados_z.split(":")
         resp_z = utils.StrToInt(miresp_z[-1])
         if resp_z <> gtk.RESPONSE_OK:
           return (False)
         estadi_z   = miresp_z[0]
         self.wTree.get_widget("edt_tipoest").set_text(estadi_z)

  def on_btn_okestadis_clicked(self, widget):
      self.toma_grupo_estadis()
      self.toma_tipo_estadis()
      grupoest_z = self.wTree.get_widget("edt_agrupapor").get_text().upper()
      estadi_z = self.wTree.get_widget("edt_tipoest").get_text().upper()
      codigo_z = self.wTree.get_widget("edt_codest").get_text().upper()
      anu_z = self.wTree.get_widget("edt_anuest").get_value_as_int()
      sql_z = "select a.alm, a.mes, sum(a.unidades) from "
      sql_z = sql_z + " estadis a join inven b on a.codigo = b.codigo and a.cia = b.cia "
      where_z = " where "
      if grupoest_z in ["GRUPO", "MARCA", "DIARY"] :
         sql_z = sql_z + " join inv_invhist c on b.codigo = c.codigo and b.cia = c.cia"
         sql_z = sql_z + " join inv_relinv d on c.idart = d.idart and d.idrel = "
         join2_z = ""
         if grupoest_z == "GRUPO":
            idrelinv_z = def_tablas.REL_INVEN_ARTDESP
            join2_z = " join inv_grupos e on d.iddato = e.idgrupo "
            where_z = where_z + " e.codigo "
         elif grupoest_z == "MARCA":
            idrelinv_z = def_tablas.REL_INVEN_MARCAS
            join2_z = " join inv_marcas e on d.iddato = e.idmarcainv "
            where_z = where_z + " e.codigo "
         elif grupoest_z == "DIARY":
            idrelinv_z = def_tablas.REL_INVEN_GPODIARY
            join2_z = " join gpodiary e on d.iddato = e.idgpodiary "
            where_z = where_z + " e.grupo "
         sql_z = sql_z + utils.IntToStr(idrelinv_z) + join2_z 
      else:
        if grupoest_z == "PROVEEDOR":
           where_z = where_z + " b.prove "
        elif grupoest_z == "SITUACION":
           where_z = where_z + " b.empaqe "
        elif grupoest_z == "CODIGO":
           where_z = where_z + " a.codigo "
        elif grupoest_z == "LINEA":
           where_z = where_z + " b.linea "
      where_z = where_z + " like '" + codigo_z + "' "
      sql_z = sql_z + where_z
      where2_z = " and ( "
      if estadi_z == "SALIDAS ESPECIALES":
         where2_z = where2_z + "a.tipo = " + utils.IntToStr(def_tablas.tipoentra("S")[0])
      elif estadi_z == "SALIDAS X VENTA":
         where2_z = where2_z + "a.tipo = " + utils.IntToStr(def_tablas.tipoentra("V")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("F")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("H")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("Q")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("1")[0])
      elif estadi_z == "ENTRADAS X CANCEL":
         where2_z = where2_z + "a.tipo = " + utils.IntToStr(def_tablas.tipoentra("C")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("O")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("J")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("U")[0])
         where2_z = where2_z + " or a.tipo = " + utils.IntToStr(def_tablas.tipoentra("2")[0])
      elif estadi_z == "ENTRADAS ESPECIALES":
         where2_z = where2_z + "a.tipo = " + utils.IntToStr(def_tablas.tipoentra("P")[0])
      elif estadi_z == "SALIDAS MAYOREO":
         where2_z = where2_z + "a.tipo = " + utils.IntToStr(def_tablas.tipoentra("M")[0])
      elif estadi_z == "ENTRADAS X COMPRA":
         where2_z = where2_z + "a.tipo = " + utils.IntToStr(def_tablas.tipoentra("E")[0])
      where2_z = where2_z + ") and anu = " + utils.IntToStr(anu_z)
      sql_z = sql_z + where2_z + " group by a.alm, a.mes"
      print sql_z
      self.lst_estadis.clear()
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      almrec_z = "-1"
      #             alm, 01  02  03  04  05  06  07  08  09  10  11  12  tot nom
      regest_z = [ "-1", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
      totest_z = [ "Tot", "", "", "", "", "", "", "", "", "", "", "", "", "", "Total General"]
      for record in result:
        almrec_z = record[0]
        if almrec_z <> regest_z[0]:
           if regest_z[0] <> "-1":
              regest_z[14] = self.toma_nombre_estadis(estadi_z, regest_z[0])
              self.lst_estadis.append(regest_z)
           #Fin de IF
           regest_z[0] = almrec_z
           unids_z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
           regest_z = [ almrec_z, "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        #End if
        mes_z = record[1]
        regest_z[mes_z] = utils.IntToStr(utils.StrToInt(regest_z[mes_z]) + record[2])
        regest_z[13] = utils.IntToStr(utils.StrToInt(regest_z[13]) + record[2])
        totest_z[mes_z] = utils.IntToStr(utils.StrToInt(totest_z[mes_z]) + record[2])
        totest_z[13] = utils.IntToStr(utils.StrToInt(totest_z[13]) + record[2])
      # Fin de For
      if almrec_z <> "-1":
        regest_z[14] = self.toma_nombre_estadis(estadi_z, almrec_z)
        self.lst_estadis.append(regest_z)
      self.lst_estadis.append(totest_z)
      
# ---Fin de on_btn_okestadis_clicked -----

  def on_edt_exipor_activate(self, widget):
      self.toma_grupo_exist()

  def toma_grupo_exist(self):
      edt_exipor = self.wTree.get_widget("edt_exipor")
      agrupapor_z = edt_exipor.get_text().upper()
      edt_exipor.set_text(agrupapor_z)
      if not(agrupapor_z in tipoagru_z):
         datosbuscados_z = utils.busca_datos(tipoagru_z, "Conjunto", "Seleccione Como desea agrupar")
         miresp_z = datosbuscados_z.split(":")
         resp_z = utils.StrToInt(miresp_z[-1])
         if resp_z <> gtk.RESPONSE_OK:
           return (False)
         agrupapor_z   = miresp_z[0]
         edt_exipor.set_text(agrupapor_z)
         if agrupapor_z == "GRUPO":
            codest_z = self.wTree.get_widget("edt_exicod").get_text()
         elif agrupapor_z == "MARCA":
            codest_z = self.wTree.get_widget("edt_marca").get_text()
         elif agrupapor_z == "SITUACION":
            codest_z = self.wTree.get_widget("edt_situac").get_text()
         elif agrupapor_z == "PROVEEDOR":
            codest_z = self.wTree.get_widget("edt_prove").get_text()
         elif agrupapor_z == "DIARY":
            codest_z = self.wTree.get_widget("edt_diary").get_text()
         elif agrupapor_z == "CODIGO":
            codest_z = self.wTree.get_widget("edt_codigo").get_text()
         elif agrupapor_z == "LINEA":
            codest_z = self.wTree.get_widget("edt_linea").get_text()
         self.wTree.get_widget("edt_exicod").set_text(codest_z)
# ---Fin de toma_grupo_exist -----
  def on_btn_catalogo_clicked(self, widget):
      self.catalogo_html(widget)
# ---Fin de on_btn_catalogo_clicked -----

  def on_btn_okexist_clicked(self, widget):
      self.toma_grupo_exist()
      grupoexi_z = self.wTree.get_widget("edt_exipor").get_text().upper()
      codigo_z = self.wTree.get_widget("edt_exicod").get_text().upper()
      self.wTree.get_widget("edt_exicod").set_text(codigo_z)
      sql_z = "select b.codigo, b.alm, b.existes + b.existen as exis from "
      sql_z = sql_z + "inven a join exist b on a.codigo = b.codigo and a.cia = b.cia "
      where_z = " where "
      if grupoexi_z in ["GRUPO", "MARCA", "DIARY"] :
         sql_z = sql_z + " join inv_invhist c on b.codigo = c.codigo and b.cia = c.cia"
         sql_z = sql_z + " join inv_relinv d on c.idart = d.idart and d.idrel = "
         join2_z = ""
         if grupoexi_z == "GRUPO":
            idrelinv_z = def_tablas.REL_INVEN_ARTDESP
            join2_z = " join inv_grupos e on d.iddato = e.idgrupo "
            where_z = where_z + " e.codigo "
         elif grupoexi_z == "MARCA":
            idrelinv_z = def_tablas.REL_INVEN_MARCAS
            join2_z = " join inv_marcas e on d.iddato = e.idmarcainv "
            where_z = where_z + " e.codigo "
         elif grupoexi_z == "DIARY":
            idrelinv_z = def_tablas.REL_INVEN_GPODIARY
            join2_z = " join gpodiary e on d.iddato = e.idgpodiary "
            where_z = where_z + " e.grupo "
         sql_z = sql_z + utils.IntToStr(idrelinv_z) + join2_z 
      else:
        if grupoexi_z == "PROVEEDOR":
           where_z = where_z + " a.prove "
        elif grupoexi_z == "LINEA":
           where_z = where_z + " a.linea "
        elif grupoexi_z == "SITUACION":
           where_z = where_z + " a.empaqe "
        elif grupoexi_z == "CODIGO":
           where_z = where_z + " a.codigo "
      where_z = where_z + " like '" + codigo_z + "' and (b.existes + b.existen) <> 0"
      sql_z = sql_z + where_z
      print sql_z
      self.lst_exists.clear()
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      almrec_z = "-1"
      antcod_z = "-1"
      alms_z = []
      existencias_z = []
      totexis_z = []
      coltotexi_z = len(self.alm_exis)
      existencias_z.append("Codigo")
      totexis_z.append("TOTAL")
      for mialm_z in self.alm_exis:
          existencias_z.append("")
          totexis_z.append("")
      existencias_z.append("Costou")
      existencias_z.append("P.Lista")
      existencias_z.append(0)
      existencias_z.append("MUB")
      existencias_z.append("Descri")
      totexis_z.append("")
      totexis_z.append("")
      totexis_z.append(0)
      totexis_z.append("")
      totexis_z.append("")
      for record in result:
        codigo_z = record[0]
        almrec_z = record[1]
        if codigo_z <> antcod_z:
           if antcod_z <> "-1":
              self.lst_exists.append(existencias_z)
           #End If
           antcod_z = codigo_z
           datos_extras_z = self.busca_datos_extras_inv(codigo_z, cia_z)
           existencias_z = []
           existencias_z.append(codigo_z)
           for mialm_z in self.alm_exis:
               existencias_z.append("")
           existencias_z.append(utils.currency(datos_extras_z['costou']))
           existencias_z.append(utils.currency(datos_extras_z['precio']))
           existencias_z.append(datos_extras_z['max'])
           existencias_z.append(utils.currency(datos_extras_z['mub']))
           existencias_z.append(datos_extras_z['descri'])
           #End For
        #End if
        exi_z = record[2]
        indice_z = self.alm_exis.index(almrec_z)+1
        existencias_z[indice_z]= utils.IntToStr(utils.StrToInt(existencias_z[indice_z]) + exi_z)
        totexis_z[indice_z]    = utils.IntToStr(utils.StrToInt(totexis_z[indice_z]) + exi_z)
        indice_z = coltotexi_z
        existencias_z[indice_z]= utils.IntToStr(utils.StrToInt(existencias_z[indice_z]) + exi_z)
        totexis_z[indice_z]    = utils.IntToStr(utils.StrToInt(totexis_z[indice_z]) + exi_z)
      # Fin de For
      self.lst_exists.append(existencias_z)
      self.lst_exists.append(totexis_z)
      
# ---Fin de on_btn_okexist_clicked -----

  def busca_datos_extras_inv(self, codigo_z, cia_z):
      datos_extras = { 'codigo':'', 'costou':0.0, 'precio':0.0, 'max':0, 'mub':0.0, 'descri':''}
      sql_z = "select codigo, costos, piva, precio, maximo, descri, fecalta, "
      sql_z = sql_z + "(salvtas + salvtan + salfons + salfonn) as ventas "
      sql_z = sql_z + "from inven where codigo = '" + codigo_z + "' and cia=" + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows <> 0:
         record = record[0] ## Solo Espero un registro
         datos_extras['codigo'] = record[0]
         datos_extras['costou'] = record[1]
         datos_extras['precio'] = record[3]
         datos_extras['max'] = record[4]
         datos_extras['descri'] = record[5]
         fecalta_z = record[6]
         univta_z  = record[7]
         piva_z    = record[2]
         precio_z  = datos_extras['precio']
         costos_z  = datos_extras['costou'] * ( piva_z / 100 + 1)
         datos_extras['mub'] = 100 * (1 -(costos_z / precio_z))
         datos_extras['max'] = utils.inv_maximo(fecalta_z, univta_z, self.hoy_z, self.inianu_z)
      return (datos_extras)
# -- Fin de busca_datos_extras_inv(self, codigo_z, cia_z): --------

  def despliega_observs(self, codigo_z):
      if len(self.lst_observs) <> 0:
         return(0)
      sql_z = "select fecha, observs from observent "
      sql_z = sql_z + " where codigo = '" + codigo_z + "' "
      sql_z = sql_z + " and cia = " + repr(cia_z) + " order by fecha desc, conse"
      self.lst_observs.clear()
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      for record in result:
          fecha_z = utils.DateToStr(record[0])
          observ_z = record[1]
          self.lst_observs.append([fecha_z, observ_z])

# -- Fin de despliega_observs ----

  def busca_vnd(self, hacia_z, codigo_z=''):
      global mydb
      global cia_z
      sql_z = "select codigo,cod2,descri,tipo,prove,linea,empaqe,minimo,maximo,"
      sql_z = sql_z + "precio,piva,costos,coston,inicials,entcoms,entcans,entesps,"
      sql_z = sql_z + "salvtas,salfons,salesps,salmays,existes,inicialn,entcomn,"
      sql_z = sql_z + "entcann,entespn,salvtan,salfonn,salespn,salmayn,existen,"
      sql_z = sql_z + "cosinicials,cosentcoms,cosentcans,cosentesps,cossalvtas,"
      sql_z = sql_z + "cossalfons,cossalesps,cossalmays,cosexistes,cosinicialn,"
      sql_z = sql_z + "cosentcomn,cosentcann,cosentespn,cossalvtan,cossalfonn,"
      sql_z = sql_z + "cossalespn,cossalmayn,cosexisten,fecalta,cia,mds,elec,precelec "
      sql_z = sql_z + "from inven where "
      if hacia_z == 'P':
        sql_z = sql_z + "codigo = ( select min(codigo) from inven where cia = " + repr(cia_z) + ") and cia = " + repr(cia_z)
      elif hacia_z == 'U':
        sql_z = sql_z + "codigo = ( select max(codigo) from inven where cia = " + repr(cia_z) + ") and cia = " + repr(cia_z)
      elif hacia_z == 'A':
        sql_z = sql_z + "codigo = ( select max(codigo) from inven where codigo < '" + codigo_z + "' and cia = " + repr(cia_z) + ") and cia = " + repr(cia_z)
      elif hacia_z == 'S':
        sql_z = sql_z + "codigo = ( select min(codigo) from inven where codigo > '" + codigo_z + "' and cia = " + repr(cia_z) + ") and cia = " + repr(cia_z)
      elif hacia_z == 'D':
        sql_z = sql_z + "codigo = '" + codigo_z + "' and cia = " + repr(cia_z)
      # execute SQL statement
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows <> 0:
        record = record[0] ## Solo Espero un registro
        inven['codigo']        = record[0]
        inven['cod2']          = record[1]
        inven['descri']        = record[2]
        inven['tipo']          = record[3]
        inven['prove']         = record[4]
        inven['linea']         = record[5]
        inven['empaqe']        = record[6]
        inven['minimo']        = record[7]
        inven['maximo']        = record[8]
        inven['precio']        = record[9]
        inven['piva']          = record[10]
        inven['costos']        = record[11]
        inven['coston']        = record[12]
        inven['inicials']      = record[13]
        inven['entcoms']       = record[14]
        inven['entcans']       = record[15]
        inven['entesps']       = record[16]
        inven['salvtas']       = record[17]
        inven['salfons']       = record[18]
        inven['salesps']       = record[19]
        inven['salmays']       = record[20]
        inven['existes']       = record[21]
        inven['inicialn']      = record[22]
        inven['entcomn']       = record[23]
        inven['entcann']       = record[24]
        inven['entespn']       = record[25]
        inven['salvtan']       = record[26]
        inven['salfonn']       = record[27]
        inven['salespn']       = record[28]
        inven['salmayn']       = record[29]
        inven['existen']       = record[30]
        inven['cosinicials']   = record[31]
        inven['cosentcoms']    = record[32]
        inven['cosentcans']    = record[33]
        inven['cosenteps']     = record[34]
        inven['cossalvtas']    = record[35]
        inven['cossalfons']    = record[36]
        inven['cossalesps']    = record[37]
        inven['cossalmays']    = record[38]
        inven['cosexistes']    = record[39]
        inven['cosinicialn']   = record[40]
        inven['cosentcomns']   = record[41]
        inven['cosentcann']    = record[42]
        inven['cosentespn']    = record[43]
        inven['cossalvtan']    = record[44]
        inven['cossalfonn']    = record[45]
        inven['cossalespn']    = record[46]
        inven['cossalmayn']    = record[47]
        inven['cosexisten']    = record[48]
        inven['fecalta']       = record[49]
        inven['cia']           = record[50]
        inven['mds']           = record[51]
        inven['elec']          = record[52]
        inven['precelec']      = record[53]
        self.despliega_datos()

  def despliega_datos(self):
      mubmds_z = 0
      mubfide_z = 0
      codigo_z = inven['codigo'] 
      costosi_z = inven['costos'] 
      costono_z = inven['coston']
      preciomds_z = inven['precio']
      precelec_z = inven['precelec']
      piva_z = inven['piva']
      empaqe_z = inven['empaqe']
      if inven['precio'] <> 0:
         mubmds_z = 100 * (1 -(costono_z / preciomds_z))
        
      if inven['precelec'] <> 0:
         mubfide_z = 100 * (1 - (costono_z / precelec_z))
         
      fecalta_z = inven['fecalta']
      univta_z  = inven['salvtas'] + \
        inven['salvtan'] + inven['salfons'] + inven['salfonn']
      maximo_z = utils.inv_maximo(fecalta_z, univta_z, self.hoy_z, self.inianu_z)
      preciomay_z = utils.calcu_preciomay(empaqe_z, costosi_z, preciomds_z, piva_z)
      preciomayneto_z = preciomay_z * ( 1 + piva_z / 100 )
      mubmay_z = -1
      if preciomds_z <> 0:
        mubmay_z = ( 1 - (preciomayneto_z / preciomds_z) ) * 100;      
      
      sql_z = "select codigo, fecha, precmds, precelec, empqe, observs, cia, fecinivig "
      sql_z = sql_z + "from invulpre where codigo = '" + codigo_z + "' and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows <> 0:
        record = record[0] ## Solo Espero un registro
        invulpre['codigo']    = record[0]
        invulpre['fecha']     = record[1]
        invulpre['precmds']   = record[2]
        invulpre['precelec']  = record[3]
        invulpre['empqe']     = record[4]
        invulpre['observs']   = record[5]
        invulpre['cia']       = record[6]
        invulpre['fecinivig'] = record[7]
        
      fecinivig_z = invulpre['fecinivig'];

      #Voy a buscar la Marca del Articulo
      marca_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_MARCAS)
      diary_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_GPODIARY)
      grupo_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_ARTDESP)
      descrilar_z = def_tablas.busca_rel_inv(mydb, codigo_z, cia_z, def_tablas.REL_INVEN_DESCRILAR)

      inicials_z = '%4d' % int(inven['inicials'])
      entcomps_z = '%4d' % int(inven['entcoms'])
      entcans_z = '%4d' % int(inven['entcans'])
      entesps_z = '%4d' % int(inven['entesps'])
      totents_z = '%4d' % int(( inven['inicials'] + inven['entcoms'] + inven['entcans'] + inven['entesps']))
      salvtas_z = '%4d' % int(inven['salvtas'])
      salfons_z = '%4d' % int(inven['salfons'])
      salesps_z = '%4d' % int(inven['salesps'])
      salmays_z = '%4d' % int(inven['salmays'])
      existes_z = '%4d' % int(inven['existes'])
      inicialn_z = '%4d' % int(inven['inicialn'])
      entcompn_z = '%4d' % int(inven['entcomn'])
      entcann_z = '%4d' % int(inven['entcann'])
      entespn_z = '%4d' % int(inven['entespn'])
      totentn_z = '%4d' % int(( inven['inicialn'] + inven['entcomn'] + inven['entcann'] + inven['entespn']))
      salvtan_z = '%4d' % int(inven['salvtan'])
      salfonn_z = '%4d' % int(inven['salfonn'])
      salespn_z = '%4d' % int(inven['salespn'])
      salmayn_z = '%4d' % int(inven['salmayn'])
      existen_z = '%4d' % int(inven['existen'])

      self.wTree.get_widget("edt_inicials").set_text(inicials_z)
      self.wTree.get_widget("edt_inicialn").set_text(inicialn_z)
      self.wTree.get_widget("edt_entcoms").set_text(entcomps_z)
      self.wTree.get_widget("edt_entcomn").set_text(entcompn_z)
      self.wTree.get_widget("edt_entcans").set_text(entcans_z)
      self.wTree.get_widget("edt_entcann").set_text(entcann_z)
      self.wTree.get_widget("edt_entesps").set_text(entesps_z)
      self.wTree.get_widget("edt_entespn").set_text(entespn_z)
      self.wTree.get_widget("edt_totents").set_text(totents_z)
      self.wTree.get_widget("edt_totentn").set_text(totentn_z)
      self.wTree.get_widget("edt_salvtas").set_text(salvtas_z)
      self.wTree.get_widget("edt_salvtan").set_text(salvtan_z)
      self.wTree.get_widget("edt_salfons").set_text(salfons_z)
      self.wTree.get_widget("edt_salfonn").set_text(salfonn_z)
      self.wTree.get_widget("edt_salesps").set_text(salesps_z)
      self.wTree.get_widget("edt_salespn").set_text(salespn_z)
      self.wTree.get_widget("edt_salmays").set_text(salmays_z)
      self.wTree.get_widget("edt_salmayn").set_text(salmayn_z)
      self.wTree.get_widget("edt_existes").set_text(existes_z)
      self.wTree.get_widget("edt_existen").set_text(existen_z)

      sql_z = "select alm, existes + existen from exist where codigo = '" + codigo_z + "'"
      sql_z = sql_z + " and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      totex_z = 0
      for edt_exialm in self.edt_exis:
          edt_exialm.set_text("")
      for record in result:
          if record[1] <> 0:
             totex_z = totex_z + record[1]
             iii_z = self.alm_exis.index(record[0])
             if iii_z <> -1:
                edt_exialm = self.edt_exis[iii_z]
                edt_exialm.set_text('%4d' % int(record[1]))

      iii_z = self.alm_exis.index("-TOTAL")
      plazomax_z = self.busca_plazomax(codigo_z, preciomds_z)
      if iii_z <> -1:
         edt_exialm = self.edt_exis[iii_z]
         edt_exialm.set_text('%4d' % int(totex_z))
         
      self.wTree.get_widget("edt_codigo").set_text(codigo_z)
      self.wTree.get_widget("edt_descri").set_text(inven['descri'])
      self.wTree.get_widget("edt_grupo").set_text(grupo_z)
      self.wTree.get_widget("edt_ulcampre").set_text(utils.DateToStr(self.inianu_z))
      self.wTree.get_widget("edt_prove").set_text(inven['prove'])
      self.wTree.get_widget("edt_diary").set_text(diary_z)
      self.wTree.get_widget("edt_linea").set_text(inven['linea'])
      self.wTree.get_widget("edt_vigen").set_text(utils.DateToStr(fecinivig_z))
      self.wTree.get_widget("edt_costosi").set_text(utils.currency(inven['costos']))
      self.wTree.get_widget("edt_costono").set_text(utils.currency(inven['coston']))
      self.wTree.get_widget("edt_tipo").set_text(inven['tipo'])
      self.wTree.get_widget("edt_fecalta").set_text(utils.DateToStr(inven['fecalta']))
      self.wTree.get_widget("edt_preciomds").set_text(utils.currency(preciomds_z))
      self.wTree.get_widget("edt_preciofide").set_text(utils.currency(precelec_z))
      self.wTree.get_widget("edt_mubmds").set_text(utils.currency(mubmds_z))
      self.wTree.get_widget("edt_mubfide").set_text(utils.currency(mubfide_z))
      self.wTree.get_widget("edt_min").set_text(repr(inven['minimo']))
      self.wTree.get_widget("edt_max").set_text(repr(maximo_z) + " - " + repr(plazomax_z) )
      self.wTree.get_widget("edt_piva").set_text(utils.currency(piva_z))
      self.wTree.get_widget("edt_situac").set_text(empaqe_z)
      self.wTree.get_widget("edt_preciomay").set_text(utils.currency(preciomay_z))
      self.wTree.get_widget("edt_preciomayneto").set_text(utils.currency(preciomayneto_z))
      self.wTree.get_widget("edt_mubmay").set_text(utils.currency(mubmay_z))
      self.wTree.get_widget("edt_marca").set_text(marca_z)
      self.wTree.get_widget("edt_descri2").set_text(descrilar_z)
      self.wTree.get_widget("edt_codest").set_text(codigo_z)
      self.lst_kardex.clear()
      self.lst_observs.clear()
      self.despliega_datos_tabs(self.wTree.get_widget("notebook_principal").get_current_page())

# --- Fin de despliega_datos ----

  def on_cambio_pagina_notebook(self, widget, page, pagenum):
      self.despliega_datos_tabs(pagenum)
# ---- Fin de on_cambio_pagina_notebook() -----------------

  def despliega_datos_tabs(self, pagina_z):
      codigo_z = inven['codigo'] 
      mitab_z = pagina_z
      #mitab_z = self.wTree.get_widget("notebook_principal").get_current_page()
      if mitab_z == TAB_KARDEX:
         self.despliega_kardex()
      elif mitab_z == TAB_OBSERVS:
        self.despliega_observs(codigo_z)
      elif mitab_z == TAB_DISPONIBLES:
         self.despliega_disponibles()
# ---- Fin de despliega_datos_tabs() -----------------

  def despliega_kardex(self):
      if len(self.lst_kardex) <> 0:
         return(0)
      global cia_z
      global mydb
      alm_z = self.wTree.get_widget("edt_almkdx").get_text().upper()
      codigo_z = inven['codigo']
      self.lst_kardex.clear()
      sql_z = "select codigo,almac,folio,prove,nompro,compro,fecha,costo,"
      sql_z = sql_z + "modsal,modent,nentrada,vienede,folviene,vahacia,folrec,"
      sql_z = sql_z + "salio,fechasal,serie,nsalida"
      sql_z = sql_z + " from movart where "
      sql_z = sql_z + "codigo = '" + codigo_z + "' and almac='" + alm_z + "'" 
      sql_z = sql_z + " and cia=" + repr(cia_z) + " order by folio"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      movart = def_tablas.define_movart()
      for record in result:
           folio_z = record[2]
           movart['folio']      = folio_z
           movart['nompro']     = record[4]
           movart['compro']     = record[5]
           movart['fecha']      = record[6]
           movart['modsal']     = record[8]
           movart['modent']     = record[9]
           movart['nentrada']   = record[10]
           movart['vienede']    = record[11]
           movart['folviene']   = record[12]
           movart['vahacia']    = record[13]
           movart['folrec']     = record[14]
           movart['salio']      = record[15]
           movart['fechasal']   = record[16]
           movart['serie']      = record[17]
           movart['nsalida']    = record[18]
           fecha_z = utils.DateToStr(movart['fecha'])
           modent_z = movart['modent']
           nentrada_z = movart['nentrada']
           vienede_z = movart['vienede']
           if movart['folviene'] <> 0:
             folviene_z = utils.IntToStr(movart['folviene'])
           else:
             folviene_z = ""
           prove_z = def_tablas.busca_dato(mydb, movart['nompro'], CONCEPTOS)
           folio_z = movart['folio']
           serie_z = movart['serie']
           almrec_z = ""
           folrec_z = ""
           if movart['salio'] == "S":
             modsal_z = movart['modsal']
             fecsal_z = utils.DateToStr(movart['fechasal'])
             compro_z = def_tablas.busca_dato(mydb, movart['compro'], CONCEPTOS)
             if movart['vahacia'] <> "":
                almrec_z = movart['vahacia']
                if movart['folrec'] <> 0:
                   folrec_z = utils.IntToStr(movart['folrec'])
                #Fin de if
             #Fin de If
           else:
             modsal_z = ""
             fecsal_z = ""
             compro_z = ""
           #Fin de If
           self.lst_kardex.append([fecha_z, modent_z, nentrada_z, vienede_z, folviene_z,\
           prove_z, folio_z, serie_z, modsal_z, fecsal_z, almrec_z, folrec_z, compro_z])
       # Fin de For
#---- Fin de despliega-Kardex -----------------

  def despliega_disponibles(self):
      if len(self.lst_disponibles) <> 0:
         return(0)
      global cia_z
      global mydb
      #alm_z = self.wTree.get_widget("edt_almkdx").get_text().upper()
      codigo_z = inven['codigo']
      self.lst_disponibles.clear()
      sql_z = "select codigo,almac,folio,prove,nompro,compro,fecha,costo,"
      sql_z = sql_z + "modsal,modent,nentrada,vienede,folviene,vahacia,folrec,"
      sql_z = sql_z + "salio,fechasal,serie,nsalida"
      sql_z = sql_z + " from movart where "
      sql_z = sql_z + "codigo = '" + codigo_z + "' and salio <> 'S'" 
      sql_z = sql_z + " and cia=" + repr(cia_z) + " order by fecha, folio"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      movart = def_tablas.define_movart()
      for record in result:
           folio_z = record[2]
           movart['folio']      = folio_z
           movart['almac']      = record[1]
           movart['nompro']     = record[4]
           movart['compro']     = record[5]
           movart['fecha']      = record[6]
           movart['modsal']     = record[8]
           movart['modent']     = record[9]
           movart['nentrada']   = record[10]
           movart['vienede']    = record[11]
           movart['folviene']   = record[12]
           movart['vahacia']    = record[13]
           movart['folrec']     = record[14]
           movart['salio']      = record[15]
           movart['fechasal']   = record[16]
           movart['serie']      = record[17]
           movart['nsalida']    = record[18]
           fecha_z = utils.DateToStr(movart['fecha'])
           modent_z = movart['modent']
           nentrada_z = movart['nentrada']
           vienede_z = movart['vienede']
           alm_z = movart['almac']
           if movart['folviene'] <> 0:
             folviene_z = utils.IntToStr(movart['folviene'])
           else:
             folviene_z = ""
           prove_z = def_tablas.busca_dato(mydb, movart['nompro'], CONCEPTOS)
           folio_z = movart['folio']
           serie_z = movart['serie']
           almrec_z = ""
           folrec_z = ""
           if movart['salio'] == "S":
             modsal_z = movart['modsal']
             fecsal_z = utils.DateToStr(movart['fechasal'])
             compro_z = def_tablas.busca_dato(mydb, movart['compro'], CONCEPTOS)
             if movart['vahacia'] <> "":
                almrec_z = movart['vahacia']
                if movart['folrec'] <> 0:
                   folrec_z = utils.IntToStr(movart['folrec'])
                #Fin de if
             #Fin de If
           else:
             modsal_z = ""
             fecsal_z = ""
             compro_z = ""
           #Fin de If
           self.lst_disponibles.append([alm_z, fecha_z, modent_z, nentrada_z, vienede_z, folviene_z,\
           prove_z, folio_z, serie_z, modsal_z, fecsal_z, almrec_z, folrec_z, compro_z])
       # Fin de For
#---- Fin de despliega-Disponibles -----------------

  def on_btn_buscaserie_clicked(self, widget):
      global cia_z
      global mydb
      serie_z = self.wTree.get_widget("edt_seriebus").get_text().upper()
      codigo_z = inven['codigo']
      self.lst_busqserie.clear()
      sql_z = "select codigo,almac,folio,prove,nompro,compro,fecha,costo,"
      sql_z = sql_z + "modsal,modent,nentrada,vienede,folviene,vahacia,folrec,"
      sql_z = sql_z + "salio,fechasal,serie,nsalida"
      sql_z = sql_z + " from movart where "
      sql_z = sql_z + "codigo = '" + codigo_z + "' and serie like '" + serie_z + "'"
      sql_z = sql_z + " and cia=" + repr(cia_z) + " order by fecha, folio"
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      result = cursor.fetchall()
      numrows = len(result)
      movart = def_tablas.define_movart()
      for record in result:
           folio_z = record[2]
           movart['folio']      = folio_z
           movart['almac']      = record[1]
           movart['nompro']     = record[4]
           movart['compro']     = record[5]
           movart['fecha']      = record[6]
           movart['modsal']     = record[8]
           movart['modent']     = record[9]
           movart['nentrada']   = record[10]
           movart['vienede']    = record[11]
           movart['folviene']   = record[12]
           movart['vahacia']    = record[13]
           movart['folrec']     = record[14]
           movart['salio']      = record[15]
           movart['fechasal']   = record[16]
           movart['serie']      = record[17]
           movart['nsalida']    = record[18]
           fecha_z = utils.DateToStr(movart['fecha'])
           modent_z = movart['modent']
           nentrada_z = movart['nentrada']
           vienede_z = movart['vienede']
           alm_z = movart['almac']
           if movart['folviene'] <> 0:
             folviene_z = utils.IntToStr(movart['folviene'])
           else:
             folviene_z = ""
           prove_z = def_tablas.busca_dato(mydb, movart['nompro'], CONCEPTOS)
           folio_z = movart['folio']
           serie_z = movart['serie']
           almrec_z = ""
           folrec_z = ""
           if movart['salio'] == "S":
             modsal_z = movart['modsal']
             fecsal_z = utils.DateToStr(movart['fechasal'])
             compro_z = def_tablas.busca_dato(mydb, movart['compro'], CONCEPTOS)
             if movart['vahacia'] <> "":
                almrec_z = movart['vahacia']
                if movart['folrec'] <> 0:
                   folrec_z = utils.IntToStr(movart['folrec'])
                #Fin de if
             #Fin de If
           else:
             modsal_z = ""
             fecsal_z = ""
             compro_z = ""
           #Fin de If
           self.lst_busqserie.append([alm_z, fecha_z, modent_z, nentrada_z, vienede_z, folviene_z,\
           prove_z, folio_z, serie_z, modsal_z, fecsal_z, almrec_z, folrec_z, compro_z])
       # Fin de For
#---- Fin de on_btn_buscaserie_clicked -----------------

  def busca_alm(self, alm_z = ''):
      edt_almkdx  = self.wTree.get_widget("edt_almkdx")
      edt_nombre   = self.wTree.get_widget("edt_nombrealm")
      if alm_z == '':
         alm_z = edt_almkdx.get_text().upper()
         
      sql_z = "select clave, nombre from almreps where clave = '" + alm_z + "' and cia = " + repr(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows <> 0:
        record = record[0] # Solo espero un registro
        almacen['clave']    = record[0]
        almacen['nombre']  = record[1]
        edt_almkdx.set_text(almacen['clave'])
        edt_nombre.set_text(almacen['nombre'])
        resp_z = True
      else:
        sql_z = "select clave, nombre from almreps where cia = " + repr(cia_z) + " order by clave"
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        result_z = cursor.fetchall()
        datosbuscados_z = utils.busca_datos(result_z, "Codigo:Nombre", "Seleccione El Almacen")
        miresp_z = datosbuscados_z.split(":")
        resp_z = utils.StrToInt(miresp_z[-1])
        if resp_z == gtk.RESPONSE_OK:
           almacen['clave']   = miresp_z[0]
           almacen['nombre']  = miresp_z[1]
           edt_almkdx.set_text(almacen['clave'])
           edt_nombre.set_text(almacen['nombre'])
           resp_z = True
        else:
           resp_z = False
        #endif
      #endif  
      return (resp_z)
#------------Fin de busca_alm --------------

# -- Despliega los datos de detalle del folio seleccionado ---
  def on_grd_kardex_activate(self, widget, row=None, value=None):
      colfolio_z = 6
      codigo_z = self.wTree.get_widget("edt_codigo").get_text().upper()
      alm_z = self.wTree.get_widget("edt_almkdx").get_text().upper()
      grd_kardex = widget
      selection = grd_kardex.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          folio_z = utils.StrToInt(self.lst_kardex.get_value(selection_iter, colfolio_z))
          self.despliega_detalle_movart(codigo_z, alm_z, folio_z)

#------------Fin de on_grd_kardex_activate --------------

# -- Despliega los datos del articulo Seleccionado en grd_exists -----------
  def on_grd_exists_activate(self, widget, row=None, value=None):
      colcodigo_z = 0
      grd_exists = self.wTree.get_widget("grd_exists")
      selection = grd_exists.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          codigo_z = self.lst_exists.get_value(selection_iter, colcodigo_z)
          self.busca_vnd("D", codigo_z)

#------------Fin de on_grd_exists_activate --------------


  def despliega_detalle_movart(self, codigo_z, alm_z, folio_z):
      desp_movart = def_tablas.despliega_detalle_movart(mydb, codigo_z, alm_z, folio_z, cia_z)
      resp_z = desp_movart.ejecuta()
#------------Fin de despliega_detalle_movart --------------

  def limpia_campos(self):
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_direc   = self.wTree.get_widget("edt_direc")
      edt_sdoini  = self.wTree.get_widget("edt_sdoini")
      edt_impent  = self.wTree.get_widget("edt_impent")
      edt_impsal  = self.wTree.get_widget("edt_impsal")
      edt_sdofin  = self.wTree.get_widget("edt_sdofin")
      edt_ordiary = self.wTree.get_widget("edt_ordiary")
      edt_exib    = self.wTree.get_widget("edt_exib")
      edt_zona    = self.wTree.get_widget("edt_zona")
      edt_ordtab  = self.wTree.get_widget("edt_ordtab")

      edt_codigo.set_text  ('')
      edt_nombre.set_text  ('')
      edt_direc.set_text   ('')
      edt_sdoini.set_text  ('')
      edt_impent.set_text  ('')
      edt_impsal.set_text  ('')
      edt_sdofin.set_text  ('')
      edt_ordiary.set_text ('')
      edt_zona.set_text    ('')
      edt_ordtab.set_text  ('')
      edt_exib.set_text    ('')

  def editable_onoff(self, modo):
      return (-1)
      edt_codigo  = self.wTree.get_widget("edt_codigo")
      edt_nombre  = self.wTree.get_widget("edt_nombre")
      edt_direc   = self.wTree.get_widget("edt_direc")
      edt_sdoini  = self.wTree.get_widget("edt_sdoini")
      edt_impent  = self.wTree.get_widget("edt_impent")
      edt_impsal  = self.wTree.get_widget("edt_impsal")
      edt_sdofin  = self.wTree.get_widget("edt_sdofin")
      edt_ordiary = self.wTree.get_widget("edt_ordiary")
      edt_exib    = self.wTree.get_widget("edt_exib")
      edt_zona    = self.wTree.get_widget("edt_zona")
      edt_ordtab  = self.wTree.get_widget("edt_ordtab")
      btn_ok      = self.wTree.get_widget("btn_ok")
      btn_cancel  = self.wTree.get_widget("btn_cancel")
      btn_nuevo   = self.wTree.get_widget("btn_nuevo")
      btn_modif   = self.wTree.get_widget("btn_modif")
      btn_borra   = self.wTree.get_widget("btn_borra")
      btn_primero = self.wTree.get_widget("btn_primero")
      btn_anter   = self.wTree.get_widget("btn_anter")
      btn_sigte   = self.wTree.get_widget("btn_sigte")
      btn_ultimo  = self.wTree.get_widget("btn_ultimo")
    
      edt_codigo.set_editable(modo)
      edt_nombre.set_editable(modo)
      edt_direc.set_editable(modo)
      edt_sdoini.set_editable(modo)
      edt_impent.set_editable(modo)
      edt_impsal.set_editable(modo)
      edt_sdofin.set_editable(modo)
      edt_ordiary.set_editable(modo)
      edt_zona.set_editable(modo)
      edt_ordtab.set_editable(modo)
      edt_exib.set_editable(modo)
      btn_ok.set_child_visible(modo)
      btn_cancel.set_child_visible(modo)
      btn_nuevo.set_child_visible(not(modo))
      btn_modif.set_child_visible(not(modo))
      btn_borra.set_child_visible(not(modo))
      btn_primero.set_child_visible(not(modo))
      btn_anter.set_child_visible(not(modo))
      btn_sigte.set_child_visible(not(modo))
      btn_ultimo.set_child_visible(not(modo))


if __name__ == "__main__":
   mimodo_z = ""
   if(len(sys.argv) > 1):
     mimodo_z = sys.argv[1]

   print mimodo_z
   hwg = Altainv()
   hwg.wTree.get_widget("win_altainv").connect("destroy", gtk.main_quit )
   gtk.main()

def main():

    gtk.main()
    return 0
