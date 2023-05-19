# Archivo Definido en Python para las utilerias
# DRBR 14-May-2007
import string, os
import datetime
import pygtk
import gtk
import re
dirprogs_z = ".." + os.sep + "altaalm" + os.sep

EXIT         = 0
CONTINUE     = 1
NUEVO        = 1
MODIFICA     = 2
BORRAR       = 3
NUEVOREN     = 4
ESPERAREN    = 5
LINEAS_X_PAG = 60

grd_lines_soported = ["win32"]
    
def lee_basedato_ini():
    basedato_z = []
    mibd = { 'host':'',
             'user':'',
             'password':'',
             'base':'',
             'tipobd':''
            }

    fh_bd = open('basedato.ini')
    for line in fh_bd.readlines():
        basedato_z.append(string.rstrip(line))
        
    mibd['host']= basedato_z[0]
    mibd['user']= basedato_z[1]
    mibd['password']= basedato_z[2]
    mibd['base']= basedato_z[3]
    mibd['tipobd']= basedato_z[4]
    return mibd

def StrToInt(valor, default=0):
    miint_z = 0
    try:
      miint_z = int(valor)
    except:
      miint_z = default
      
    return(miint_z)

def ValFloat(valor, default=0):
    mifloat_z = 0
    try:
      mifloat_z = float(valor)
    except:
      mifloat_z = default
      
    return(mifloat_z)

def IntToStr(valor):
    mistr_z = 0
    try:
      mistr_z = '%d' % valor
    except:
      mistr_z = "0"
      
    return(mistr_z)
# --- Fin de IntTo Str  -----

def StringOf(char_z, cuantos_z):
    mistr_z = "".ljust(cuantos_z).replace(" ", char_z)
#    mistr_z = mistr_z.replace(" ", char_z)
    return(mistr_z)
# --- Fin de StringOf  -----

def StrToFloat(valor, default=0):
    mifloat_z = 0.0
    try:
      mifloat_z = float(valor.replace(",", ""))
    except:
      mifloat_z = default
      
    return(mifloat_z)

def Porcentaje(valor_z, total_z):
    porc_z = 0
    if total_z <> 0:
       porc_z = valor_z / total_z * 100
    cosstr_z = currency(porc_z)
    if len(cosstr_z) > 5:
       cosstr_z = cosstr_z[:5]
    return (cosstr_z)

def StrToDate(fecha, default=0):
    mifecha_z = datetime.date.today()
    mianu_z = 0
    mimes_z = 0
    midia_z = 0
    mianu_z = StrToInt(fecha[6:10])
    mimes_z = StrToInt(fecha[3:5])
    midia_z = StrToInt(fecha[0:2])
    try:
      mifecha_z = datetime.date(mianu_z, mimes_z, midia_z)
    except:
      mifecha_z = -1
    return(mifecha_z)

def Fecha_a_Perio(fecha):
    anu_z = fecha.year
    mes_z = fecha.month
    perio_z = chr(anu_z - 1999 + 65 ) + "%2d" % mes_z 
    return (perio_z)

def Perio_a_Fecha (perio):
    if len(perio) > 3:
       fecha_z = -1
    else:
      anu_z = ord(perio[0]) + 1999 - 65
      hoy_z = datetime.date.today()
      if hoy_z.day > 28:
         fecha_z = UltimoDeMes(StrToDate("01/"+perio[1:]+"/"+str(anu_z)))
      else:
         fecha_z = StrToDate(str(hoy_z.day).rjust(2)+"/"+perio[1:]+"/"+str(anu_z))
    #End If
    return (fecha_z)

def DateToStr(fecha, formato_z='%d/%m/%Y'):
    try:
      mifecha_z = fecha.strftime(formato_z)
    except:
      mifecha_z = "  /  /"
    return(mifecha_z)

def PrimeroDeMes(fecha, formato_z='%m/%Y'):
    try:
      mifecha_z = StrToDate("01/"+fecha.strftime(formato_z))
    except:
      mifecha_z = -1
    return(mifecha_z)

def UltimoDiaDeMes(anu_z=0, mes_z=0):
    if mes_z in [ 1, 3, 5, 7, 8, 10, 12]:
       dia_z = 31
    elif mes_z in [ 4, 6, 9, 11]:
       dia_z = 30
    else:
       if anu_z % 4 == 0:
          dia_z = 29
       else:
          dia_z = 28
    return(dia_z)

