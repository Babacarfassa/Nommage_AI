# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Nommage_Support_AI
                                 A QGIS plugin
 Nommage_Support_AI
                             -------------------
        begin                : 2018-07-26
        copyright            : (C) 2018 by Circet
        email                : Babacar.FASSA@circet.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Nommage_Support_AI class from file Nommage_Support_AI.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Nommage_AI import Nommage_AI
    return Nommage_AI(iface)
