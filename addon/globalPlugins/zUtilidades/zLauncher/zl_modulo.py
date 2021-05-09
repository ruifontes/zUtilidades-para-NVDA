# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import gui
from tones import beep
import wx
import zipfile
import hashlib
from shutil import rmtree
from threading import Thread
import winsound
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zl_ajustes as ajustes
import zl_funciones as funciones

class zLanzador(wx.Dialog):
	def mensaje(self, mensaje, titulo, valor):
		if valor == 0:
			self.parametro = wx.OK | wx.ICON_INFORMATION
		elif valor == 1:
			self.parametro = wx.OK | wx.ICON_ERROR
		dlg = wx.MessageDialog(None, mensaje, titulo, self.parametro)
		dlg.SetOKLabel("&Aceptar")
		dlg.ShowModal()
		dlg.Destroy()

	def __init__(self, parent):

		WIDTH = 1200
		HEIGHT = 850
		pos = funciones._calculatePosition(WIDTH, HEIGHT)

		super(zLanzador,self).__init__(parent, -1, title="Lanzador de Aplicaciones", pos = pos, size = (WIDTH, HEIGHT))

		self.archivoAplicaciones = None
		self.dbAplicaciones = None
		ajustes.IS_WinON = True

		self.Panel = wx.Panel(self, 0)

		lbCategoria = wx.StaticText(self.Panel, wx.ID_ANY, label="&Categorías:")
		self.lstCategorias = wx.ListBox(self.Panel, 1, style = wx.LB_NO_SB)
		self.lstCategorias.Bind(wx.EVT_LISTBOX,self.onRefrescar)
		self.lstCategorias.Bind(wx.EVT_CONTEXT_MENU,self.menuCategoria)
		self.lstCategorias.Bind(wx.EVT_KEY_UP, self.onTeclasCategoria)

		lbAplicaciones = wx.StaticText(self.Panel, wx.ID_ANY, "&Lista aplicaciones:")
		self.lstAplicaciones = wx.ListBox(self.Panel, 2, style = wx.LB_NO_SB)
		self.lstAplicaciones.Bind(wx.EVT_CONTEXT_MENU,self.menuAplicaciones)
		self.lstAplicaciones.Bind(wx.EVT_KEY_UP, self.onTeclasAplicaciones)
 
		self.menuBTN = wx.Button(self.Panel, 3, "&Menú")
		self.menuBTN.Bind(wx.EVT_BUTTON,self.menuBoton)

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onSalir)

		szMain = wx.BoxSizer(wx.HORIZONTAL)
		szCategoria = wx.BoxSizer(wx.VERTICAL)
		szGeneral = wx.BoxSizer(wx.VERTICAL)

		szCategoria.Add(lbCategoria, 0)
		szCategoria.Add(self.lstCategorias, 1, wx.EXPAND)

		szGeneral.Add(lbAplicaciones, 0, wx.EXPAND)
		szGeneral.Add(self.lstAplicaciones, 1, wx.EXPAND)

		szGeneral.Add(self.menuBTN, 0, wx.EXPAND)

		szMain.Add(szCategoria, 0, wx.EXPAND)
		szMain.Add(szGeneral, 1, wx.EXPAND)

		self.Panel.SetSizer(szMain)

		self.onFocus()
		self.chkDatos()
		self.onRefrescar(None)
		ajustes.posicion = [0, 0]

		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onFocus(self):
		""" Definimos los controles de todos los widgets"""
		self.Bind(wx.EVT_ACTIVATE, self.onSetFocus)
		self.Panel.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)        
		# WidGets
		self.lstCategorias.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.lstAplicaciones.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		# Botones
		self.menuBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)

	def onSetFocus(self, event):
		"""Devolvemos el foco al último widget que lo tubo"""
		if event.GetActive() == True:
			getattr(self, ajustes.focoActual).SetFocus()
			pass

	def onSetSelection(self, event):
		"""Guarda en la variable el widgetque tiene el foco"""
		id_widgets = {
# WidGets generales
			0:"Panel",
			1:"lstCategorias",
			2:"lstAplicaciones",
			3:"menuBTN"
		}

		ajustes.focoActual = id_widgets.get(event.GetId())

	def chkDatos(self):
		tempDel = []
		for x in range(0, len(ajustes.nombreCategoria)):
			if os.path.isfile(os.path.join(ajustes.dbDir, ajustes.archivoCategoria[x])):
				pass
			else:
				ajustes.posicion = [0, 0]
				tempDel.append(x)

		for x in reversed(tempDel):
			del ajustes.nombreCategoria[x]
			del ajustes.archivoCategoria[x]

		ajustes.guardaCategorias()
		ajustes.refrescaCategorias()

		if len(ajustes.nombreCategoria) == 0:
			self.lstCategorias.Append("No hay categorías")
			self.lstCategorias.SetSelection(0)
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
			self.lstCategorias.SetSelection(ajustes.posicion[0])

		if self.lstCategorias.GetString(self.lstCategorias.GetSelection()) == "No hay categorías":
			self.lstAplicaciones.Append("Sin aplicaciones")
			self.lstAplicaciones.SetSelection(0)
		else:
			self.onRefrescar(None)

	def onRefrescar(self, event):
		seleccion = self.lstCategorias.GetSelection()
		nombre =self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		try:
			self.archivoAplicaciones = os.path.join(ajustes.dbDir, ajustes.archivoCategoria[seleccion])
			self.dbAplicaciones = ajustes.dbAplicaciones(self.archivoAplicaciones)
			self.dbAplicaciones.CargaDatos()
			ajustes.aplicacionesLista = self.dbAplicaciones.aplicacion
			if len(ajustes.aplicacionesLista) == 0:
				self.lstAplicaciones.Clear()
				self.lstAplicaciones.Append("Sin aplicaciones")
				self.lstAplicaciones.SetSelection(0)
			else:
				self.lstAplicaciones.Clear()
				for i in range(0, len(ajustes.aplicacionesLista)):
					self.lstAplicaciones.Append(ajustes.aplicacionesLista[i][1])
				try:
					self.lstAplicaciones.SetSelection(ajustes.posicion[1])
				except:
					self.lstAplicaciones.SetSelection(0)
		except:
			self.lstAplicaciones.Clear()
			self.lstAplicaciones.Append("Sin aplicaciones")
			self.lstAplicaciones.SetSelection(0)

	def onPosicion(self):
		ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstAplicaciones.GetSelection()]

	def menuBoton(self, event):
		self.menu = wx.Menu()

		self.categoria = wx.Menu()
		itemAñadir = self.categoria.Append(1, "&Añadir categoría")
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemAñadir)
		itemEditar = self.categoria.Append(2, "&Editar categoría")
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemEditar)
		itemBorrar = self.categoria.Append(3, "&Borrar categoría")
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemBorrar)
		self.menu.AppendSubMenu(self.categoria, "&Categorías")

		self.aplicacion = wx.Menu()

		self.añadir = wx.Menu()
		itemAñadirApp = self.añadir.Append(4, "Añadir &aplicación")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirApp)
		itemAñadirCmd = self.añadir.Append(5, "Añadir comando &CMD")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirCmd)
		itemAñadirFol = self.añadir.Append(6, "Añadir accesos a car&petas")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirFol)
		itemAñadirLnk = self.añadir.Append(7, "Añadir ejecutar accesos directos de &Windows")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirLnk)
		self.aplicacion.AppendSubMenu(self.añadir, "&Añadir")

		itemEditar = self.aplicacion.Append(10, "&Editar aplicación")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemEditar)
		itemBorrar = self.aplicacion.Append(11, "&Borrar aplicación")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemBorrar)
		self.menu.AppendSubMenu(self.aplicacion, "&Aplicaciones")

		self.copiaSeguridad = wx.Menu()
		itemHacer = self.copiaSeguridad.Append(20, "&Hacer copia de seguridad")
		self.Bind(wx.EVT_MENU, self.HacerBackup, itemHacer)
		itemRestaurar = self.copiaSeguridad.Append(21, "&Restaurar copia de seguridad")
		self.Bind(wx.EVT_MENU, self.RestaurarBackup, itemRestaurar)
		self.menu.AppendSubMenu(self.copiaSeguridad, "&Hacer o restaurar copias de seguridad")

		itemSalir = self.menu.Append(0, "&Salir")
		self.Bind(wx.EVT_MENU, self.onSalir, itemSalir)

		# Aqui lo que hace esto es llamar al constructor del menu para que se muestren los items centrados en la posición donde se encuentra el botón
		position = self.menuBTN.GetPosition()
		self.PopupMenu(self.menu,position)
		pass

	def menuCategoria(self, event):
		self.menu = wx.Menu()
		item1 = self.menu.Append(1, "&Añadir categoría")
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		item2 = self.menu.Append(2, "&Editar categoría")
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		item3 = self.menu.Append(3, "&Borrar categoría")
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		self.lstCategorias.PopupMenu(self.menu)

	def onMenuCategoria(self, event):
		id = event.GetId()
		nombreCategoria = self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		if id == 1:
			dlg = AñadirCategoria(self)
			res = dlg.ShowModal()
			if res == 0:
				self.añadirCategoria(dlg.texto.GetValue())
			else:
				dlg.Destroy()
		elif id == 2:
			if nombreCategoria == "No hay categorías":
				msg = \