def FechaValida(anu_z=0, mes_z=0, dia_z=0):
    result_z = True
    if dia_z > 31:
       result_z = False
    elif mes_z in [ 4, 6, 9, 11]:
       if dia_z > 30:
          result_z = False
    elif mes_z == 2:
       if dia_z > 29:
          result_z = False
       elif anu_z % 4 <> 0:
          if dia_z > 28:
             result_z = False
    return(result_z)

def UltimoDeMes(fecha):
    try:
      dia_z = fecha.day
      mes_z = fecha.month
      anu_z = fecha.year
      dia_z = UltimoDiaDeMes(anu_z, mes_z)
      strfecha_z = "%2d/" % dia_z + "%2d/" % mes_z + "%4d/" % anu_z
      mifecha_z = StrToDate(strfecha_z)
    except:
      mifecha_z = -1
    return(mifecha_z)

def NombreMes(fecha):
    dia_z = fecha.day
    mes_z = fecha.month
    anu_z = fecha.year
    meses_z = [ "Enero", "Febrero", "Marzo", "Abril", \
       "Mayo", "Junio", "Julio", "Agosto", "Septiembre", \
       "Octubre", "Noviembre", "Diciembre"]
    nommes_z = meses_z[mes_z - 1]
    return(nommes_z)

def EsUltimoDeMes(fecha):
    result_z = False
    try:
      dia_z = fecha.day
      mes_z = fecha.month
      anu_z = fecha.year
      result_z = False
      if mes_z in [ 1, 3, 5, 7, 8, 10, 12]:
         if dia_z == 31:
            result_z = True
      elif mes_z in [ 4, 6, 9, 11]:
         if dia_z == 30:
            result_z = True
      else:
         if anu_z % 4 == 0:
            if dia_z == 29:
               result_z = True
         else:
            if dia_z == 28:
               result_z = True
    except:
      mifecha_z = -1
    return(result_z)

def SumaMeses(fecha, meses_z=1):
    result_z = False
    esultimodemes_z = EsUltimoDeMes(fecha)
    dia_z = fecha.day
    mes_z = fecha.month
    anu_z = fecha.year
    anuinc_z = int(meses_z / 12.0)
    mesinc_z = int(abs(meses_z) % 12)
    if meses_z < 0:
       mesinc_z = mesinc_z * -1
    mes_z = mes_z + mesinc_z
    if mes_z < 1:
       anuinc_z = anuinc_z -1
       mes_z = 12 + mes_z
    if mes_z > 12:
       anuinc_z = anuinc_z +1
       mes_z = 12 - mes_z
    anu_z = anu_z + anuinc_z
    if not FechaValida(anu_z, mes_z, dia_z):
       dia_z = UltimoDiaDeMes(anu_z, mes_z)
    strfecha_z = "%2d/" % dia_z + "%2d/" % mes_z + "%4d" % anu_z
    mifecha_z = StrToDate(strfecha_z)
    if esultimodemes_z == True:
       mifecha_z = UltimoDeMes(mifecha_z)
    return(mifecha_z)

def msgdlg(mensaje_z):
    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, mensaje_z)
    message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
    message.set_position(gtk.WIN_POS_CENTER)
    message.run()
    message.destroy()
    
def yesnodlg(mensaje_z):
    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, mensaje_z)
    message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
    message.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
    message.set_position(gtk.WIN_POS_CENTER)
    resp_z = message.run()
    message.destroy()
    return(resp_z)

