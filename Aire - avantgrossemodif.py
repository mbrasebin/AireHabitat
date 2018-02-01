# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Airehabitat
                                 A QGIS plugin
 Nombre d'objets de la couche, leur superficie moyenne et selection d'objets
                              -------------------
        begin                : 2017-04-26
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Jennifer Benchetrit
        email                : jennifer.benchetrit@ign.fr
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
import sys
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import * #QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import * #QAction, QIcon

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from Aire_dialog import AirehabitatDialog
import os.path

#Import the libraries
from qgis.core import *
from qgis.gui import * 

class Airehabitat:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
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
            'Airehabitat_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Aire habitat')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Airehabitat')
        self.toolbar.setObjectName(u'Airehabitat')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Airehabitat', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = AirehabitatDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Airehabitat/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Aire habitat'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        # set the layers combobox items
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        self.dlg.couche.clear()
        for layer in layers:
            self.dlg.couche.addItem(layer.name(),layer)
        
        # set the operation combobox items
        self.dlg.operation.clear()
        self.dlg.operation.addItem("Nombre d'objets")
        self.dlg.operation.addItem("Superficie") 
        self.dlg.operation.addItem("Objets de cet attribut")
        self.dlg.operation.addItem("Proportion d'habitat")    
        self.dlg.operation.addItem("Proximite")                
        self.dlg.operation.addItem("Nombre de logements")      
        #-------------------
        #Edited function (exemple Laurence)        

            
        def nombre_objets(layer):
            fCount = layer.featureCount()
            phrase = "La couche %s a %d objets" %(layer.name(), fCount)
            return phrase

        def superficie_moy_objets(layer):
            print "Superficie moyenne des objets"
            taille = layer.featureCount()
            #print "taille =", taille
            listemoy = []

            # if layer.name() == "fusion_OCS_lib15niv2":
            #     attrib = 'lib15_niv2'
            # if layer.name() == "fusion_OCS_libniv2_sim2":
            #     attrib = 'libniv2sim'
            if layer.name() == "fusion_OCS_lib15niv2_sim2AU":
                attrib = 'libniv2sim'
 

                #récupérer la liste des valeurs de l'attribut 
                attname = layer.fieldNameIndex(attrib)
                #print "Pour l'attribut", attname
                listeValAttrCode = layer.uniqueValues(attname)  #{1;2;etc}  #liste de toutes les valeurs possibles d'un attribut
                # print listeValAttrCode (objet de type QLIST)

                #iterliste = listeValAttrCode  #itérateur parcourant l'ensemble des valeurs d'un attribut
                phrase = ""

                #boucle sur les valeurs de l'attribut                
                #j = 0
                for j in range(0, len(listeValAttrCode)):  
                #for j in iterliste:  #retourner les résultats pour chaque valeur d'attribut
                    i = 0  #i permet de récuperer le nombre d'objet d'un type d'habitat
                    surfsum = 0

                    iter = layer.getFeatures()
                    for feature in iter:
                        if feature[attrib] == listeValAttrCode[j]:               
                            superficie1 = feature.geometry().area();   
                            surfsum = surfsum + superficie1
                            i = i+1
                    surfmoy = surfsum/i
                    phrase += "L'habitat de type %s a des entites de superficie moyenne:\n %.2f m2\n" %(listeValAttrCode[j], surfmoy)
                    #return phrase
                    #j = j+1
                    # print ("j",j)
                    listemoy.append(surfmoy)

                # print len(listeValAttrCode)
                # print len(listemoy)

                #creation d'un fichier de résultats Excel
                from xlwt import Workbook

                # création 
                book = Workbook()                
                # création de la feuille 1
                feuil1 = book.add_sheet('feuille 1')
                
                for k in range(0, len(listeValAttrCode)):   
                    # ajout des en-têtes
                    feuil1.write(0,k,listeValAttrCode[k])
                    # ajout des valeurs dans la ligne suivante
                    ligne1 = feuil1.row(1)
                    ligne1.write(k, listemoy[k])
                
                # création matérielle du fichier résultant
                book.save('D:\\fichiers_excel_plugins\\superficies_habitats_sim2AUb.xls')


            else:   
                iter = layer.getFeatures()
                i = 0
                surfsum = 0
                nb = taille
                for feature in iter:
                    if i<nb:
                        superficie1 = feature.geometry().area();
                        surfsum = surfsum + superficie1
                    i=i+1
                surfmoy = surfsum/i
                phrase = "La couche %s a des entites de superficie moyenne %.2f m2" %(layer.name(), surfmoy)
            return phrase

        def selection_objets_attribut(layer,nomattr,valattr):
            print "*Recuperation des objets avec une valeur attributtaire particuliere"
            iter = layer.getFeatures()
            nb = 0
            for feature in iter:
                attr1 = feature[nomattr]
                if attr1 == valattr:
                    nb = nb + 1
            phrase = "Il y a %d objets selectionnes" %(nb)
            return phrase



        def proportion_habitat(layer):
            print "Proportion d'un type d'habitat dans le paysage:"
            phrase = ""
            
            #pour la couche OCS stJDV

            #aire totale de la commune
            layerpays = QgsVectorLayer("C:/Users/jbenchetrit/Desktop/QGIS-shapes/Poly StJDV.shp","stjdv","ogr")
            iter2 = layerpays.getFeatures()  #recuperation des objets de la couche
            for poly in iter2:
                totalarea = poly.geometry().area();


            listpland = []
            
            #Somme des aire des entités de l'habitat choisi
            if layer.name() == "OCS St-JDV":
                #récupérer la liste des valeurs de l'attribut du code d'OCS correspondant au type d'habitat
                attrib = 'lib15_niv2'  

                attname = layer.fieldNameIndex(attrib)
                listeValAttrCode = layer.uniqueValues(attname)


                #boucle sur les valeurs de l'attribut
                for j in range(0, len(listeValAttrCode)):  

                    surfsum = 0  
                    
                    iter = layer.getFeatures()
                    for feature in iter:
                        if feature[attrib] == listeValAttrCode[j]:
                            superficie1 = feature.geometry().area();
                            surfsum = surfsum + superficie1

            #calcul de PLAND
                    PLAND = (surfsum/totalarea)*100
                    phrase += "L'habitat %s represente %.2f%% du paysage\n" %(listeValAttrCode[j], PLAND)

                    listpland.append(PLAND)


                #creation d'un fichier de résultats Excel
                from xlwt import Workbook

                # création 
                book = Workbook()                
                # création de la feuille 1
                feuil1 = book.add_sheet('feuille 1')
                
                for k in range(0, len(listeValAttrCode)):   
                    # ajout des en-têtes
                    feuil1.write(0,k,listeValAttrCode[k])
                    # ajout des valeurs dans la ligne suivante
                    ligne1 = feuil1.row(1)
                    ligne1.write(k, listpland[k])
                
                # création matérielle du fichier résultant
                book.save('D:\\fichiers_excel_plugins\\PLAND_initial.xls')


            elif layer.name() == "OCS St-JDV modifie2":
                attrib = 'libniv2sim' 
            # elif layer.name() == "OCS St-JDV 2AU split":
            #     attrib = 'libniv2sim'

                attname = layer.fieldNameIndex(attrib)
                listeValAttrCode = layer.uniqueValues(attname)


                #boucle sur les valeurs de l'attribut
                for j in range(0, len(listeValAttrCode)):  

                    surfsum = 0  
                    
                    iter = layer.getFeatures()
                    for feature in iter:
                        if feature[attrib] == listeValAttrCode[j]:
                            superficie1 = feature.geometry().area();
                            surfsum = surfsum + superficie1

            #calcul de PLAND
                    PLAND = (surfsum/totalarea)*100
                    phrase += "L'habitat %s represente %.2f%% du paysage\n" %(listeValAttrCode[j], PLAND)

                    listpland.append(PLAND)


                #creation d'un fichier de résultats Excel
                from xlwt import Workbook

                # création 
                book = Workbook()                
                # création de la feuille 1
                feuil1 = book.add_sheet('feuille 1')
                
                for k in range(0, len(listeValAttrCode)):   
                    # ajout des en-têtes
                    feuil1.write(0,k,listeValAttrCode[k])
                    # ajout des valeurs dans la ligne suivante
                    ligne1 = feuil1.row(1)
                    ligne1.write(k, listpland[k])
                
                # création matérielle du fichier résultant
                book.save('D:\\fichiers_excel_plugins\\PLAND_sim2AU.xls')

            else:
                phrase += "ERREUR -> Selectionnez une couche d\'OCS pour appliquer cet indice. "
            
            return phrase


        def proximite(layer):
            print "Habitats du meme type a proximite:"
            print "(Pour utiliser cet indicateur, penser a fusionner les parcelles de meme type de la couche OCS \n avec dissolve en selectionnant 1 attribut a etudier, \n puis distinguer les entites en modifiant la geometrie de morceaux multiples a uniques.)"
            phrase = "" 
            

            # if layer.name() == "fusion_OCS_lib15niv2":
            #     attrib = 'lib15_niv2'
            # if layer.name() == "fusion_OCS_libniv2_sim":
            #     attrib = 'libniv2sim'
            if layer.name() == "fusion_OCS_libniv2_sim2":
                attrib = 'libniv2sim'

                #ou mettre proximite("fusion_OCS_libniv2_sim", 'libniv2sim') et changer def proximite en def proximite(layer, attrib)
                #ou juste décaler à gauche tt ce qu'il y a en dessous et afficher tt les if

                msgBox = QtGui.QMessageBox()
                msgBox.setText('Cliquez sur le type d\'indice que vous desirez')
                msgBox.addButton(QtGui.QPushButton('Prox par parcelle'), QtGui.QMessageBox.YesRole)
                msgBox.addButton(QtGui.QPushButton('Prox moyen par type d\'habitat'), QtGui.QMessageBox.NoRole)
                #msgBox.addButton(QtGui.QPushButton('Annuler'), QtGui.QMessageBox.RejectRole)
                ret = msgBox.exec_();
                #print ret

                listhabit = layer.uniqueValues(layer.fieldNameIndex(attrib)) #liste de ses valeurs = habitats
                print "liste=", listhabit
                

                #Delimmitation d'un rayon d'etude
                rayon, ok = QInputDialog.getInt(None, "Rayon d\'etude", "Entrer le rayon d\'etude en m")
                print "rayon a etudier =", rayon, "m"

                #boucle sur les valeurs de l'attribut               
                for j in range (0, len(listhabit)):
                    liste = []
                    iter1 = layer.getFeatures()

                    for feature in iter1:
                        if feature[attrib] == listhabit[j]:   
                            #print "feature=", feature[attrib]
                            iter2 = layer.getFeatures()
                            frac = 0 #initialise la formule de PROX (frac = PROX)

                            for feature2 in iter2:
                                #s'il  y a une autre parcelle de même type, différent de lui même
                                if (feature2[attrib] == feature[attrib]) and (feature2['id'] != feature['id']):
                                    
                                    distij = feature.geometry().distance(feature2.geometry());  #distij =   #distance entre parcelles i et j du même type     
                                    aj = feature2.geometry().area(); #aire de la parcelle j 

                                    #si l'autre parcelle est dans le rayon étudié
                                    if distij != 0 and distij < rayon: 
                                        frac = frac + aj/distij  #on somme pour chq nouvelle parcelle j identiques à i                             
                            liste.append(frac)
                            
                            if ret == 0:
                                phrase += "Valeur de PROX pour la parcelle %s de type %s = %.2f m \n" %(feature['id'] ,feature[attrib], frac)

                                #Ajout de la valeur de PROX dans la table d'attribut de la parcelle (creer d'abord attribut 'PROX_value' sur QGIS)
                                layer.startEditing()
                                feature['PROX_value'] = frac
                                layer.updateFeature(feature)
                                layer.commitChanges()                                       
                    
                    #print "liste des PROXi pour l'habitat", listhabit[j], "=", liste, "de longueur", len(liste)
                    
                    if ret == 1:
                        moy = sum(liste)/len(liste)   #moyenne pour le type d'habitat i
                        #calcul de l'ecart-type pour voir la dispersion entre les valeurs des PROX d'un type d'habitat
                        var = sum([ x**2 for x in liste])/len(liste) - moy**2
                        std = var**0.5
                        phrase += "Type d'habitat: %s \n PROX moyen= %.2f ;  Ecart-type= %.2f \n" %(listhabit[j], moy, std)

                            # if feature['lib15_niv3'] == "Jardins familiaux":
                            #     print "distance entre", feature['lib15_niv3'], " et ", feature2['lib15_niv3'], "=", distij
            else:
                phrase += "ERREUR -> Selectionnez une couche fusion_OCS pour appliquer cet indice. "

            return phrase

        def nblogements(layer):
            print "Nombre de logements"
            phrase = "" 

            if layer.name() == "out3AU_fusion" or layer.name() == "out3AU_fusion2":
                iter1 = layer.getFeatures()
                listlog = []

                for feature in iter1:
                    val = feature['Nb_logemt']
                    listlog.append(val)

                nblog = sum(listlog)
                print "Nb batiments=", len(listlog)
                phrase += "Nombre de logements contenus dans les batiments simules: " + str(nblog)

            else:
                phrase += "ERREUR -> Selectionnez une couche out3AU_fusion pour appliquer cet indice. "

            return phrase


        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            indexOp = self.dlg.operation.currentIndex()
            indexCouche = self.dlg.couche.currentIndex()
            layer = self.dlg.couche.itemData(indexCouche)

            if indexOp == 0:
                print nombre_objets(layer)
            elif indexOp == 1:
                QMessageBox.information(self.iface.mainWindow(),"Surface moyenne des taches d'habitat", superficie_moy_objets(layer))
            elif indexOp == 2:
                print selection_objets_attribut(layer,'lib15_niv3','Tissu urbain continu')
            elif indexOp == 3:
                QMessageBox.information(self.iface.mainWindow(),"Indice PLAND: Proportion d'habitat", proportion_habitat(layer))
                # print proportion_habitat(layer)
            elif indexOp == 4:
                QMessageBox.information(self.iface.mainWindow(),"Indice de Proximite", proximite(layer))
            elif indexOp == 5:
                QMessageBox.information(self.iface.mainWindow(),"Nombre de logements", nblogements(layer))
            else:
                print "pas de indexOp"
            #pass




