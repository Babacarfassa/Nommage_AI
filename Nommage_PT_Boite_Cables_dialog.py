# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Nommage_PT_Boite_CablesDialog
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

import os

from qgis.PyQt import QtGui, uic, QtWidgets
#from PyQt5 import uic
#from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Nommage_PT_Boite_Cables_dialog_base.ui'))


class Nommage_PT_Boite_CablesDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Nommage_PT_Boite_CablesDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