def piderangosdlg(titulo_z, tipo_z, titini_z="", ini_z=0, titfin_z = "", fin_z=0):
      message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, titulo_z)
      vbox_options = gtk.HBox()
      frame = gtk.Frame(titini_z)
      hbox = gtk.VBox()
      adj = gtk.Adjustment(1.0, 1.0, 31.0, 1.0, 5.0, 0.0)
      spin_ini = gtk.SpinButton(adj, 0, 0)
      spin_ini.set_range(ini_z, fin_z)
      hbox.pack_start(spin_ini, True, True)
      spin_ini.show()
      hbox.show()
      frame.add(hbox)
      frame.show()
      vbox_options.pack_start(frame, True, True)
      vbox_options.show()
      frame = gtk.Frame(titfin_z)
      hbox = gtk.VBox()
      adj = gtk.Adjustment(1.0, 1.0, 31.0, 1.0, 5.0, 0.0)
      spin_fin = gtk.SpinButton(adj, 0, 0)
      spin_fin.set_range(ini_z, fin_z)
      spin_fin.set_value(fin_z)
      hbox.pack_start(spin_fin, True, True)
      spin_fin.show()
      hbox.show()
      frame.add(hbox)
      frame.show()
      vbox_options.pack_start(frame, True, True)
      vbox_options.show()
      message.vbox.pack_start(vbox_options, True, True)
      message.vbox.show()
      message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
      message.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
      message.set_position(gtk.WIN_POS_CENTER)
      resp_z = message.run()
      valini_z = spin_ini.get_value()
      valfin_z = spin_fin.get_value()
      respu_z = [ resp_z, valini_z, valfin_z ]
      message.destroy()
      return(respu_z)


def currency(amount):
    temp = "%.2f" % amount
    profile=re.compile(r"(\d)(\d\d\d[.,])")
    while 1:
        temp, count = re.subn(profile,r"\1,\2",temp)
        if not count:
           break
    # optionally adds a dollar sign
    return temp

def canticodif(amount):
    temp = repr(int(amount))
    temp = temp.replace("0", "Z")
    temp = temp.replace("1", "Y")
    temp = temp.replace("2", "X")
    temp = temp.replace("3", "W")
    temp = temp.replace("4", "V")
    temp = temp.replace("5", "U")
    temp = temp.replace("6", "T")
    temp = temp.replace("7", "S")
    temp = temp.replace("8", "R")
    temp = temp.replace("9", "Q")
    return temp

def obten_tipago(tipo_z=''):
    if len(tipo_z) < 1:
       tipo_z = 'E'
         
    if tipo_z[0] == 'C':
       midato_z = 'CAJA AHORRO'
    elif tipo_z[0] == 'A':
       midato_z = 'ACL'
    else:
       midato_z = 'EFECTIVO'
    return (midato_z)

def busca_datos(recordset, titcols_z, titulo_z=''):
    dlg_datosalm = dirprogs_z + "dlg_selalm.glade"
    wTree       = gtk.glade.XML(dlg_datosalm)
    wdlgalm     = wTree.get_widget  ("dlg_selalm")
    grd_almacen = wTree.get_widget  ("grd_almacen")
    #grd_almacen.set_grid_lines(True)
    wdlgalm.set_title(titulo_z)
    titcolumns_z = titcols_z.split(":")
    ncols_z = len(titcolumns_z)
    lista_seleccionados = gtk.ListStore(*[str for col in titcolumns_z])

    grd_almacen.set_model(lista_seleccionados)
    ii_z=0
    for columna_z in titcolumns_z:
        col = gtk.TreeViewColumn(columna_z)
        grd_almacen.append_column(col)
        cell = gtk.CellRendererText()
        col.pack_start(cell, False)
        col.set_attributes(cell, text=ii_z)
        ii_z = ii_z + 1
        
    for record in recordset:
        if ncols_z == 1:
           lista_seleccionados.append([record])
        else:
           lista_seleccionados.append(record)
    resp_z = wdlgalm.run()
    datosresult_z = ""
    if resp_z == gtk.RESPONSE_OK:
       selection = grd_almacen.get_selection()
       # Get the selection iter
       model, selection_iter = selection.get_selected()
       if (selection_iter):
          for ii_z in range(0, ncols_z):
              datosresult_z = datosresult_z + lista_seleccionados.get_value(selection_iter, ii_z) + ":"
          datosresult_z = datosresult_z + repr(resp_z)
    wdlgalm.destroy()
    return(datosresult_z)

