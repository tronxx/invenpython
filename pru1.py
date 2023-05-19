#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
###############################################################################
# ADMINCFD - Administra archivos de CFD
# Autor: Ricardo Torres
# email: rictor@cuhrt.com
# blog: htpp://rctorr.wordpress.com
# twitter: @rctorr
#
# Descripci�n
# Este script ayuda a leer un CFD para despues formatear el nombre del archivo
# de la siguiente manera:
#    Fecha_RFCemisor_serie_folio_subtotal_iva_total.xml
#
# Fecha: Fecha en que se gener� el comprobante
# RFCemisor: RFC de quien emite el cfd/cfdi
# Serie y Folio: Numero de Serie y folio de la factura
# Subtotal, iva, total: Importes de la factura.
#
# El nombre del xml se proporciona desde la l�nea de comandos, de tal forma que
# se puede usar en alg�n otro script para automatizar el proceso.
#
###############################################################################
 
# Ver 1.0
# - Se lee el nombre del archivo desde la l�nea de comando
# - Se leer los atributos del archivo xml
# - Genera el nombre con la sintaxis solicitada
# - Renombra el archivo xml al nuevo nombre
#
 
import sys
import os.path
import datetime
import os
from optparse import OptionParser
import ConfigParser
from xml.dom import minidom


xmlDoc = minidom.parse('\tmp\d1.xml')
nodes = xmlDoc.childNodes
comprobante = nodes[0]
compAtrib = dict(comprobante.attributes.items())
emisor = comprobante.getElementsByTagName('Emisor')
self.atributos['rfc'] = emisor[0].getAttribute('rfc')
self.atributos['nombre'] = emisor[0].getAttribute('nombre')

print self.atributos['rfc']
print self.atributos['nombre']
