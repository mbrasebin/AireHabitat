# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Airehabitat
                                 A QGIS plugin
 Nombre d'objets de la couche, leur superficie moyenne et selection d'objets
                             -------------------
        begin                : 2017-04-26
        copyright            : (C) 2017 by Jennifer Benchetrit
        email                : jennifer.benchetrit@ign.fr
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
    """Load Airehabitat class from file Airehabitat.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Aire import Airehabitat
    return Airehabitat(iface)