class pide_series:
  """Esta es una Clase que pide las Series"""
  def __init__(self, titcols_z='', titulo_z='', folios_z=(), tipo_z="E", cuantos_z=0):
        dlg_series = dirprogs_z + "dlg_series.glade"
        self.cuantos_z = cuantos_z
        self.wTreeSeries       = gtk.glade.XML(dlg_series)
        self.wdlgalm     = self.wTreeSeries.get_widget  ("dlg_series")
        self.grd_seleccionados = self.wTreeSeries.get_widget  ("grd_seleccionados")
        self.grd_disponibles = self.wTreeSeries.get_widget  ("grd_disponibles")
        self.frame_disponibles = self.wTreeSeries.get_widget  ("frame_disponibles")
        self.btnbar_control = self.wTreeSeries.get_widget  ("btnbar_control")
        btn_modifserie = self.wTreeSeries.get_widget  ("btn_modifserie")
        box_contenedor = self.wTreeSeries.get_widget  ("box_contenedor")
        if tipo_z == "E":
           box_contenedor.remove(self.frame_disponibles)
           box_contenedor.remove(self.btnbar_control)
        else:
           btn_tomatodos=self.wTreeSeries.get_widget  ("btn_tomatodos")
           btn_tomauno=self.wTreeSeries.get_widget  ("btn_tomauno")
           btn_qitatodos=self.wTreeSeries.get_widget  ("btn_qitatodos")
           btn_qitauno=self.wTreeSeries.get_widget  ("btn_qitauno")
           btn_tomatodos.connect("clicked", self.btn_tomatodos_clicked)
           btn_tomauno.connect  ("clicked", self.btn_tomauno_clicked)
           btn_qitatodos.connect("clicked", self.btn_qitatodos_clicked)
           btn_qitauno.connect  ("clicked", self.btn_qitauno_clicked)
           
        #grd_seleccionados.set_grid_lines(True)
        self.wdlgalm.set_title(titulo_z)
        titcolumns_z = titcols_z.split(":")
        miscolumnas_z = []
           
        ii_z=0
        for columna_z in titcolumns_z:
            miscolumnas_z.append(str)
            col = gtk.TreeViewColumn(columna_z)
            self.grd_seleccionados.append_column(col)
            cell = gtk.CellRendererText()
            col.pack_start(cell, False)
            col.set_attributes(cell, text=ii_z)
            
            col = gtk.TreeViewColumn(columna_z)
            self.grd_disponibles.append_column(col)
            cell = gtk.CellRendererText()
            col.pack_start(cell, False)
            col.set_attributes(cell, text=ii_z)
            ii_z = ii_z + 1
        self.lista_seleccionados = gtk.ListStore(*[col for col in miscolumnas_z])
        self.lista_disponibles = gtk.ListStore(*[col for col in miscolumnas_z])
        self.grd_seleccionados.set_model(self.lista_seleccionados)
        self.grd_disponibles.set_model(self.lista_disponibles)

        for datos in folios_z:
            if tipo_z == "E":
               self.lista_seleccionados.append(datos)
            else:
               self.lista_disponibles.append(datos)
               
        self.grd_seleccionados.connect("cursor-changed", self.ren_serie_selec)
        btn_modifserie.connect("clicked", self.btn_modifserie_clicked)
        self.wTreeSeries.get_widget("edt_serie").connect("activate", self.btn_modifserie_clicked)

  def ejecuta(self):
        resp_z = self.wdlgalm.run()
        folios_z=[]
        datosresult_z = ""
        if resp_z == gtk.RESPONSE_OK:
           for datos in self.lista_seleccionados:
               folios_z.append(datos)
        self.wdlgalm.destroy()
        return(folios_z)

  def ren_serie_selec(self, widget):
      edt_serie    = self.wTreeSeries.get_widget("edt_serie")
      edt_folio    = self.wTreeSeries.get_widget("edt_folio")
      selection = self.grd_seleccionados.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          folio_z = self.lista_seleccionados.get_value(selection_iter, 0)
          serie_z = self.lista_seleccionados.get_value(selection_iter, 1)
          editable_z = self.lista_seleccionados.get_value(selection_iter, 2)
      edt_folio.set_text(folio_z)
      edt_serie.set_text(serie_z)
      self.wTreeSeries.get_widget  ("btn_modifserie").set_child_visible(editable_z == "S")
      edt_serie.set_editable(editable_z == "S")

  def btn_tomatodos_clicked(self, widget):
      self.pasa_la_serie(len(self.lista_disponibles), "AGREGAR")

  def btn_tomauno_clicked(self, widget):
      self.pasa_la_serie(1, "AGREGAR")

  def btn_qitatodos_clicked(self, widget):
      self.pasa_la_serie(len(self.lista_seleccionados), "QUITAR")

  def btn_qitauno_clicked(self, widget):
      self.pasa_la_serie(1, "QUITAR")

  def pasa_la_serie(self, cuantos_z=1, hacia_z=''):
      if hacia_z == "AGREGAR":
         if len(self.lista_seleccionados) >= self.cuantos_z:
            msgdlg("Ya tiene seleccionados todos los que debe");
            return(-1)

         if cuantos_z == 1:
            selection = self.grd_disponibles.get_selection()
            # Get the selection iter
            model, selection_iter = selection.get_selected()
            if (selection_iter):
               folio_z = self.lista_disponibles.get_value(selection_iter, 0)
               serie_z = self.lista_disponibles.get_value(selection_iter, 1)
               editable_z = self.lista_disponibles.get_value(selection_iter, 2)
               self.lista_seleccionados.append([folio_z, serie_z, editable_z])
               self.lista_disponibles.remove(selection_iter)
            # Fin de If Iter 
         else:
            for midato_z in self.lista_disponibles:
               if len(self.lista_seleccionados) < self.cuantos_z:
                 folio_z = midato_z[0]
                 serie_z = midato_z[1]
                 editable_z = midato_z[2]
                 self.lista_seleccionados.append([folio_z, serie_z, editable_z])
               #Fin de if
            # Fin de for
            self.lista_disponibles.clear()
         # Fin de If cuantos
      else:
         if cuantos_z == 1:
            selection = self.grd_seleccionados.get_selection()
            # Get the selection iter
            model, selection_iter = selection.get_selected()
            if (selection_iter):
               folio_z = self.lista_seleccionados.get_value(selection_iter, 0)
               serie_z = self.lista_seleccionados.get_value(selection_iter, 1)
               editable_z = self.lista_seleccionados.get_value(selection_iter, 2)
               self.lista_disponibles.append([folio_z, serie_z, editable_z])
               self.lista_seleccionados.remove(selection_iter)
            # Fin de If Iter 
         else:
            for midato_z in self.lista_seleccionados:
                folio_z = midato_z[0]
                serie_z = midato_z[1]
                editable_z = midato_z[2]
                self.lista_disponibles.append([folio_z, serie_z, editable_z])
            #Fin de for
            self.lista_seleccionados.clear()
         # Fin de If cuantos
      #Fin de If Izq o Der 

  def btn_modifserie_clicked(self, widget):
      edt_serie    = self.wTreeSeries.get_widget("edt_serie")
      serie_z = edt_serie.get_text().upper()
      selection = self.grd_seleccionados.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          self.lista_seleccionados.set_value(selection_iter, 1, serie_z)

