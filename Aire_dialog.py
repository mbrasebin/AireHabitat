# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AirehabitatDialog
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

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Aire_dialog_base.ui'))


class AirehabitatDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(AirehabitatDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
