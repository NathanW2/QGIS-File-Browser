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

explorer = None

vectors = [
            'shp','mif', 'tab','000','dgn','vrt','bna','csv','gml',
            'gpx','kml','geojson','itf','xml','ili','gmt',
            'sqlite','mdb','e00','dxf','gxt','txt','xml'
            ]

rasters = [
          'ecw','sid','vrt','tiff',
          'tif','ntf','toc','img',
          'gff','asc','ddf','dt0',
          'dt1','dt2','png','jpg',
          'jpeg','mem','gif','n1',
          'xpm','bmp','pix','map',
          'mpr','mpl','rgb','hgt',
          'ter','nc','grb','hdr',
          'rda','bt','lcp','rik',
          'dem','gxf','hdf5','grd',
          'grc','gen','img','blx',
          'blx','sqlite','sdat'
          ]


class QGISFileBrowser:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        self.pluginname = "&QGIS File Browser"
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/qgisfilebrowser/icon.png"), \
            self.pluginname, self.iface.mainWindow())

        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(self.pluginname, self.action)

        for action in self.iface.pluginMenu().actions():
            if action.text() == QString(self.pluginname):
                # update the icon
                action.setIcon(QIcon(":/plugins/qgisfilebrowser/icon.png"))

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(self.pluginname,self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        global explorer
        if explorer is None:
        # create and show the dialog
            explorer = QGISFileBrowserDialog()
            explorer.LoadFiles()
            explorer.fileOpenRequest.connect(self.openFile)
                    # show the dialog
            if not self.iface.mainWindow().restoreDockWidget(explorer):
                self.iface.mainWindow().addDockWidget(Qt.LeftDockWidgetArea,explorer)
            explorer.show()
        else:
            explorer.setVisible(not explorer.isVisible())


    def openFile(self,filePath):
        filePath = unicode(filePath.toUtf8(),"utf-8")
        #Get the extension without the .
        extn = os.path.splitext(filePath)[1][1:].lower()
        if extn == 'qgs':
            #If we are project file we can just open that.
            self.iface.addProject(filePath)
        elif extn in vectors:
            self.iface.addVectorLayer(filePath,"","ogr")
        elif extn in rasters:
            self.iface.addRasterLayer(filePath,"")
        else:
            #We should never really get here, but just in case.
            pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow(None)
    explorer = QGISFileBrowserDialog()
    explorer.LoadFiles()
    win.addDockWidget(Qt.LeftDockWidgetArea,explorer)
    win.show()

    retval = app.exec_()
    sys.exit(retval)

