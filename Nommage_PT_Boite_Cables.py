# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Nommage_PT_Boite_Cables
                                 A QGIS plugin
 Nommage_PT_Boite_Cables
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
'test_baba'
import processing, re,itertools,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *


def Nommage_PT_Boite_Cables_function(shape_pbo, shape_cables,shape_pt):
	"""Run method that performs all the real work"""

	Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON_NOMMAGE_AI", "", "xlsx files (*.xlsx)")

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
	shape_BP_name_BP_NOM='BP_NOM'
	shape_BP_name_BP_FONCTION='BP_FONCTION'
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CB_name_CB_Origine='CB_Origine'
	shape_CB_name_CB_Extremite='CB_Extremite'
	shape_PT_name_PT_NOM='PT_NOM'
	shape_PT_name_PT_TYPE='PT_TYPE'

	#Declaration des noms des entites
	shape_BP_name_BP_FONCTION_PBO='BP_FONCTION_PBO'
	shape_BP_name_BP_FONCTION_BPE='BP_FONCTION_BPE'
	shape_BP_name_BP_FONCTION_PEC_PBO='BP_FONCTION_PEC'
	shape_CB_name_CB_Origine_SRO='CB_Origine_SRO'
	shape_PT_name_PT_TYPE_CHAMBRE='PT_TYPE_CHAMBRE'
	shape_PT_name_PT_TYPE_POTEAU='PT_TYPE_POTEAU'
	shape_PT_name_PT_TYPE_IMMEUBLE='PT_TYPE_IMMEUBLE'
	shape_PT_name_PT_TYPE_FACADE='PT_TYPE_FACADE'

	#Declaration des noms des variable_utilisateur
	variable_utilisateur_Nom_NRO='Nom_NRO'
	variable_utilisateur_Numero_NRO='Numero_NRO'
	variable_utilisateur_Nom_SRO='Nom_SRO'
	variable_utilisateur_Numero_SRO='Numero_SRO'
	variable_utilisateur_Code_departement='Code_departement'

	#Recuperation des noms des colonnes a partir du fichier de configuration
	shape_cables_Nom_Colonne_Nom=get_field_name(shape_CB_name_CB_NOM,shape_cables)#NOM
	shape_cables_Nom_Origine_Depart_Valeur=get_field_name(shape_CB_name_CB_Origine_SRO,shape_cables)#SRO-68-047-DVF
	Nom_Colonne_Origine_cable=get_field_name(shape_CB_name_CB_Origine,shape_cables)#originee
	Nom_Colonne_cable_Extremite=get_field_name(shape_CB_name_CB_Extremite,shape_cables)#extremitee

	shape_pbo_Nom_Colonne_Nom=get_field_name(shape_BP_name_BP_NOM,shape_pbo)#NOM
	shape_pbo_Nom_Colonne_TYPE_FONC=get_field_name(shape_BP_name_BP_FONCTION,shape_pbo)#FONCTION
	shape_pbo_TYPE_FONC_PBO=get_field_name(shape_BP_name_BP_FONCTION_PBO,shape_pbo)#PBO
	shape_pbo_TYPE_FONC_BPE=get_field_name(shape_BP_name_BP_FONCTION_BPE,shape_pbo)#BPE
	shape_pbo_TYPE_FONC_PEC_PBO=get_field_name(shape_BP_name_BP_FONCTION_PEC_PBO,shape_pbo)#PEC-PBO

	shape_pt_Nom_Colonne_Nom=get_field_name(shape_PT_name_PT_NOM,shape_pt)#CODE
	shape_pt_Nom_Colonne_TYPE_STRUC=get_field_name(shape_PT_name_PT_TYPE,shape_pt)#TYPE_STRUC
	shape_pt_TYPE_STRUC_CHAMBRE=get_field_name(shape_PT_name_PT_TYPE_CHAMBRE,shape_pt)#CHAMBRE
	shape_pt_TYPE_STRUC_POTEAU=get_field_name(shape_PT_name_PT_TYPE_POTEAU,shape_pt)#APPUI
	#shape_pt_TYPE_STRUC_ANCRAGE_FACADE_IMMEUBLE=get_field_name(shape_PT_name_PT_TYPE_IMMEUBLE,shape_pt)#ANCRAGE FACADE IMMEUBLE
	shape_pt_TYPE_STRUC_IMMEUBLE=get_field_name(shape_PT_name_PT_TYPE_IMMEUBLE,shape_pt)#IMMEUBLE
	shape_pt_TYPE_STRUC_FACADE=get_field_name(shape_PT_name_PT_TYPE_FACADE,shape_pt)#FACADE

	Nom_du_NRO=get_field_name(variable_utilisateur_Nom_NRO,shape_cables)#NRO
	numero_nro_existant=get_field_name(variable_utilisateur_Numero_NRO,shape_cables)#047
	numero_sro_existant=get_field_name(variable_utilisateur_Numero_SRO,shape_cables)#DVF
	Nom_du_SRO=get_field_name(variable_utilisateur_Nom_SRO,shape_cables)#SRO
	Code_deperatement=get_field_name(variable_utilisateur_Code_departement,shape_cables)#68


	Id_NRO='code_nro'
	Id_SRO='code_sro'
	Id_POCHE='poche'
	Id_INCR='incr'
	Id_NOMPT='nompt'
	CODE_PT='CODE_PT_AI'
	CODE_BP='CODE_BP_AI'
	CODE_CB='CODE_CB_AI'
	Nom_PT_CHAMBRE='CHA'
	Nom_PT_POTEAU='POT'
	Nom_PT_FACADE='FAC'
	Nom_PT_IMMEUBLE='IMM'
	Increment_nro='1'
	Increment_sro='2'
	Nom_Cable_DISTRI='CDI'
	CODE_PT_origine='PT_AVAL'
	CODE_PT_extremite='PT_AMONT'
	code_pec_PBO='PEC'



	layershape_pbo = shape_pbo
	layershape_cables = shape_cables
	layershape_pt = shape_pt
	#layershape_support = processing.getObject(shape_support)


	list_cable_pt=[]
	list_unique_cable_pt=[]
	seen = []

	distance = QgsDistanceArea()
	crs = QgsCoordinateReferenceSystem()
	crs.createFromSrsId(2154) # EPSG:4326
	distance.setSourceCrs(crs)
	distance.setEllipsoidalMode(True)
	distance.setEllipsoid('RGF93')

	origine_AI='Orig_AI'
	extremite_AI='Extrem_AI'


	#Parti dajout des champs dans les shapes pour des utilisations ulterieur
	def ajout_champs(Id_NRO,Id_SRO):
		
		#layershape_pbo = processing.getObject(shape_pbo)
		#layershape_cables = processing.getObject(shape_cables)

		#Partie des colonnes a ajouter  dans le shapefile shape_pbo
		nom_champs_shape_pbo=[]
		for j in layershape_pbo.dataProvider().fields():
			nom_champs_shape_pbo.append(j.name()) 
		if (Id_NRO not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Id_NRO,QVariant.String)])
		if (Id_SRO not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Id_SRO,QVariant.String)])
		if (Id_POCHE not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Id_POCHE,QVariant.Int)])
		if (CODE_BP not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(CODE_BP,QVariant.String)])
		if (CODE_PT not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(CODE_PT,QVariant.String)])
		
		layershape_pbo.updateFields()
		layershape_pbo.commitChanges()

		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_cable=[]
		for k in layershape_cables.dataProvider().fields():
			nom_champs_cable.append(k.name()) 
		if  (Id_NRO not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Id_NRO,QVariant.String)])
		if  (Id_SRO not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Id_SRO,QVariant.String)])
		if  (Id_POCHE not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Id_POCHE,QVariant.Int)])
		if  (CODE_CB not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(CODE_CB,QVariant.String)])
		if  (origine_AI not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(origine_AI,QVariant.String)])
		if  (extremite_AI not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(extremite_AI,QVariant.String)])
		
		layershape_cables.updateFields()
		layershape_cables.commitChanges()
		
		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_pt=[]
		for k in layershape_pt.dataProvider().fields():
			nom_champs_pt.append(k.name()) 
		if  (Id_NRO not in nom_champs_pt) :
			layershape_pt.dataProvider().addAttributes([QgsField(Id_NRO,QVariant.String)])
		if  (Id_SRO not in nom_champs_pt) :
			layershape_pt.dataProvider().addAttributes([QgsField(Id_SRO,QVariant.String)])
		if  (Id_POCHE not in nom_champs_pt) :
			layershape_pt.dataProvider().addAttributes([QgsField(Id_POCHE,QVariant.Int)])
		if  (Id_INCR not in nom_champs_pt) :
			layershape_pt.dataProvider().addAttributes([QgsField(Id_INCR,QVariant.Int)])
		if  (Id_NOMPT not in nom_champs_pt) :
			layershape_pt.dataProvider().addAttributes([QgsField(Id_NOMPT,QVariant.String)])
		if  (CODE_PT not in nom_champs_pt) :
			layershape_pt.dataProvider().addAttributes([QgsField(CODE_PT,QVariant.String)])

		layershape_pt.updateFields()
		layershape_pt.commitChanges()
		
		'''
		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_shape_support=[]
		for k in layershape_support.dataProvider().fields():
			nom_champs_shape_support.append(k.name()) 
		if  (CODE_PT_origine not in nom_champs_shape_support) :
			layershape_support.dataProvider().addAttributes([QgsField(CODE_PT_origine,QVariant.String)])
		if  (CODE_PT_extremite not in nom_champs_shape_support) :
			layershape_support.dataProvider().addAttributes([QgsField(CODE_PT_extremite,QVariant.String)])
		
		layershape_support.updateFields()
		layershape_support.commitChanges()'''


	#Partie de la creation des listes pour une utilisation de parcours des cables
	listshape_cables_temp = []
	for shape_cables in layershape_cables.getFeatures():
		cable = [shape_cables[shape_cables_Nom_Colonne_Nom],shape_cables[Nom_Colonne_Origine_cable],shape_cables[Nom_Colonne_cable_Extremite],-1,-1,-1,shape_cables.geometry().exportToWkt(),shape_cables.geometry().length()]
		listshape_cables_temp.append(cable)
	#Tri pour numeroter en premier les poches des cables de transport les plus courts
	listshape_cables= sorted(listshape_cables_temp,key=lambda colonnes: colonnes[7]) 
		
	listshape_pbo = []
	for shape_pbos in layershape_pbo.getFeatures():
		shape_pbo = [shape_pbos[shape_pbo_Nom_Colonne_Nom],-1,-1,-1,shape_pbos.geometry().exportToWkt(),-1]
		listshape_pbo.append(shape_pbo)

	listshape_pt = []
	for shape_pts in layershape_pt.getFeatures():
		shape_pt = [shape_pts[shape_pt_Nom_Colonne_Nom],shape_pts.geometry().exportToWkt(),-1,-1,-1,-1]
		listshape_pt.append(shape_pt)

	#Nommage du NRO
	Code_du_NRO_DEP=Nom_du_NRO+'-'+Code_deperatement
	Code_du_NRO = Code_du_NRO_DEP+'-'+numero_nro_existant.zfill(3) 
	#Increment_nro.zfill(3)
	#Nommage du SRO
	Code_du_SRO_NRO=Nom_du_SRO+Code_du_NRO.replace(Nom_du_NRO,'')+'-'
	Code_du_SRO = Code_du_SRO_NRO+numero_sro_existant
	#Increment_sro.zfill(3)

	#Function de codage ascii
	def codagePTAI(i):
		j = i*5
		centaines = int(j/100)
		if centaines <10 :
			premcar = str(centaines)
		else :
			premcar = chr(55+centaines)
		unites = j%100
		unites = str(unites).zfill(2)
		   
		return premcar+unites


	#Function de parcours des boites dans les cableset recupertion de certains informations
	nopttech = 0 #int("000")
	def nommage_cable_boite_pt(noeud, niveau, poche) :
		
		global nopttech
		
		if niveau < 1000:
			#print "debut sommefib " + noeud
			for shape_cables in listshape_cables:
				
				if shape_cables[1] == noeud:  
					if niveau== 1 :
						poche = poche +1
						nopttech = 1
					
					#remplir les codes nro, sro et la poche dans cable
					shape_cables[3] =Code_du_NRO
					shape_cables[4] =Code_du_SRO
					shape_cables[5] = poche
					
					geom_cable=QgsGeometry.fromWkt(shape_cables[6])
					bboxshape_cables = geom_cable.buffer(5,5).boundingBox()
					request = QgsFeatureRequest()
					request.setFilterRect(bboxshape_cables)
					
					if geom_cable.wkbType()==QGis.WKBMultiLineString:
						geom_cable_type=geom_cable.asMultiPolyline()
						cable_origine=geom_cable_type[0][0]
					
					if geom_cable.wkbType()==QGis.WKBLineString:
						geom_cable_type=geom_cable.asPolyline()
						cable_origine=geom_cable_type[0]
					
					cable_origine_point = (QgsGeometry.fromPoint(QgsPoint(cable_origine))).asPoint()
					
					
					if geom_cable.wkbType() in [QGis.WKBMultiLineString,QGis.WKBLineString]: 
						#Parcours des PT et recuperation des PT sur les cables
						listATrier_pt = []
						list_cable_poche_PT = []
						for shape_pt in layershape_pt.getFeatures(request):
							#print shape_pt['ID_PT']#,";",shape_pt.geometry().exportToWkt()
							if shape_pt.geometry().within(geom_cable.buffer(0.5,0.5)):
								pt_geom = shape_pt.geometry()
								
								m = distance.measureLine(cable_origine_point, (pt_geom.asPoint()))
								listATrier_pt.append([shape_pt[shape_pt_Nom_Colonne_Nom],m,-1])
								list_cable_poche_PT.append([shape_pt[shape_pt_Nom_Colonne_Nom],geom_cable.length(),-1])

					#Trier laliste selon la distance            
					listTriee_pt = sorted(listATrier_pt,key=lambda colonnes: colonnes[1]) 
					listTriee_cable_poche_PT = sorted(list_cable_poche_PT,key=lambda colonnes: colonnes[1]) 
					for pttrie in listTriee_pt :
						#print pttrie[0],";",pttrie[1]
						for pt in listshape_pt :
							#Prendre que les PT qui ne sont pas remplis cest a dire egal a -1
							if pt[2] == -1 :
								if pttrie[0] == pt[0]:
									#remplir les codes nro, sro, la poche et le numero de dans PT
									pt[2]=shape_cables[3]#NRO
									pt[3]=shape_cables[4]#SRO
									#pt[4]= shape_cables[5]#POCHE
									pt[5]= nopttech#Numero PT
									nopttech+=1
					
					for pttrie in listTriee_cable_poche_PT :
						for pt in listshape_pt :
							if pttrie[0] == pt[0]:
								#Prendre que les poches dans les cables selon la longueur du cable la plus courte
								pt[4]= shape_cables[5]#POCHE

					besoinsfoextremite = nommage_cable_boite_pt(shape_cables[2],niveau + 1, poche)
				

					
			for shape_pbo in listshape_pbo:
				if shape_pbo[0]== noeud:
					#remplir nom du sro,nro pour chaque boite
					shape_pbo[1]=Code_du_NRO
					shape_pbo[2]=Code_du_SRO
					shape_pbo[3] = poche
		
		#return somme

		#return -11111


	#Function dajout du NRO,SRO,POCHE,CODE_CB,CODE_BP_CODE_PT,Numero_PT,CODE_PT dans les shapefiles
	def ajout_code_nro_sro_cables_boites():
		
		#layershape_pbo = processing.getObject(shape_pbo)
		#layershape_cables = processing.getObject(shape_cables)
		
		#Defintion des index des shapes a utiliser
		indexe_code_nro_cable=layershape_cables.fieldNameIndex(Id_NRO)
		indexe_code_sro_cable=layershape_cables.fieldNameIndex(Id_SRO)
		indexe_poche_cable=layershape_cables.fieldNameIndex(Id_POCHE)
		indexe_CODE_CB_cable=layershape_cables.fieldNameIndex(CODE_CB)
		indexe_CODE_CB_cable_Ori_AI=layershape_cables.fieldNameIndex(origine_AI)
		indexe_CODE_CB_cable_Extrem_AI=layershape_cables.fieldNameIndex(extremite_AI)
		
		indexe_code_nro_pbo=layershape_pbo.fieldNameIndex(Id_NRO)
		indexe_code_sro_pbo=layershape_pbo.fieldNameIndex(Id_SRO)
		indexe_poche_pbo=layershape_pbo.fieldNameIndex(Id_POCHE)
		indexe_CODE_BP_pbo=layershape_pbo.fieldNameIndex(CODE_BP)
		indexe_CODE_PT_pbo=layershape_pbo.fieldNameIndex(CODE_PT)
		
		indexe_code_nro_pt=layershape_pt.fieldNameIndex(Id_NRO)
		indexe_code_sro_pt=layershape_pt.fieldNameIndex(Id_SRO)
		indexe_poche_pt=layershape_pt.fieldNameIndex(Id_POCHE)
		indexe_incr_pt=layershape_pt.fieldNameIndex(Id_INCR)
		indexe_nom_pt=layershape_pt.fieldNameIndex(Id_NOMPT)
		indexe_CODE_PT=layershape_pt.fieldNameIndex(CODE_PT)

		#Debut des start editing pour modification des shapes
		layershape_cables.startEditing()           
		layershape_pbo.startEditing()        
		layershape_pt.startEditing()
		
		#Ajout du NRO, SRO,POCHE,NUMERO DU PT ET CODE_PT_AI dans le shape PT
		for shape_pts in layershape_pt.getFeatures():
			for shape_pt in listshape_pt:
				if shape_pts[shape_pt_Nom_Colonne_Nom] == shape_pt[0]:
					
					#print shape_pt[5]
					#Ajout des codes NRo et SRO dans Boites
					layershape_pt.changeAttributeValue(shape_pts.id(),indexe_code_nro_pt, shape_pt[2])
					layershape_pt.changeAttributeValue(shape_pts.id(),indexe_code_sro_pt, shape_pt[3])
					layershape_pt.changeAttributeValue(shape_pts.id(),indexe_poche_pt, shape_pt[4])
					layershape_pt.changeAttributeValue(shape_pts.id(),indexe_incr_pt, shape_pt[5])
					layershape_pt.changeAttributeValue(shape_pts.id(),indexe_nom_pt, unicode(codagePTAI(shape_pt[5])))                
					if shape_pt[2] != -1:
						if shape_pts[CODE_PT] == NULL:
						#Il faut le champs et et la valeur du PT
							if shape_pts[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_CHAMBRE:
								layershape_pt.changeAttributeValue(shape_pts.id(),indexe_CODE_PT, unicode(Nom_PT_CHAMBRE+'-'+(shape_pt[2]).replace(Nom_du_NRO+'-','')+'-'+(shape_pt[3].replace(Code_du_SRO_NRO,''))+'-'+str(shape_pt[4])+str(codagePTAI(shape_pt[5]))))
							if shape_pts[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_POTEAU:
								layershape_pt.changeAttributeValue(shape_pts.id(),indexe_CODE_PT, unicode(Nom_PT_POTEAU+'-'+(shape_pt[2]).replace(Nom_du_NRO+'-','')+'-'+(shape_pt[3].replace(Code_du_SRO_NRO,''))+'-'+str(shape_pt[4])+str(codagePTAI(shape_pt[5]))))
							if shape_pts[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_FACADE:
								layershape_pt.changeAttributeValue(shape_pts.id(),indexe_CODE_PT, unicode(Nom_PT_FACADE+'-'+(shape_pt[2]).replace(Nom_du_NRO+'-','')+'-'+(shape_pt[3].replace(Code_du_SRO_NRO,''))+'-'+str(shape_pt[4])+str(codagePTAI(shape_pt[5]))))
							if shape_pts[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_IMMEUBLE:
								layershape_pt.changeAttributeValue(shape_pts.id(),indexe_CODE_PT, unicode(Nom_PT_IMMEUBLE+'-'+(shape_pt[2]).replace(Nom_du_NRO+'-','')+'-'+(shape_pt[3].replace(Code_du_SRO_NRO,''))+'-'+str(shape_pt[4])+str(codagePTAI(shape_pt[5]))))
							
		#Ajout du NRO, SRO,POCHE et CODE_BP_AI dans  le shape PBO 
		for shape_pbos in layershape_pbo.getFeatures():
			for shape_pbo in listshape_pbo:
				if shape_pbos[shape_pbo_Nom_Colonne_Nom] == shape_pbo[0]:
					#Ajout des codes NRo et SRO dans Boites
					layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_code_nro_pbo, shape_pbo[1])
					layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_code_sro_pbo, shape_pbo[2])
					layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_poche_pbo, shape_pbo[3])    
			#for shape_pbos in layershape_pbo.getFeatures():
			geom_boite=shape_pbos.geometry()
			bboxinfra = geom_boite.buffer(5, 5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxinfra)
			res='KO'
		
			#Nommage PBO+BPE
			
			for shape_point_technique in layershape_pt.getFeatures(request):
				if geom_boite.within((shape_point_technique.geometry().buffer(0.1, 0.1))):
					res='OK'
					layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_CODE_PT_pbo, (shape_point_technique[CODE_PT]))
					#Si PT == CHAMBRE, POTEAU  FACADE ou IMMEUBLE et boite == PBO donc nommage avec id PBO
					if shape_pbos[shape_pbo_Nom_Colonne_TYPE_FONC] == shape_pbo_TYPE_FONC_PBO and (shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_POTEAU or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_CHAMBRE  or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_IMMEUBLE or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_FACADE):
						if shape_point_technique[CODE_PT] != NULL:
							layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_CODE_BP_pbo, unicode(shape_point_technique[CODE_PT].replace (Nom_PT_POTEAU,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_CHAMBRE,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_IMMEUBLE,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_FACADE,shape_pbo_TYPE_FONC_PBO)))
					#Si PT == CHAMBRE,POTEAU , POTEAU  FACADE ou IMMEUBLE et boite == BPE donc nommage avec id BPE
					
					if shape_pbos[shape_pbo_Nom_Colonne_TYPE_FONC] == shape_pbo_TYPE_FONC_BPE and (shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_POTEAU or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_CHAMBRE  or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] ==  shape_pt_TYPE_STRUC_IMMEUBLE or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_FACADE):
						 if shape_point_technique[CODE_PT] != NULL:
							 layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_CODE_BP_pbo, unicode(shape_point_technique[CODE_PT].replace (Nom_PT_POTEAU,code_pec_PBO).replace (Nom_PT_CHAMBRE,code_pec_PBO).replace (Nom_PT_IMMEUBLE,code_pec_PBO).replace (Nom_PT_FACADE,code_pec_PBO)))
					#Si PT == CHAMBRE, POTEAU, POTEAU  FACADE ou IMMEUBLE  et boite == BPE donc nommage avec id PEC-PBO
					
					if shape_pbos[shape_pbo_Nom_Colonne_TYPE_FONC] == shape_pbo_TYPE_FONC_PEC_PBO and (shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_POTEAU or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_CHAMBRE  or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] ==  shape_pt_TYPE_STRUC_IMMEUBLE or shape_point_technique[shape_pt_Nom_Colonne_TYPE_STRUC] == shape_pt_TYPE_STRUC_FACADE):
						 if shape_point_technique[CODE_PT] != NULL:
							 layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_CODE_BP_pbo, unicode(shape_point_technique[CODE_PT].replace (Nom_PT_POTEAU,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_CHAMBRE,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_FACADE,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_IMMEUBLE,shape_pbo_TYPE_FONC_PBO)))
					#Si PT == CHAMBRE, POTEAU, POTEAU  FACADE ou IMMEUBLE  et boite != PBO ou BPE donc nommage avec id PBO
					elif shape_pbos[shape_pbo_Nom_Colonne_TYPE_FONC] not in [shape_pbo_TYPE_FONC_BPE,shape_pbo_TYPE_FONC_PBO,shape_pbo_TYPE_FONC_PEC_PBO]:
						 if shape_point_technique[CODE_PT] != NULL:
							 layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_CODE_BP_pbo, unicode(shape_point_technique[CODE_PT].replace (Nom_PT_POTEAU,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_CHAMBRE,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_IMMEUBLE,shape_pbo_TYPE_FONC_PBO).replace (Nom_PT_FACADE,shape_pbo_TYPE_FONC_PBO)))
					
			#Erreur de supperposition entre PT et Boite
			if res == 'KO':
				layershape_pbo.changeAttributeValue(shape_pbos.id(),indexe_CODE_BP_pbo, ('-1'))
			
		#Renommage des boites qui se superposent
		for shape_pt in layershape_pt.getFeatures():
			bboxshape_boites= shape_pt.geometry().buffer(5,5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxshape_boites)   
			count_boite_pt=0 
			list_boite_pt=[]
			for shape_boite in layershape_pbo.getFeatures(request):
				if shape_boite.geometry().within(shape_pt.geometry().buffer(0.1,0.1)):
					count_boite_pt += 1
					list_boite_pt.append([shape_pt[CODE_PT],shape_boite[CODE_BP],count_boite_pt])
			if count_boite_pt >1:
				for ilist in  list_boite_pt:
					if ilist[0]==shape_pt[CODE_PT]:
						for shape_boite in layershape_pbo.getFeatures(request):
							if ilist[1]==shape_boite[CODE_BP]:
								if shape_boite[CODE_BP]!=NULL:
									#print (str(ilist[2]).zfill(2))
									layershape_pbo.changeAttributeValue(shape_boite.id(),indexe_CODE_BP_pbo, unicode(shape_boite[CODE_BP]+'-'+(str(ilist[2]).zfill(2))))
								#print shape_boite[CODE_BP],';',ilist[2],';',shape_boite[CODE_BP]+'-'+str(ilist[2])
		
		layershape_cables.commitChanges()
		layershape_pbo.commitChanges()
		layershape_pt.commitChanges()
		#Ajout du NRO, SRO,POCHE et CODE_CB_AI dans  le shape PBO 
		
		
		layershape_cables.startEditing()           
		layershape_pbo.startEditing()        
		layershape_pt.startEditing()
		
		for shape_cables in layershape_cables.getFeatures():
			for list_cable in listshape_cables:
				if shape_cables[shape_cables_Nom_Colonne_Nom] == list_cable[0]:
					#Ajout des codes NRo et SRO dans Cables
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_code_nro_cable,list_cable[3])
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_code_sro_cable,list_cable[4])
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_poche_cable,list_cable[5])
			geom_cable=shape_cables.geometry()
			
			bboxinfra = geom_cable.buffer(5, 5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxinfra)
			for shape_pbo in layershape_pbo.getFeatures(request):
				if shape_cables[Nom_Colonne_cable_Extremite] == shape_pbo[shape_pbo_Nom_Colonne_Nom]:
					if shape_pbo[CODE_BP] != '-1' and shape_pbo[CODE_BP] != NULL:
						if shape_cables[CODE_CB] =='-1' or shape_cables[CODE_CB] ==NULL:
							layershape_cables.changeAttributeValue(shape_cables.id(),indexe_CODE_CB_cable,(shape_pbo[CODE_BP].replace (shape_pbo_TYPE_FONC_PBO,Nom_Cable_DISTRI).replace (shape_pbo_TYPE_FONC_BPE,Nom_Cable_DISTRI).replace (code_pec_PBO,Nom_Cable_DISTRI).replace (Nom_PT_IMMEUBLE,Nom_Cable_DISTRI).replace (Nom_PT_FACADE,Nom_Cable_DISTRI)))
					else :
						layershape_cables.changeAttributeValue(shape_cables.id(),indexe_CODE_CB_cable,('-1'))
				 
				 #Remplir des origines et extremites AI dans Cables
				if shape_cables[Nom_Colonne_cable_Extremite] == shape_pbo[shape_pbo_Nom_Colonne_Nom]:
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_CODE_CB_cable_Extrem_AI,(shape_pbo[CODE_BP]))
				if shape_cables[Nom_Colonne_Origine_cable] == shape_pbo[shape_pbo_Nom_Colonne_Nom]:
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_CODE_CB_cable_Ori_AI,(shape_pbo[CODE_BP]))
					
		layershape_cables.commitChanges()
		layershape_pbo.commitChanges()
		layershape_pt.commitChanges()

		


	#1.Execution de la fonction ajout des champs code nro et sro dans cables et boites
	ajout_champs(Id_NRO,Id_SRO)

	#2.Execution de la function parcours des cables
	nommage_cable_boite_pt(shape_cables_Nom_Origine_Depart_Valeur,1,0)

	#3.Execution de la function ajout des codes nro et sro dans cables et boites
	ajout_code_nro_sro_cables_boites()

