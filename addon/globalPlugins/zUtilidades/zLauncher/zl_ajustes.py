# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import os
import sys
import pickle
import globalVars
import addonHandler

# For translation
addonHandler.initTranslation()

# Directorios
dbDir =os.path.join(globalVars.appArgs.configPath, "zUtilidades", "zLauncher")
dirRestaura = os.path.join(globalVars.appArgs.configPath, "zUtilidades")
if os.path.exists(dbDir) == False:
	try:
		os.mkdir(os.path.join(globalVars.appArgs.configPath, "zUtilidades"))
	except:
		pass
	os.mkdir(dbDir)


class dbCategorias():
	def __init__(self):

		self.archivoIndex = os.path.join(dbDir, "index.dat")
		self.version = 1.0
		self.versionTemp = None
		self.nombreCategoria = []
		self.archivoCategoria = []

	def GuardaDatos(self):
		p = open(self.archivoIndex, "wb")
		pickle.dump(self.version, p)
		pickle.dump(self.nombreCategoria, p)
		pickle.dump(self.archivoCategoria, p)
		p.close()

	def CargaDatos(self):
		if os.path.isfile(self.archivoIndex):
			p = open(self.archivoIndex, 'rb')
			self.versionTemp = pickle.load(p)
			if self.versionTemp == 1.0:
				self.nombreCategoria = pickle.load(p)
				self.archivoCategoria = pickle.load(p)
			p.close()
		else:
			dbCategorias.GuardaDatos(self)
			dbCategorias.CargaDatos(self)

class dbAplicaciones():
	def __init__(self, archivo):
		self.archivoAplicacion = os.path.join(dbDir, archivo)
		self.version = 1.0
		self.versionTemp = None
		self.aplicacion = []

	def GuardaDatos(self):
		p = open(	self.archivoAplicacion, "wb")
		pickle.dump(self.version, p)
		pickle.dump(self.aplicacion, p)
		p.close()

	def CargaDatos(self):
		if os.path.isfile(self.archivoAplicacion):
			p = open(	self.archivoAplicacion, 'rb')
			self.versionTemp = pickle.load(p)
			if self.versionTemp == 1.0:
				self.aplicacion = pickle.load(p)
			p.close()
		else:
			dbAplicaciones.GuardaDatos(self)
			dbAplicaciones.CargaDatos(self)


# Cargamos Categorías
dbOBJ = dbCategorias()
dbOBJ.CargaDatos()
# Variables Categorías
nombreCategoria = dbOBJ.nombreCategoria
archivoCategoria = dbOBJ.archivoCategoria
# Variables Aplicaciones
aplicacionesLista = []
# Variables Generales
IS_WinON = False # Bandera para saber si esta abierta una ventana del complemento
focoActual = "lstCategorias"
posicion = [0, 0]

def guardaCategorias():
	dbOBJ.nombreCategoria = nombreCategoria
	dbOBJ.archivoCategoria = archivoCategoria
	dbOBJ.GuardaDatos()

def refrescaCategorias():
	global nombreCategoria, archivoCategoria
	dbOBJ.CargaDatos()
	nombreCategoria = dbOBJ.nombreCategoria
	archivoCategoria = dbOBJ.archivoCategoria

def refrescaCategoriasBackup():
	global nombreCategoria, archivoCategoria
	dbOBJ.CargaDatos()
	nombreCategoria = dbOBJ.nombreCategoria
	archivoCategoria = dbOBJ.archivoCategoria
	dbOBJ.GuardaDatos()


def guardaAplicaciones(frame):
	frame.aplicacion = aplicacionesLista
	frame.GuardaDatos()

