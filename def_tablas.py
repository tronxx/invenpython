# Archivo Definido en Python para las tablas de Inven
# DRBR 14-May-2007
import string, os
import datetime
import pygtk
import gtk
import re
import utils
import types
ENTRADAS     = 1
RENENTRA     = 2
POBLACIONES  = 3
CONCEPTOS    = 4
ALMACEN      = 5
PTOVTA       = 6
VENDEDOR     = 7
CREDCON      = 8
LINEA        = 9
PROVEEDOR    = 10
PLANESP      = 11
ENTPAG       = 12
MVENTPAG     = 13
OBSERVENT    = 14
MAYORIS      = 15
FACTURMA     = 16
RENFACMA     = 17
MOVMAY       = 18
POLCOB       = 19
INV_CONCEPS  = 20
RENPOLCO     = 21
CONSE_RENPOLCO = 22
CONSE_MOVMAY = 23
FOLIO_POLCOB = 24
INVEN        = 25
ZONASINVEN   = 26
GPOARTDESP   = 27
MARCAS       = 28
DIARY        = 29
SITUACIONES  = 30
INV_MARCAS   = 31
INV_GRUPOS   = 32
GPODIARY     = 33
INV_SITUACIONES  = 34
INV_POLCAMPRE    = 35
INV_RENPOLCAMPRE = 36
INV_INVHIST      = 37
INV_INVHIST_CODIGO = 38
FOLIO_POLCAMPRE    = 39
INVULPRE           = 40
INV_RELINV         = 41

POLCAMPRE_STATUS_ABIERTO = 1
POLCAMPRE_STATUS_CERRADO = 2
INV_TIPOPRE_PLAZO_LINEA  = 1
INV_TIPOPRE_PLAZO_PRECIO = 2
INV_TIPOPRE_PLAZO_ARTICULO  = 3

dirprogs_z = ".." + os.sep + "altaalm" + os.sep

REL_INVEN_ARTDESP                = 1
REL_INVEN_PROVE                  = 2
REL_INVEN_LINEA                  = 3
REL_INVEN_SITUACION              = 4
REL_INVEN_GPODIARY               = 5
REL_INVEN_MARCAS                 = 6
REL_INVEN_DESCRILAR              = 7
REL_INVEN_GRUPOS_INTERNET        = 10
REL_SERIES_RENENTRA              = 101
REL_SERIES_KARDEX                = 102
REL_SERIES_EXIST_DISP            = 103
REL_SERIES_REN_FACMA             = 104
TIPO_INV_SERVICIO_SERIESAUMENTADAS = 3

TIPO_PLAZO_LINEA                 = 1
TIPO_PLAZO_PRECIO                = 2
TIPO_PLAZO_ARTICULO              = 3
TIPO_PLAZO_LINEA_PRIORIDAD       = 11
TIPO_PLAZO_LINEA_X_TABLA         = 12
TIPO_PLAZO_LINEA_X_GRUPO         = 13
TIPO_PLAZO_X_GRUPOX_TABLA        = 14
TIPO_PLAZO_GRUPO_PRIORIDAD       = 15
TIPO_PLAZO_GRUPO                 = 16


def tipoentra(tipo_z):
    tiposentrada_z = []
    tiposentrada_z.append( (05, 'T', 'Traspasos/Almacenes') )
    tiposentrada_z.append( (10, 'D', 'Devoulciones/Almacenes'))
    tiposentrada_z.append( (15, 'S', 'Salidas especiales'))
    tiposentrada_z.append( (20, 'V', 'Salidas por Sabanas'))
    tiposentrada_z.append( (25, 'C', 'Entradas por Cancelacion'))
    tiposentrada_z.append( (30, 'P', 'Entradas Especiales'))
    tiposentrada_z.append( (35, 'F', 'Salidas por Sabana Fonacot'))
    tiposentrada_z.append( (40, 'O', 'Cancelaciones Fonacot'))
    tiposentrada_z.append( (45, 'M', 'Salidas de Mayoreo'))
    tiposentrada_z.append( (50, 'Y', 'Cancelaciones Mayoreo'))
    tiposentrada_z.append( (55, 'L', 'Devoluciones S/Ventas'))
    tiposentrada_z.append( (60, 'I', 'Movimientos Internos'))
    tiposentrada_z.append( (65, 'X', 'Cancelacion x Cambio Tradicional'))
    tiposentrada_z.append( (70, 'N', 'Cancelacion x Cambio Fonacot'))
    tiposentrada_z.append( (75, 'E', 'Entradas Proveedor'))
    tiposentrada_z.append( (80, 'R', 'Devoluciones a Proveedor'))
    tiposentrada_z.append( (85, 'A', 'Inventario Inicial'))
    tiposentrada_z.append( (90, 'B', 'Pedidos a Proveedor'))
    tiposentrada_z.append( (95, 'G', 'Pedidos de Mayoreo'))
    tiposentrada_z.append( (100, 'H', 'Salidas x Sabana FIDE'))
    tiposentrada_z.append( (105, 'J', 'Cancelacion FIDE'))
    tiposentrada_z.append( (110, 'Q', 'Salidas x Sabana Celulares'))
    tiposentrada_z.append( (115, 'U', 'Cancelacion Celulares'))
    tiposentrada_z.append( (120, 'K', 'Cancelacion x Cambio FIDE'))
    tiposentrada_z.append( (125, 'W', 'Cancelacion x Cambio Celulares'))
    tiposentrada_z.append( (130, '1', 'Ventas Imevi'))
    tiposentrada_z.append( (135, '2', 'Cancelacion Imevi'))
    tiposentrada_z.append( (140, '3', 'Cancelacion x Cambio Imevi'))

    for dato_z in tiposentrada_z:
        if dato_z[1] == tipo_z:
           midato_z = dato_z;
    return (midato_z)

def define_inv_relinv():
    inv_relinv = {
      'idrelinv':0,
      'idart':0,
      'idrel':0,
      'iddato':0,
      'conse':0
    }
    return (inv_relinv)
#Fin de define_inv_relinv


def define_invulpre():
    invulpre = {
       'codigo':'',
       'fecha':datetime.date.today(),
       'precmds':0.0,
       'precelec':0.0,
       'empqe':'',
       'observs':'',
       'cia':0,
       'fecinivig':datetime.date.today()
    }
    return(invulpre)
#Fin define invulpre
   
def define_inv_polcampre():
    inv_polcampre = {
       'idpolcampre':0,
       'folio':0,
       'fecha':datetime.date.today(),
       'fecini':datetime.date.today(),
       'idusuario':0,
       'status':0,
       'idconcep':0,
       'cia':0
    }
    return (inv_polcampre)

def define_inv_renpolcampre():
    inv_renpolcampre = {
       'idrenpolcampre':0,
       'idpolcampre':0,
       'idart':0,
       'antprmds':0.0,
       'antprecelec':0.0,
       'precmds':0.0,
       'precelec':0.0,
       'antempaq':0,
       'nvoempaq':0,
       'idobserv':0
    }
    return (inv_renpolcampre)

def define_proveedor():
     proveedor = {
       'codigo':'',
       'nombre':'',
       'direc':'',
       'ciu':'',
       'rfc':'',
       'tel':'',
       'cargos':0.0,
       'abonos':0.0,
       'compraanu':0.0,
       'comprames':0.0,
       'limite':0.0,
       'contacto':'',
       'ultmov':0,
       'status':'',
       'cia':0
     }
     return (proveedor)
#Fin define_proveedor

def define_poblacs():
    poblacs = { 'nombre':'',
              'numero':0
    }
    return (poblacs)
#Fin define_poblacs

def define_inv_marcas():
	inv_marcas = {
	   'idmarcainv':0,
	   'codigo':'',
	   'marca':''
	}
	return (inv_marcas)
#Fin define_inv_marcas():

def define_zonainv():
    zonainv = { 'zona':'',
              'nombre':'',
              'tipo':''
    }
    return (zonainv)
#Fin define_zonainv

def define_facturma():
    facturma = { 'num':0,
             'mayoris':'',
             'refer':'',
             'nomay':'',
             'dir':'',
             'rfc':'',
             'status':'',
             'fecha':datetime.date.today(),
             'vence':datetime.date.today(),
             'importe':0.0,
             'descu':0.0,
             'neto':0.0,
             'iva':0.0,
             'total':0.0,
             'cia':0,
             'npagos':0,
             'plazo':0,
             'tipago':'',
             'pdsc':0.0,
             'mayomen':''
  	        }
    return (facturma)
#Fin define_facturma

def define_renfacma():
    renfacma = { 'factur':0,
             'consec':0,
             'codigo':'',
             'descri':'',
             'unids':0.0,
             'preciou':0.0,
             'importe':0.0,
             'pordsc':0.0,
             'descu':0.0,
             'poriva':0.0,
             'iva':0.0,
             'total':0.0,
             'costou':0.0,
             'cia':0
	        }
    return (renfacma)
#Fin define_renfacma

def define_polcob():
    polcob = { 'alm':'',
             'fecha':datetime.date.today(),
             'importe':0.0,
             'status':'',
             'cia':0,
             'idpolcob':0,
             'folio':0,
             'idconcep':0
	        }
    return (polcob)
#Fin define_polcob

def define_renpolco():
    renpolco = { 'alm':'',
             'fecha':datetime.date.today(),
             'numren':0,
             'docto':0,
             'refer':'',
             'numren':0,
             'concep':'',
             'importe':0.0,
             'cliente':'',
             'letra':0,
             'cia':0,
             'tipago':'',
             'idpolcob':0,
             'idpolcob':0,
             'folio':0,
             'idrenpolco':0,
             'idconcep':0
	        }
    return (renpolco)
#Fin define_renpolco

def define_movmay():
    movmay = { 'mayoris':'',
             'docto':0,
             'pagare':0,
             'conse':0,
             'fecha':datetime.date.today(),
             'vence':datetime.date.today(),
             'concep':'',
             'coa':'',
             'importe':0.0,
             'saldo':0.0,
             'cia':0,
             'tipago':'',
             'idconcep':0,
             'fecsal':datetime.date.today(),
             'idmov':0
	        }
    return (movmay)
#Fin define_movmay

def define_edomay():
    movmay = { 'fecha':datetime.date.today(),
             'compras':0.0,
             'abonos':0.0,
             'devols':0.0,
             'sdofin':0.0,
             'cia':0,
             'mayoris':'',
             'bonif':0.0,
             'vencant':0.0,
             'vencrec':0.0,
             'porvenc':0.0,
             'cobinterna':0.0,
             'cartera':0.0
	        }
    return (edomay)
#Fin define_edomay

def define_mayoris():
    mayoris = { 'codigo':'',
              'nombre':'',
              'direc':'',
              'ciu':'',
              'rfc':'',
              'tel':'',
              'cargos':0.0,
              'abonos':0.0,
              'compraanu':0.0,
              'comprames':0.0,
              'pdsc':0.0,
              'ultmov':0,
              'status':'',
              'cia':0,
              'nompag1':'',
              'nompag2':'',
              'dirpag1':'',
              'dirpag2':'',
              'ciupag':'',
              'nombre2':''
    }
    return (mayoris)
    
def define_prove():
    prove  =   {'codigo': '',
            'nombre': '',
            'direc': '',
            'ciu': '',
            'rfc': '',
            'tel': '',
            'cargos': 0,
            'abonos': 0,
            'compraanu': 0,
            'comprames': 0,
            'limite': 0,
            'contacto': '',
            'ultmov': 0,
            'status': '',
            'cia': 0
           }
    return (prove)

def define_estadis():
    estadis =   {'tipo': 0,
            'codigo': '',
            'alm': '',
            'anu': 0,
            'mes': 0,
            'unidades': 0,
            'importe': 0.0,
            'cia': 0
           }
    return (estadis)

def define_cias():
    cias = {'cia':'',
	'razon':'',
        'dir':'',
        'dir2':'',
        'nomfis':'',
        'tel':'',
        'fax':'',
        'rfc':''
        }
    return (cias)

def define_almacen():
    almacen = {'clave': '',
            'nombre': '',
            'direc': '',
            'sdoini': 0,
            'impent': 0,
            'impsal': 0,
            'sdofin': 0,
            'cia': 0,
            'ordiary': '',
            'exib': '',
            'zona': '',
            'ordtab': ''
           }
    return (almacen)

def define_ptovta():
    ptovta = {'clave': '',
            'nombre': '',
            'direc': '',
            'sdoini': 0,
            'impent': 0,
            'impsal': 0,
            'sdofin': 0,
            'cia': 0,
            'ordiary': ''
            }
    return (ptovta)

def define_marcainv():
   marcainv = {'idmarcainv': 0,
           'codigo': '',
           'marca': ''
           }
   return (marcainv)

def define_observent():
    observent = {
      'tipo':'',
      'alm':'',
      'numero':0,
      'fecha':datetime.date.today(),
      'conse':0,
      'observs':'',
      'cia':0,
      'codigo':''
    }
    return (observent)

def define_invulpre():
   invulpre = { 'codigo':'',
       'fecha': datetime.date.today(),
       'precmds': 0.0,
       'precelec': 0.0,
       'empqe':'',
       'observs':'',
       'cia':0
   }
   return (invulpre)

def define_vendedor():
    vendedor = {'codigo': '',
            'nombre': ''
           }
    return (vendedor)

def define_invulpre():
    invulpre = { 'codigo':'',
        'fecha': datetime.date.today(),
        'precmds': 0.0,
        'precelec': 0.0,
        'empqe':'',
        'observs':'',
        'cia':0
    }
    return (invulpre)

