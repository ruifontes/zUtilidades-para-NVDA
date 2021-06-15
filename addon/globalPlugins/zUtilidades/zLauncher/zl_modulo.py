# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import gui
import globalVars
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

# For translation
addonHandler.initTranslation()

class zLanzador(wx.Dialog):
	def mensaje(self, mensaje, titulo, valor):
		if valor == 0:
			self.parametro = wx.OK | wx.ICON_INFORMATION
		elif valor == 1:
			self.parametro = wx.OK | wx.ICON_ERROR
		dlg = wx.MessageDialog(None, mensaje, titulo, self.parametro)
		dlg.SetOKLabel(_("&Aceptar"))
		dlg.ShowModal()
		dlg.Destroy()

	def __init__(self, parent):

		WIDTH = 1200
		HEIGHT = 850
		pos = funciones._calculatePosition(WIDTH, HEIGHT)

		super(zLanzador,self).__init__(parent, -1, title=_("Lanzador de Aplicaciones"), pos = pos, size = (WIDTH, HEIGHT))

		self.archivoAplicaciones = None
		self.dbAplicaciones = None
		ajustes.IS_WinON = True

		self.Panel = wx.Panel(self, 0)

		lbCategoria = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Categorías:"))
		self.lstCategorias = wx.ListBox(self.Panel, 1, style = wx.LB_NO_SB)
		self.lstCategorias.Bind(wx.EVT_LISTBOX,self.onRefrescar)
		self.lstCategorias.Bind(wx.EVT_CONTEXT_MENU,self.menuCategoria)
		self.lstCategorias.Bind(wx.EVT_KEY_UP, self.onTeclasCategoria)

		lbAplicaciones = wx.StaticText(self.Panel, wx.ID_ANY, _("&Lista aplicaciones:"))
		self.lstAplicaciones = wx.ListBox(self.Panel, 2, style = wx.LB_NO_SB)
		self.lstAplicaciones.Bind(wx.EVT_CONTEXT_MENU,self.menuAplicaciones)
		self.lstAplicaciones.Bind(wx.EVT_KEY_UP, self.onTeclasAplicaciones)
 
		self.menuBTN = wx.Button(self.Panel, 3, _("&Menú"))
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

		self.CenterOnScreen()

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
			self.lstCategorias.Append(_("No hay categorías"))
			self.lstCategorias.SetSelection(0)
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
			self.lstCategorias.SetSelection(ajustes.posicion[0])

		if self.lstCategorias.GetString(self.lstCategorias.GetSelection()) == _("No hay categorías"):
			self.lstAplicaciones.Append(_("Sin acciones"))
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
				self.lstAplicaciones.Append(_("Sin acciones"))
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
			self.lstAplicaciones.Append(_("Sin acciones"))
			self.lstAplicaciones.SetSelection(0)

	def onPosicion(self):
		ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstAplicaciones.GetSelection()]

	def menuBoton(self, event):
		self.menu = wx.Menu()

		self.categoria = wx.Menu()
		itemAñadir = self.categoria.Append(1, _("&Añadir categoría"))
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemAñadir)
		itemEditar = self.categoria.Append(2, _("&Editar categoría"))
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemEditar)
		itemBorrar = self.categoria.Append(3, _("&Borrar categoría"))
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemBorrar)
		self.menu.AppendSubMenu(self.categoria, _("&Categorías"))

		self.aplicacion = wx.Menu()

		self.añadir = wx.Menu()
		itemAñadirApp = self.añadir.Append(4, _("Añadir &aplicación"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirApp)
		itemAñadirCmd = self.añadir.Append(5, _("Añadir comando &CMD"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirCmd)
		itemAñadirFol = self.añadir.Append(6, _("Añadir accesos a car&petas"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirFol)
		itemAñadirLnk = self.añadir.Append(7, _("Añadir ejecutar accesos directos de &Windows"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirLnk)
		itemAñadirInstalada = self.añadir.Append(8, _("Añadir aplicación &instalada"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirInstalada)
		self.aplicacion.AppendSubMenu(self.añadir, _("&Añadir acción"))

		itemEditar = self.aplicacion.Append(10, _("&Editar acción"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemEditar)
		itemBorrar = self.aplicacion.Append(11, _("&Borrar acción"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemBorrar)
		self.menu.AppendSubMenu(self.aplicacion, _("&Acciones"))

		self.copiaSeguridad = wx.Menu()
		itemHacer = self.copiaSeguridad.Append(20, _("&Hacer copia de seguridad"))
		self.Bind(wx.EVT_MENU, self.HacerBackup, itemHacer)
		itemRestaurar = self.copiaSeguridad.Append(21, _("&Restaurar copia de seguridad"))
		self.Bind(wx.EVT_MENU, self.RestaurarBackup, itemRestaurar)
		self.menu.AppendSubMenu(self.copiaSeguridad, _("&Hacer o restaurar copias de seguridad"))

		self.opciones = wx.Menu()
		itemdefecto = self.opciones.Append(wx.ID_ANY, _("&Volver a valores por defecto el lanzador de aplicaciones"))
		self.Bind(wx.EVT_MENU, self.borrarValores, itemdefecto)
		self.menu.AppendSubMenu(self.opciones, _("&Opciones"))

		itemSalir = self.menu.Append(0, _("&Salir"))
		self.Bind(wx.EVT_MENU, self.onSalir, itemSalir)

		# Aqui lo que hace esto es llamar al constructor del menu para que se muestren los items centrados en la posición donde se encuentra el botón
		position = self.menuBTN.GetPosition()
		self.PopupMenu(self.menu,position)
		pass

	def menuCategoria(self, event):
		self.menu = wx.Menu()
		item1 = self.menu.Append(1, _("&Añadir categoría"))
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		item2 = self.menu.Append(2, _("&Editar categoría"))
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		item3 = self.menu.Append(3, _("&Borrar categoría"))
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
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría para Editar.

Agregue antes una para llevar a cabo esta acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = EditarCategoria(self)
				res = dlg.ShowModal()
				if res == 0:
					self.editarCategoria(dlg.texto.GetValue())
				else:
					dlg.Destroy()
		elif id == 3:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría para Borrar.

Agregue antes una para llevar a cabo esta acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				msg = \
_("""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar la categoría:

{}

Tenga en cuenta que al borrar la categoría se eliminaran las aplicaciones que estuvieran en dicha categoría.

¿Esta seguro que desea continuar?""").format(nombreCategoria)
				MsgBox = wx.MessageDialog(None, msg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
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
						self.lstCategorias.Append(_("No hay categorías"))
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
			self.lstCategorias.Append(_("No hay categorías"))
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
			self.lstCategorias.Append(_("No hay categorías"))
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
		self.lstCategorias.SetSelection(indice)
		self.onRefrescar(None)

	def onTeclasCategoria(self, event):
		if self.lstCategorias.GetSelection() == -1:
			pass
		else:
			if self.lstCategorias.GetString(self.lstCategorias.GetSelection()) == _("No hay categorías"):
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
						self.lstCategorias.Append(_("No hay categorías"))
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
						self.lstCategorias.Append(_("No hay categorías"))
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(indice + 1)
				self.onRefrescar(None)

	def menuAplicaciones(self, event):
		self.menu = wx.Menu()

		self.añadir = wx.Menu()
		itemAñadirApp = self.añadir.Append(4, _("Añadir &aplicación"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirApp)
		itemAñadirCmd = self.añadir.Append(5, _("Añadir comando &CMD"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirCmd)
		itemAñadirFol = self.añadir.Append(6, _("Añadir accesos a car&petas"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirFol)
		itemAñadirLnk = self.añadir.Append(7, _("Añadir ejecutar accesos directos de &Windows"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirLnk)
		itemAñadirInstalada = self.añadir.Append(8, _("Añadir aplicación &instalada"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemAñadirInstalada)

		self.menu.AppendSubMenu(self.añadir, _("&Añadir acción"))

		itemEditar = self.menu.Append(10, _("&Editar acción"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemEditar)
		itemBorrar = self.menu.Append(11, _("&Borrar acción"))
		self.Bind(wx.EVT_MENU, self.onMenuAplicacion, itemBorrar)
		self.lstAplicaciones.PopupMenu(self.menu)

	def onMenuAplicacion(self, event):
		id = event.GetId()
		nombreCategoria = self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		nombreItem = self.lstAplicaciones.GetString(self.lstAplicaciones.GetSelection())
		indice = self.lstAplicaciones.GetSelection()
		if id == 4:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
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
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = AñadirCMD(self)
				res = dlg.ShowModal()
				if res == 0:
					dlg.Destroy()
					ajustes.aplicacionesLista.append(dlg.lista)
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					self.onRefrescar(None)
				else:
					dlg.Destroy()

		elif id == 6:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = AñadirCarpeta(self)
				res = dlg.ShowModal()
				if res == 0:
					dlg.Destroy()
					ajustes.aplicacionesLista.append(dlg.lista)
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					self.onRefrescar(None)
				else:
					dlg.Destroy()

		elif id == 7:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = AñadirAcceso(self)
				res = dlg.ShowModal()
				if res == 0:
					dlg.Destroy()
					ajustes.aplicacionesLista.append(dlg.lista)
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					self.onRefrescar(None)
				else:
					dlg.Destroy()

		elif id == 8:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = AñadirInstalada(self)
				res = dlg.ShowModal()
				if res == 0:
					dlg.Destroy()
					ajustes.aplicacionesLista.append(dlg.lista)
					ajustes.guardaAplicaciones(self.dbAplicaciones)
					self.onRefrescar(None)
				else:
					dlg.Destroy()

		elif id == 10:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				if nombreItem == _("Sin acciones"):
					msg = \
_("""No tiene ninguna acción.

Agregue una antes para poder editar.""")
					self.mensaje(msg, _("Información"), 0)
				else:
					if ajustes.aplicacionesLista[indice][0] == "sap":
						msg = \
_("""Esta acción no es editable.

Si lo desea puede eliminarla y volver a añadir otra.""")
						self.mensaje(msg, _("Información"), 0)
					else:
						if ajustes.aplicacionesLista[indice][0] == "app":
							dlg = EditarAplicacion(self)
						if ajustes.aplicacionesLista[indice][0] == "cmd":
							dlg = EditarCMD(self)
						if ajustes.aplicacionesLista[indice][0] == "fol":
							dlg = EditarCarpeta(self)
						if ajustes.aplicacionesLista[indice][0] == "adr":
							dlg = EditarAcceso(self)

						res = dlg.ShowModal()
						if res == 0:
							dlg.Destroy()
							del ajustes.aplicacionesLista[indice]
							ajustes.aplicacionesLista.insert(indice, dlg.lista)
							ajustes.guardaAplicaciones(self.dbAplicaciones)
							self.onRefrescar(None)
						else:
							dlg.Destroy()

		elif id == 11:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				if nombreItem == _("Sin acciones"):
					msg = \
_("""No tiene ninguna acción.

Agregue una antes para poder borrar.""")
					self.mensaje(msg, _("Información"), 0)
				else:
					msg = \
_("""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar la acción:

{}

¿Esta seguro que desea continuar?""").format(nombreItem)
					MsgBox = wx.MessageDialog(None, msg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
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
			if self.lstAplicaciones.GetString(self.lstAplicaciones.GetSelection()) == _("Sin acciones"):
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
						funciones.ejecutar(self, "open", ajustes.aplicacionesLista[valor][2], None, os.path.dirname(ajustes.aplicacionesLista[valor][2]), 10)
					else:
						funciones.ejecutar(self, "open", ajustes.aplicacionesLista[valor][2], ajustes.aplicacionesLista[valor][4], os.path.dirname(ajustes.aplicacionesLista[valor][2]), 10)
				else:
					if ajustes.aplicacionesLista[valor][3] == False:
						funciones.ejecutar(self, "runas", ajustes.aplicacionesLista[valor][2], None, os.path.dirname(ajustes.aplicacionesLista[valor][2]), 10)
					else:
						funciones.ejecutar(self, "runas", ajustes.aplicacionesLista[valor][2], ajustes.aplicacionesLista[valor][4], os.path.dirname(ajustes.aplicacionesLista[valor][2]), 10)
			else:
				indice = self.lstAplicaciones.GetSelection()
				msg = \
_("""La ruta a la aplicación {}, no se encontró.

¿Desea editar la entrada de la aplicación para corregir el problema?""").format(self.lstAplicaciones.GetString(self.lstAplicaciones.GetSelection()))
				dlg = wx.MessageDialog( None, msg, _("Aviso"), wx.YES_NO | wx.ICON_QUESTION )
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

		elif ajustes.aplicacionesLista[valor][0] == "cmd":
			self.onSalir(None)
			if ajustes.aplicacionesLista[valor][4] == False:
				if ajustes.aplicacionesLista[valor][3] == False:
					funciones.ejecutar(self, "open", "cmd.exe", "/c" + ajustes.aplicacionesLista[valor][2], None, 10)
				else:
					funciones.ejecutar(self, "open", "cmd.exe", "/c" + ajustes.aplicacionesLista[valor][2] + "&pause", None, 10)
			else:
				if ajustes.aplicacionesLista[valor][3] == False:
					funciones.ejecutar(self, "runas", "cmd.exe", "/c" + ajustes.aplicacionesLista[valor][2], None, 10)
				else:
					funciones.ejecutar(self, "runas", "cmd.exe", "/c" + ajustes.aplicacionesLista[valor][2] + "&pause", None, 10)

		elif ajustes.aplicacionesLista[valor][0] == "fol":
			if os.path.isdir(ajustes.aplicacionesLista[valor][2]):
				self.onSalir(None)
				funciones.ejecutar(self, "explore", ajustes.aplicacionesLista[valor][2], None, None, 10)
			else:
				indice = self.lstAplicaciones.GetSelection()
				msg = \
_("""La ruta a la carpeta no se encontró.

{}

¿Desea editar la entrada de la aplicación para corregir el problema?""").format(ajustes.aplicacionesLista[valor][2])
				dlg = wx.MessageDialog( None, msg, _("Aviso"), wx.YES_NO | wx.ICON_QUESTION )
				aceptar = dlg.ShowModal()
				dlg.Destroy()
				if wx.ID_YES == aceptar:
					dlg = EditarCarpeta(self)
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

		elif ajustes.aplicacionesLista[valor][0] == "adr":
			if os.path.isfile(ajustes.aplicacionesLista[valor][2]):
				self.onSalir(None)
				if ajustes.aplicacionesLista[valor][3] == False:
					funciones.ejecutar(self, "open", ajustes.aplicacionesLista[valor][2], None, None, 10)
				else:
					funciones.ejecutar(self, "runas", ajustes.aplicacionesLista[valor][2], None, None, 10)
			else:
				indice = self.lstAplicaciones.GetSelection()
				msg = \
_("""La ruta al acceso directo no se encontró.

{}

¿Desea editar la entrada de la aplicación para corregir el problema?""").format(ajustes.aplicacionesLista[valor][2])
				dlg = wx.MessageDialog( None, msg, _("Aviso"), wx.YES_NO | wx.ICON_QUESTION )
				aceptar = dlg.ShowModal()
				dlg.Destroy()
				if wx.ID_YES == aceptar:
					dlg = EditarAcceso(self)
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

		elif ajustes.aplicacionesLista[valor][0] == "sap":
			self.onSalir(None)
			if ajustes.aplicacionesLista[valor][3] == False:
				funciones.ejecutar(self, "open", "explorer.exe", "shell:appsfolder\{}".format(ajustes.aplicacionesLista[valor][2]), None, 10)
			else:
				funciones.ejecutar(self, "runas", "explorer.exe", "shell:appsfolder\{}".format(ajustes.aplicacionesLista[valor][2]), None, 10)

	def HacerBackup(self, event):
		wildcard = _("Archivo copia de seguridad zUtilidades (*.zut-zl)|*.zut-zl")
		dlg = wx.FileDialog(self, message=_("Guardar en..."), defaultDir=os.getcwd(), defaultFile=funciones.fecha(), wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			pathbackup = dlg.GetPath()
			fichero_final = os.path.basename(pathbackup)
			dlg.Destroy()
			dlg = BackupDialogo(_("Haciendo copia de seguridad..."), pathbackup)
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
_("""*** ADVERTENCIA ***

Esto borrara toda la base de datos del lanzador de aplicaciones

Toda la base de datos será sustituida por la copia de seguridad.

El complemento restaurara la copia de seguridad y se cerrara.

Esta acción no es reversible.

¿Desea continuar con el proceso?""")
		msg = wx.MessageDialog(None, xguiMsg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = msg.ShowModal()
		if ret == wx.ID_YES:
			msg.Destroy
			wildcard = _("Archivo copia de seguridad zUtilidades (*.zut-zl)|*.zut-zl")
			dlgF = wx.FileDialog(None, message=_("Seleccione un archivo de copia de seguridad"), defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
			if dlgF.ShowModal() == wx.ID_OK:
				pathbackup = dlgF.GetPath()
				dlgF.Destroy()
				dlg = BackupDialogo(_("Restaurando copia de seguridad..."), pathbackup, True)
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

	def borrarValores(self, event):
		xguiMsg = \
_("""*** ADVERTENCIA ***

Esto borrara toda la base de datos del lanzador de aplicaciones

El complemento borrara la base de datos y se cerrara.

Esta acción no es reversible.

¿Desea continuar con el proceso?""")
		msg = wx.MessageDialog(None, xguiMsg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = msg.ShowModal()
		if ret == wx.ID_YES:
			msg.Destroy
			rmtree(ajustes.dbDir)
			if os.path.exists(ajustes.dbDir) == False:
				try:
					os.mkdir(os.path.join(globalVars.appArgs.configPath, "zUtilidades"))
				except:
					pass
				os.mkdir(ajustes.dbDir)
			ajustes.refrescaCategoriasBackup()
			ajustes.posicion = [0, 0]
			ajustes.IS_WinON = False
			ajustes.focoActual = "lstCategorias"
			self.Destroy()
			gui.mainFrame.postPopup()
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

		super(AñadirCategoria, self).__init__(None, -1, title=_("Añadir categoría"))

		self.frame = frame
		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Introduzca el nombre de la categoría:"))
		self.texto = wx.TextCtrl(self.Panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.texto.Bind(wx.EVT_TEXT_ENTER, self.onPass)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		self.CenterOnScreen()

	def onPass(self, event):
		pass

	def onAceptar(self, event):
		if self.texto.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una categoría.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.texto.SetFocus()
		else:
			p = funciones.estaenlistado(ajustes.nombreCategoria, self.texto.GetValue())
			if p == True:
				msg = \
_("""No puede duplicar el nombre de una categoría.

Modifique el nombre para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
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

		super(EditarCategoria, self).__init__(None, -1, title=_("Editar categoría"))

		self.frame = frame
		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Introduzca el nombre de la categoría:"))
		self.texto = wx.TextCtrl(self.Panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.texto.Bind(wx.EVT_TEXT_ENTER, self.onPass)
		self.texto.SetValue(self.frame.lstCategorias.GetString(self.frame.lstCategorias.GetSelection()))

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		self.CenterOnScreen()

	def onPass(self, event):
		pass

	def onAceptar(self, event):
		if self.texto.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una categoría.""")
			self.frame.mensaje(msg, _("Información"), 0)
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
_("""No puede duplicar el nombre de una categoría.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
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

		super(AñadirAplicacion, self).__init__(None, -1, title=_("Añadir aplicación"),size=(600,300))

		self.frame = frame
		self.parametro = False
		self.administrador = False
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la aplicación:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Ruta de la aplicación:"))
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label=_("&Seleccionar archivo"))
		self.Bind(wx.EVT_BUTTON, self.archivo_pulsar, id=self.directorioBTN.GetId())

		self.chkParametro = wx.CheckBox(self.Panel, 1, _("Usar parámetros adicionales"))
		label3 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca los parámetros para la aplicación:"))
		self.textoParametro = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoParametro.Disable()

		self.chkAdministrador = wx.CheckBox(self.Panel, 2, _("Ejecutar como administrador"))
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		self.CenterOnScreen()

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
		wildcard = _("Todos los archivos ejecutables (*.exe, *.com, *.bat)|*.exe;*.com;*.bat|")
		dlg = wx.FileDialog(None, message=_("Seleccione un archivo"), defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
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
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una aplicación.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Seleccione una aplicación para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.directorioBTN.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.aplicacionesLista)):
					listaTemporal.append(ajustes.aplicacionesLista[i][1])
				p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
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

		super(EditarAplicacion, self).__init__(None, -1, title=_("Editar aplicación"), size=(600,300))

		self.frame = frame
		self.indice = self.frame.lstAplicaciones.GetSelection()
		self.parametro = ajustes.aplicacionesLista[self.indice][3]
		self.administrador = ajustes.aplicacionesLista[self.indice][5]
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la aplicación:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoNombre.SetValue(ajustes.aplicacionesLista[self.indice][1])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Ruta de la aplicación:"))
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label=_("&Seleccionar archivo"))
		self.Bind(wx.EVT_BUTTON, self.archivo_pulsar, id=self.directorioBTN.GetId())
		self.textoDirectorio.SetValue(ajustes.aplicacionesLista[self.indice][2])

		self.chkParametro = wx.CheckBox(self.Panel, 1, _("Usar parámetros adicionales"))
		self.chkParametro.SetValue(self.parametro)
		label3 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca los parámetros para la aplicación:"))
		self.textoParametro = wx.TextCtrl(self.Panel, wx.ID_ANY)
		if self.parametro == True:
			self.textoParametro.Enable()
		else:
			self.textoParametro.Disable()
		self.textoParametro.SetValue(ajustes.aplicacionesLista[self.indice][4])

		self.chkAdministrador = wx.CheckBox(self.Panel, 2, _("Ejecutar como administrador"))
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 
		self.chkAdministrador.SetValue(self.administrador)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		self.CenterOnScreen()

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
		wildcard = _("Todos los archivos ejecutables (*.exe, *.com, *.bat)|*.exe;*.com;*.bat|")
		dlg = wx.FileDialog(None, message=_("Seleccione un archivo"), defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
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
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una aplicación.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Seleccione una aplicación para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
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
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
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

class AñadirCMD(wx.Dialog):
	def __init__(self, frame):

		super(AñadirCMD, self).__init__(None, -1, title=_("Añadir CMD"),size=(600,300))

		self.frame = frame
		self.parametro = False
		self.administrador = False
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca un nombre para identificar el comando CMD:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca los comandos de CMD. Puede usar el símbolo (et = Shift+6) para usar más de una línea de comandos:"))
		self.textoParametro = wx.TextCtrl(self.Panel, wx.ID_ANY)

		self.chkParametro = wx.CheckBox(self.Panel, 1, _("Pausar la consola de CMD al finalizar el comando. Evitara que se cierre al terminar"))
		self.chkAdministrador = wx.CheckBox(self.Panel, 2, _("Ejecutar como administrador"))
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)
		sizeV.Add(label2, 0, wx.EXPAND)
		sizeV.Add(self.textoParametro, 1, wx.EXPAND)

		sizeV.Add(self.chkParametro, 0, wx.EXPAND)
		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.parametro = temp
		elif id == 2:
			temp =  chk.GetValue()
			self.administrador = temp

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo (Introduzca un nombre para identificar el comando CMD) no puede quedar en blanco.

Introduzca un nombre para poder identificar el comando.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoParametro.GetValue() == "":
				msg = \
_("""El campo (Introduzca los comandos de CMD. Puede usar el símbolo (et = Shift+6) para usar más de una línea de comandos) no puede quedar en blanco.

Escriba una línea de comandos para continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.textoParametro.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.aplicacionesLista)):
					listaTemporal.append(ajustes.aplicacionesLista[i][1])
				p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
					self.textoNombre.SetFocus()
				else:
					self.lista = ["cmd", self.textoNombre.GetValue(), self.textoParametro.GetValue(), self.parametro, self.administrador]
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

class EditarCMD(wx.Dialog):
	def __init__(self, frame):

		super(EditarCMD, self).__init__(None, -1, title=_("Editar CMD"),size=(600,300))

		self.frame = frame
		self.indice = self.frame.lstAplicaciones.GetSelection()
		self.parametro = ajustes.aplicacionesLista[self.indice][3]
		self.administrador = ajustes.aplicacionesLista[self.indice][4]
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca un nombre para identificar el comando CMD:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoNombre.SetValue(ajustes.aplicacionesLista[self.indice][1])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca los comandos de CMD. Puede usar el símbolo (et = Shift+6) para usar más de una línea de comandos:"))
		self.textoParametro = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoParametro.SetValue(ajustes.aplicacionesLista[self.indice][2])

		self.chkParametro = wx.CheckBox(self.Panel, 1, _("Pausar la consola de CMD al finalizar el comando. Evitara que se cierre al terminar"))
		self.chkParametro.SetValue(self.parametro)

		self.chkAdministrador = wx.CheckBox(self.Panel, 2, _("Ejecutar como administrador"))
		self.chkAdministrador.SetValue(self.administrador)

		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(label2, 0)
		sizeV.Add(self.textoParametro, 1, wx.EXPAND)

		sizeV.Add(self.chkParametro, 0, wx.EXPAND)
		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.parametro = temp
		elif id == 2:
			temp =  chk.GetValue()
			self.administrador = temp

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo (Introduzca un nombre para identificar el comando CMD) no puede quedar en blanco.

Introduzca un nombre para poder identificar el comando.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoParametro.GetValue() == "":
				msg = \
_("""El campo (Introduzca los comandos de CMD. Puede usar el símbolo (et = Shift+6) para usar más de una línea de comandos) no puede quedar en blanco.

Escriba una línea de comandos para continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.textoParametro.SetFocus()
			else:
				if self.textoNombre.GetValue() == ajustes.aplicacionesLista[self.indice][1]:
					self.lista = ["cmd", self.textoNombre.GetValue(), self.textoParametro.GetValue(), self.parametro, self.administrador]
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
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
						self.frame.mensaje(msg, _("Información"), 0)
						self.textoNombre.SetFocus()
					else:
						self.lista = ["cmd", self.textoNombre.GetValue(), self.textoParametro.GetValue(), self.parametro, self.administrador]
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

class AñadirCarpeta(wx.Dialog):
	def __init__(self, frame):

		super(AñadirCarpeta, self).__init__(None, -1, title=_("Añadir carpeta"),size=(600,300))

		self.frame = frame
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la carpeta:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Ruta de la carpeta:"))
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label=_("&Seleccionar carpeta"))
		self.Bind(wx.EVT_BUTTON, self.carpetaPulsar, id=self.directorioBTN.GetId())

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def carpetaPulsar(self, event):
		dlg = wx.DirDialog(self, _("Seleccione una carpeta:"),
			style=wx.DD_DEFAULT_STYLE
#			| wx.DD_DIR_MUST_EXIST
#			| wx.DD_CHANGE_DIR
			)
		if dlg.ShowModal() == wx.ID_OK:
			self.textoDirectorio.SetValue(dlg.GetPath())
			self.textoDirectorio.SetFocus()
		dlg.Destroy()

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para identificar una carpeta.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Seleccione una carpeta para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.directorioBTN.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.aplicacionesLista)):
					listaTemporal.append(ajustes.aplicacionesLista[i][1])
				p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
					self.textoNombre.SetFocus()
				else:
					self.lista = ["fol", self.textoNombre.GetValue(), self.textoDirectorio.GetValue()]
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

class EditarCarpeta(wx.Dialog):
	def __init__(self, frame):

		super(EditarCarpeta, self).__init__(None, -1, title=_("Editar carpeta"), size=(600,300))

		self.frame = frame
		self.indice = self.frame.lstAplicaciones.GetSelection()
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la carpeta:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoNombre.SetValue(ajustes.aplicacionesLista[self.indice][1])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Ruta de la carpeta:"))
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label=_("&Seleccionar carpeta"))
		self.Bind(wx.EVT_BUTTON, self.carpetaPulsar, id=self.directorioBTN.GetId())
		if os.path.isdir(ajustes.aplicacionesLista[self.indice][2]):
			self.textoDirectorio.SetValue(ajustes.aplicacionesLista[self.indice][2])
		else:
			self.textoDirectorio.Clear()

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def carpetaPulsar(self, event):
		dlg = wx.DirDialog(self, _("Seleccione una carpeta:"),
			style=wx.DD_DEFAULT_STYLE
#			| wx.DD_DIR_MUST_EXIST
#			| wx.DD_CHANGE_DIR
			)
		if dlg.ShowModal() == wx.ID_OK:
			self.textoDirectorio.SetValue(dlg.GetPath())
			self.textoDirectorio.SetFocus()
		dlg.Destroy()

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para identificar una carpeta.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Seleccione una carpeta para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.directorioBTN.SetFocus()
			else:
				if self.textoNombre.GetValue() == ajustes.aplicacionesLista[self.indice][1]:
					self.lista = ["fol", self.textoNombre.GetValue(), self.textoDirectorio.GetValue()]
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
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
						self.frame.mensaje(msg, "Información", 0)
						self.textoNombre.SetFocus()
					else:
						self.lista = ["fol", self.textoNombre.GetValue(), self.textoDirectorio.GetValue()]
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

class AñadirAcceso(wx.Dialog):
	def __init__(self, frame):

		super(AñadirAcceso, self).__init__(None, -1, title=_("Añadir acceso directo"),size=(600,300))

		self.frame = frame
		self.lista = []
		self.administrador = False

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre del acceso directo:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Ruta del acceso directo:"))
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label=_("&Seleccionar acceso directo"))
		self.Bind(wx.EVT_BUTTON, self.accesoPulsar, id=self.directorioBTN.GetId())

		self.chkAdministrador = wx.CheckBox(self.Panel, 1, _("Ejecutar como administrador"))
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.administrador = temp

	def accesoPulsar(self, event):
		wildcard = _("Accesos directos (*.lnk)|*.lnk|")
		dlg = wx.FileDialog(None, message=_("Seleccione un acceso directo"), defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
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
_("""El campo no puede quedar en blanco.

Introduzca un nombre para identificar un acceso directo.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Seleccione un acceso directo para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.directorioBTN.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.aplicacionesLista)):
					listaTemporal.append(ajustes.aplicacionesLista[i][1])
				p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
					self.textoNombre.SetFocus()
				else:
					self.lista = ["adr", self.textoNombre.GetValue(), self.textoDirectorio.GetValue(), self.administrador]
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

class EditarAcceso(wx.Dialog):
	def __init__(self, frame):

		super(EditarAcceso, self).__init__(None, -1, title=_("Editar acceso directo"), size=(600,300))

		self.frame = frame
		self.indice = self.frame.lstAplicaciones.GetSelection()
		self.lista = []
		self.administrador = ajustes.aplicacionesLista[self.indice][3]

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre del acceso directo:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoNombre.SetValue(ajustes.aplicacionesLista[self.indice][1])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Ruta del acceso directo:"))
		self.textoDirectorio = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.directorioBTN = wx.Button(self.Panel, wx.ID_ANY, label=_("&Seleccionar acceso directo"))
		self.Bind(wx.EVT_BUTTON, self.accesoPulsar, id=self.directorioBTN.GetId())
		if os.path.isfile(ajustes.aplicacionesLista[self.indice][2]):
			self.textoDirectorio.SetValue(ajustes.aplicacionesLista[self.indice][2])
		else:
			self.textoDirectorio.Clear()

		self.chkAdministrador = wx.CheckBox(self.Panel, 1, _("Ejecutar como administrador"))
		self.chkAdministrador.SetValue(self.administrador)

		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
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

		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.administrador = temp

	def accesoPulsar(self, event):
		wildcard = _("Accesos directos (*.lnk)|*.lnk|")
		dlg = wx.FileDialog(None, message=_("Seleccione un acceso directo"), defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
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
_("""El campo no puede quedar en blanco.

Introduzca un nombre para identificar un acceso directo.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoDirectorio.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Seleccione un acceso directo para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.directorioBTN.SetFocus()
			else:
				if self.textoNombre.GetValue() == ajustes.aplicacionesLista[self.indice][1]:
					self.lista = ["adr", self.textoNombre.GetValue(), self.textoDirectorio.GetValue(), self.administrador]
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
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
						self.frame.mensaje(msg, "Información", 0)
						self.textoNombre.SetFocus()
					else:
						self.lista = ["adr", self.textoNombre.GetValue(), self.textoDirectorio.GetValue(), self.administrador]
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

class AñadirInstalada(wx.Dialog):
	def __init__(self, frame):

		super(AñadirInstalada, self).__init__(None, -1, title=_("Añadir aplicación instalada"),size=(600,300))

		self.frame = frame
		self.lista = []
		self.administrador = False
		self.lista_Apps = funciones.obtenApps()
		self.choiceSelection = 0

		self.Panel = wx.Panel(self)

		msg = \
_("""En el siguiente campo combinado tendrá todas las aplicaciones instaladas.

Esto incluye las aplicaciones instaladas desde la tienda, por el usuario y aquellos accesos que las aplicaciones instalan junto a la aplicación en sí.

También tiene aplicaciones del sistema las cuales también se pueden añadir.

Advertencia:

Las aplicaciones añadidas desde este apartado no pueden ser editadas en el lanzador, por lo que si sufren cambios tendrá que eliminar la entrada en el lanzador y volver a elegir de nuevo la aplicación y añadirla.

Igualmente si la aplicación ha sido desinstalada tendrá que borrar el acceso en el lanzador.""")
		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Información importante:"))
		self.textoinfo = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.textoinfo.SetValue(msg)
		self.textoinfo.SetInsertionPoint(0)
		self.textoinfo.SetFocus()

		self.temp = []
		for x in self.lista_Apps:
			self.temp.append(x[0])
		self.choiceApps = wx.Choice(self.Panel, wx.ID_ANY, choices = [_("Seleccione algo para añadir al lanzador.")] + self.temp)
		self.choiceApps.SetSelection(self.choiceSelection)
		self.choiceApps.Bind(wx.EVT_CHOICE, self.onChoiceApp)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la aplicación:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)


		self.chkAdministrador = wx.CheckBox(self.Panel, 1, _("Ejecutar como administrador"))
		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoinfo, 1, wx.EXPAND)

		sizeV.Add(self.choiceApps, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(self.chkAdministrador, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onChoiceApp(self, event):
		if self.choiceApps.GetString(self.choiceApps.GetSelection()) == _("Seleccione algo para añadir al lanzador."):
			self.choiceSelection = 0
			self.textoNombre.Clear()
		else:
			self.choiceSelection = event.GetSelection()
			self.textoNombre.SetValue(self.choiceApps.GetString(self.choiceApps.GetSelection()))

	def onChecked(self, event):
		# Con la siguiente linea lo que hacemos es capturar toda la información del evento chk para actualizar luego las variables.
		chk = event.GetEventObject()
		id = chk.GetId()
		if id == 1:
			temp =  chk.GetValue()
			self.administrador = temp

	def onAceptar(self, event):
		id = self.lista_Apps[self.choiceSelection - 1][1]
		if self.choiceSelection == 0:
			msg = \
_("""Tiene que elegir una aplicación del cuadro combinado para poder añadirla.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.choiceApps.SetFocus()
		else:
			if self.textoNombre.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para identificar un acceso.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.textoNombre.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.aplicacionesLista)):
					listaTemporal.append(ajustes.aplicacionesLista[i][1])
				p = funciones.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una acción.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
					self.textoNombre.SetFocus()
				else:
					self.lista = ["sap", self.textoNombre.GetValue(), id, self.administrador]
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
				wx.CallAfter(self.frame.TextoRefresco, _("Comprimiendo el archivo: %s") % filename)
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
			wx.CallAfter(self.frame.TextoRefresco, _("Descomprimiendo el archivo: %s") % filename)
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
					wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))
				else:
					wx.CallAfter(self.frame.next, 100)
					wx.CallAfter(self.frame.done, _("La copia de seguridad fue un éxito.\n") + _("Ya puede cerrar esta ventana."))
			except:
				try:
					os.remove(self.nombreFichero)
				except:
					pass
				wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))
		elif self.restore == True:
			try:
				t = self.chk_validez(self.nombreFichero)
				if t == False:
					wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))
				else:
					rmtree(ajustes.dbDir)
					self.descomprimir_zip(self.nombreFichero, ajustes.dirRestaura)
				wx.CallAfter(self.frame.next, 100)
				wx.CallAfter(self.frame.done, _("Se completo la restauración correctamente.\n") + _("Ya puede cerrar esta ventana."))
			except:
				wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))

class BackupDialogo(wx.Dialog):
	def __init__(self, titulo, nombreFichero, restore=False):

		super(BackupDialogo, self).__init__(None, -1, title=titulo)

		self.CenterOnScreen()

		self.nombreFichero = nombreFichero
		self.restore = restore

		self.Panel = wx.Panel(self)

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.AceptarTRUE = wx.Button(self.Panel, 0, _("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, 1, _("&Cerrar"))
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
