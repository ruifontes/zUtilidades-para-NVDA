# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import os, sys
import ctypes
import string
import random
import wx
from datetime import datetime

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

def ejecutaAdmin(objeto, aplicacion, parametros=False):
	if parametros == False:
		p = ctypes.windll.shell32.ShellExecuteW(None, 'runas', os.path.basename(aplicacion), None, os.path.dirname(aplicacion), 10)
	else:
		p = ctypes.windll.shell32.ShellExecuteW(None, 'runas', os.path.basename(aplicacion), parametros, os.path.dirname(aplicacion), 10)
	if p <= 32:
		if p == 5:
			pass
		else:
			msg = \
"""Compruebe que los datos introducidos son correctos.

Se produjo el error: {}

Puede buscar información del error en:

https://tinyurl.com/yhel7t8c""".format(p)
			objeto.mensaje(msg, "Error", 1)

def ejecutaNormal(objeto, aplicacion, parametros=False):
	if parametros == False:
		p = ctypes.windll.shell32.ShellExecuteW(None, 'open', os.path.basename(aplicacion), None, os.path.dirname(aplicacion), 10)
	else:
		p = ctypes.windll.shell32.ShellExecuteW(None, 'open', os.path.basename(aplicacion), parametros, os.path.dirname(aplicacion), 10)
	if p <= 32:
		msg = \
"""Compruebe que los datos introducidos son correctos.

Se produjo el error: {}

Puede buscar información del error en:

https://tinyurl.com/yhel7t8c""".format(p)
		objeto.mensaje(msg, "Error", 1)
