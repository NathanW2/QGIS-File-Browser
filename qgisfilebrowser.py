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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import sys
import os
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from qgisfilebrowserdialog import QGISFileBrowserDialog

class QGISFileBrowser:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/qgisfilebrowser/icon.png"), \
        "QGISFileBrowser", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("triggered()"), self.run)

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&QGISFileBrowser", self.action)

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&QGISFileBrowser",self.action)
    self.iface.removeToolBarIcon(self.action)

  # run method that performs all the real work
  def run(self):
    # create and show the dialog
    dlg = QGISFileBrowserDialog()

    dlg.LoadFiles()
    # show the dialog
    dlg.show()
    result = dlg.exec_()
    # See if OK was pressed
    if result == 1:
      # do something useful (delete the line containing pass and
      # substitute with your code
      pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow(None)
    #brow = QGISFileBrowser(None)
    dlg = QGISFileBrowserDialog()
    dlg.LoadFiles()
    win.addDockWidget(Qt.LeftDockWidgetArea,dlg)
    #brow.run()
    win.show()

    retval = app.exec_()
    sys.exit(retval)
