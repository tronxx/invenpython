#!/usr/bin/env python

# ejemplo entry.py

import pygtk
pygtk.require('2.0')
import gtk
import MySQLdb
import def_tablas

global mydb
global cia_z
global mibd

#-- Define additional constants
EXIT         = 0
CONTINUE     = 1
NUEVO        = 1
MODIFICA     = 2
BORRAR       = 3
modo_z   = 0
mibd = def_tablas.lee_basedato_ini()
cias = def_tablas.define_cias()

vendedor = {'codigo': '',
            'nombre': ''
           }

class MantoVnd:
    def enter_callback(self, widget, entry):
        entry_text = entry.get_text()
        print "Entry contents: %s\n" % entry_text

    def entry_toggle_editable(self, checkbutton, entry):
        entry.set_editable(checkbutton.get_active())

    def entry_toggle_visibility(self, checkbutton, entry):
        entry.set_visibility(checkbutton.get_active())

    def __init__(self):
        # create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.set_size_request(200, 100)
        window.set_title("Mantenimiento de Vendedores")
        window.connect("delete_event", lambda w,e: gtk.main_quit())

        vbox = gtk.VBox(gtk.FALSE, 0)
        window.add(vbox)
        vbox.show()

        self.h_sizer_btn = gtk.HButtonBox()
        self.h_sizer_btn.set_layout(gtk.BUTTONBOX_SPREAD)

        self.h_sizer_btn.show()
        # and a few controls
#        btn_primer = gtk.Button("Primero")
#        btn_anter  = gtk.Button("Anterior")
#        btn_sigte  = gtk.Button("Siguiente")
#        btn_ultim  = gtk.Button("Ultimo")
        btn_nuevo  = gtk.Button("Nuevo")
        btn_modif  = gtk.Button("Modifica")
        btn_borra  = gtk.Button("Borra")

#        self.h_sizer_btn.add(btn_primer)
#        btn_primer.show()
#        self.h_sizer_btn.add(btn_anter)
#        btn_anter.show()
#        self.h_sizer_btn.add(btn_sigte)
#        btn_sigte.show()
#        self.h_sizer_btn.add(btn_ultim)
#        btn_ultim.show()
        self.h_sizer_btn.add(btn_nuevo)
        btn_nuevo.show()
        self.h_sizer_btn.add(btn_modif)
        btn_modif.show()
        self.h_sizer_btn.add(btn_borra)
        btn_borra.show()
        vbox.pack_start(self.h_sizer_btn, gtk.TRUE, gtk.TRUE, 0)
        vbox.show()
        btn_nuevo.connect ("clicked", self.OnNuevoButton,  None)
        btn_modif.connect ("clicked", self.OnModifButton,  None)
        btn_borra.connect ("clicked", self.OnBorraButton,  None)
#        btn_primer.connect("clicked", self.OnPrimerButton, None)
#        btn_anter.connect ("clicked", self.OnAnterButton,  None)
#        btn_sigte.connect ("clicked", self.OnSigteButton,  None)
#        btn_ultim.connect ("clicked", self.OnUltimButton,  None)


        h_sizer = gtk.HBox(homogeneous=gtk.FALSE, spacing=5)
	lbl_codigo      = gtk.Label("Codigo")
        self.edt_codigo = gtk.Entry(max=3)
        self.edt_codigo.set_width_chars(4)
	lbl_nombre      = gtk.Label("Nombre")
        self.edt_nombre = gtk.Entry(max=20)
        self.edt_nombre.set_width_chars(22)
	lbl_esp      = gtk.Label(" ")
        h_sizer.pack_start(lbl_codigo, gtk.TRUE, gtk.TRUE, 5)
        lbl_codigo.show()
        h_sizer.pack_start(self.edt_codigo, gtk.TRUE, gtk.TRUE, 5)
        self.edt_codigo.show()
        h_sizer.pack_start(lbl_nombre, gtk.TRUE, gtk.TRUE, 5)
        lbl_nombre.show()
        h_sizer.pack_start(self.edt_nombre, gtk.TRUE, gtk.TRUE, 5)
        self.edt_nombre.show()
        h_sizer.show()
        vbox.pack_start(h_sizer, gtk.TRUE, gtk.TRUE, 0)
        vbox.show()  
        
        self.liststore = gtk.ListStore(str, str, str)
        self.treeview = gtk.TreeView(self.liststore)

        # create the TreeViewColumns to display the data
        self.tvcolumn = gtk.TreeViewColumn('Codigo')
        self.tvcolumn1 = gtk.TreeViewColumn('Nombre')

        # add a row with text and a stock item - color strings for
        # the background
        mydb = MySQLdb.connect(mibd['host'], mibd['user'], mibd['password'], mibd['base'])

        vendedores_z = []
        cursor = mydb.cursor()
        sql_z = "select codigo, nombre from vendedor order by codigo"
        cursor.execute(sql_z)
        result = cursor.fetchall()
        for record in result:
          self.liststore.append([ record[0], "", record[1] ])
        # add columns to treeview
        self.treeview.append_column(self.tvcolumn)
        self.treeview.append_column(self.tvcolumn1)

        # create a CellRenderers to render the data
        self.cell = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()

        # add the cells to the columns - 2 in the first
        self.tvcolumn.pack_start(self.cell, False)
        self.tvcolumn1.pack_start(self.cell1, False)

        # set the cell attributes to the appropriate liststore column
        self.tvcolumn.set_attributes(self.cell, text=0)
        self.tvcolumn1.set_attributes(self.cell1, text=2)
        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(0)
        self.treeview.set_reorderable(True)