"""No tiene ninguna categoría para Editar.

Agregue antes una para llevar a cabo esta acción."""
				self.mensaje(msg, "Información", 0)
			else:
				dlg = EditarCategoria(self)
				res = dlg.ShowModal()
				if res == 0:
					self.editarCategoria(dlg.texto.GetValue())
				else:
					dlg.Destroy()
		elif id == 3:
			if nombreCategoria == "No hay categorías":
				msg = \
"""No tiene ninguna categoría para Borrar.

Agregue antes una para llevar a cabo esta acción."""
				self.mensaje(msg, "Información", 0)
			else:
				msg = \
"""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar la categoría:

{}

Tenga en cuenta que al borrar la categoría se eliminaran las aplicaciones que estuvieran en dicha categoría.

¿Esta seguro que desea continuar?""".format(nombreCategoria)
				MsgBox = wx.MessageDialog(None, msg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				ret = MsgBox.ShowModal()
				if ret == wx.ID_YES:
					MsgBox.Destroy
					idel = ajustes.nombreCategoria.index(nombreCategoria)
					ifile = ajustes.archivoCategoria[idel]
					del ajustes.nombreCategoria[idel]
					del ajustes.archivoCategoria[idel]
					ajustes.aplicacionesLista = []
					try:
						os.remove(os.path.join(ajustes.dbDir, ifile))
					except:
						pass
					ajustes.guardaCategorias()
					self.lstCategorias.Clear()
					if len(ajustes.nombreCategoria) == 0:
						self.lstCategorias.Append("No hay categorías")
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(0)
					self.onRefrescar(None)
				else:
					MsgBox.Destroy

	def añadirCategoria(self, valor):
		ajustes.nombreCategoria.append(valor)
		nombre_archivo_db = False
		while nombre_archivo_db == False:
			nombre_archivo_db =  funciones.comprobar_archivo_db(15, ajustes.archivoCategoria)
			pass
		archivo = os.path.join(ajustes.dbDir, nombre_archivo_db)
		ajustes.dbAplicaciones(archivo).GuardaDatos()
		ajustes.archivoCategoria.append(nombre_archivo_db)
		ajustes.guardaCategorias()
		self.lstCategorias.Clear()
		if len(ajustes.nombreCategoria) == 0:
			self.lstCategorias.Append("No hay categorías")
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
		self.lstCategorias.SetSelection(ajustes.nombreCategoria.index(valor))
		self.onRefrescar(None)

	def editarCategoria(self, valor):
		indice = self.lstCategorias.GetSelection()
		del ajustes.nombreCategoria[indice]
		ajustes.nombreCategoria.insert(indice, valor)
		ajustes.guardaCategorias()
		self.lstCategorias.Clear()
		if len(ajustes.nombreCategoria) == 0:
			self.lstCategorias.Append("No hay categorías")
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
		self.lstCategorias.SetSelection(indice)
		self.onRefrescar(None)

	def onTeclasCategoria(self, event):
		if self.lstCategorias.GetSelection() == -1:
			pass
		else:
			if self.lstCategorias.GetString(self.lstCategorias.GetSelection()) == "No hay categorías":
				pass
			else:
				if (event.AltDown(), event.GetKeyCode()) == (True, 315):
					self.mueveCategoria("arriba")
					event.Skip()
				elif (event.AltDown(), event.GetKeyCode()) == (True, 317):
					self.mueveCategoria("abajo")
					event.Skip()

	def mueveCategoria(self, valor):
		indice = self.lstCategorias.GetSelection()
		if valor == "arriba":
			totalLista = len(ajustes.nombreCategoria) - 1
			if totalLista == -1:
				pass
			else:
				if indice == 0:
					beep(100,150)
				else:
					ajustes.nombreCategoria.insert(indice - 1, ajustes.nombreCategoria.pop(indice))
					ajustes.archivoCategoria.insert(indice - 1, ajustes.archivoCategoria.pop(indice))
					ajustes.guardaCategorias()
					self.lstCategorias.Clear()
					if len(ajustes.nombreCategoria) == 0:
						self.lstCategorias.Append("No hay categorías")
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(indice - 1)
				self.onRefrescar(None)
		elif valor == "abajo":
			totalLista = len(ajustes.nombreCategoria) - 1
			if totalLista == -1:
				pass
			else:
				if indice == totalLista:
					beep(200,150)
				else:
					ajustes.nombreCategoria.insert(indice + 1, ajustes.nombreCategoria.pop(indice))
					ajustes.archivoCategoria.insert(indice + 1, ajustes.archivoCategoria.pop(indice))
					ajustes.guardaCategorias()
					self.lstCategorias.Clear()
					if len(ajustes.nombreCategoria) == 0:
						self.lstCategorias.Append("No hay categorías")
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(indice + 1)
				self.onRefrescar(None)

	def menuAplicaciones(self, event):
		self.menu = wx.Menu()

		self.añadir = wx.Menu()
		itemAñadirApp = self.añadir.Append(4, "Añadir &aplicación")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirApp)
		itemAñadirCmd = self.añadir.Append(5, "Añadir comando &CMD")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirCmd)
		itemAñadirFol = self.añadir.Append(6, "Añadir accesos a car&petas")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirFol)
		itemAñadirLnk = self.añadir.Append(7, "Añadir ejecutar accesos directos de &Windows")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirLnk)
		self.menu.AppendSubMenu(self.añadir, "&Añadir")

		itemEditar = self.menu.Append(10, "&Editar aplicación")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemEditar)
		itemBorrar = self.menu.Append(11, "&Borrar aplicación")
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemBorrar)
		self.lstAplicaciones.PopupMenu(self.menu)

	def onMenuAplicacion(self, event):
		id = event.GetId()
		nombreCategoria = self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		nombreItem = self.lstAplicaciones.GetString(self.lstAplicaciones.GetSelection())
		indice = self.lstAplicaciones.GetSelection()
		if id == 4:
			if nombreCategoria == "No hay categorías":
				msg = \
