# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import os, sys
import ctypes
import string
import random
import wx
from datetime import datetime
import subprocess

# For translation
addonHandler.initTranslation()

class disable_file_system_redirection:

	_disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
	_revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

	def __enter__(self):
		self.old_value = ctypes.c_long()
		self.success = self._disable(ctypes.byref(self.old_value))

	def __exit__(self, type, value, traceback):
		if self.success:
			self._revert(self.old_value)

class chk32(object):
	def __init__(self, func):

		self.func = func

	def __call__(self, *args, **kwargs):
		try:
			os.environ['PROGRAMFILES(X86)']
			with disable_file_system_redirection():
				self.func(*args)
		except:
			self.func(*args)

@chk32
def ejecutar(objeto, modo, aplicacion, parametros, directorio, ventana):
# Explicación de los parámetros de esta función:
#
# modo: Este parámetro admite "edit" que sirve para editar un documento, "explore" que sirve para explorar una carpeta, "find" que sirve para buscar en una carpeta, "open" sirve para abrir archivos o carpetas también, "print" para imprimir un documento, "runas" para elevar a modo administrador.
#
# aplicacion: este parámetro es el que tenemos que pasar con la aplicación que queremos abrir o en el caso que el modo sea para carpeta la carpeta u objeto correspondientes si fuese imprimir o editar el archivo a editar.
#
# parametro: Si la aplicación o acción tiene parámetros podemos ponerlo aquí. Bien si no necesita tendremos que poner None.
#
# directorio: bien si queremos que una aplicación se ejecute su acción en un directorio especifico podemos pasarlo aquí o None si no queremos usar este parámetro.
#
# ventana: como queremos que se ejecute la ventana, lo normal es pasarle 10 pero dejo la lista:
#    HIDE = 0
#    MAXIMIZE = 3
#    MINIMIZE = 6
#    RESTORE = 9
#    SHOW = 5
#    SHOWDEFAULT = 10
#    SHOWMAXIMIZED = 3
#    SHOWMINIMIZED = 2
#    SHOWMINNOACTIVE = 7
#    SHOWNA = 8
#    SHOWNOACTIVATE = 4
#    SHOWNORMAL = 1
#
# Bien esta función devolvera un número que puede comprender entre 0 y vete tu a saber. Pero lo importante es que tenemos que saber que si devuelve un valor menor de 32 es que algo salió mal y la acción dio error, si es mayor de 32 la acción se ejecutó correctamente y nos puede devolver cualquier número mayor de 32 dependiendo de que ejecutemos.
#
# Principales errores:
#
#    ZERO = 0
#    FILE_NOT_FOUND = 2
#    PATH_NOT_FOUND = 3
#    BAD_FORMAT = 11
#    ACCESS_DENIED = 5
#    ASSOC_INCOMPLETE = 27
#    DDE_BUSY = 30
#    DDE_FAIL = 29
#    DDE_TIMEOUT = 28
#    DLL_NOT_FOUND = 32
#    NO_ASSOC = 31
#    OOM = 8
#    SHARE = 26
	p = ctypes.windll.shell32.ShellExecuteW(
		None,
		modo,
		aplicacion,
		parametros,
		directorio,
		ventana)
	if p <= 32:
		if p == 5:
			pass
		else:
			if objeto == None:
				pass
			else:
				msg = \
_("""Compruebe que los datos introducidos son correctos.

Se produjo el error: {}

Puede buscar información del error en:

https://tinyurl.com/yhel7t8c""").format(p)
				objeto.mensaje(msg, _("Error"), 1)

def obtenApps():
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	try:
		os.environ['PROGRAMFILES(X86)']
		with disable_file_system_redirection():
			p = subprocess.Popen('PowerShell get-StartApps'.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='CP437', startupinfo=si, creationflags = 0x08000000, universal_newlines=True)
	except:
		p = subprocess.Popen('PowerShell get-StartApps'.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='CP437', startupinfo=si, creationflags = 0x08000000, universal_newlines=True)
	result_string = str(p.communicate()[0])
	lines = [s.strip() for s in result_string.split('\n') if s]
	nuevo = lines[2:]
	lista_final = []
	for x in nuevo:
		y = ' '.join(x.split())
		z = y.rsplit(' ', 1)
		lista_final.append(z)
	return lista_final

def fecha():
	fecha_hora = datetime.now()  # Obtiene fecha y hora actual
	formato1 = "%d%m%Y%H%M%S"
	cadena1 = fecha_hora.strftime(formato1)
	return "Backup-{0}".format(cadena1)

def _calculatePosition(width, height):
	w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
	h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
	# Centre of the screen
	x = w / 2
	y = h / 2
	# Minus application offset
	x -= (width / 2)
	y -= (height / 2)
	return (x, y)

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def estaenlistado(listado, buscar):
	if not buscar in listado:
		return False
	return True

def comprobar_archivo_db(n, lista):
	aleatorios=id_generator(n) + ".dat"
	p = estaenlistado(lista, aleatorios)
	if p == False:
		return aleatorios
	else:
		return False

# variables Globales
IS_WinON = False # Bandera para saber si esta abierta una ventana del complemento