#        self.treeview.set_grid_lines(True)
        self.treeview.connect("cursor-changed", self.get_seleccion)
#        self.treeview.connect("row_selected", self.get_seleccion)
        
        vbox.pack_start(self.treeview, gtk.FALSE, gtk.FALSE, 0)
        vbox.show()
        window.show_all()

    def OnPrimerButton(self, widget, data=None):
         self.busca_vnd("P")

    def OnAnterButton(self, widget, data=None):
         self.busca_vnd("A", vendedor['codigo'])

    def OnSigteButton(self, widget, data=None):
         self.busca_vnd("S", vendedor['codigo'])

    def OnUltimButton(self, widget, data=None):
         self.busca_vnd("U")

    def OnNuevoButton(self, widget, data=None):
         global modo_z
         modo_z = NUEVO
         result_z = self.Dialog_pide_datos(None, None)

    def OnModifButton(self, widget, data=None):
         global modo_z
         modo_z = MODIFICA
         self.get_seleccion(None, None)
         result_z = self.Dialog_pide_datos(None, None)

    def OnBorraButton(self, widget, data=None):
         global modo_z
         modo_z = BORRAR
         self.get_seleccion(None, None)
         codigo_z = vendedor['codigo']
         nombre_z = vendedor['nombre']
         message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Seguro de Eliminar este Vendedor ? \n" + nombre_z)
         message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
         message.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
         resp = message.run()
         if resp == gtk.RESPONSE_OK:
            sql_z = "delete from vendedor where codigo='" + codigo_z + "'"
            cursor = mydb.cursor()
            cursor.execute(sql_z)
            self.edt_codigo.set_text('')
            self.edt_nombre.set_text('')
         #End if
         message.destroy()

    def busca_vnd(self, hacia_z, codigo_z=''):
        global mydb
        cursor = mydb.cursor()
        if hacia_z == 'P':
          sql_z = "SELECT codigo, nombre FROM vendedor where codigo = ( select min(codigo) from vendedor)"
        elif hacia_z == 'U':
          sql_z = "SELECT codigo, nombre FROM vendedor where codigo = ( select max(codigo) from vendedor)"
        elif hacia_z == 'A':
          sql_z = "SELECT codigo, nombre FROM vendedor where codigo = ( select max(codigo) from vendedor where codigo < '" + codigo_z + "')"
        elif hacia_z == 'S':
          sql_z = "SELECT codigo, nombre FROM vendedor where codigo = ( select min(codigo) from vendedor where codigo > '" + codigo_z + "')"
# execute SQL statement
        cursor.execute(sql_z)
        numrows = int(cursor.rowcount)
        if numrows > 0:
          record = cursor.fetchone()
          vendedor['codigo'] = record[0]
          vendedor['nombre'] = record[1]
          
        self.edt_codigo.set_text(vendedor['codigo'])
        self.edt_nombre.set_text(vendedor['nombre'])

    def get_seleccion(self, widget, data=None, data2=None):
       self.edt_nombre.set_text("Estoy en Selected")
       # Get the selection in the gtk.TreeView
       selection = self.treeview.get_selection()
       # Get the selection iter
       model, selection_iter = selection.get_selected()
       if (selection_iter):
          codigo_z = self.liststore.get_value(selection_iter, 0)
          nombre_z = self.liststore.get_value(selection_iter, 2)
          self.edt_codigo.set_text(codigo_z)
          self.edt_nombre.set_text(nombre_z)
          vendedor['codigo'] = codigo_z;
          vendedor['nombre'] = nombre_z;
          
    

    def Dialog_pide_datos(self, widget, data=None):
    	self.dlg_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    	self.dlg_window = gtk.Dialog(title="Teclee los datos", parent=None, flags=gtk.DIALOG_MODAL)