"""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una aplicación."""
				self.mensaje(msg, "Información", 0)
			else:
				dlg = AñadirAplicacion(self)
				res = dlg.ShowModal()
				if res == 0:
					dlg.Destroy()
					ajustes.aplicacionesLista.append(dlg.lista)
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					self.onRefrescar(None)
				else:
					dlg.Destroy()
		elif id == 5:
			print("CMD")
		elif id == 6:
			print("Carpeta")
		elif id == 7:
			print("Acceso directo")
		elif id == 10:
			if nombreCategoria == "No hay categorías":
				msg = \
"""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una aplicación."""
				self.mensaje(msg, "Información", 0)
			else:
				if nombreItem == "Sin aplicaciones":
					msg = \
"""No tiene ninguna aplicación.

Agregue una antes para poder editar."""
					self.mensaje(msg, "Información", 0)
				else:
					if ajustes.aplicacionesLista[indice][0] == "app":
						dlg = EditarAplicacion(self)
					res = dlg.ShowModal()
					if res == 0:
						dlg.Destroy()
						if ajustes.aplicacionesLista[indice][0] == "app":
							del ajustes.aplicacionesLista[indice]
							ajustes.aplicacionesLista.insert(indice, dlg.lista)
							ajustes.guardaAplicaciones(self.dbAplicaciones)
							self.onRefrescar(None)

					else:
						dlg.Destroy()
		elif id == 11:
			if nombreCategoria == "No hay categorías":
				msg = \