def define_entradas():
    entradas = {
        'tipo':'',
        'alm':'',
        'recemi':'',
        'numero':0,
        'facpro':'',
        'prove':'',
        'perenvrec':'',
        'status':'',
        'coniva':'',
        'fecha': datetime.date.today(),
        'importe':0.0,
        'iva':0.00,
        'total':0.0,
        'vence': datetime.date.today(),
        'ctofin':0.0,
        'tascomp':0.0,
	      'taspro':0.0,
        'fechafac':datetime.date.today(),
	      'letras':0,
	      'plazocfp':'',
	      'planp':0,
	      'fletes':0.0,
	      'desxap':0.0,
	      'fechaprp': datetime.date.today(),
	      'ctofincomp':0.0,
	      'usuario':'',
        'cia':0
	}
    return (entradas)

def define_renentra():
    renentra = {
       'tipo':'',
       'alm':'',
       'recemi':'',
       'numero':0,
       'conse':0,
       'codinv':'',
       'serie':'',
       'siono':'',
       'folsal':0,
       'folent':0,
       'unids':0,
       'costou':0,
       'piva':0,
       'importe':0,
       'cantmueve':0,
       'status':'',
       'persenvrec':0,
       'cia':0,
       'vend':'',
       'poblac':0,
       'tipago':'',
       'prvta':0,
       'entosal':'',
       'entcan':''
    }
    return (renentra)

def define_inven():
    inven = {
       'codigo':'',
       'cod2':'',
       'descri':'',
       'tipo':'',
       'prove':'',
       'linea':'',
       'empaqe':'',
       'minimo':0,
       'maximo':0,
       'precio':0.0,
       'piva':0.00,
       'costos':0.0,
       'coston':0.0,
       'inicials':0.0,
       'entcoms':0.0,
       'entcans':0.0,
       'entesps':0.0,
       'salvtas':0.0,
       'salfons':0.0,
       'salesps':0.0,
       'salmays':0.0,
       'existes':0.0,
       'inicialn':0.0,
       'entcomn':0.0,
       'entcann':0.0,
       'entespn':0.0,
       'salvtan':0.0,
       'salfonn':0.0,
       'salespn':0.0,
       'salmayn':0.0,
       'existen':0.0,
       'cosinicials':0.0,
       'cosentcoms':0.0,
       'cosentcans':0.0,
       'cosentesps':0.0,
       'cossalvtas':0.0,
       'cossalfons':0.0,
       'cossalesps':0.0,
       'cossalmays':0.0,
       'cosexistes':0.0,
       'cosinicialn':0.0,
       'cosentcomn':0.0,
       'cosentcann':0.0,
       'cosentespn':0.0,
       'cossalvtan':0.0,
       'cossalfonn':0.0,
       'cossalespn':0.0,
       'cossalmayn':0.0,
       'cosexisten':0.0,
       'fecalta':datetime.date.today(),
       'cia':0,
       'mds':'',
       'elec':'',
       'precelec':0.0
    }
    return (inven)
    
def define_exist():
    exist = {
       'codigo':'',
       'alm':'',
       'inicials':0.0,
       'entcoms':0.0,
       'entcans':0.0,
       'entesps':0.0,
       'salvtas':0.0,
       'salfons':0.0,
       'salesps':0.0,
       'salmays':0.0,
       'existes':0.0,
       'inicialn':0.0,
       'entcomn':0.0,
       'entcann':0.0,
       'entespn':0.0,
       'salvtan':0.0,
       'salfonn':0.0,
       'salespn':0.0,
       'salmayn':0.0,
       'existen':0.0,
       'cosinicials':0.0,
       'cosentcoms':0.0,
       'cosentcans':0.0,
       'cosentesps':0.0,
       'cossalvtas':0.0,
       'cossalfons':0.0,
       'cossalesps':0.0,
       'cossalmays':0.0,
       'cosexistes':0.0,
       'cosinicialn':0.0,
       'cosentcomn':0.0,
       'cosentcann':0.0,
       'cosentespn':0.0,
       'cossalvtan':0.0,
       'cossalfonn':0.0,
       'cossalespn':0.0,
       'cossalmayn':0.0,
       'cosexisten':0.0,
       'ultfol':0,
       'cia':0
    }
    return (exist)
    
def define_movart():
    movart = {
       'codigo':'',
       'almac':'',
       'folio':0,
       'prove':'',
       'nompro':0,
       'compro':0,
       'facpro':'',
       'fecha':datetime.date.today(),
       'costo':0.0,
       'sespe':'',
       'modsal':'',
       'modent':'',
       'nentrada':0,
       'tipo':'',
       'vienede':'',
       'folviene':0,
       'vahacia':'',
       'folrec':0,
       'pueblo':0,
       'numfac':0,
       'seriefac':'',
       'salio':'',
       'smay':'',
       'fechasal':datetime.date.today(),
       'canti':0,
       'serie':'',
       'salvta':'',
       'entcan':'',
       'nsalida':0,
       'entrapor':0,
       'salepor':0,
       'fecentori':datetime.date.today(),
       'fecvencto':datetime.date.today(),
       'usuario':'',
       'cia':0,
       'ptvta':'',
       'vend':''
    }
    return (movart)

def define_entpag():
    entpag = {
      'prove':'',
      'numero':0,
      'fecha':datetime.date.today(),
      'facpro':'',
      'fecentra':datetime.date.today(),
      'tasacfc':0.0,
      'importe':0.0,
      'total':0.0,
      'ctofinent':0.0,
      'ivacfcent':0.0,
      'capital':0.0,
      'letras':0,
      'iva':0.0,
      'ivaint':0.0,
      'poriva':0.0,
      'tasapro':0.0,
      'plazo':0,
      'sdocap':0.0,
      'pagcap':0.0,
      'pagint':0.0,
      'totalinter':0.0,
      'pagos':0.0,
      'pagiva':0.0,
      'tasmen':'',
      'planp':0,
      'descxap':0.0,
      'fecprp':datetime.date.today(),
      'feculp':datetime.date.today(),
      'fletes':0.0,
      'cia':0,
      'fecsal':datetime.date.today()
    }
    return entpag

def define_mventpag():
    mventpag = {
      'prove':'',
      'entrada':0,
      'fecha':datetime.date.today(),
      'pagare':0,
      'conse':0,
      'tpmov':'',
      'tipo2':'',
      'concep':0,
      'vence':datetime.date.today(),
      'capital':0.0,
      'interes':0.0,
      'iva':0.0,
      'saldo':0.0,
      'cfc':0.0,
      'desxap':0.0,
      'cia':0
    }
    return (mventpag)

def define_planesp():
    planesp = {
      'clave':0,
      'descri':'',
      'numlet':0,
      'ivadis':'',
      'nletiva':0,
      'feciva':0,
      'plazo':0,
      'tasa':0.0,
      'intssal':'',
      'fletedis':'',
      'letivaemp':'',
      'cia':0,
      'letivasol':'',
      'dscxapdis':''
    }
    return (planesp)

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
        
    mibd['host']     = basedato_z[0]
    mibd['user']     = basedato_z[1]
    mibd['password'] = basedato_z[2]
    mibd['base']     = basedato_z[3]
    mibd['tipobd']   = basedato_z[4]
    
    return (mibd)

def busca_cia(mydb, cia_z):
    sql_z = "select * from ciasinv where cia = " + utils.IntToStr(cia_z)
    cias = define_cias()
    cias['razon']="MDS"
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchall()
    for ren in record:
      cias['cia'] = ren[0]
      cias['razon'] = ren[1]
      cias['dir'] = ren[2]
      cias['dir2'] = ren[3]
      cias['nomfis'] = ren[4]
      cias['tel'] = ren[5]
      cias['fax'] = ren[6]
      cias['rfc'] = ren[7]
      return (cias)

def borra_facturma(mydb, num=0, cia=0):
    sql_z = "delete from facturma where num = " + utils.IntToStr(num)
    sql_z = sql_z + " and cia = "  + utils.IntToStr(cia)
    sql2_z = "delete from renfacma where factur = " + utils.IntToStr(num)
    sql2_z = sql2_z + " and cia = "  + utils.IntToStr(cia)
    sql3_z = "delete from seriefacma where factur = " + utils.IntToStr(num)
    sql3_z = sql3_z + " and cia = "  + utils.IntToStr(cia)
    start_trans(mydb)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    cursor.execute(sql2_z)
    cursor.execute(sql3_z)
    commit_trans(mydb)

def agrega_inv_relinv (mydb, idart_z, idrel_z, iddato_z):
    sql_z = "select idrelinv, iddato from inv_relinv where idart = " + str(idart_z)\
         + " and idrel = " + str(idrel_z)
    start_trans(mydb)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    result = cursor.fetchone()
    if result <> None:
       idrelinv_z = result[0]
       if iddato_z <> result[1]:
          # ---> Solo lo modifico si es diferente iddato
          sql_z = "update inv_relinv set iddato = " + str(iddato_z)
          sql_z = " where idrelinv = " + str(idrelinv_z)
       #End If
    else:
       # ---> No Existe, lo agrego <--- #
       idrelinv_z = busca_sigte(mydb, '', '', 0, cia_z, def_tablas.INV_RELINV)
       sql_z = "insert into inv_relinv (idrelinv,idart,idrel,iddato,conse) values ("
       sql_z = sql_z + str(idrelinv_z) + ", "
       sql_z = sql_z + str(idart_z) + ", "
       sql_z = sql_z + str(idrel_z) + ", "
       sql_z = sql_z + str(iddato_z) + ", 0 )"
    #Fin de If
    cursor.execute(sql_z)
    commit_trans(mydb)
    return(idrelinv_z)
#Fin de insert_into_inv_relinv (inv_relinv):

