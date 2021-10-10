# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import braille
import config
import ui
import os, sys
import ctypes
import string
import random
import wx
from datetime import datetime
import subprocess
import pickle

# For translation
addonHandler.initTranslation()

class dbDatos():
	def __init__(self, baseDir):

		self.archivoIndex = baseDir

	def CargaDatosIndex(self):
		if os.path.isfile(self.archivoIndex):
			p = open(self.archivoIndex, 'rb')
			self.versionTemp = pickle.load(p)
			if self.versionTemp == 1.0:
				self.nombreCategoria = pickle.load(p)
				self.archivoCategoria = pickle.load(p)
			p.close()
			return list(zip(self.nombreCategoria, self.archivoCategoria))
		else:
			return False

	def CargaDatosDB(self):
		if os.path.isfile(self.archivoIndex):
			p = open(	self.archivoIndex, 'rb')
			self.versionTemp = pickle.load(p)
			if self.versionTemp == 1.0:
				self.aplicacion = pickle.load(p)
			p.close()
			return self.aplicacion
		else:
			return False

class AnalizaDatos():
	def __init__(self, datos):

		self.datos = datos

	def GetCategoria(self):
			return self.datos if self.datos == False else [x[0] for x in self.datos]

	def GetArchivosCat(self):
		return self.datos if self.datos == False else [x[1] for x in self.datos]

	def GetNombreDB(self):
		return self.datos if self.datos == False else [x[1] for x in self.datos]

	def chkDatos(self, lista):
		compare = lambda a,b: len(a)==len(b) and len(a)==sum([1 for i,j in zip(a,b) if i==j])
		return compare(self.datos, lista)

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

def returnDict(a, b):
	return dict(zip(a, b))

def returnValue(diccionario, valor):
	return diccionario.get(valor)

def returnKeys(diccionario):
	return list(diccionario.keys())

def mensaje(msg): 
	# Esto solo funciona si está el seguimiento de braille a la revisión, así que primero guardamos el ajuste original y luego lo cambiamos a revisión 
	tether = braille.handler.TETHER_AUTO if config.conf["braille"]["autoTether"] else config.conf["braille"]["tetherTo"] 
	braille.handler.setTether("review") 
	# Ahora lanzamos el mensaje 
	ui.message(msg) 
	# ui.message llama internamente a braille.handler.message 
	if braille.handler._messageCallLater : 
		braille.handler._messageCallLater .Stop() 
	# Con esto el mensaje quedaría estático en la línea hasta que se envíe otro mensaje o algún otroproceso quiera escribir en ella. 
	# Devolvemos el ajuste original 
	braille.handler.setTether(tether) 

def initConfiguration():
	confspec = {
		"tituloCaptura": "boolean(default=False)",
	}
	config.conf.spec['zUtilidades'] = confspec

def getConfig(key):
	value = config.conf["zUtilidades"][key]
	return value

def setConfig(key, value):
	try:
		config.conf.profiles[0]["zUtilidades"][key] = value
	except:
		config.conf["zUtilidades"][key] = value

initConfiguration()
# variables Globales
IS_WinON = False # Bandera para saber si esta abierta una ventana del complemento
ID_TRUE = wx.NewIdRef() # para botón aceptar
ID_FALSE = wx.NewIdRef() # para botón cancelar
try:
	tituloCaptura = getConfig("tituloCaptura")
except:
	tituloCaptura = False
