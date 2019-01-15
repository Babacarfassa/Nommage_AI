# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Nommage_Supports_function
                                 A QGIS plugin
 Nommage_Supports_function
                              -------------------
        begin                : 2018-07-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Circet
        email                : labhalmehdi@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import processing, re,itertools,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
'my test modify GIT'
def  Nommage_Supports_function(shape_pt, shape_sro,shape_support, Fichier_CONF_PYTHON):
	"""Run method that performs all the real work"""
			
	
	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_CB_name_CB_NOM='CB_NOM'
	distance_buffer_tampon='GLOB_DIST_TAMPON'
	#Function pour la recuperation de mon code_parametre en fonction de mon fichier de parametrage
	def get_field_name(name_attribut,shape_name):
		field_name=''
		#prov = processing.getObject(shape_name).dataProvider()
		field_names_shape = [field.name() for field in shape_name.pendingFields()]
		for field_ref in list_file_con:
			for field_shape in field_names_shape:
				#if field_shape == field_ref[2]: #feat[1] == nom dattribut du shape dans le fichier de conf
				if field_ref[1] == name_attribut: #feat[4] == code du nom dattribut du shape dans le fichier de conf
						field_name=field_ref[2]
		return field_name


	#Declaration des noms des colonnes
	shape_CM_name_CM_NOM='CM_NOM'
	shape_CM_STRUCTURE_TRI='CM_STRUCTURE_TRI'
	shape_PT_name_PT_NOM='PT_NOM'
	shape_PT_name_PT_TYPE='PT_TYPE'

	#Declaration des noms des entites
	shape_PT_name_PT_TYPE_CHAMBRE='PT_TYPE_CHAMBRE'
	shape_PT_name_PT_TYPE_POTEAU='PT_TYPE_POTEAU'


	shape_pt_Nom_Colonne_Nom=get_field_name(shape_PT_name_PT_NOM,shape_pt)#CODE_PTECH
	shape_pt_Nom_Colonne_TYPE_STRUC=get_field_name(shape_PT_name_PT_TYPE,shape_pt)#TYPE_STRUC
	shape_pt_TYPE_STRUC_CHAMBRE=get_field_name(shape_PT_name_PT_TYPE_CHAMBRE,shape_pt)#CHAMBRE
	shape_pt_TYPE_STRUC_POTEAU=get_field_name(shape_PT_name_PT_TYPE_POTEAU,shape_pt)#POTEAU
	shape_support_Nom_Colonne_Nom=get_field_name(shape_CM_name_CM_NOM,shape_support)#CODE_INF
	shape_support_Nom_Colonne_CM_STRUCTURE_TRI=get_field_name(shape_CM_STRUCTURE_TRI,shape_support)#CODE_INF



	Id_NRO='code_nro'
	Id_SRO='code_sro'
	Id_POCHE='poche'
	Id_INCR='incr'
	Id_NOMPT='nompt'
	CODE_PT='CODE_PT_AI'
	CODE_BP='CODE_BP_AI'
	CODE_CB='CODE_CB_AI'
	CODE_SUPPORT='CODE_CH_AI'
	Nom_PT_CHAMBRE='CHA'
	Nom_PT_POTEAU='POT'
	Increment_nro='1'
	Increment_sro='2'
	Nom_Cable_DISTRI='CDI'
	CODE_PT_origine='PT_AMONT'
	CODE_PT_extremite='PT_AVAL'


	layershape_pt = shape_pt
	layershape_sro = shape_sro
	layershape_support = shape_support

	#Parti dajout des champs dans les shapes pour des utilisations ulterieur
	def ajout_champs():
		
		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_shape_support=[]
		for k in layershape_support.dataProvider().fields():
			nom_champs_shape_support.append(k.name()) 
		if  (CODE_PT_origine not in nom_champs_shape_support) :
			layershape_support.dataProvider().addAttributes([QgsField(CODE_PT_origine,QVariant.String)])
		if  (CODE_PT_extremite not in nom_champs_shape_support) :
			layershape_support.dataProvider().addAttributes([QgsField(CODE_PT_extremite,QVariant.String)])
		if  (CODE_SUPPORT not in nom_champs_shape_support) :
			layershape_support.dataProvider().addAttributes([QgsField(CODE_SUPPORT,QVariant.String)])

		layershape_support.updateFields()
		layershape_support.commitChanges()

	#Execution de la fonction ajout des champs
	ajout_champs()


	listshape_pt = []
	for shape_pts in layershape_pt.getFeatures():
		shape_pt = [shape_pts[CODE_PT],shape_pts.geometry().exportToWkt(),-1,-1,-1,-1]
		listshape_pt.append(shape_pt)


	listshape_sro = []
	for shape_sro  in layershape_sro.getFeatures():
		shape_sros = [shape_sro.geometry().exportToWkt()]
		#print shape_sro.geometry().exportToWkt()
		listshape_sro.append(shape_sros)
		
	point_depart_sro=str(min(listshape_sro)).replace('[','').replace(']','').replace('u','').replace("'",'')
	#print point_depart_sro

	list_shape_support=[]
	for shape_support in layershape_support.getFeatures():
		
		res_origine='KO'
		res_extremite='KO'
		

		geom_support=shape_support.geometry()
		if geom_support != NULL:
		
			bboxinfra = geom_support.buffer(5, 5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxinfra)
			
			if geom_support.wkbType()==QGis.WKBMultiLineString:
				geom_support_type=geom_support.asMultiPolyline()
				support_origine=geom_support_type[0][0]
				support_extremite=geom_support_type[-1][-1]
				
			if geom_support.wkbType()==QGis.WKBLineString:
				geom_support_type=geom_support.asPolyline()
				support_origine=geom_support_type[0]
				support_extremite=geom_support_type[-1]
			
			shape_supports_origine=(QgsGeometry.fromPoint(QgsPoint(support_origine))).exportToWkt()
			shape_supports_extremite=(QgsGeometry.fromPoint(QgsPoint(support_extremite))).exportToWkt()
			
			geom_support_lines=geom_support.exportToWkt()
			
			list_shape_support.append([shape_support[shape_support_Nom_Colonne_Nom],shape_supports_origine,shape_supports_extremite,0,-1,-1,geom_support_lines,shape_support[shape_support_Nom_Colonne_CM_STRUCTURE_TRI]])


	#Fonction nommage_support_parcours
	#depart_origine_support : point de depart courant de la recursion
	#pt_amont :  nom du dernier point technique rencontredans la reursion
	#ordre : ordre du support depuis le dernier point technique rencontre
	def nommage_support_parcours(depart_origine_support,pt_amont,ordre,niveau):
		
		pt_aval = ""

		if niveau < 100000:
			for shape_support in list_shape_support:		 
				# On ne prend que les supports non parcourus dont lorigine est le point dorigine est depart_origine_support
				if (shape_support[1]==depart_origine_support) and (shape_support[3]==0):
					#print shape_support[0],';',depart_origine_support,';',shape_support[1]
					#le support est dans le bon sens
					shape_support[3] = 1
					#print 'depart',';',shape_support[1],';',shape_support[0]
					# on verifie si il y a un point technique en extremite de ce support
					ptextremite_good_sens = 0
					for shape_pt in listshape_pt:
						if shape_support[2] == shape_pt[1]:
							# si il y a un point technique en extremite, on recommence la reursion a partir de ce point
							ptextremite_good_sens = 1
							nommage_support_parcours(shape_support[2],shape_pt[0],ordre,niveau+1)
							if shape_pt[0] != NULL:
								pt_aval = shape_pt[0]
							elif shape_pt[0] == NULL:
								pt_aval = 'pas de cable dans cette zone lors du nommage des POINTS TECHNIQUES'
							#print 'extremite=pt_good_sens',';',shape_support[0],';',shape_pt[0],';',1,';',niveau+1,';',pt_aval,';','sens:',shape_support[3]
					if ptextremite_good_sens == 0:
						# si il ny a pas de point technique en extremite, on recommence la recursion apartir de lextremiteen se souvenant du dernier point technique rencontre
						pt_aval =nommage_support_parcours(shape_support[2],pt_amont,ordre+1,niveau+1)
						#print 'sans_extremite=pt_good_sens',';',shape_support[0],';',pt_amont,';',ordre+1,';',niveau+1,';',pt_aval
					#print shape_support[0],';',pt_amont,';',ordre+1,';',niveau+1,';',pt_aval
					#print shape_support[0],';',pt_amont,';',pt_aval
					if pt_amont != NULL:
						shape_support[4]=pt_amont
					elif pt_amont == NULL:
						shape_support[4] = 'pas de cable dans cette zone lors du nommage des POINTS TECHNIQUES'
					shape_support[5]=pt_aval
					
				# On ne prend que les supports non parcourus dont l'extremite est le point dorigine est depart_origine_support
				elif (shape_support[2]==depart_origine_support) and (shape_support[3]==0):
					#le support nest pas dans le bon sens
					shape_support[3] = -1
					#print 'depart',';',shape_support[2],';',shape_support[0]
					# on verifie si il y a un point technique en extremite en fait origine) de ce support
					ptextremite_bad_sens = 0
					for shape_pt in listshape_pt:
						if shape_support[1] == shape_pt[1]:
							ptextremite_bad_sens = 1
							# si il y a un point technique en extremite (en fait origine), on recommence la recursion a partir de ce point
							nommage_support_parcours(shape_support[1],shape_pt[0],1,niveau+1)
							
							if shape_pt[0] != NULL:
								pt_aval = shape_pt[0]
							elif shape_pt[0] == NULL:
								pt_aval = 'pas de cable dans cette zone lors du nommage des POINTS TECHNIQUES'
								
							#pt_aval = shape_pt[0]
							#print 'extremite_avec_pt_bad_sens',';',shape_support[0],';',shape_pt[0],';',1,';',niveau+1,';',pt_aval,';','sens:',shape_support[3]
					if ptextremite_bad_sens == 0:
						# si il ny a pas de point technique en extremite, on recommence la recursion a partir de lextremite en se souvenant du dernier point technique rencontre
						pt_aval=nommage_support_parcours(shape_support[1],pt_amont,ordre+1,niveau+1)
							#print 'extremite_sans_pt_bad_sens_',';',shape_support[0],';',pt_amont,';',ordre+1,';',niveau+1,';',pt_aval
					#print 'nomsupport',';',shape_support[0],';',pt_amont,';',ordre+1,';',niveau+1,';',pt_aval
					
					if pt_amont != NULL:
						shape_support[4]=pt_amont
					elif pt_amont == NULL:
						shape_support[4] = 'pas de cable dans cette zone lors du nommage des POINTS TECHNIQUES'
						
					#shape_support[4]=pt_amont
					shape_support[5]=pt_aval

			if pt_aval == "" or pt_aval == NULL:
				pt_aval = 'Erreur pas de PT Extremite'
				for shape_pt in listshape_pt:
					if depart_origine_support == shape_pt[1]:
						pt_aval = shape_pt[0]

			return pt_aval

	nommage_support_parcours(point_depart_sro ,'PM',1,1)


	Support_mauvais_sens = QgsVectorLayer("LineString?crs=epsg:2154", "Support_mauvais_sens", "memory")
	Support_mauvais_sens_pr2 = Support_mauvais_sens.dataProvider()
	Support_mauvais_sens_attr2 = layershape_support.dataProvider().fields().toList()
	Support_mauvais_sens_pr2.addAttributes(Support_mauvais_sens_attr2)
	Support_mauvais_sens.updateFields()
	Support_mauvais_sens.commitChanges()

	#Declaration des indexes pour une utilisation de mise a jour des entites des attributs
	indexe_CODE_PT_origine=layershape_support.fieldNameIndex(CODE_PT_origine)
	indexe_CODE_PT_extremite=layershape_support.fieldNameIndex(CODE_PT_extremite)
	indexe_CODE_SUPPORT=layershape_support.fieldNameIndex(CODE_SUPPORT)

	for shape_support in list_shape_support: 
		outFeat = QgsFeature()
		a= shape_support[0],';',shape_support[1],';',shape_support[2],';',shape_support[3],';',shape_support[4],';',shape_support[5]
		attribut_support=[shape_support[0]]
		
		layershape_support.startEditing()
		
		#print shape_support[0],';',shape_support[4],';',shape_support[5]
		for shape_support_shape in layershape_support.getFeatures():
			if shape_support[0] == shape_support_shape[shape_support_Nom_Colonne_Nom]:
				layershape_support.changeAttributeValue(shape_support_shape.id(),indexe_CODE_PT_origine, shape_support[4])
				layershape_support.changeAttributeValue(shape_support_shape.id(),indexe_CODE_PT_extremite, shape_support[5])
				if (shape_support[4] != 'Erreur pas de PT Extremite' and  shape_support[4] != 'pas de cable dans cette zone lors du nommage des POINTS TECHNIQUES') and (shape_support[5] != 'Erreur pas de PT Extremite' and shape_support[5] != 'pas de cable dans cette zone lors du nommage des POINTS TECHNIQUES'):
					if shape_support[4] != -1 and shape_support[5] != -1:
						code_amont=shape_support[4].replace(Nom_PT_CHAMBRE,shape_support[7]).replace(Nom_PT_POTEAU,shape_support[7])
						code_aval=shape_support[5].replace(Nom_PT_CHAMBRE,shape_support[7]).replace(Nom_PT_POTEAU,shape_support[7])
						code_aval_last=code_aval[-5:].replace('-','')
						layershape_support.changeAttributeValue(shape_support_shape.id(),indexe_CODE_SUPPORT, code_amont+'-'+code_aval_last)
				else:
					layershape_support.changeAttributeValue(shape_support_shape.id(),indexe_CODE_SUPPORT, 'Voir champs Amont ou Aval')

		#Prendre que les supports qui sont dans le mauvais sens
		if shape_support[3] == -1:
			geom_support=QgsGeometry.fromWkt(shape_support[6])
			
			#Inverser le sens
			geom_support_Rec=None
			if geom_support and not geom_support.isEmpty():
				reversedLine = geom_support.geometry().reversed()
			geom_support_Rec=QgsGeometry(reversedLine)
			"""outFeat.setGeometry(geom_support_Rec)
			outFeat.setAttributes(attribut_support)
			pr_Support_sens_corriger.addFeatures([outFeat])"""
			
			#Mise a jour de la geometrie dans le shape support
			#layershape_support.startEditing()
			for shape_support_shape in layershape_support.getFeatures():
				if shape_support[0] == shape_support_shape[shape_support_Nom_Colonne_Nom]:
					Support_mauvais_sens_pr2.addFeatures([shape_support_shape]) 
					layershape_support.dataProvider().changeGeometryValues({shape_support_shape.id(): (geom_support_Rec)})
					#a=shape_support[0] 

		#print shape_support[0],';',shape_support[3],';',shape_support[4],';',shape_support[5]

	layershape_support.commitChanges()
	layershape_support.commitChanges()


	QgsMapLayerRegistry.instance().addMapLayer(Support_mauvais_sens)