def insert_into_inven(inven):
    sql_z = "insert into inven (codigo,cod2,descri,tipo,prove,linea,empaqe,\
    minimo,maximo,precio,piva,costos,coston,inicials,entcoms,entcans,entesps,\
    salvtas,salfons,salesps,salmays,existes,inicialn,entcomn,entcann,entespn,\
    salvtan,salfonn,salespn,salmayn,existen,cosinicials,cosentcoms,cosentcans,\
    cosentesps,cossalvtas,cossalfons,cossalesps,cossalmays,cosexistes,\
    cosinicialn,cosentcomn,cosentcann,cosentespn,cossalvtan,cossalfonn,\
    cossalespn,cossalmayn,cosexisten,fecalta,cia,mds,elec,precelec) values ("
    sql_z = sql_z + "'" + inven['codigo'] + "',"
    sql_z = sql_z + "'" + inven['cod2'] + "',"
    sql_z = sql_z + "'" + inven['descri'] + "',"
    sql_z = sql_z + "'" + inven['tipo'] + "',"
    sql_z = sql_z + "'" + inven['prove'] + "',"
    sql_z = sql_z + "'" + inven['linea'] + "',"
    sql_z = sql_z + "'" + inven['empaqe'] + "',"
    sql_z = sql_z + str(inven['minimo']) + ","
    sql_z = sql_z + str(inven['maximo']) + ","
    sql_z = sql_z + str(inven['precio']) + ","
    sql_z = sql_z + str(inven['piva']) + ","
    sql_z = sql_z + str(inven['costos']) + ","
    sql_z = sql_z + str(inven['coston']) + ","
    sql_z = sql_z + str(inven['inicials']) + ","
    sql_z = sql_z + str(inven['entcoms']) + ","
    sql_z = sql_z + str(inven['entcans']) + ","
    sql_z = sql_z + str(inven['entesps']) + ","
    sql_z = sql_z + str(inven['salvtas']) + ","
    sql_z = sql_z + str(inven['salfons']) + ","
    sql_z = sql_z + str(inven['salesps']) + ","
    sql_z = sql_z + str(inven['salmays']) + ","
    sql_z = sql_z + str(inven['existes']) + ","
    sql_z = sql_z + str(inven['inicialn']) + ","
    sql_z = sql_z + str(inven['entcomn']) + ","
    sql_z = sql_z + str(inven['entcann']) + ","
    sql_z = sql_z + str(inven['entespn']) + ","
    sql_z = sql_z + str(inven['salvtan']) + ","
    sql_z = sql_z + str(inven['salfonn']) + ","
    sql_z = sql_z + str(inven['salespn']) + ","
    sql_z = sql_z + str(inven['salmayn']) + ","
    sql_z = sql_z + str(inven['existen']) + ","
    sql_z = sql_z + str(inven['cosinicials']) + ","
    sql_z = sql_z + str(inven['cosentcoms']) + ","
    sql_z = sql_z + str(inven['cosentcans']) + ","
    sql_z = sql_z + str(inven['cosentesps']) + ","
    sql_z = sql_z + str(inven['cossalvtas']) + ","
    sql_z = sql_z + str(inven['cossalfons']) + ","
    sql_z = sql_z + str(inven['cossalesps']) + ","
    sql_z = sql_z + str(inven['cossalmays']) + ","
    sql_z = sql_z + str(inven['cosexistes']) + ","
    sql_z = sql_z + str(inven['cosinicialn']) + ","
    sql_z = sql_z + str(inven['cosentcomn']) + ","
    sql_z = sql_z + str(inven['cosentcann']) + ","
    sql_z = sql_z + str(inven['cosentespn']) + ","
    sql_z = sql_z + str(inven['cossalvtan']) + ","
    sql_z = sql_z + str(inven['cossalfonn']) + ","
    sql_z = sql_z + str(inven['cossalespn']) + ","
    sql_z = sql_z + str(inven['cossalmayn']) + ","
    sql_z = sql_z + str(inven['cosexisten']) + ","
    sql_z = sql_z + "'" + inven['fecalta'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + str(inven['cia']) + ","
    sql_z = sql_z + "'" + inven['mds'] + "',"
    sql_z = sql_z + "'" + inven['elec'] + "',"
    sql_z = sql_z + str(inven['precelec']) + ")"
    return (sql_z)

def insert_into_renpolco(renpolco):
    sql_z = "insert into renpolco (alm,fecha,numren,docto,refer,concep,importe, \
        cliente,letra,cia,tipago,idpolcob,folio,idrenpolco,idconcep) values ("
    sql_z = sql_z + "'" + renpolco['alm'] + "',"
    sql_z = sql_z + "'" + renpolco['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + str(renpolco['numren']) + ","
    sql_z = sql_z + str(renpolco['docto']) + ","
    sql_z = sql_z + "'" + renpolco['refer'] + "',"
    sql_z = sql_z + "'" + renpolco['concep'] + "',"
    sql_z = sql_z + str(renpolco['importe']) + ","
    sql_z = sql_z + "'" + renpolco['cliente'] + "',"
    sql_z = sql_z + str(renpolco['letra']) + ","
    sql_z = sql_z + str(renpolco['cia']) + ","
    sql_z = sql_z + "'" + renpolco['tipago'] + "',"
    sql_z = sql_z + str(renpolco['idpolcob']) + ","
    sql_z = sql_z + str(renpolco['folio']) + ","
    sql_z = sql_z + str(renpolco['idrenpolco']) + ","
    sql_z = sql_z + str(renpolco['idconcep']) + ")"
    return (sql_z)
#Fin de insert_into_renpolco

def insert_into_invulpre(invulpre):
    sql_z = "insert into invulpre (codigo,fecha,precmds,precelec,empqe,"
    sql_z = sql_z + "observs,cia,fecinivig) values ("
    sql_z = sql_z + "'" + invulpre['codigo'] + "', "
    sql_z = sql_z + "'" + invulpre['fecha'].strftime('%Y-%m-%d') + "', "
    sql_z = sql_z + str(invulpre['precmds']) + ", "
    sql_z = sql_z + str(invulpre['precelec']) + ", "
    sql_z = sql_z + "'" + invulpre['empqe'] + "', "
    sql_z = sql_z + "'" + invulpre['observs'] + "', "
    sql_z = sql_z + str(invulpre['cia']) + ", "
    sql_z = sql_z + "'" + invulpre['fecinivig'].strftime('%Y-%m-%d') + "') "
    return (sql_z)

#Fin de insert_into_invulpre

def insert_into_inv_renpolcampre(inv_renpolcampre):
    sql_z = "insert into inv_renpolcampre (idrenpolcampre,idpolcampre,idart,antprmds,"
    sql_z = sql_z + "antprelec,precmds,precelec,antempaq,nvoempaq,idobserv) values ( "
    sql_z = sql_z + str(inv_renpolcampre['idrenpolcampre']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['idpolcampre']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['idart']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['antprmds']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['antprelec']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['precmds']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['precelec']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['antempaq']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['nvoempaq']) + ", "
    sql_z = sql_z + str(inv_renpolcampre['idobserv']) + ") "
    return (sql_z)
#Fin de insert_into_inv_renpolcampre


def insert_into_movmay(movmay):
    sql_z = "insert into movmay2 ( mayoris, docto, pagare,conse, fecha,vence, concep,"
    sql_z = sql_z + "coa,importe,saldo,cia,tipago,idconcep,fecsal,idmov) values ("
    sql_z = sql_z + "'" + movmay['mayoris'] + "',"
    sql_z = sql_z + str(movmay['docto']) + ","
    sql_z = sql_z + str(movmay['pagare']) + ","
    sql_z = sql_z + str(movmay['conse']) + ","
    sql_z = sql_z + "'" + movmay['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + "'" + movmay['vence'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + "'" + movmay['concep'] + "',"
    sql_z = sql_z + "'" + movmay['coa'] + "',"
    sql_z = sql_z + str(movmay['importe']) + ","
    sql_z = sql_z + str(movmay['saldo']) + ","
    sql_z = sql_z + str(movmay['cia']) + ","
    sql_z = sql_z + "'" + movmay['tipago'] + "',"
    sql_z = sql_z + str(movmay['idconcep']) + ","
    sql_z = sql_z + "'" + movmay['fecsal'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + str(movmay['idmov']) + ")"
    return (sql_z)
#Fin de insert_into_movmay

def insert_into_edomay(edomay):
    sql_z = "into edomay (fecha,compras,abonos,devols,sdofin,cia,mayoris,"
    sql_z = sql_z + "bonif,vencant,vencrec,porvenc,cobinterna,cartera)"
    sql_z = sql_z + " values ("
    sql_z = sql_z + "'" + edmomay['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + str(edomay['compras']) + ","
    sql_z = sql_z + str(edomay['abonos']) + ","
    sql_z = sql_z + str(edomay['devols']) + ","
    sql_z = sql_z + str(edomay['sdofin']) + ","
    sql_z = sql_z + str(edomay['cia']) + ","
    sql_z = sql_z + "'" + edomay['mayoris'] + "',"
    sql_z = sql_z + str(edomay['bonif']) + ","
    sql_z = sql_z + str(edomay['vencant']) + ","
    sql_z = sql_z + str(edomay['vencrec']) + ","
    sql_z = sql_z + str(edomay['cobinterna']) + ","
    sql_z = sql_z + str(edomay['cartera']) + ")"
    return (sql_z)
#Fin de insert_into_edomay

def insert_into_facturma(facturma):
    sql_z = "insert into facturma ( num, mayoris, refer, nomay, dir, rfc, "
    sql_z = sql_z + " status, fecha, vence, importe, descu, neto, iva, total,"
    sql_z = sql_z + " cia, npagos, plazo, tipago, pdsc, mayomen )"
    sql_z = sql_z + " values ("
    sql_z = sql_z + utils.IntToStr(facturma['num']) + ","
    sql_z = sql_z + "'" + facturma['mayoris'] + "',"
    sql_z = sql_z + "'" + facturma['refer'] + "',"
    sql_z = sql_z + "'" + facturma['nomay'] + "',"
    sql_z = sql_z + "'" + facturma['dir'] + "',"
    sql_z = sql_z + "'" + facturma['rfc'] + "',"
    sql_z = sql_z + "'" + facturma['status'] + "',"
    sql_z = sql_z + "'" + facturma['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + "'" + facturma['vence'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + str(facturma['importe']) + ","
    sql_z = sql_z + str(facturma['descu']) + ","
    sql_z = sql_z + str(facturma['neto']) + ","
    sql_z = sql_z + str(facturma['iva']) + ","
    sql_z = sql_z + str(facturma['total']) + ","
    sql_z = sql_z + utils.IntToStr(facturma['cia']) + ","
    sql_z = sql_z + utils.IntToStr(facturma['npagos']) + ","
    sql_z = sql_z + utils.IntToStr(facturma['plazo']) + ","
    sql_z = sql_z + "'" + facturma['tipago'] + "',"
    sql_z = sql_z + str(facturma['pdsc']) + ","
    sql_z = sql_z + "'" + facturma['mayomen'] + "')"
    return sql_z
#Fin de insert_into_facturma(facturma):

def insert_into_renfacma(renfacma):
    sql_z = "insert into renfacma ( factur, consec, codigo, descri, unids, preciou, "
    sql_z = sql_z + " importe, pordsc, descu, poriva, iva, total, costou, cia )"
    sql_z = sql_z + " values ("
    sql_z = sql_z + utils.IntToStr(renfacma['factur']) + ","
    sql_z = sql_z + utils.IntToStr(renfacma['consec']) + ","
    sql_z = sql_z + "'" + renfacma['codigo'] + "',"
    sql_z = sql_z + "'" + renfacma['descri'] + "',"
    sql_z = sql_z + str(renfacma['unids']) + ","
    sql_z = sql_z + str(renfacma['preciou']) + ","
    sql_z = sql_z + str(renfacma['importe']) + ","
    sql_z = sql_z + str(renfacma['pordsc']) + ","
    sql_z = sql_z + str(renfacma['descu']) + ","
    sql_z = sql_z + str(renfacma['poriva']) + ","
    sql_z = sql_z + str(renfacma['iva']) + ","
    sql_z = sql_z + str(renfacma['total']) + ","
    sql_z = sql_z + str(renfacma['costou']) + ","
    sql_z = sql_z + utils.IntToStr(renfacma['cia']) + " )"
    return sql_z
#Fin de insert_into_renfacma(renfacma):


def insert_into_observent(observent):
    sql_z = "insert into observent (tipo, alm, numero, fecha, conse, observs, cia, codigo) "
    sql_z = sql_z + " values ("
    sql_z = sql_z + "'" + observent['tipo'] + "',"
    sql_z = sql_z + "'" + observent['alm'] + "',"
    sql_z = sql_z + utils.IntToStr(observent['numero']) + ","
    sql_z = sql_z + "'" + observent['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + utils.IntToStr(observent['conse']) + ","
    sql_z = sql_z + "'" + observent['observs'] + "',"
    sql_z = sql_z + utils.IntToStr(observent['cia']) + ","
    sql_z = sql_z + "'" + observent['codigo'] + "')"
    return sql_z

def insert_into_mayoris(mayoris):
    sql_z = "insert into mayoris (codigo, nombre, direc, ciu, rfc, tel, cargos, abonos, "
    sql_z = sql_z + " compraanu, comprames, pdsc, ultmov, status, cia, nompag1,"
    sql_z = sql_z + " nompag2, dirpag1, dirpag2, ciupag, nombre2) "
    sql_z = sql_z + " values ("
    sql_z = sql_z + "'" + mayoris['codigo'] + "',"
    sql_z = sql_z + "'" + mayoris['nombre'] + "',"
    sql_z = sql_z + "'" + mayoris['direc'] + "',"
    sql_z = sql_z + "'" + mayoris['ciu'] + "',"
    sql_z = sql_z + "'" + mayoris['rfc'] + "',"
    sql_z = sql_z + "'" + mayoris['tel'] + "',"
    sql_z = sql_z + repr( mayoris['cargos']) + ","
    sql_z = sql_z + repr( mayoris['abonos']) + ","
    sql_z = sql_z + repr( mayoris['compraanu']) + ","
    sql_z = sql_z + repr( mayoris['comprames']) + ","
    sql_z = sql_z + repr( mayoris['pdsc']) + ","
    sql_z = sql_z + utils.IntToStr( mayoris['ultmov']) + ","
    sql_z = sql_z + "'" + mayoris['status'] + "',"
    sql_z = sql_z + utils.IntToStr( mayoris['cia']) + ","
    sql_z = sql_z + "'" + mayoris['nompag1'] + "',"
    sql_z = sql_z + "'" + mayoris['nompag2'] + "',"
    sql_z = sql_z + "'" + mayoris['dirpag1'] + "',"
    sql_z = sql_z + "'" + mayoris['dirpag2'] + "',"
    sql_z = sql_z + "'" + mayoris['ciupag'] + "',"
    sql_z = sql_z + "'" + mayoris['nombre2'] + "')"
    return sql_z

def insert_into_entpag(entpag):
    sql_z = "insert into entpag (prove,numero,fecha,facpro,fecentra,tasacfc,"
    sql_z = sql_z + "poriva,tasapro,importe,descxap,ctofinent,capital,letras,iva,"
    sql_z = sql_z + "ivacfcent,plazo,planp,fletes,fecprp,feculp,sdocap,cia,"
    sql_z = sql_z + "total,ivaint,pagcap,pagint,totalinter,pagos,pagiva,tasmen,fecsal)"
    sql_z = sql_z + " values ("
    sql_z = sql_z + "'" + entpag['prove'] + "',"
    sql_z = sql_z + utils.IntToStr(entpag['numero']) + ","
    sql_z = sql_z + "'" + entpag['fecha'].strftime('%Y-%m-%d')  + "',"
    sql_z = sql_z + "'" + entpag['facpro'] + "',"
    sql_z = sql_z + "'" + entpag['fecentra'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + repr(entpag['tasacfc']) + ","
    sql_z = sql_z + repr(entpag['poriva']) + ","
    sql_z = sql_z + repr(entpag['tasapro']) + ","
    sql_z = sql_z + repr(entpag['importe']) + ","
    sql_z = sql_z + repr(entpag['descxap']) + ","
    sql_z = sql_z + repr(entpag['ctofinent']) + ","
    sql_z = sql_z + repr(entpag['capital']) + ","
    sql_z = sql_z + utils.IntToStr(entpag['letras']) + ","
    sql_z = sql_z + repr(entpag['iva']) + ","
    sql_z = sql_z + repr(entpag['ivacfcent']) + ","
    sql_z = sql_z + utils.IntToStr(entpag['plazo']) + ","
    sql_z = sql_z + utils.IntToStr(entpag['planp']) + ","
    sql_z = sql_z + repr(entpag['fletes']) + ","
    sql_z = sql_z + "'" + entpag['fecprp'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + "'" + entpag['feculp'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + repr(entpag['sdocap']) + ","
    sql_z = sql_z + utils.IntToStr(entpag['cia']) + ","
    sql_z = sql_z + repr(entpag['total']) + ","
    sql_z = sql_z + repr(entpag['ivaint']) + ","
    sql_z = sql_z + repr(entpag['pagcap']) + ","
    sql_z = sql_z + repr(entpag['pagint']) + ","
    sql_z = sql_z + repr(entpag['totalinter']) + ","
    sql_z = sql_z + repr(entpag['pagos']) + ","
    sql_z = sql_z + repr(entpag['pagiva']) + ","
    sql_z = sql_z + repr(entpag['tasmen']) + ","
    sql_z = sql_z + "'" + entpag['fecsal'].strftime('%Y-%m-%d') + "')"
    return sql_z

def insert_into_mventpag(mventpag):
    sql_z = "insert into mventpag (prove,entrada,fecha,pagare,conse,tpmov,tipo2,"
    sql_z = sql_z + "concep,vence,capital,interes,iva,saldo,cfc,desxap,cia)"
    sql_z = sql_z + " values ("
    sql_z = sql_z + "'" + mventpag['prove'] + "',"
    sql_z = sql_z + utils.IntToStr(mventpag['entrada']) + ","
    sql_z = sql_z + "'" + mventpag['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + utils.IntToStr(mventpag['pagare']) + ","
    sql_z = sql_z + utils.IntToStr(mventpag['conse']) + ","
    sql_z = sql_z + "'" + mventpag['tpmov'] + "',"
    sql_z = sql_z + "'" + mventpag['tipo2'] + "',"
    sql_z = sql_z + utils.IntToStr(mventpag['concep']) + ","
    sql_z = sql_z + "'" + mventpag['vence'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + repr(mventpag['capital']) + ","
    sql_z = sql_z + repr(mventpag['interes']) + ","
    sql_z = sql_z + repr(mventpag['iva']) + ","
    sql_z = sql_z + repr(mventpag['saldo']) + ","
    sql_z = sql_z + repr(mventpag['cfc']) + ","
    sql_z = sql_z + repr(mventpag['desxap']) + ","
    sql_z = sql_z + utils.IntToStr(mventpag['cia']) + ")"
    return sql_z


def insert_into_renentra(renentra):
    sql_z = "insert into renentra ( tipo,alm,recemi,numero,conse,codinv,serie,"
    sql_z = sql_z + "siono,folsal,folent,unids,costou,piva,importe,cantmueve,"
    sql_z = sql_z + "status,persenvrec,cia,vend,poblac,tipago,prvta,entosal,entcan )"
    sql_z = sql_z + " values ("
    sql_z = sql_z + "'" + renentra['tipo'] + "',"
    sql_z = sql_z + "'" + renentra['alm'] + "',"
    sql_z = sql_z + "'" + renentra['recemi'] + "',"
    sql_z = sql_z + "" + utils.IntToStr(renentra['numero']) + ","
    sql_z = sql_z + "" + utils.IntToStr(renentra['conse']) + ","
    sql_z = sql_z + "'" + renentra['codinv'] + "',"
    sql_z = sql_z + "'" + renentra['serie'] + "',"
    sql_z = sql_z + "'" + renentra['siono'] + "',"
    sql_z = sql_z + utils.IntToStr(renentra['folsal']) + ","
    sql_z = sql_z + utils.IntToStr(renentra['folent']) + ","
    sql_z = sql_z + utils.IntToStr(renentra['unids']) + ","
    sql_z = sql_z + repr(renentra['costou']) + ","
    sql_z = sql_z + repr(renentra['piva']) + ","
    sql_z = sql_z + repr(renentra['importe']) + ","
    sql_z = sql_z + repr(renentra['cantmueve']) + ","
    sql_z = sql_z + "'" + renentra['status'] + "',"
    sql_z = sql_z + utils.IntToStr(renentra['persenvrec']) + ","
    sql_z = sql_z + utils.IntToStr(renentra['cia']) + ","
    sql_z = sql_z + "'" + renentra['vend'] + "',"
    sql_z = sql_z + utils.IntToStr(renentra['poblac']) + ","
    sql_z = sql_z + "'" + renentra['tipago'] + "',"
    sql_z = sql_z + repr(renentra['prvta']) + ","
    sql_z = sql_z + "'" + renentra['entosal'] + "',"
    sql_z = sql_z + "'" + renentra['entcan'] + "'"
    sql_z = sql_z + ")"
    return(sql_z)

def insert_into_entradas(entradas):
    sql_z = "insert into entradas ( tipo,alm,recemi,numero,facpro,prove,perenvrec,status,"
    sql_z = sql_z + "coniva,fecha,importe,iva,total,vence,ctofin,tascomp,taspro,fechafac,"
    sql_z = sql_z + "letras,plazocfp,planp,fletes,desxap,fechaprp,ctofincomp,usuario,cia)"
    sql_z = sql_z + " values ( "
    sql_z = sql_z + "'" + entradas['tipo'] + "',"
    sql_z = sql_z + "'" + entradas['alm'] + "',"
    sql_z = sql_z + "'" + entradas['recemi'] + "',"
    sql_z = sql_z + utils.IntToStr(entradas['numero']) + ","
    sql_z = sql_z + "'" + entradas['facpro'] + "',"
    sql_z = sql_z + "'" + entradas['prove'] + "',"
    sql_z = sql_z + utils.IntToStr(entradas['perenvrec']) + ","
    sql_z = sql_z + "'" + entradas['status'] + "',"
    sql_z = sql_z + "'" + entradas['coniva'] + "',"
    sql_z = sql_z + "'" + entradas['fecha'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + repr(entradas['importe']) + ","
    sql_z = sql_z + repr(entradas['iva']) + ","
    sql_z = sql_z + repr(entradas['total']) + ","
    sql_z = sql_z + "'" + entradas['vence'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + repr(entradas['ctofin']) + ","
    sql_z = sql_z + repr(entradas['tascomp']) + ","
    sql_z = sql_z + repr(entradas['taspro']) + ","
    sql_z = sql_z + "'" + entradas['fechafac'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + utils.IntToStr(entradas['letras']) + ","
    sql_z = sql_z + utils.IntToStr(entradas['plazocfp']) + ","
    sql_z = sql_z + utils.IntToStr(entradas['planp']) + ","
    sql_z = sql_z + repr(entradas['fletes']) + ","
    sql_z = sql_z + repr(entradas['desxap']) + ","
    sql_z = sql_z + "'" + entradas['fechaprp'].strftime('%Y-%m-%d') + "',"
    sql_z = sql_z + repr(entradas['ctofincomp']) + ","
    sql_z = sql_z + "'" + entradas['usuario'] + "',"
    sql_z = sql_z + utils.IntToStr(entradas['cia']) + ")"
    return(sql_z)

def insert_into_exist(exist):
    sql_z = "insert into exist ( codigo,alm,inicials,entcoms,entcans,entesps,salvtas,salfons,"
    sql_z = sql_z + "salesps,salmays,existes,inicialn,entcomn,entcann,entespn,salvtan,salfonn,"
    sql_z = sql_z + "salespn,salmayn,existen,cosinicials,cosentcoms,cosentcans,cosentesps,"
    sql_z = sql_z + "cossalvtas,cossalfons,cossalesps,cosexistes,cosinicialn,cosentcomn,"
    sql_z = sql_z + "cosentcann,cosentespn,cossalvtan,cossalfonn,cossalespn,cossalmayn,"
    sql_z = sql_z + "cosexisten,ultfol,cia) values ("
    sql_z = sql_z + "'" + exist['codigo'] + "',"
    sql_z = sql_z + "'" + exist['alm'] + "',"
    sql_z = sql_z + repr(exist['inicials']) + ","
    sql_z = sql_z + repr(exist['entcoms']) + ","
    sql_z = sql_z + repr(exist['entcans']) + ","
    sql_z = sql_z + repr(exist['entesps']) + ","
    sql_z = sql_z + repr(exist['salvtas']) + ","
    sql_z = sql_z + repr(exist['salfons']) + ","
    sql_z = sql_z + repr(exist['salesps']) + ","
    sql_z = sql_z + repr(exist['salmays']) + ","
    sql_z = sql_z + repr(exist['existes']) + ","
    sql_z = sql_z + repr(exist['inicialn']) + ","
    sql_z = sql_z + repr(exist['entcomn']) + ","
    sql_z = sql_z + repr(exist['entcann']) + ","
    sql_z = sql_z + repr(exist['entespn']) + ","
    sql_z = sql_z + repr(exist['salvtan']) + ","
    sql_z = sql_z + repr(exist['salfonn']) + ","
    sql_z = sql_z + repr(exist['salespn']) + ","
    sql_z = sql_z + repr(exist['salmayn']) + ","
    sql_z = sql_z + repr(exist['existen']) + ","
    sql_z = sql_z + repr(exist['cosinicials']) + ","
    sql_z = sql_z + repr(exist['cosentcoms']) + ","
    sql_z = sql_z + repr(exist['cosentcans']) + ","
    sql_z = sql_z + repr(exist['cosentesps']) + ","
    sql_z = sql_z + repr(exist['cossalvtas']) + ","
    sql_z = sql_z + repr(exist['cossalfons']) + ","
    sql_z = sql_z + repr(exist['cossalesps']) + ","
    sql_z = sql_z + repr(exist['cosexistes']) + ","
    sql_z = sql_z + repr(exist['cosinicialn']) + ","
    sql_z = sql_z + repr(exist['cosentcomn']) + ","
    sql_z = sql_z + repr(exist['cosentcann']) + ","
    sql_z = sql_z + repr(exist['cosentespn']) + ","
    sql_z = sql_z + repr(exist['cossalvtan']) + ","
    sql_z = sql_z + repr(exist['cossalfonn']) + ","
    sql_z = sql_z + repr(exist['cossalespn']) + ","
    sql_z = sql_z + repr(exist['cossalmayn']) + ","
    sql_z = sql_z + repr(exist['cosexisten']) + ","
    sql_z = sql_z + repr(exist['ultfol']) + ","
    sql_z = sql_z + repr(exist['cia']) + ")"
    return (sql_z)

def insert_into_movart(movart):
    sql_z = "insert into movart (codigo,almac,folio,prove,nompro,compro,facpro,fecha,costo,"
    sql_z = sql_z + "sespe,modsal,modent,nentrada,tipo,vienede,folviene,vahacia,folrec,pueblo,"
    sql_z = sql_z + "numfac,seriefac,salio,smay,fechasal,canti,serie,salvta,entcan,nsalida,"
    sql_z = sql_z + "entrapor,salepor,fecentori,fecvencto,usuario,cia,ptvta,vend) values ("
    sql_z = sql_z + "'" + movart['codigo'] + "',"
    sql_z = sql_z + "'" + movart['almac'] + "',"
    sql_z = sql_z + utils.IntToStr(movart['folio']) + ","
    sql_z = sql_z + "'" + movart['prove'] + "',"
    sql_z = sql_z + utils.IntToStr(movart['nompro']) + ","
    sql_z = sql_z + utils.IntToStr(movart['compro']) + ","
    sql_z = sql_z + "'" + movart['facpro'] + "',"
    sql_z = sql_z + "'" + movart['fecha'].strftime('%Y-%m-%d') + "',"    
    sql_z = sql_z + repr(movart['costo']) + ","
    sql_z = sql_z + "'" + movart['sespe'] + "',"
    sql_z = sql_z + "'" + movart['modsal'] + "',"
    sql_z = sql_z + "'" + movart['modent'] + "',"
    sql_z = sql_z + repr(movart['nentrada']) + ","
    sql_z = sql_z + "'" + movart['tipo'] + "',"
    sql_z = sql_z + "'" + movart['vienede'] + "',"
    sql_z = sql_z + utils.IntToStr(movart['folviene']) + ","
    sql_z = sql_z + "'" + movart['vahacia'] + "',"
    sql_z = sql_z + repr(movart['folrec']) + ","
    sql_z = sql_z + repr(movart['pueblo']) + ","
    sql_z = sql_z + utils.IntToStr(movart['numfac']) + ","
    sql_z = sql_z + "'" + movart['seriefac'] + "',"
    sql_z = sql_z + "'" + movart['salio'] + "',"
    sql_z = sql_z + "'" + movart['smay'] + "',"
    sql_z = sql_z + "'" + movart['fechasal'].strftime('%Y-%m-%d') + "',"    
    sql_z = sql_z + repr(movart['canti']) + ","
    sql_z = sql_z + "'" + movart['serie'] + "',"
    sql_z = sql_z + "'" + movart['salvta'] + "',"
    sql_z = sql_z + "'" + movart['entcan'] + "',"
    sql_z = sql_z + repr(movart['nsalida']) + ","
    sql_z = sql_z + repr(movart['entrapor']) + ","
    sql_z = sql_z + repr(movart['salepor']) + ","
    sql_z = sql_z + "'" + movart['fecentori'].strftime('%Y-%m-%d') + "',"    
    sql_z = sql_z + "'" + movart['fecvencto'].strftime('%Y-%m-%d') + "',"    
    sql_z = sql_z + "'" + movart['usuario'] + "',"
    sql_z = sql_z + repr(movart['cia']) + ","
    sql_z = sql_z + "'" + movart['ptvta'] + "',"
    sql_z = sql_z + "'" + movart['vend'] + "')"
    return (sql_z)

def insert_into_estadis(estadis):
    sql_z = "insert into estadis ( tipo, codigo, alm,  anu, mes, unidades, importe, cia)"
    sql_z = sql_z + " values ("
    sql_z = sql_z + '%d' % estadis['tipo'] + ","
    sql_z = sql_z + "'" + estadis['codigo'] +"',"
    sql_z = sql_z + "'" + estadis['alm'] + "',"
    sql_z = sql_z + ' %d' % estadis['anu'] + ","
    sql_z = sql_z + ' %d' % estadis['mes'] + ","
    sql_z = sql_z + ' %d' % estadis['unidades'] + ","
    sql_z = sql_z + ' %10.2f' % estadis['importe'] + ","
    sql_z = sql_z + ' %d' % estadis['cia']
    sql_z = sql_z + ")"
    return (sql_z)

def afecta_renentra(mydb, renentra, entradas):
    #print "Estoy en afecta renentra"
    #print renentra['alm']
    #print renentra['tipo']
    #print renentra['numero']
    #print renentra['conse']
    #print renentra['entosal']
    
    if entradas['tipo'] == "T" or entradas['tipo'] == "D":
       result_z = haz_traspaso(mydb, renentra, entradas)
    else:
       if renentra['entosal'] == "E":
          result_z = haz_entrada(mydb, renentra, entradas)
       elif renentra['entosal'] == "S":
          result_z = haz_salida(mydb, renentra, entradas)
       
    #print "Resultado:", result_z
    if result_z == True:
        sqlren_z = "update renentra set status = 'C' where "
        sqlren_z = sqlren_z + "tipo = '" + renentra['tipo'] + "'"
        sqlren_z = sqlren_z + " and alm = '" + renentra['alm'] + "'"
        sqlren_z = sqlren_z + " and numero = " + '%d' % renentra['numero']
        sqlren_z = sqlren_z + " and conse = " + '%d' % renentra['conse']
        start_trans(mydb)
        cursor = mydb.cursor()
        cursor.execute(sqlren_z)
        commit_trans(mydb)
    #Fin de if
    return (result_z)
    
def haz_entrada(mydb, renentra, entradas):
    #Una Entrada, primero voy a asumir las entradas especiales
    # Primero afecto Inven
    inven     = define_inven()
    exist     = define_exist()
    movart    = define_movart()
    tipo_z    = renentra['tipo']
    codigo_z  = renentra['codinv']
    ptvta_z   = renentra['recemi']
    costou_z  = renentra['costou']
    canti_z   = renentra['unids']
    alm_z     = renentra['alm']
    cia_z     = renentra['cia']
    fecha_z   = entradas['fecha']
    nument_z  = entradas['numero']
    conse_z   = renentra['conse']
    almestadi_z = alm_z
    entrapor_z = tipoentra(tipo_z)[0]
    cambiar_folio_en_renentra = False
    start_trans(mydb)
    folent_z = busca_sigfolio(mydb, codigo_z, alm_z, cia_z)
    if folent_z <> renentra['folsal']:
       cambiar_folio_en_renentra = True
    serie_z = renentra['serie']

    sqlinv_z = "select codigo, descri, tipo from inven where codigo = '" + renentra['codinv'] + "'"
    sqlinv_z = sqlinv_z + " and cia = " + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sqlinv_z)
    record = cursor.fetchall()
    rens = len(record)
    if int(rens) <> 1:
       error_z = "No existe el codigo " + codigo_z + " En Inventario" + ":ERROR -1"
       return(error_z)
    if renentra['tipo'] == 'C':
       if renentra['siono'] == 'S':
          campoinv_z = ("entcans", "existes")
          almestadi_z = ptvta_z
       else:
          almestadi_z = alm_z
          campoinv_z = ("entcann", "existen")
    else:
       if renentra['siono'] == 'S':
          campoinv_z = ("entesps", "existes")
       else:
          campoinv_z = ("entespn", "existen")
    #Primero afecto Inven
    if renentra['tipo'] <> 'T' and renentra['tipo'] <> 'D':
       sqlinv_z = " update inven set " + campoinv_z[0] + " = " + campoinv_z[0] + " + " + repr(renentra['unids']) + ","
       sqlinv_z = sqlinv_z + campoinv_z[1] + " = " + campoinv_z[1] + " + " + repr(renentra['unids'])
       sqlinv_z = sqlinv_z + " where codigo = '" + codigo_z + "'"
       sqlinv_z = sqlinv_z + " and cia = " + repr(cia_z)
       #print sqlinv_z
       cursor = mydb.cursor()
       cursor.execute(sqlinv_z)
    # Ahora afecto Exist
    sqlexist_z = "select codigo, alm, ultfol from exist where codigo = '" + codigo_z + "'"
    sqlexist_z = sqlexist_z + " and alm = '" + alm_z + "'"
    sqlexist_z = sqlexist_z + " and cia = " + repr(cia_z)
    #print "Afecto Exist:" , sqlexist_z
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    record = cursor.fetchall()
    rens = len(record)
    if rens == 1:
       sqlexist_z = " update exist set " + campoinv_z[0] + " = " + campoinv_z[0] + " + " + repr(renentra['unids']) + ","
       sqlexist_z = sqlexist_z + campoinv_z[1] + " = " + campoinv_z[1] + " + " + repr(renentra['unids']) + ","
       sqlexist_z = sqlexist_z + " ultfol = ultfol + " + repr(renentra['unids'])
       sqlexist_z = sqlexist_z + " where codigo = '" + codigo_z + "'"
       sqlexist_z = sqlexist_z + " and alm = '" + renentra['alm'] + "'"
       sqlexist_z = sqlexist_z + " and cia = " + repr(cia_z)
    else:
       exist['codigo'] = renentra['codinv']
       exist['alm'] = renentra['alm']
       exist['cia'] = renentra['cia']
       exist[campoinv_z[0]]= renentra['unids']
       exist[campoinv_z[1]]= renentra['unids']
       exist['ultfol']= renentra['unids']
       sqlexist_z = insert_into_exist(exist)
    #print sqlexist_z
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    
    #Ahora Afecto Movart
    movart['codigo'] = renentra['codinv']
    movart['almac'] = renentra['alm']
    movart['folio'] = folent_z
    movart['prove'] = entradas['prove']
    movart['nompro'] = renentra['persenvrec']
    movart['compro'] = 0
    movart['facpro'] = ''
    movart['fecha'] = entradas['fecha']
    movart['costo'] = renentra['costou']
    movart['sespe'] = 'S'
    movart['modsal'] = ''
    movart['modent'] = renentra['siono']
    movart['nentrada'] = renentra['numero']
    movart['tipo'] = renentra['tipo']
    movart['vienede'] = ''
    movart['folviene'] = 0
    movart['vahacia'] = ''
    movart['folrec'] = 0
    movart['pueblo'] = renentra['poblac']
    movart['numfac'] = utils.StrToInt(entradas['facpro'])
    movart['seriefac'] = ''
    movart['salio'] = 'N'
    movart['smay'] = ''
    movart['fechasal'] = entradas['fecha']
    movart['canti'] = renentra['unids']
    movart['serie'] = renentra['serie']
    movart['salvta'] = ''
    movart['entcan'] = renentra['entcan']
    movart['nsalida'] = 0
    movart['entrapor'] = tipoentra(tipo_z)[0]
    movart['salepor'] = 0
    movart['fecentori'] = entradas['fecha']
    movart['fecvencto'] = entradas['fecha']
    movart['usuario'] = ''
    movart['cia'] = renentra['cia']
    movart['ptvta'] = renentra['recemi']
    movart['vend'] = renentra['vend']
    sqlmovart_z = insert_into_movart(movart)
    #print sqlmovart_z
    cursor = mydb.cursor()
    cursor.execute(sqlmovart_z)
    if cambiar_folio_en_renentra == True:
       sql_z = "update renentra set folent = " + '%d' % folent_z 
       sql_z = sql_z + " where tipo = '" + tipo_z + "' and alm = '" + alm_z + "'"
       sql_z = sql_z + " and numero=" + '%d' % nument_z 
       sql_z = sql_z + " and conse = " + '%d' % conse_z 
       sql_z = sql_z + " and cia= " + '%d' % cia_z
       #print sql_z
       cursor = mydb.cursor()
       cursor.execute(sql_z)
    #Fin de cambiar folio de Entrada   
    commit_trans(mydb)
       
    afecta_estadis(mydb, entrapor_z, codigo_z, almestadi_z, fecha_z, canti_z, costou_z, cia_z)
    return(True)

def haz_salida(mydb, renentra, entradas):
    inven = define_inven()
    exist = define_exist()
    movart = define_movart()
    tipo_z = renentra['tipo']
    folsal_z = renentra['folsal']
    serie_z = renentra['serie']
    codigo_z = renentra['codinv']
    ptvta_z = renentra['recemi']
    costou_z = renentra['costou']
    canti_z = renentra['unids']
    alm_z = renentra['alm']
    cia_z = renentra['cia']
    fecha_z = entradas['fecha']
    prove_z = entradas['prove']
    almestadi_z = alm_z
    salepor_z = tipoentra(tipo_z)[0]
    
    start_trans(mydb)
    sqlinv_z = "select codigo, descri, tipo from inven where codigo = '" + codigo_z + "'"
    sqlinv_z = sqlinv_z + " and cia = " + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sqlinv_z)
    record = cursor.fetchone()
    if record == None:
       error_z = "No existe el codigo " + codigo_z + " En Inventario" + ":ERROR -1"
       return(error_z)
    if tipo_z == 'V' or tipo_z == '1' or tipo_z == 'Q' or tipo_z == 'H':
       almestadi_z = ptvta_z
       if renentra['siono'] == 'S':
          campoinv_z = ("salvtas", "existes")
       else:
          campoinv_z = ("salvtan", "existen")
    elif tipo_z == 'F':
       almestadi_z = ptvta_z
       if renentra['siono'] == 'S':
          campoinv_z = ("salfons", "existes")
       else:
          campoinv_z = ("salfonn", "existen")
    elif tipo_z == 'M':
       almestadi_z = prove_z
       ptvta_z = prove_z
       if renentra['siono'] == 'S':
          campoinv_z = ("salmays", "existes")
       else:
          campoinv_z = ("salmayn", "existen")
    else:
       almestadi_z = alm_z
       if renentra['siono'] == 'S':
          campoinv_z = ("salesps", "existes")
       else:
          campoinv_z = ("salespn", "existen")
    
    #Primero afecto Inven
    if renentra['tipo'] <> 'T' and renentra['tipo'] <> 'D':
      sqlinv_z = " update inven set " + campoinv_z[0] + " = " + campoinv_z[0] + " + " + repr(renentra['unids']) + ","
      sqlinv_z = sqlinv_z + campoinv_z[1] + " = " + campoinv_z[1] + " - " + repr(renentra['unids'])
      sqlinv_z = sqlinv_z + " where codigo = '" + codigo_z + "'"
      sqlinv_z = sqlinv_z + " and cia = " + repr(renentra['cia'])
      #print sqlinv_z
      cursor = mydb.cursor()
      cursor.execute(sqlinv_z)
    # Ahora afecto Exist
    sqlexist_z = "select codigo, alm, ultfol from exist where codigo = '" + codigo_z + "'"
    sqlexist_z = sqlexist_z + " and alm = '" + alm_z + "'"
    sqlexist_z = sqlexist_z + " and cia = " + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    record = cursor.fetchall()
    rens = len(record)
    if rens == 1:
       sqlexist_z = " update exist set " + campoinv_z[0] + " = " + campoinv_z[0] + " + " + repr(renentra['unids']) + ","
       sqlexist_z = sqlexist_z + campoinv_z[1] + " = " + campoinv_z[1] + " - " + repr(renentra['unids'])
       sqlexist_z = sqlexist_z + " where codigo = '" + codigo_z + "'"
       sqlexist_z = sqlexist_z + " and alm = '" + alm_z + "'"
       sqlexist_z = sqlexist_z + " and cia = " + repr(cia_z)
    else:
       exist['codigo'] = codigo_z
       exist['alm'] = alm_z
       exist['cia'] = cia_z
       exist[campoinv_z[0]]= renentra['unids']
       exist[campoinv_z[1]]= 0 - renentra['unids']
       exist['ultfol']= renentra['unids']
       sqlexist_z = insert_into_exist(exist)
    #print sqlexist_z
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    
    #Ahora Afecto Movart
    poblac_z = renentra['poblac']
    sqlmovart_z = "update movart set salio = 'S', fechasal = '" + fecha_z.strftime('%Y-%m-%d') + "',"
    sqlmovart_z = sqlmovart_z + " compro = " '%d' % renentra['persenvrec'] + ","
    sqlmovart_z = sqlmovart_z + " salepor = " '%d' % salepor_z + ","
    sqlmovart_z = sqlmovart_z + " nsalida = " '%d' % renentra['numero'] + ","
    sqlmovart_z = sqlmovart_z + " modsal = '" + renentra['siono'] + "',"
    sqlmovart_z = sqlmovart_z + " pueblo = " '%d' % poblac_z + ","
    sqlmovart_z = sqlmovart_z + " serie = '" + serie_z + "', "
    sqlmovart_z = sqlmovart_z + " ptvta = '" + ptvta_z + "', "
    sqlmovart_z = sqlmovart_z + " vahacia = '" + ptvta_z + "' "
    sqlmovart_z = sqlmovart_z + " where codigo = '" + codigo_z + "' "
    sqlmovart_z = sqlmovart_z + " and almac = '" + alm_z + "' "
    sqlmovart_z = sqlmovart_z + " and folio = " + '%d' % folsal_z
    sqlmovart_z = sqlmovart_z + " and cia = " + '%d' % cia_z
    #print sqlmovart_z
    cursor = mydb.cursor()
    cursor.execute(sqlmovart_z)
    commit_trans(mydb)
    afecta_estadis(mydb, salepor_z, codigo_z, almestadi_z, fecha_z, canti_z, costou_z, cia_z)
    return(True)

def afecta_estadis(mydb, tipo_z, codigo_z, almestadi_z, fecha_z, canti_z, costou_z, cia_z):
    start_trans(mydb)
    estadis = define_estadis()
    sql_z = "select codigo, alm,  anu, mes, unidades, importe, cia from estadis where "
    sql_z = sql_z + " tipo = " + '%d' % tipo_z
    sql_z = sql_z + " and codigo = '" + codigo_z + "'"
    sql_z = sql_z + " and alm = '" + almestadi_z + "'"
    sql_z = sql_z + " and anu = " + fecha_z.strftime('%Y') 
    sql_z = sql_z + " and mes = " + fecha_z.strftime('%m') 
    sql_z = sql_z + " and cia = " + '%d' % cia_z
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchall()
    numrows = len(record)
    if numrows:
       
       sql_z = "update estadis set unidades = unidades + " + '%d' % canti_z +","
       sql_z = sql_z + " importe = importe + " + '%10.2f' % (costou_z * canti_z )
       sql_z = sql_z + " where "
       sql_z = sql_z + " tipo = " + '%d' % tipo_z
       sql_z = sql_z + " and codigo = '" + codigo_z + "'"
       sql_z = sql_z + " and alm = '" + almestadi_z + "'"
       sql_z = sql_z + " and anu = " + fecha_z.strftime('%Y') 
       sql_z = sql_z + " and mes = " + fecha_z.strftime('%m') 
       sql_z = sql_z + " and cia = " + '%d' % cia_z
    else:
       estadis['tipo'] = tipo_z
       estadis['codigo'] = codigo_z
       estadis['alm'] = almestadi_z
       estadis['anu'] = utils.StrToInt(fecha_z.strftime('%Y') )
       estadis['mes'] = utils.StrToInt(fecha_z.strftime('%m') )
       estadis['unidades'] = canti_z
       estadis['importe'] = canti_z * costou_z
       estadis['cia'] = cia_z
       sql_z = insert_into_estadis(estadis)
    #Fin de If
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    commit_trans(mydb)
    return (True)

#--------------------
def haz_traspaso(mydb, renentra, entradas):
    #primero voy a generar la entrada
    inven     = define_inven()
    exist     = define_exist()
    tipo_z    = renentra['tipo']
    codigo_z  = renentra['codinv']
    ptvta_z   = renentra['recemi']
    costou_z  = renentra['costou']
    canti_z   = renentra['unids']
    almrec_z  = renentra['recemi']
    almemi_z  = renentra['alm']
    folsal_z = renentra['folsal']
    folent_z  = renentra['folent']
    cia_z     = renentra['cia']
    fecha_z   = entradas['fecha']
    nument_z  = entradas['numero']
    conse_z   = renentra['conse']
    entrapor_z = tipoentra(tipo_z)[0]
    salepor_z  = entrapor_z
    idnompro_z = busca_idnombrealm(mydb, almemi_z, cia_z)
    idcompro_z = busca_idnombrealm(mydb, almrec_z, cia_z)
    cambiar_folio_en_renentra = False
    
    start_trans(mydb)
    sqlinv_z = "select codigo, descri, tipo from inven where codigo = '" + codigo_z + "'"
    sqlinv_z = sqlinv_z + " and cia = " + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sqlinv_z)
    record = cursor.fetchone()
    if record == None:
       error_z = "No existe el codigo " + codigo_z + ":" + repr(cia_z) + ":En Inventario" + ":ERROR -1"
       return(error_z)

    folent_z = busca_sigfolio(mydb, codigo_z, almrec_z, cia_z)
    movart = busca_folio_movart(mydb, codigo_z, almemi_z, folsal_z, cia_z)
    if movart['salio'] == 'S':
       error_z = "El Folio" + repr(folsal_z) + " No esta Disponible" + ":ERROR -1"
       return(error_z)
    
    costou_z = movart['costo']
    fecentori_z = movart['fecentori']
    fecvence_z = movart['fecvencto']
    siono_z = movart['modent']
    entcan_z = movart['entcan']
    facpro_z = movart['facpro']
    serie_z = renentra['serie']
    prove_z = movart['prove']
    if renentra['siono'] == 'S':
       campoinv_z = ("entesps", "existes")
    else:
       campoinv_z = ("entespn", "existen")
    
    # Ahora afecto Exist
    sqlexist_z = "select codigo, alm, ultfol from exist where codigo = '" + codigo_z + "'"
    sqlexist_z = sqlexist_z + " and alm = '" + almemi_z + "'"
    sqlexist_z = sqlexist_z + " and cia = " + utils.IntToStr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    record = cursor.fetchone()
    if record <> None:
       sqlexist_z = " update exist set " + campoinv_z[0] + " = " + campoinv_z[0] + " + " + repr(renentra['unids']) + ","
       sqlexist_z = sqlexist_z + campoinv_z[1] + " = " + campoinv_z[1] + " - " + repr(renentra['unids'])
       sqlexist_z = sqlexist_z + " where codigo = '" + codigo_z + "'"
       sqlexist_z = sqlexist_z + " and alm = '" + almemi_z + "'"
       sqlexist_z = sqlexist_z + " and cia = " + utils.IntToStr(cia_z)
    else:
       exist['codigo'] = codigo_z
       exist['alm'] = almemi_z
       exist['cia'] = cia_z
       exist[campoinv_z[0]]= renentra['unids']
       exist[campoinv_z[1]]= 0 - renentra['unids']
       exist['ultfol']= 0
       sqlexist_z = insert_into_exist(exist)
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    
    #Ahora Afecto Movart
    poblac_z = renentra['poblac']
    sqlmovart_z = "update movart set salio = 'S', fechasal = '" + fecha_z.strftime('%Y-%m-%d') + "',"
    sqlmovart_z = sqlmovart_z + " compro = " '%d' % idcompro_z + ","
    sqlmovart_z = sqlmovart_z + " salepor = " '%d' % salepor_z + ","
    sqlmovart_z = sqlmovart_z + " nsalida = " '%d' % nument_z + ","
    sqlmovart_z = sqlmovart_z + " modsal = '" + siono_z + "',"
    sqlmovart_z = sqlmovart_z + " pueblo = " '%d' % poblac_z + ","
    sqlmovart_z = sqlmovart_z + " serie = '" + serie_z + "', "
    sqlmovart_z = sqlmovart_z + " ptvta = '" + ptvta_z + "', "
    sqlmovart_z = sqlmovart_z + " vahacia = '" + almrec_z + "', "
    sqlmovart_z = sqlmovart_z + " folrec = " '%d' % folent_z
    sqlmovart_z = sqlmovart_z + " where codigo = '" + codigo_z + "' "
    sqlmovart_z = sqlmovart_z + " and almac = '" + almemi_z + "' "
    sqlmovart_z = sqlmovart_z + " and folio = " + '%d' % folsal_z
    sqlmovart_z = sqlmovart_z + " and cia = " + '%d' % cia_z
    cursor = mydb.cursor()
    cursor.execute(sqlmovart_z)

    # Ahora afecto Exist en Recepcion
    sqlexist_z = "select codigo, alm, ultfol from exist where codigo = '" + codigo_z + "'"
    sqlexist_z = sqlexist_z + " and alm = '" + almrec_z + "'"
    sqlexist_z = sqlexist_z + " and cia = " + utils.IntToStr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    record = cursor.fetchone()
    if record <> None:
       sqlexist_z = " update exist set " + campoinv_z[0] + " = " + campoinv_z[0] + " + " + repr(renentra['unids']) + ","
       sqlexist_z = sqlexist_z + campoinv_z[1] + " = " + campoinv_z[1] + " + " + repr(renentra['unids']) + ","
       sqlexist_z = sqlexist_z + " ultfol = ultfol + " + repr(renentra['unids'])
       sqlexist_z = sqlexist_z + " where codigo = '" + codigo_z + "'"
       sqlexist_z = sqlexist_z + " and alm = '" + almrec_z + "'"
       sqlexist_z = sqlexist_z + " and cia = " + utils.IntToStr(cia_z)
    else:
       exist['codigo'] = codigo_z
       exist['alm'] = almrec_z
       exist['cia'] = renentra['cia']
       exist[campoinv_z[0]]= renentra['unids']
       exist[campoinv_z[1]]= renentra['unids']
       exist['ultfol']= renentra['unids']
       sqlexist_z = insert_into_exist(exist)
    #print sqlexist_z
    cursor = mydb.cursor()
    cursor.execute(sqlexist_z)
    
    #Ahora Afecto Movart
    movart['codigo'] = renentra['codinv']
    movart['almac'] = almrec_z
    movart['folio'] = folent_z
    movart['prove'] = prove_z
    movart['nompro'] = idnompro_z
    movart['compro'] = 0
    movart['facpro'] = facpro_z
    movart['fecha'] = entradas['fecha']
    movart['costo'] = renentra['costou']
    movart['sespe'] = 'S'
    movart['modsal'] = ''
    movart['modent'] = siono_z
    movart['nentrada'] = renentra['numero']
    movart['tipo'] = renentra['tipo']
    movart['vienede'] = almemi_z
    movart['folviene'] = folsal_z
    movart['vahacia'] = ''
    movart['folrec'] = 0
    movart['pueblo'] = renentra['poblac']
    movart['numfac'] = utils.StrToInt(entradas['facpro'])
    movart['seriefac'] = ''
    movart['salio'] = 'N'
    movart['smay'] = ''
    movart['fechasal'] = entradas['fecha']
    movart['canti'] = renentra['unids']
    movart['serie'] = renentra['serie']
    movart['salvta'] = ''
    movart['entcan'] = entcan_z
    movart['nsalida'] = 0
    movart['entrapor'] = tipoentra(tipo_z)[0]
    movart['salepor'] = 0
    movart['fecentori'] = fecentori_z
    movart['fecvencto'] = fecvence_z
    movart['usuario'] = ''
    movart['cia'] = renentra['cia']
    movart['ptvta'] = renentra['recemi']
    movart['vend'] = renentra['vend']
    sqlmovart_z = insert_into_movart(movart)
    #print sqlmovart_z
    cursor = mydb.cursor()
    cursor.execute(sqlmovart_z)
    if cambiar_folio_en_renentra == True:
       sql_z = "update renentra set folent = " + '%d' % folent_z 
       sql_z = " folsal = " + '%d' % folsal_z 
       sql_z = sql_z + " where tipo = '" + tipo_z + "' and alm = '" + alm_z + "'"
       sql_z = sql_z + " and numero=" + '%d' % nument_z 
       sql_z = sql_z + " and conse = " + '%d' % conse_z 
       sql_z = sql_z + " and cia= " + '%d' % cia_z
       #print sql_z
       cursor = mydb.cursor()
       cursor.execute(sql_z)
    #Fin de cambiar folio de Entrada   
    commit_trans(mydb)
    return(True)

#--------------
def busca_sigfolio(mydb, codigo_z, alm_z, cia_z):
    sql_z = "select ultfol from exist where "
    sql_z = sql_z + "codigo = '" + codigo_z + "' and alm='" + alm_z + "' and cia=" + utils.IntToStr(cia_z)
    sigte_z = 0
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    if record <> None:
       if type(record[0]) <> types.NoneType:
          sigte_z = int(record[0])
       #End if
    #End if
    sigte_z = sigte_z + 1
    return (sigte_z)

def busca_idnombrealm(mydb, alm_z, cia_z):
    idnombre_z = 0
    sql_z = "select clave, nombre from almacen where clave = '" + alm_z + "'"
    sql_z = sql_z + " and cia=" + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    if record <> None:
       # get and display one row at a time
       if type(record[0]) <> types.NoneType:
          nombre_z = record[1]
          idnombre_z = busca_iddato(mydb, nombre_z, CONCEPTOS)
       #End if
    return (idnombre_z)

def busca_idart(mydb, codigo_z, cia_z):
    idart_z = 0
    sql_z = "select idart from inv_invhist where codigo = '" + codigo_z + "'"
    sql_z = sql_z + " and cia=" + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    if record <> None:
       idart_z = record[0]
    #End if
    return (idart_z)
#---> Fin busca_idart <----- #

def busca_nombre(mydb, clave_z, cia_z, tipo_z):
    nombre_z = ""
    if tipo_z == ALMACEN:
       sql_z = "select nombre from almacen where clave = '" + clave_z + "'"
       sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
    elif tipo_z == PTOVTA:
       sql_z = "select nombre from ptovta where clave = '" + clave_z + "'"
       sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
    elif tipo_z == LINEA:
       sql_z = "select descri from lineas where numero = '" + clave_z + "'"
       sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
    elif tipo_z == PROVEEDOR:
       sql_z = "select nombre from proveedor where codigo = '" + clave_z + "'"
       sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
    elif tipo_z == VENDEDOR:
       sql_z = "select nombre from vendedor where codigo = '" + clave_z + "'"
    elif tipo_z == MAYORIS:
       sql_z = "select nombre from mayoris where codigo = '" + clave_z + "'"
       sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
    elif tipo_z == INVEN:
       sql_z = "select descri from inven where codigo = '" + clave_z + "'"
       sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
    elif tipo_z == PLANESP:
       sql_z = "select descri from planesp where clave = " + utils.IntToStr(clave_z)
       sql_z = sql_z + " and cia=" + repr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    if record <> None:
       # get and display one row at a time
       if type(record[0]) <> types.NoneType:
          nombre_z = record[0]
       #End if
    return (nombre_z)
# --- Fin de Busca_nombre ----

def busca_exist(mydb, codigo_z, alm_z, cia_z):
    sql_z = "select existes + existen from exist where "
    sql_z = sql_z + "codigo = '" + codigo_z + "' and alm='" + alm_z + "' and cia=" + repr(cia_z)
    exist_z = 0
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchall()
    numrows = len(record)
    if numrows:
       # get and display one row at a time
       record = record[0] ## Solo Espero un registro
       if type(record[0]) <> types.NoneType:
          exist_z = int(record[0])
       #End if
    return (exist_z)

def busca_folios_libres(mydb, codigo_z, alm_z, fecha_z, cia_z):
    sql_z = "select folio, serie from movart where "
    sql_z = sql_z + "codigo = '" + codigo_z + "' and almac='" + alm_z + "' and cia=" + repr(cia_z)
    sql_z = sql_z + " and salio <> 'S' and fecha <= '" + fecha_z.strftime('%Y-%m-%d') + "' order by folio"
    folios_z = []
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    result = cursor.fetchall()
    numrows = len(result)
    if numrows:
       # get and display one row at a time
       for record in result:
           folios_z.append(record)
       #End if
    return (folios_z)

def busca_folio_movart(mydb, codigo_z, alm_z, folio_z, cia_z):
    sql_z = "select codigo,almac,folio,prove,nompro,compro,facpro,fecha,costo,"
    sql_z = sql_z + "sespe,modsal,modent,nentrada,tipo,vienede,folviene,vahacia,folrec,pueblo,"
    sql_z = sql_z + "numfac,seriefac,salio,smay,fechasal,canti,serie,salvta,entcan,nsalida,"
    sql_z = sql_z + "entrapor,salepor,fecentori,fecvencto,usuario,cia,ptvta,vend from movart where "
    sql_z = sql_z + "codigo = '" + codigo_z + "' and almac='" + alm_z + "'" 
    sql_z = sql_z + " and folio = " + '%d' % folio_z + " and cia=" + repr(cia_z)
    movart = define_movart()
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    
    if record <> None:
       movart['codigo']   = record[0]
       movart['almac']    = record[1]
       movart['folio']    = record[2]
       movart['prove']    = record[3]
       movart['nompro']   = record[4]
       movart['compro']   = record[5]
       movart['facpro']   = record[6]
       movart['fecha']    = record[7]
       movart['costo']    = record[8]
       movart['sespe']    = record[9]
       movart['modsal']   = record[10]
       movart['modent']   = record[11]
       movart['nentrada'] = record[12]
       movart['tipo']     = record[13]
       movart['vienede']  = record[14]
       movart['folviene'] = record[15]
       movart['vahacia']  = record[16]
       movart['folrec']   = record[17]
       movart['pueblo']   = record[18]
       movart['numfac']   = record[19]
       movart['seriefac'] = record[20]
       movart['salio']    = record[21]
       movart['smay']     = record[22]
       movart['fechasal'] = record[23]
       movart['canti']    = record[24]
       movart['serie']    = record[25]
       movart['salvta']   = record[26]
       movart['entcan']   = record[27]
       movart['nsalida']  = record[28]
       movart['entrapor'] = record[29]
       movart['salepor']  = record[30]
       movart['fecentori']= record[31]
       movart['fecvencto']= record[32]
       movart['usuario']  = record[33]
       movart['cia']      = record[34]
       movart['ptvta']    = record[35]
       movart['vend']     = record[36]
    #End if
    return (movart)

def busca_sigte(mydb, tipent_z='', alm_z='', numero_z=0, cia_z=0, tipo_z=0):
      sigte_z=0
      #print tipo_z
      if tipo_z == RENENTRA:
        sql_z = "select max(conse) as ultimo from renentra \
        where tipo = '" + tipent_z + "' and alm = '" + alm_z + \
        "' and numero = " + utils.IntToStr(numero_z) + " and cia=" + utils.IntToStr(cia_z)
      if tipo_z == MVENTPAG:
        sql_z = "select max(conse) as ultimo from mventpag \
        where prove = '" + alm_z + "' and entrada = " + utils.IntToStr(numero_z) + \
        " and cia=" + utils.IntToStr(cia_z)
      elif tipo_z == ENTRADAS:
        sql_z = "select max(numero) as ultimo from entradas \
        where tipo = '" + tipent_z + "' and alm = '" + alm_z + "' and cia=" + utils.IntToStr(cia_z)
      elif tipo_z == OBSERVENT:
        sql_z = "select max(conse) as ultimo from observent \
        where tipo = '" + tipent_z + "' and alm = '" + alm_z + "' and cia=" + repr(cia_z) + \
        " and numero = " + utils.IntToStr(numero_z)
      elif tipo_z == CONCEPTOS:
        sql_z = "select max(ncon) as ultimo from conceps where ncon > 0"
      elif tipo_z == POBLACIONES:
        sql_z = "select max(numero) as ultimo from poblacs where numero > 0"
      elif tipo_z == RENFACMA:
        sql_z = "select max(consec) as ultimo from renfacma where factur = "  
        sql_z = sql_z + utils.IntToStr(numero_z) + " and cia=" + utils.IntToStr(cia_z)
      elif tipo_z == FACTURMA:
        sql_z = "select max(num) as ultimo from facturma where num > 0 "  
        sql_z = sql_z + " and cia=" + utils.IntToStr(cia_z)
      elif tipo_z == MOVMAY:
        sql_z = "select max(idmov) as ultimo from movmay2 where idmov > 0 "  
      elif tipo_z == INV_GRUPOS:
        sql_z = "select max(idgrupo) as ultimo from inv_grupos where idgrupo > 0 "  
      elif tipo_z == GPODIARY:
        sql_z = "select max(idgpodiary) as ultimo from gpodiary where idgpodiary > 0 "  
      elif tipo_z == CONSE_MOVMAY:
        ##-- Cuando es Conse Movmay en tipent_z recibo la fecha y alm recibo mayorista
        sql_z = "select max(conse) as ultimo from movmay2 "
        sql_z = sql_z + " where mayoris = '"  + alm_z + "' "
        sql_z = sql_z + " and fecha = '" + tipent_z + "' " + " and cia = " + str(cia_z)
      elif tipo_z == INV_MARCAS:
        sql_z = "select max(idmarcainv) as ultimo from inv_marcas where idmarcainv > 0 "
      elif tipo_z == INV_SITUACIONES:
        sql_z = "select max(idsituac) as ultimo from inv_situaciones where idsituac > 0 "
      elif tipo_z == INV_RELINV:
        sql_z = "select max(idrelinv) as ultimo from inv_relinv where idrelinv > 0 "
      elif tipo_z == POLCOB:
        sql_z = "select max(idpolcob) as ultimo from polcob where idpolcob > 0 "  
      elif tipo_z == FOLIO_POLCOB:
        sql_z = "select max(folio) as ultimo from polcob where cia = "  + str(cia_z)
      elif tipo_z == FOLIO_POLCAMPRE:
        sql_z = "select max(folio) as ultimo from inv_polcampre where cia = "  + str(cia_z)
      elif tipo_z == RENPOLCO:
        sql_z = "select max(idrenpolco) as ultimo from renpolco where idrenpolco > 0 "  
      elif tipo_z == CONSE_RENPOLCO:
        sql_z = "select max(numren) as ultimo from renpolco where folio = " + str(numero_z)
        sql_z = sql_z + " and cia = " + str(cia_z)
      elif tipo_z == INV_POLCAMPRE:
        sql_z = "select max(idpolcampre) as ultimo from inv_polcampre where idpolcampre > 0 "  
      elif tipo_z == INV_RENPOLCAMPRE:
        sql_z = "select max(idrenpolcampre) as ultimo from inv_renpolcampre where idrenpolcampre > 0 "  
      
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        # get and display one row at a time
        if type(record[0]) <> types.NoneType:
           sigte_z = int(record[0])
        #End if
      sigte_z = sigte_z + 1
      return (sigte_z)

def tiene_renglones_cerrados(mydb, tipent_z='', alm_z='', numero_z=0, cia_z=0):
      sqlren_z = "select count(*) from renentra where tipo = '" + tipent_z + "' and alm = '" + alm_z + "' and numero = " + repr(numero_z) + " and cia=" + repr(cia_z)
      sqlren_z = sqlren_z + " and status = 'C'"
      haycerrados_z = False
      cursor = mydb.cursor()
      cursor.execute(sqlren_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows:
        # get and display one row at a time
        record = record[0] ## Solo Espero un registro
        if type(record[0]) <> types.NoneType:
           if record[0] > 0:
             haycerrados_z = True
           #End if
        #End if     
      #End if
      return (haycerrados_z)

def borra_entradas(mydb, tipent_z='', alm_z='', numero_z=0, cia_z=0):
      sqlren_z = "delete from renentra where tipo = '" + tipent_z + "' and alm = '" + alm_z + "' and numero = " + repr(numero_z) + " and cia=" + repr(cia_z)
      sqlent_z = "delete from entradas where tipo = '" + tipent_z + "' and alm = '" + alm_z + "' and numero = " + repr(numero_z) + " and cia=" + repr(cia_z)
      start_trans(mydb)
      cursor = mydb.cursor()
      cursor.execute(sqlren_z)
      cursor.execute(sqlent_z)
      commit_trans(mydb)
      return (True)

def start_trans(mydb):
    tipobd_z = "ODBC"
    if tipobd_z == "MYSQL":
       sql_z = "start transaction"
       cursor = mydb.cursor()
       cursor.execute(sql_z)
    #End if

def commit_trans(mydb):
    tipobd_z = "ODBC"
    if tipobd_z == "MYSQL":
       sql_z = "commit"
    else:
       sql_z = "commit work"
    cursor = mydb.cursor()
    cursor.execute(sql_z)
         

def busca_iddato(mydb, dato_z, tipodato_z=0):
      iddato_z=0
      #print "El tipodato es:", tipodato_z
      if tipodato_z == POBLACIONES:
        sql_z = "select numero from poblacs where nombre = '" + dato_z + "'"
      if tipodato_z == CONCEPTOS:
        sql_z = "select ncon from conceps where concepto = '" + dato_z + "'"
      elif tipodato_z == CREDCON:
        sql_z = "select idcrdcon as ultimo from inv_credcon where descri = '" + dato_z + "'"
      if tipodato_z == INV_CONCEPS:
        sql_z = "select idconcep from inv_conceps where concep = '" + dato_z + "'"
      if tipodato_z == INV_SITUACIONES:
        sql_z = "select idsituac from inv_situaciones where situacion = '" + dato_z + "'"
      
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
        # get and display one row at a time
        iddato_z = record[0]
      else:
        #No existe asi que lo agrego
        iddato_z = busca_sigte(mydb, '', '', 0, 0, tipodato_z)
        if tipodato_z == POBLACIONES:
          sql_z = "insert into poblacs (nombre, numero) values ('" + dato_z + "', " + str(iddato_z) + ")"
        elif tipodato_z == CONCEPTOS:
          sql_z = "insert into conceps (concepto, ncon) values ('" + dato_z + "', " + str(iddato_z) + ")"
        elif tipodato_z == INV_CONCEPS:
          sql_z = "insert into conceps (concep, idconcep) values ('" + dato_z + "', " + str(iddato_z) + ")"
        elif tipodato_z == INV_SITUACIONES:
          sql_z = "insert into inv_situaciones (situacion, idsituac) values ('" + dato_z + "', " + str(iddato_z) + ")"

        start_trans(mydb)
        cursor = mydb.cursor()
        cursor.execute(sql_z)
        commit_trans(mydb)
      return (iddato_z)
#----- Fin de busca_iddato -----

def font(mydb, impre_z=1, font_z=""):
      sql_z = "select * from fonts where impre = " + repr(impre_z) + " and nombre= '" + font_z + "'"
      """
      01 ITALICAS_ON2 *  `27,52;R;
      02 ITALICAS_OFF          2 *  `27,53;            R;
      03 COURIER               3 *  `27,107,0;         R;
      04 SANSERIF              3 *  `27,107,1;         R;
      05 LETTER-GOTHIC         3  * `27,107,2;         R;
      06 ORATOR                3  * `27,107,3;         R;
      07 SCRIPT                3  * `27,107,4;         R;
      08 OCR-B                 3  * `27,107,5;         R;
      09 TW-LIGHT              3  * `27,107,6;         R;
      10 CINEMA                3  * `27,107,7;         R;
      11 PICA-PITCH            2  * `27,80;            R;
      12 ELITE                 2  * `27,77;            R;
      13 CONDENSADO_ON         1  * `15;               R;
      14 CONDENSADO_OFF        1  * `18;               R;
      15 ON LINE EXPANDED ON   1  * `14;               R;
      16 ON LINE EXPANDED OFF  1  * `20;               R;
      17 EMPHAIZED ON          2  * `27,69;            R;
      18 EMPHAIZED OFF         2  * `27,70;            R;
      19 SUBRAYADO ON          3  * `27,45,49;         R;
      20 SUBRAYADO OFF         3  * `27,45,48;         R;
      21 SUPERAYADO ON         3  * `27,95,49;         R;
      22 SUPERAYADO OFF        3  * `27,95,49;         R;
      23 SUBSCRIPT ON          3  * `27,83,49;         R;
      24 SUPERSCRIPT ON        3  * `27,83,48;         R;
      25 SUPER-SUBSCRIPT OFF   2  * `27,84;            R;
      26 REVERSE LF            2  * `27,10;            R;
      27 OCTAVOS               2  * `27,48;            R;
      28 ESPACIO 7/72          2  * `27,49;            R;
      29 SEXTOS                2  * `27,50;            R;
      30 FORM-FEED FF          1  * `12;               R;
      31 REVERSE FEED FF       2  * `27,12;            R;
      32 ZERO SLASH            3  * `27,126,49;        R;
      33 ZERO NOT SLASH        3  * `27,126,48;        R;
      34 RESET                 2  * `27,64;            R;
      35 DISABLE PAPER-OUT     2  * `27,56;            R;
      36 ENABLE PAPER-OUT      2  * `27,57;            R;
      37 SET ON-LINE           1  * `17;               R;
      38 SET OFF-LINE          1  * `19;               R;
      39 MAST-COND-ENF-ON      3  * `27,33,4;          R;
      40 MAST-COND-ENF-OFF     3  * `27,33,0;          R;
      """
      font_z = ''
      strfont_z = ''
      ncars_z = 0
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchall()
      numrows = len(record)
      if numrows <> 0:
        # get and display one row at a time
        record = record[0] ## Solo Espero un registro
        ncars_z = record[3]
        strfont_z = record[4]
        for ii_z in range (ncars_z):
            #print "ii_z", ii_z, " Cad:", strfont_z[ ii_z*3 : ii_z *3 +3]
            font_z = font_z + chr(utils.StrToInt(strfont_z[ii_z*3: ii_z*3+3]))
            
      return (font_z)
# --- Fin de Font -----

#-- Rutina que busca un plan de pago y devuelve sus datos
def busca_planp(mydb, planp_z, cia_z):
    campos_z = [ "clave", "descri", "numlet", "ivadis", "nletiva", "feciva", "plazo", "tasa", \
       "intssal", "fletedis", "letivaemp", "cia", "letivasol", "dscxapdis" ]

    sql_z = arma_select(campos_z)
    sql_z = sql_z + " from planesp where clave = " + utils.IntToStr(planp_z)
    sql_z = sql_z + " and cia = " + utils.IntToStr(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    planesp = define_planesp()
    if record <> None:
        for micampo_z in campos_z:
            planesp[micampo_z] = record[campos_z.index(micampo_z)]
        #Fin de For
    #Fin de if
    return (planesp)

def arma_select(campos_z):
    sql_z = "select "
    ii_z = 0
    for micampo_z in campos_z:
        if ii_z > 0:
           sql_z = sql_z + ","
        #End if
        sql_z = sql_z + micampo_z
        ii_z = ii_z + 1
    #Fin  de For
    return (sql_z)
#Fin de arma_select


# -- Rutina que busca el plazo que le corresponde a un articulo
def busca_plazo_venta(mydb, codigo_z, cia_z):
    plazo_z     = 0
    plazoxlin_z = 0
    plazoxpre_z = 0
    idlinea_z   = 0
    precio_z    = 0.0
    sql_z = "select b.idlinea, a.precio from inven a join inv_lineas b on a.linea = b.linea"
    sql_z = sql_z + " and a.cia = b.cia where codigo = '" + codigo_z + "' "
    sql_z = sql_z + " and a.cia = " + str(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    if record <> None:
       idlinea_z = record[0]
       precio_z  = record[1]
    #End If
    sql_z = "select plazomax from plazoscrd where idlinea=" + str(idlinea_z) 
    sql_z = sql_z + " and tipo=" + str(INV_TIPOPRE_PLAZO_ARTICULO) 
    sql_z = sql_z + " and cia=" + str(cia_z)
    cursor = mydb.cursor()
    cursor.execute(sql_z)
    record = cursor.fetchone()
    if record <> None:
       plazo_z = record[0]
    else:
       #---> Primero busco el plazo por articulo
       sql_z = "select plazomax from plazoscrd where idlinea=" + str(idlinea_z) 
       sql_z = sql_z + " and tipo=" + str(INV_TIPOPRE_PLAZO_LINEA) 
       sql_z = sql_z + " and cia=" + str(cia_z)
       cursor = mydb.cursor()
       cursor.execute(sql_z)
       record = cursor.fetchone()
       if record <> None:
          plazoxlin_z = record[0]
       #End If
       sql_z = "select plazomax from plazoscrd where "
       sql_z = sql_z + " tipo=" + str(INV_TIPOPRE_PLAZO_PRECIO) 
       sql_z = sql_z + " and cia=" + str(cia_z)
       sql_z = sql_z + " and plistamax = ( select max(plistamax) from plazoscrd "
       sql_z = sql_z + " where tipo=" + str(INV_TIPOPRE_PLAZO_PRECIO) 
       sql_z = sql_z + " and plistamax <= " + str(precio_z) + " and cia=" + str(cia_z) + " )"
       cursor = mydb.cursor()
       cursor.execute(sql_z)
       record = cursor.fetchone()
       if record <> None:
          plazoxpre_z = record[0]
       #End If
       if plazoxpre_z > plazoxlin_z:
          plazo_z = plazoxlin_z
       else:
          plazo_z = plazoxpre_z
       #End if
    #End if
    return(plazo_z)
#Fin busca_plazo_venta

# -- Rutina que busca las relaciones de Inven para Grupos, marcas, y diary
def busca_rel_inv(mydb, codigo_z, cia_z, tiporel_z):
      dato_z = ""
      if tiporel_z == REL_INVEN_MARCAS:
        sql_z = "select c.codigo from inv_invhist a join inv_relinv b"
        sql_z = sql_z + " on a.idart = b.idart and b.idrel = " + utils.IntToStr(REL_INVEN_MARCAS)
        sql_z = sql_z + " join inv_marcas c on b.iddato = c.idmarcainv"
        sql_z = sql_z + " where a.codigo= '" + codigo_z + "' and a.cia = " + repr(cia_z)
      elif tiporel_z == REL_INVEN_GPODIARY:
        sql_z = "select c.grupo from inv_invhist a join inv_relinv b"
        sql_z = sql_z + " on a.idart = b.idart and b.idrel = " + utils.IntToStr(REL_INVEN_GPODIARY)
        sql_z = sql_z + " join gpodiary c on b.iddato = c.idgpodiary"
        sql_z = sql_z + " where a.codigo= '" + codigo_z + "' and a.cia = " + repr(cia_z)
      elif tiporel_z == REL_INVEN_ARTDESP:
        sql_z = "select c.codigo from inv_invhist a join inv_relinv b"
        sql_z = sql_z + " on a.idart = b.idart and b.idrel = " + utils.IntToStr(REL_INVEN_ARTDESP)
        sql_z = sql_z + " join inv_grupos c on b.iddato = c.idgrupo"
        sql_z = sql_z + " where a.codigo= '" + codigo_z + "' and a.cia = " + repr(cia_z)
      elif tiporel_z == REL_INVEN_DESCRILAR:
        sql_z = "select d.concep as descri from inven a "
        sql_z = sql_z + " join inv_invhist b on b.codigo = a.codigo and b.cia = a.cia "
        sql_z = sql_z + " join inv_relinv c on c.idart = b.idart "
        sql_z = sql_z + " and c.idrel = " + utils.IntToStr(REL_INVEN_DESCRILAR)
        sql_z = sql_z + " join inv_conceps d on d.idconcep  = c.iddato"
        sql_z = sql_z + " where a.codigo= '" + codigo_z + "' and a.cia = " + str(cia_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         dato_z = record[0]
      #Fin de If
        
      return (dato_z)
# --- Fin de Busca Rel --------

# -- Rutina que tiene un iddato y regresa el valor  ----
def busca_dato(mydb, iddato_z, tipodato_z):
      dato_z = ""
      if tipodato_z == CONCEPTOS:
        sql_z = "select concepto from conceps where ncon = " + utils.IntToStr(iddato_z)
      if tipodato_z == INV_CONCEPS:
        sql_z = "select concep from inv_conceps where idconcep = " + utils.IntToStr(iddato_z)
      elif tipodato_z == POBLACIONES:
        sql_z = "select nombre from poblacs where numero = " + utils.IntToStr(iddato_z)
      elif tipodato_z == CREDCON:
        sql_z = "select descri from inv_credcon where idcrdcon = " + utils.IntToStr(iddato_z)
      elif tipodato_z == INV_INVHIST:
        sql_z = "select codigo from inv_invhist where idart = " + utils.IntToStr(iddato_z)
      elif tipodato_z == INV_SITUACIONES:
        sql_z = "select situacion from inv_situaciones where idsituac = " + utils.IntToStr(iddato_z)
      cursor = mydb.cursor()
      cursor.execute(sql_z)
      record = cursor.fetchone()
      if record <> None:
         dato_z = record[0]
      #End if
        
      return (dato_z)
# --- Fin de busca_dato --------

# --- Clase que Muestra los detalles del Movart --------
class despliega_detalle_movart:
  """Esta es una Clase que pide las Series"""
  def __init__(self, mydb, codigo_z, alm_z, folio_z, cia_z):
        dlg_movart = dirprogs_z + "dlg_movart.glade"
        self.mydb     = mydb
        self.codigo_z = codigo_z
        self.alm_z    = alm_z
        self.folio_z  = folio_z
        self.cia_z    = cia_z
        self.wTreeMovart       = gtk.glade.XML(dlg_movart)
        self.wdlgmovart     = self.wTreeMovart.get_widget("dlg_movart")
        dic = { "on_btn_anter_clicked": self.on_btn_anter_clicked, \
            "on_btn_sigte_clicked": self.on_btn_sigte_clicked, \
            "on_btn_origen_clicked": self.on_btn_origen_clicked, \
            "on_btn_destino_clicked": self.on_btn_destino_clicked, \
            "on_btn_salir_clicked": self.on_btn_salir_clicked 
            }
        self.wTreeMovart.signal_autoconnect(dic)

  def ejecuta(self):
      self.despliega_movart(self.codigo_z, self.alm_z, self.folio_z)
      resp_z = self.wdlgmovart.run()
      return(True)

  def on_btn_anter_clicked(self, widget):
      folio_z = utils.StrToInt(self.wTreeMovart.get_widget("edt_folio").get_text())
      alm_z = self.wTreeMovart.get_widget("edt_alm").get_text()
      folio_z = folio_z - 1
      self.despliega_movart(self.codigo_z, alm_z, folio_z)
      return (True)

  def on_btn_sigte_clicked(self, widget):
      folio_z = utils.StrToInt(self.wTreeMovart.get_widget("edt_folio").get_text())
      alm_z = self.wTreeMovart.get_widget("edt_alm").get_text()
      folio_z = folio_z + 1
      self.despliega_movart(self.codigo_z, alm_z, folio_z)
      return (True)

  def on_btn_origen_clicked(self, widget):
      folio_z = utils.StrToInt(self.wTreeMovart.get_widget("edt_folviene").get_text())
      alm_z = self.wTreeMovart.get_widget("edt_vienede").get_text()
      self.despliega_movart(self.codigo_z, alm_z, folio_z)
      return (True)

  def on_btn_destino_clicked(self, widget):
      folio_z = utils.StrToInt(self.wTreeMovart.get_widget("edt_folrec").get_text())
      alm_z = self.wTreeMovart.get_widget("edt_almrec").get_text()
      self.despliega_movart(self.codigo_z, alm_z, folio_z)
      return (True)

  def on_btn_salir_clicked(self, widget):
      self.wdlgmovart.destroy()

  def despliega_movart(self, codigo_z, alm_z, folio_z):
      movart = busca_folio_movart(self.mydb, codigo_z, alm_z, folio_z, self.cia_z)
      if movart['codigo'] == '':
         return (False)
      self.wTreeMovart.get_widget("edt_alm").set_text(movart['almac'])
      self.wTreeMovart.get_widget("edt_folio").set_text(utils.IntToStr(movart['folio']))
      self.wTreeMovart.get_widget("edt_serie").set_text(movart['serie'])
      self.wTreeMovart.get_widget("edt_costou").set_text(utils.currency(movart['costo']))
      self.wTreeMovart.get_widget("edt_entrapor").set_text(utils.IntToStr(movart['entrapor']))
      self.wTreeMovart.get_widget("edt_nument").set_text(utils.IntToStr(movart['nentrada']))
      self.wTreeMovart.get_widget("edt_fecha").set_text(utils.DateToStr(movart['fecha']))
      self.wTreeMovart.get_widget("edt_entcan").set_text(movart['entcan'])
      self.wTreeMovart.get_widget("edt_prove").set_text(movart['prove'])
      self.wTreeMovart.get_widget("edt_nombrepro").set_text(busca_dato(self.mydb, movart['nompro'], CONCEPTOS))
      self.wTreeMovart.get_widget("edt_fentori").set_text(utils.DateToStr(movart['fecentori']))
      self.wTreeMovart.get_widget("edt_modent").set_text(movart['modent'])
      self.wTreeMovart.get_widget("edt_vienede").set_text(movart['vienede'])
      if movart['folviene'] <> 0:
         self.wTreeMovart.get_widget("edt_folviene").set_text(utils.IntToStr(movart['folviene']))
      else:
         self.wTreeMovart.get_widget("edt_nument").set_text("")
      self.wTreeMovart.get_widget("edt_fvenfac").set_text(utils.DateToStr(movart['fecvencto']))
      self.wTreeMovart.get_widget("edt_folrec").set_text("")
      if movart['salio'] == 'S':
         self.wTreeMovart.get_widget("edt_salepor").set_text(utils.IntToStr(movart['salepor']))
         self.wTreeMovart.get_widget("edt_numsal").set_text(utils.IntToStr(movart['nsalida']))
         self.wTreeMovart.get_widget("edt_fechasal").set_text(utils.DateToStr(movart['fechasal']))
         self.wTreeMovart.get_widget("edt_modsal").set_text(movart['modsal'])
         self.wTreeMovart.get_widget("edt_comprador").set_text(busca_dato(self.mydb, movart['compro'], CONCEPTOS))
         self.wTreeMovart.get_widget("edt_almrec").set_text(movart['vahacia'])
         if movart['folrec'] <> 0:
            self.wTreeMovart.get_widget("edt_folrec").set_text(utils.IntToStr(movart['folrec']))
         self.wTreeMovart.get_widget("edt_poblac").set_text(busca_dato(self.mydb, movart['pueblo'], POBLACIONES))
         self.wTreeMovart.get_widget("edt_ptovta").set_text(movart['ptvta'])
         self.wTreeMovart.get_widget("edt_vend").set_text(movart['vend'])
      else:
         self.wTreeMovart.get_widget("edt_salepor").set_text("")
         self.wTreeMovart.get_widget("edt_numsal").set_text("")
         self.wTreeMovart.get_widget("edt_fechasal").set_text("")
         self.wTreeMovart.get_widget("edt_modsal").set_text("")
         self.wTreeMovart.get_widget("edt_comprador").set_text("")
         self.wTreeMovart.get_widget("edt_almrec").set_text("")
         self.wTreeMovart.get_widget("edt_poblac").set_text("")
         self.wTreeMovart.get_widget("edt_ptovta").set_text("")
         self.wTreeMovart.get_widget("edt_vend").set_text("")
      return (True)
# --Fin de despliega_movart ---      
