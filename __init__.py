"""
/***************************************************************************
QGISFileBrowser
A QGIS plugin
A tree like file browser that can open any qgis supported format into qgis.
                             -------------------
begin                : 2011-01-20
copyright            : (C) 2011 by Nathan Woodrow
email                : woodrow.nathan@gmail.com
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
def name():
  return "QGIS File Browser"
def description():
  return "A tree like file browser that can open any qgis supported format into qgis."
def version():
  return "Version 1.2"
def icon():
  return "icon.png"
def qgisMinimumVersion():
  return "1.5"
def classFactory(iface):
  # load QGISFileBrowser class from file QGISFileBrowser
  from qgisfilebrowser import QGISFileBrowser
  return QGISFileBrowser(iface)