"""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una aplicación."""
				self.mensaje(msg, "Información", 0)
			else:
				if nombreItem == "Sin aplicaciones":
					msg = \
"""No tiene ninguna aplicación.

Agregue una antes para poder borrar."""
					self.mensaje(msg, "Información", 0)
				else:
					msg = \
"""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar la aplicación:

{}

¿Esta seguro que desea continuar?""".format(nombreItem)
					MsgBox = wx.MessageDialog(None, msg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
					ret = MsgBox.ShowModal()
					if ret == wx.ID_YES:
						MsgBox.Destroy
						del ajustes.aplicacionesLista[indice]
						ajustes.guardaAplicaciones(self.dbAplicaciones)
						self.onRefrescar(None)
					else:
						MsgBox.Destroy

	def onTeclasAplicaciones(self, event):
		if self.lstAplicaciones.GetSelection() == -1:
			pass
		else:
			if self.lstAplicaciones.GetString(self.lstAplicaciones.GetSelection()) == "Sin aplicaciones":
				pass
			else:
				if event.GetKeyCode() == 32: # 13 Intro 32 Espacio
					self.onEjecuta(self.lstAplicaciones.GetSelection())
				elif (event.AltDown(), event.GetKeyCode()) == (True, 315):
					self.mueveAplicacion("arriba")
				elif (event.AltDown(), event.GetKeyCode()) == (True, 317):
					self.mueveAplicacion("abajo")
				event.Skip()

	def mueveAplicacion(self, valor):
		indice = self.lstAplicaciones.GetSelection()
		if valor == "arriba":
			totalLista = len(ajustes.aplicacionesLista) - 1
			if totalLista == -1:
				pass
			else:
				if indice == 0:
					beep(100,150)
				else:
					ajustes.aplicacionesLista.insert(indice - 1, ajustes.aplicacionesLista.pop(indice))
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstAplicaciones.GetSelection() - 1]
					self.onRefrescar(None)
		elif valor == "abajo":
			totalLista = len(ajustes.aplicacionesLista) - 1
			if totalLista == -1:
				pass
			else:
				if indice == totalLista:
					beep(200,150)
				else:
					ajustes.aplicacionesLista.insert(indice + 1, ajustes.aplicacionesLista.pop(indice))
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstAplicaciones.GetSelection() + 1]
					self.onRefrescar(None)

	def onEjecuta(self, valor):
		if ajustes.aplicacionesLista[valor][0] == "app":
			if os.path.isfile(ajustes.aplicacionesLista[valor][2]):
				self.onSalir(None)
				if ajustes.aplicacionesLista[valor][5] == False:
					if ajustes.aplicacionesLista[valor][3] == False:
						funciones.ejecutar(self, "open", ajustes.aplicacionesLista[valor][2], None, None, 10)
					else:
						funciones.ejecutar(self, "open", ajustes.aplicacionesLista[valor][2], ajustes.aplicacionesLista[valor][4], None, 10)
				else:
					if ajustes.aplicacionesLista[valor][3] == False:
						funciones.ejecutar(self, "runas", ajustes.aplicacionesLista[valor][2], None, None, 10)
					else:
						funciones.ejecutar(self, "runas", ajustes.aplicacionesLista[valor][2], ajustes.aplicacionesLista[valor][4], None, 10)
			else:
				indice = self.lstAplicaciones.GetSelection()
				msg = \
