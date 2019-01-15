# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Nommage_AI
								 A QGIS plugin
 Nommage_AI
							  -------------------
		begin				: 2018-07-26
		git sha			  : $Format:%H$
		copyright			: (C) 2018 by Circet
		email				: labhalmehdi@gmail.com
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""
import processing, re,itertools,sys,qgis
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.utils import *
from qgis.PyQt.QtWidgets import *
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the scripts
from .Nommage_PT_Boite_Cables_Support import Nommage_PT_Boite_Cables_function
from .Nommage_PT_Boite_Cables_Support import Nommage_Supports_function
# Import the code for the dialog
from .Nommage_Support_AI_dialog import Nommage_Support_AIDialog
from .Nommage_PT_Boite_Cables_dialog import Nommage_PT_Boite_CablesDialog

import os.path


class Nommage_AI:
	"""QGIS Plugin Implementation."""

	def __init__(self, iface):
		"""Constructor.

		:param iface: An interface instance that will be passed to this class
			which provides the hook by which you can manipulate the QGIS
			application at run time.
		:type iface: QgisInterface
		"""
		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value('locale/userLocale')[0:2]
		locale_path = os.path.join(
			self.plugin_dir,
			'i18n',
			'Nommage_AI_{}.qm'.format(locale))

		if os.path.exists(locale_path):
			self.translator = QTranslator()
			self.translator.load(locale_path)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)
		self.actions=[]

		# Declare instance attributes

	# noinspection PyMethodMayBeStatic
	def tr(self, message):
		# noinspection PyTypeChecker,PyArgumentList,PyCallByClass
		return message
	
	#Declaration des actions pour regrouper des plugins
	def initGui(self):
		self.menu = "&[Circet] B. Nommage Altitude Infrastructure"
		self.action = QAction(
			QIcon(':/plugins/Nommage_Support_AI/icon.png'),
			u"Nommage_AI", self.iface.mainWindow())
		self.action0 = QAction( QCoreApplication.translate("Nommage_AI", "B.1. Nommage des points techniques/boites/cables" ), self.iface.mainWindow() )
		self.action1 = QAction( QCoreApplication.translate("Nommage_AI", "B.2.Nommage des supports" ), self.iface.mainWindow() )
	
		# connect the action to the run method
		self.action.triggered.connect(self.runNommageReste)
		self.action0.triggered.connect(self.runNommageReste)
		self.action1.triggered.connect(self.runNommageSupports)
	 
		self.iface.addPluginToMenu(self.menu, self.action0)
		self.iface.addPluginToMenu(self.menu, self.action1)

		self.actions.append(self.action0)
		self.actions.append(self.action1)
	
	#Suppression des menus ajoutes dans le toolbar
	def unload(self):
		"""Removes the plugin menu item and icon from QGIS GUI."""
		for action in self.actions:
			self.iface.removePluginMenu(self.menu,action)

	#Creation des fonction pour chaque execution
	def runNommageReste(self):
		"""Run method that performs all the real work"""
		#Declaration de la boite de dialogue
		self.dlgreste = Nommage_PT_Boite_CablesDialog()
		#Vider des comboxes existants
		self.dlgreste.comboPBO.clear()
		self.dlgreste.comboCABLES.clear()
		self.dlgreste.comboPT.clear()
		#recuperation des tous les shapes charger dans Qgis et ajout dans les comboxes
		layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
		#self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())
		self.dlgreste.comboPBO.addItems(layer_list)
		self.dlgreste.comboCABLES.addItems(layer_list)
		self.dlgreste.comboPT.addItems(layer_list)
		self.dlgreste.show()
		# Run the dialog event loop
		result = self.dlgreste.exec_()
		# See if OK was pressed
		if result:
			PBOLayerIndex = self.dlgreste.comboPBO.currentIndex()
			PBOLayer = layers[PBOLayerIndex]
			shape_pbo= PBOLayer

			CABLESLayerIndex = self.dlgreste.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			PTLayerIndex = self.dlgreste.comboPT.currentIndex()
			PTLayer = layers[PTLayerIndex]
			shape_pt= PTLayer

			Nommage_PT_Boite_Cables_function(shape_pbo, shape_cables,shape_pt)
		
	def runNommageSupports(self):
		"""Run method that performs all the real work"""
		self.dlg = Nommage_Support_AIDialog()
		self.dlg.comboPT.clear()
		self.dlg.comboSRO.clear()
		self.dlg.comboSupport.clear()
		self.dlg.windowTitle = "testesrser"
		layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
		#self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())
		self.dlg.comboPT.addItems(layer_list)
		self.dlg.comboSRO.addItems(layer_list)
		self.dlg.comboSupport.addItems(layer_list)
		# show the dialog
		self.dlg.show()
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result:
			PTLayerIndex = self.dlg.comboPT.currentIndex()
			PTLayer = layers[PTLayerIndex]
			shape_pt= PTLayer

			SROLayerIndex = self.dlg.comboSRO.currentIndex()
			SROLayer = layers[SROLayerIndex]
			shape_sro= SROLayer

			SupportLayerIndex = self.dlg.comboSupport.currentIndex()
			SupportLayer = layers[SupportLayerIndex]
			shape_support= SupportLayer
			
			#Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON_NOMMAGE_AI", "", "xlsx files (*.xlsx)")

			Nommage_Supports_function(shape_pt, shape_sro,shape_support)