# Fin de Clase pide Series

class visor_editor:
  """Esta es una Clase que muestra un archivo de Texto"""
  def __init__(self):
        dlg_impri = dirprogs_z + "visortex.glade"
        self.wTreeSeries       = gtk.glade.XML(dlg_impri)
        self.wdlgalm     = self.wTreeSeries.get_widget  ("dlg_impri")

  def ejecuta(self, archivo_z):
        self.wdlgalm     = self.wTreeSeries.get_widget  ("dlg_impri")
        self.wdlgalm.set_title(archivo_z)
        fh_arch = open(archivo_z)
        mislineas_z = fh_arch.read()
        textview = self.wTreeSeries.get_widget  ("text_vista")
        buffer_z = gtk.TextBuffer()
        buffer_z.set_text(mislineas_z)
        tag=buffer_z.create_tag("default")
        tag.set_property("font", "lucida console 10" )
        start, end=buffer_z.get_bounds()
        buffer_z.apply_tag_by_name("default",start,end)
        #textview.modify_font("luxi mono 12")
        textview.set_buffer(buffer_z)
        resp_z = self.wdlgalm.run()
        folios_z=[]
        datosresult_z = ""
        if resp_z == gtk.RESPONSE_OK:
           cmd_z = "copy " + archivo_z + " \\\\rosario\\epsnfx1180"
           print cmd_z
           os.system(cmd_z)
        self.wdlgalm.destroy()
        return(resp_z)

# Fin de Clase Visor Editor