"""La ruta a la aplicación {}, no se encontró.

¿Desea editar la entrada de la aplicación para corregir el problema?""".format(self.lstAplicaciones.GetString(self.lstAplicaciones.GetSelection()))
				dlg = wx.MessageDialog( None, msg, "Aviso", wx.YES_NO | wx.ICON_QUESTION )
				aceptar = dlg.ShowModal()
				dlg.Destroy()
				if wx.ID_YES == aceptar:
					dlg = EditarAplicacion(self)
					res = dlg.ShowModal()
					if res == 0:
						dlg.Destroy()
						del ajustes.aplicacionesLista[indice]
						ajustes.aplicacionesLista.insert(indice, dlg.lista)
						ajustes.guardaAplicaciones(self.dbAplicaciones)
						self.onRefrescar(None)
					else:
						pass
				else:
					pass

	def HacerBackup(self, event):
		wildcard = "Archivo copia de seguridad zUtilidades (*.zut-zl)|*.zut-zl"
		dlg = wx.FileDialog(self, message="Guardar en...", defaultDir=os.getcwd(), defaultFile=funciones.fecha(), wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			fichero_final = os.path.basename(path)
			dlg.Destroy()
			dlg = BackupDialogo("Haciendo copia de seguridad…", path)
			result = dlg.ShowModal()
			if result == 0:
				pass
			else:
				pass
			dlg.Destroy()
		else:
			dlg.Destroy()
			pass

	def RestaurarBackup(self, event):
		xguiMsg = \
"""*** ADVERTENCIA ***

Esto borrara toda la base de datos del lanzador de aplicaciones

Toda la base de datos será sustituida por la copia de seguridad.

El complemento restaurara la copia de seguridad y se cerrara.

Esta acción no es reversible.

¿Desea continuar con el proceso?"""

		msg = wx.MessageDialog(None, xguiMsg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = msg.ShowModal()
		if ret == wx.ID_YES:
			msg.Destroy
			wildcard = "Archivo copia de seguridad zUtilidades (*.zut-zl)|*.zut-zl"
			dlgF = wx.FileDialog(None, message="Seleccione un archivo de copia de seguridad", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
			if dlgF.ShowModal() == wx.ID_OK:
				path = dlg.GetPath()
				dlgF.Destroy()
				dlg = BackupDialogo("Restaurando copia de seguridad…", path, True)
				result = dlg.ShowModal()
				if result == 0:
					dlg.Destroy()
					ajustes.refrescaCategoriasBackup()
					ajustes.posicion = [0, 0]
					ajustes.IS_WinON = False
					ajustes.focoActual = "lstCategorias"
					self.Destroy()
					gui.mainFrame.postPopup()
				else:
					dlg.Destroy()
			else:
				dlgF.Destroy()
				getattr(self, ajustes.focoActual).SetFocus()
		else:
			msg.Destroy

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			self.onPosicion()
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			event.Skip()

	def onSalir(self, event):
		self.onPosicion()
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class AñadirCategoria(wx.Dialog):
	def __init__(self, frame):

		super(AñadirCategoria, self).__init__(None, -1, title="Añadir categoría")

		self.frame = frame
		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label="&Introduzca el nombre de la categoría:")
		self.texto = wx.TextCtrl(self.Panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.texto.Bind(wx.EVT_TEXT_ENTER, self.onPass)

		self.AceptarBTN = wx.Button(self.Panel, 0, label="&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label="&Cancelar")
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.texto, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

	def onPass(self, event):
		pass

	def onAceptar(self, event):
		if self.texto.GetValue() == "":
			msg = \
"""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una categoría."""
			self.frame.mensaje(msg, "Información", 0)
			self.texto.SetFocus()
		else:
			p = funciones.estaenlistado(ajustes.nombreCategoria, self.texto.GetValue())
			if p == True:
				msg = \
"""No puede duplicar el nombre de una categoría.

Modifique el nombre para poder continuar."""
				self.frame.mensaje(msg, "Información", 0)
				self.texto.SetFocus()
			else:
				if self.IsModal():
					self.EndModal(event.EventObject.Id)
				else:
					self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class EditarCategoria(wx.Dialog):
	def __init__(self, frame):

		super(EditarCategoria, self).__init__(None, -1, title="Editar categoría")

		self.frame = frame
		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label="&Introduzca el nombre de la categoría:")
		self.texto = wx.TextCtrl(self.Panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.texto.Bind(wx.EVT_TEXT_ENTER, self.onPass)
		self.texto.SetValue(self.frame.lstCategorias.GetString(self.frame.lstCategorias.GetSelection()))

		self.AceptarBTN = wx.Button(self.Panel, 0, label="&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label="&Cancelar")
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.texto, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

	def onPass(self, event):
		pass

	def onAceptar(self, event):
		if self.texto.GetValue() == "":
			msg = \
"""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una categoría."""
			self.frame.mensaje(msg, "Información", 0)
			self.texto.SetFocus()
		else:
			if self.frame.lstCategorias.GetString(self.frame.lstCategorias.GetSelection()) == self.texto.GetValue():
				if self.IsModal():
					self.EndModal(event.EventObject.Id)
				else:
					self.Close()
			else:
				p = funciones.estaenlistado(ajustes.nombreCategoria, self.texto.GetValue())
				if p == True:
					msg = \
"""No puede duplicar el nombre de una categoría.

Modifique el nombre para poder continuar."""
					self.frame.mensaje(msg, "Información", 0)
					self.texto.SetFocus()
				else:
					if self.IsModal():
						self.EndModal(event.EventObject.Id)
					else:
						self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class AñadirAplicacion(wx.Dialog):
	def __init__(self, frame):

		super(AñadirAplicacion, self).__init__(None, -1, title="Añadir aplicación",size=(500,250))

		self.frame = frame
		self.parametro = False
		self.administrador = False
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label="Introduzca el nombre de la aplicación:")
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label="Ruta de la aplicación:")
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label="&Seleccionar archivo")
		self.Bind(wx.EVT_BUTTON, self.archivo_pulsar, id=self.directorioBTN.GetId())

		self.chkParametro = wx.CheckBox(self.Panel, 1, "Usar parámetros adicionales")
		label3 = wx.StaticText(self.Panel, wx.ID_ANY, label="Introduzca los parámetros para la aplicación:")
		self.textoParametro = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoParametro.Disable()

		self.chkAdministrador = wx.CheckBox(self.Panel, 2, "Ejecutar como administrador")
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label="&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label="&Cancelar")
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeD = wx.BoxSizer(wx.HORIZONTAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeD.Add(self.textoDirectorio, 1, wx.EXPAND)
		sizeD.Add(self.directorioBTN, 0)
		sizeV.Add(sizeD, 0, wx.EXPAND)

		sizeV.Add(self.chkParametro, 0, wx.EXPAND)
		sizeV.Add(label3, 0, wx.EXPAND)
		sizeV.Add(self.textoParametro, 0, wx.EXPAND)
		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.parametro = temp
			if self.parametro == False:
				self.textoParametro.Disable()
				self.textoParametro.Clear()
			else:
				self.textoParametro.Enable()
		elif id == 2:
			temp =  chk.GetValue()
			self.administrador = temp

	def archivo_pulsar(self, event):
		wildcard = "Todos los archivos ejecutables|*.exe;*.com;*.bat|" \
         "Archivo .exe (*.exe) | *.exe|" \
         "Archivo .com (*.com) | *.com|" \
         "Archivo .bat (*.bat) | *.bat|" \
         "Todos los ficheros (*.*)|*.*"    
		dlg = wx.FileDialog(None, message="Seleccione un archivo", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			for path in paths:
				rutacompleta_seleccionado = path
				archivo_seleccionado = os.path.basename(rutacompleta_seleccionado)
			self.textoDirectorio.Clear()
			self.textoDirectorio.SetValue(rutacompleta_seleccionado)
			self.textoDirectorio.SetFocus()
			dlg.Destroy()
		else:
			self.directorioBTN.SetFocus()
			dlg.Destroy()

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
"""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una aplicación."""
			self.frame.mensaje(msg, "Información", 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
"""El campo no puede quedar en blanco.

Seleccione una aplicación para poder continuar."""
				self.frame.mensaje(msg, "Información", 0)
				self.directorioBTN.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.aplicacionesLista)):
					listaTemporal.append(ajustes.aplicacionesLista[i][1])
				p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
"""No puede duplicar el nombre de una aplicación.

Modifique el nombre para poder continuar."""
					self.frame.mensaje(msg, "Información", 0)
					self.textoNombre.SetFocus()
				else:
					self.lista = ["app", self.textoNombre.GetValue(), self.textoDirectorio.GetValue(), self.parametro, self.textoParametro.GetValue(), self.administrador]
					if self.IsModal():
						self.EndModal(event.EventObject.Id)
					else:
						self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class EditarAplicacion(wx.Dialog):
	def __init__(self, frame):

		super(EditarAplicacion, self).__init__(None, -1, title="Editar aplicación",size=(500,250))

		self.frame = frame
		self.indice = self.frame.lstAplicaciones.GetSelection()
		self.parametro = ajustes.aplicacionesLista[self.indice][3]
		self.administrador = ajustes.aplicacionesLista[self.indice][5]
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label="Introduzca el nombre de la aplicación:")
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoNombre.SetValue(ajustes.aplicacionesLista[self.indice][1])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label="Ruta de la aplicación:")
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label="&Seleccionar archivo")
		self.Bind(wx.EVT_BUTTON, self.archivo_pulsar, id=self.directorioBTN.GetId())
		self.textoDirectorio.SetValue(ajustes.aplicacionesLista[self.indice][2])

		self.chkParametro = wx.CheckBox(self.Panel, 1, "Usar parámetros adicionales")
		self.chkParametro.SetValue(self.parametro)
		label3 = wx.StaticText(self.Panel, wx.ID_ANY, label="Introduzca los parámetros para la aplicación:")
		self.textoParametro = wx.TextCtrl(self.Panel, wx.ID_ANY)
		if self.parametro == True:
			self.textoParametro.Enable()
		else:
			self.textoParametro.Disable()
		self.textoParametro.SetValue(ajustes.aplicacionesLista[self.indice][4])

		self.chkAdministrador = wx.CheckBox(self.Panel, 2, "Ejecutar como administrador")
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 
		self.chkAdministrador.SetValue(self.administrador)

		self.AceptarBTN = wx.Button(self.Panel, 0, label="&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label="&Cancelar")
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeD = wx.BoxSizer(wx.HORIZONTAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeD.Add(self.textoDirectorio, 1, wx.EXPAND)
		sizeD.Add(self.directorioBTN, 0)
		sizeV.Add(sizeD, 0, wx.EXPAND)

		sizeV.Add(self.chkParametro, 0, wx.EXPAND)
		sizeV.Add(label3, 0, wx.EXPAND)
		sizeV.Add(self.textoParametro, 0, wx.EXPAND)
		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.parametro = temp
			if self.parametro == False:
				self.textoParametro.Disable()
				self.textoParametro.Clear()
			else:
				self.textoParametro.Enable()
		elif id == 2:
			temp =  chk.GetValue()
			self.administrador = temp

	def archivo_pulsar(self, event):
		wildcard = "Todos los archivos ejecutables|*.exe;*.com;*.bat|" \
         "Archivo .exe (*.exe) | *.exe|" \
         "Archivo .com (*.com) | *.com|" \
         "Archivo .bat (*.bat) | *.bat|" \
         "Todos los ficheros (*.*)|*.*"    
		dlg = wx.FileDialog(None, message="Seleccione un archivo", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			for path in paths:
				rutacompleta_seleccionado = path
				archivo_seleccionado = os.path.basename(rutacompleta_seleccionado)
			self.textoDirectorio.Clear()
			self.textoDirectorio.SetValue(rutacompleta_seleccionado)
			self.textoDirectorio.SetFocus()
			dlg.Destroy()
		else:
			self.directorioBTN.SetFocus()
			dlg.Destroy()

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
"""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una aplicación."""
			self.frame.mensaje(msg, "Información", 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
"""El campo no puede quedar en blanco.

Seleccione una aplicación para poder continuar."""
				self.frame.mensaje(msg, "Información", 0)
				self.directorioBTN.SetFocus()
			else:
				if self.textoNombre.GetValue() == ajustes.aplicacionesLista[self.indice][1]:
					self.lista = ["app", self.textoNombre.GetValue(), self.textoDirectorio.GetValue(), self.parametro, self.textoParametro.GetValue(), self.administrador]
					if self.IsModal():
						self.EndModal(event.EventObject.Id)
					else:
						self.Close()
				else:
					listaTemporal = []
					for i in range(0, len(ajustes.aplicacionesLista)):
						listaTemporal.append(ajustes.aplicacionesLista[i][1])
					p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
					if p == True:
						msg = \
"""No puede duplicar el nombre de una aplicación.

Modifique el nombre para poder continuar."""
						self.frame.mensaje(msg, "Información", 0)
						self.textoNombre.SetFocus()
					else:
						self.lista = ["app", self.textoNombre.GetValue(), self.textoDirectorio.GetValue(), self.parametro, self.textoParametro.GetValue(), self.administrador]
						if self.IsModal():
							self.EndModal(event.EventObject.Id)
						else:
							self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class HiloBackup(Thread):
	def __init__(self, frame, nombreFichero, restore=False):
		super(HiloBackup, self).__init__()

		self.frame = frame
		self.nombreFichero = nombreFichero
		self.restore = restore
		self.daemon = True
		self.start()

	def comprimir_directorio(self, nombrezip, directorio):
		total = 0
		for root, dirs, files in os.walk(directorio):
			for fname in files:
				path = os.path.join(root, fname)
				total += os.path.getsize(path)
		basename = os.path.basename(directorio)
		z = zipfile.ZipFile(nombrezip, 'w', zipfile.ZIP_DEFLATED)
		current = 0
		for root, dirs, files in os.walk(directorio):
			for fname in files:
				path = os.path.join(root, fname)
				arcname = os.path.join(basename, fname)
				progress = (lambda x, y: (int(x), int(x*y) % y/y))(100 * current / total, 1e0)
				filename = os.path.basename(arcname)
				wx.CallAfter(self.frame.TextoRefresco, "Comprimiendo el archivo: %s" % filename)
				wx.CallAfter(self.frame.next, progress[0])
				z.write(path, arcname)
				current += os.path.getsize(path)
		z.close()

	def descomprimir_zip(self, archivo, directorio_destino):
		zf = zipfile.ZipFile(archivo)
		uncompress_size = sum((file.file_size for file in zf.infolist()))
		extracted_size = 0
		for file in zf.infolist():
			extracted_size += file.file_size
			progress = (lambda x, y: (int(x), int(x*y) % y/y))((extracted_size * 100/uncompress_size), 1e0)
			filename = os.path.basename(file.filename)
			wx.CallAfter(self.frame.TextoRefresco, "Descomprimiendo el archivo: %s" % filename)
			wx.CallAfter(self.frame.next, progress[0])
			zf.extract(file, directorio_destino)

	def ponerComentario(self, archivo, comentario):
		with zipfile.ZipFile(archivo, 'a') as zip:
			zip.comment = comentario.encode("utf-8")

	def leerComentario(self, archivo):
		archive = zipfile.ZipFile(archivo, 'r')
		return archive.comment.decode("utf-8")

	def generar_md5(self, text):
		return hashlib.md5(text).hexdigest()

	def generar_listaZIP(self, archivo):
		with zipfile.ZipFile(archivo, "r") as zip_ref:
			lista_ficheros = zip_ref.namelist()
		lista_unida = "-".join(lista_ficheros)
		return lista_unida.encode("utf-8")

	def chk_validez(self, archivo):
		p = self.leerComentario(archivo)
		if self.generar_md5(self.generar_listaZIP(archivo)) == p:
			return True
		else:
			return False

	def run(self):
		if self.restore == False:
			try:
# Creamos el archivo zip
				self.comprimir_directorio(self.nombreFichero, ajustes.dbDir)
# Creamos el md5 a partir de la lista de archivos del zip
				self.ponerComentario(self.nombreFichero, self.generar_md5(self.generar_listaZIP(self.nombreFichero)))
#Comprobamos el md5 del archivo con el md5 del comentario y si es correcto terminamos
				t = self.chk_validez(self.nombreFichero)
				if t == False:
					try:
						os.remove(self.nombreFichero)
					except:
						pass
					wx.CallAfter(self.frame.error, "Algo salió mal.\n" + "Inténtelo de nuevo.\n" + "Ya puede cerrar esta ventana.")
				else:
					wx.CallAfter(self.frame.next, 100)
					wx.CallAfter(self.frame.done, "La copia de seguridad fue un éxito.\nYa puede cerrar esta ventana.")
			except:
				try:
					os.remove(self.nombreFichero)
				except:
					pass
				wx.CallAfter(self.frame.error, "Algo salió mal.\n" + "Inténtelo de nuevo.\n" + "Ya puede cerrar esta ventana.")
		elif self.restore == True:
			try:
				t = self.chk_validez(self.nombreFichero)
				if t == False:
					wx.CallAfter(self.frame.error, "Algo salió mal.\n" + "Inténtelo de nuevo.\n" + "Ya puede cerrar esta ventana.")
				else:
					rmtree(ajustes.dbDir)
					self.descomprimir_zip(self.nombreFichero, ajustes.dirRestaura)
				wx.CallAfter(self.frame.next, 100)
				wx.CallAfter(self.frame.done, "Se completo la restauración correctamente.\n" + "Ya puede cerrar esta ventana.")
			except:
				wx.CallAfter(self.frame.error, "Algo salió mal.\n" + "Inténtelo de nuevo.\n" + "Ya puede cerrar esta ventana.")

class BackupDialogo(wx.Dialog):
	def __init__(self, titulo, nombreFichero, restore=False):

		super(BackupDialogo, self).__init__(None, -1, title=titulo)

		self.Centre()

		self.nombreFichero = nombreFichero
		self.restore = restore

		self.Panel = wx.Panel(self)

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.AceptarTRUE = wx.Button(self.Panel, 0, "&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, 1, "&Cerrar")
		self.Bind(wx.EVT_BUTTON, self.onAceptarFALSE, id=self.AceptarFALSE.GetId())
		self.AceptarFALSE.Disable()

		self.Bind(wx.EVT_CLOSE, self.onNull)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.progressBar, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.AceptarTRUE, 2, wx.CENTER)
		sizer_botones.Add(self.AceptarFALSE, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		if self.restore == False:
			HiloBackup(self, self.nombreFichero)
		else:
			HiloBackup(self, self.nombreFichero, self.restore)

		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

	def next(self, event):
		self.progressBar.SetValue(event)

	def TextoRefresco(self, event):
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)

	def done(self, event):
		winsound.MessageBeep(0)
		self.AceptarTRUE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def error(self, event):
		winsound.MessageBeep(16)
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def onAceptarTRUE(self, event):
		if self.IsModal():
			self.EndModal(0)
		else:
			self.Close()

	def onAceptarFALSE(self, event):
		if self.IsModal():
			self.EndModal(1)
		else:
			self.Close()