#    	self.dlg_window.connect("delete_event", self.delete_event)
#    	self.dlg_window.connect("destroy", self.dlg_destroy)
        self.dlg_window.show()
    	self.dlg_okcancel = 0
        
        self.dlg_h_sizer_btn = gtk.HButtonBox()
        self.dlg_h_sizer_btn.set_layout(gtk.BUTTONBOX_SPREAD)
        self.dlg_h_sizer_btn.set_spacing(40)
        self.dlg_btn_ok     = gtk.Button("Aceptar", gtk.STOCK_OK)
        self.dlg_btn_cancel = gtk.Button("Cancelar", gtk.STOCK_CANCEL)
        self.dlg_h_sizer_btn.add(self.dlg_btn_ok)
        self.dlg_btn_ok.show()
        self.dlg_h_sizer_btn.add(self.dlg_btn_cancel)
        self.dlg_btn_cancel.show()
        self.dlg_h_sizer_btn.show()

        #Create the static text widget and set the text
	self.dlg_datos_h_sizer = gtk.HBox(gtk.FALSE, 0)
	dlg_lbl_codigo      = gtk.Label("Codigo")
        self.dlg_edt_codigo = gtk.Entry(max=3)
	dlg_lbl_nombre      = gtk.Label("Nombre")
        self.dlg_edt_nombre = gtk.Entry(max=20)
        self.dlg_datos_h_sizer.pack_start(dlg_lbl_codigo, gtk.FALSE, gtk.FALSE, 0)

        if modo_z == MODIFICA:
           self.dlg_edt_codigo.set_text(vendedor['codigo'])
           self.dlg_edt_nombre.set_text(vendedor['nombre'])

        dlg_lbl_codigo.show()
        self.dlg_datos_h_sizer.pack_start(self.dlg_edt_codigo, gtk.FALSE, gtk.FALSE, 0)
        self.dlg_edt_codigo.show()
        self.dlg_datos_h_sizer.pack_start(dlg_lbl_nombre, gtk.FALSE, gtk.FALSE, 0)
        dlg_lbl_nombre.show()
        self.dlg_datos_h_sizer.pack_start(self.dlg_edt_nombre, gtk.FALSE, gtk.FALSE, 0)
        self.dlg_edt_nombre.show()
        self.dlg_datos_h_sizer.show()
        
        self.dlg_btn_ok.connect("clicked", self.OnAceptar, None)
        self.dlg_btn_cancel.connect("clicked", self.OnCancelar, None)

        self.dlg_sizer = gtk.VBox(gtk.FALSE, 0)
        self.dlg_sizer.pack_start(self.dlg_datos_h_sizer, gtk.TRUE, gtk.TRUE, 0)
        self.dlg_sizer.show()
        self.dlg_sizer.pack_start(self.dlg_h_sizer_btn, gtk.TRUE, gtk.TRUE, 0)
        self.dlg_sizer.show()
#       self.dlg_window.add(self.dlg_sizer)
        self.dlg_window.action_area.pack_start(self.dlg_sizer, gtk.TRUE, gtk.TRUE, 0)
        if modo_z == MODIFICA:
           self.dlg_edt_nombre.grab_focus()
        else:
           self.dlg_edt_codigo.grab_focus()
    
    def OnAceptar(self, widget, data=None):
        global modo_z
        sql_z = ''
        self.okcancel = gtk.TRUE
        codigo_z = self.dlg_edt_codigo.get_text().upper()
        nombre_z = self.dlg_edt_nombre.get_text().upper()
        cursor = mydb.cursor()
        if modo_z == NUEVO:
           sql_z = "insert into vendedor ( codigo, nombre ) values ('"+ codigo_z + "','"+ nombre_z + "')"
           self.liststore.append([ codigo_z, "", nombre_z ])
        elif modo_z == MODIFICA:
           sql_z = "update vendedor set nombre = '"+ nombre_z + "' where codigo='" + codigo_z + "'"
        
        self.edt_codigo.set_text(codigo_z)
        self.edt_nombre.set_text(nombre_z)

        cursor.execute(sql_z)
        self.dlg_window.destroy()

    def OnCancelar(self, widget, data=None):
        self.okcancel = gtk.FALSE
        self.dlg_window.destroy()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    MantoVnd()
    main()