def inv_maximo (fecalta_z, univta_z, hoy_z, inianu_z):
  maxim_z=0
  diasdif_z=1
  fecini_z = inianu_z
  strfecalta_z = DateToStr(fecalta_z, "%Y%m%d")
  strinianu_z = DateToStr(inianu_z, "%Y%m%d")
  if strfecalta_z > strinianu_z:
     fecini_z = fecalta_z
  diasdif_z = (hoy_z - fecini_z).days
  if diasdif_z  <= 0:
     diasdif_z = 1
  maxim_z = int(65 * univta_z /diasdif_z)
  return(maxim_z)
#---------------------------------------------------------------------------

def elimina_car_esp(cadena_z):
  cadena_z = cadena_z.replace("/", "_")
  cadena_z = cadena_z.replace("\#", "_")
  cadena_z = cadena_z.replace("\\", "_")
  cadena_z = cadena_z.replace("\'", "_")
  cadena_z = cadena_z.replace("\"", "_")
  return (cadena_z)
#---------------------------------------------------------------------------

def convierte_string(cadena_z):
  if (cadena_z == None):
     cadena_z = ""
  #End if
  return (cadena_z)
#---------------------------------------------------------------------------

def  calcu_preciomay(empaqe_z, costo_z, preciou_z, piva_z):
  factor_z=0;
  costoneto_z=0
  mub_z=0
  costoneto_z = costo_z * ( piva_z / 100 + 1 )
  if(empaqe_z == "SUNTUARIO"):
    factor_z = .6 / .64;
  else:
    if preciou_z <> 0:
       mub_z =  ( 1 - ( costoneto_z / preciou_z  ) ) * 100
    if mub_z < 39:
      preciou_z = costoneto_z / .94
      factor_z = 1
    elif mub_z < 41:
      factor_z = .645
    elif mub_z < 43:
      factor_z = .63
    elif mub_z < 45:
      factor_z = .62
    elif mub_z < 47:
      factor_z = .61
    else:
      factor_z =  .60
  
  preciou_z = round(( preciou_z * factor_z ) / ( piva_z / 100 + 1), 2)
  return (preciou_z)
#//---------------------------------------------------------------------------

class pide_series_mayoreo:
  """Esta es una Clase que pide las Series"""
  def __init__(self, titcols_z='', titulo_z='', folios_z=(), editable_z="S", cuantos_z=0):
        dlg_series = dirprogs_z + "dlg_seriesmay.glade"
        self.cuantos_z = cuantos_z
        self.wTreeSeries       = gtk.glade.XML(dlg_series)
        self.wdlgalm     = self.wTreeSeries.get_widget  ("dlg_seriesmay")
        self.grd_seleccionados = self.wTreeSeries.get_widget  ("grd_seleccionados")
        #self.grd_disponibles = self.wTreeSeries.get_widget  ("grd_disponibles")
        self.btnbar_control = self.wTreeSeries.get_widget  ("btnbar_control")
        box_contenedor = self.wTreeSeries.get_widget  ("box_contenedor")
        #btn_tomatodos=self.wTreeSeries.get_widget  ("btn_tomatodos")
        btn_tomauno=self.wTreeSeries.get_widget  ("btn_tomauno")
        #btn_qitatodos=self.wTreeSeries.get_widget  ("btn_qitatodos")
        btn_quitauno=self.wTreeSeries.get_widget  ("btn_quitauno")
        btn_tomauno.set_child_visible(editable_z == "S")
        btn_quitauno.set_child_visible(editable_z == "S")
        if editable_z == "S":
           #btn_tomatodos.connect("clicked", self.btn_tomatodos_clicked)
           btn_tomauno.connect  ("clicked", self.btn_tomauno_clicked)
           #btn_qitatodos.connect("clicked", self.btn_qitatodos_clicked)
           btn_quitauno.connect  ("clicked", self.btn_quitauno_clicked)
        #End If
        self.wTreeSeries.get_widget("btn_serie").connect("clicked", self.btn_serie_clicked)
           
        #grd_seleccionados.set_grid_lines(True)
        self.wdlgalm.set_title(titulo_z)
        titcolumns_z = titcols_z.split(":")
        miscolumnas_z = []
           
        ii_z=0
        for columna_z in titcolumns_z:
            miscolumnas_z.append(str)
            col = gtk.TreeViewColumn(columna_z)
            self.grd_seleccionados.append_column(col)
            cell = gtk.CellRendererText()
            col.pack_start(cell, False)
            col.set_attributes(cell, text=ii_z)
            
            #col = gtk.TreeViewColumn(columna_z)
            #self.grd_disponibles.append_column(col)
            #cell = gtk.CellRendererText()
            #col.pack_start(cell, False)
            #col.set_attributes(cell, text=ii_z)
            ii_z = ii_z + 1
        self.lista_seleccionados = gtk.ListStore(*[col for col in miscolumnas_z])
        #self.lista_disponibles = gtk.ListStore(*[col for col in miscolumnas_z])
        self.grd_seleccionados.set_model(self.lista_seleccionados)
        #self.grd_disponibles.set_model(self.lista_disponibles)

        for datos in folios_z:
            self.lista_seleccionados.append(datos)
               
        self.grd_seleccionados.connect("cursor-changed", self.ren_serie_selec)
        #btn_modifserie.connect("clicked", self.btn_modifserie_clicked)
        self.wTreeSeries.get_widget("edt_serie").connect("activate", self.btn_tomauno_clicked)

  def ejecuta(self):
        resp_z = self.wdlgalm.run()
        valdev_z = []
        folios_z=[]
        datosresult_z = ""
        if resp_z == gtk.RESPONSE_OK:
           for datos in self.lista_seleccionados:
               folios_z.append(datos)
           #End For
           #Agrego al Final la respuesta
        self.wdlgalm.destroy()
        valdev_z.append ([ folios_z, resp_z])
        return(valdev_z)

  def ren_serie_selec(self, widget):
      edt_serie    = self.wTreeSeries.get_widget("edt_serie")
      #edt_folio    = self.wTreeSeries.get_widget("edt_folio")
      selection = self.grd_seleccionados.get_selection()
      # Get the selection iter
      model, selection_iter = selection.get_selected()
      if (selection_iter):
          folio_z = self.lista_seleccionados.get_value(selection_iter, 0)
          serie_z = self.lista_seleccionados.get_value(selection_iter, 1)
          editable_z = self.lista_seleccionados.get_value(selection_iter, 2)
      #edt_folio.set_text(folio_z)
      edt_serie.set_text(serie_z)
      #self.wTreeSeries.get_widget  ("btn_modifserie").set_child_visible(editable_z == "S")
      edt_serie.set_editable(editable_z == "S")

  def btn_tomauno_clicked(self, widget):
      self.pasa_la_serie(1, "AGREGAR")

  def btn_quitauno_clicked(self, widget):
      self.pasa_la_serie(1, "QUITAR")

  def btn_serie_clicked(self, widget):
      self.wTreeSeries.get_widget("edt_serie").grab_focus()

  def pasa_la_serie(self, cuantos_z=1, hacia_z=''):
      if hacia_z == "AGREGAR":
         if len(self.lista_seleccionados) >= self.cuantos_z:
            msgdlg("Ya tiene seleccionados todos los que debe");
            return(-1)

         if cuantos_z == 1:
            sigte_z = len(self.lista_seleccionados) + 1
            serie_z = self.wTreeSeries.get_widget("edt_serie").get_text().upper()
            self.lista_seleccionados.append([sigte_z, serie_z, "S"])
            #self.lista_disponibles.remove(selection_iter)
         #End If
      elif hacia_z == "QUITAR":
         if cuantos_z == 1:
            selection = self.grd_seleccionados.get_selection()
            # Get the selection iter
            model, selection_iter = selection.get_selected()
            if (selection_iter):
               folio_z = self.lista_seleccionados.get_value(selection_iter, 0)
               serie_z = self.lista_seleccionados.get_value(selection_iter, 1)
               editable_z = self.lista_seleccionados.get_value(selection_iter, 2)
               self.lista_seleccionados.remove(selection_iter)
            # Fin de If Iter 
         else:
            for midato_z in self.lista_seleccionados:
                folio_z = midato_z[0]
                serie_z = midato_z[1]
                editable_z = midato_z[2]
                self.lista_disponibles.append([folio_z, serie_z, editable_z])
            #Fin de for
            self.lista_seleccionados.clear()
         # Fin de If cuantos
      #Fin de If Izq o Der 

# Fin de Clase pide Series Mayoreo
