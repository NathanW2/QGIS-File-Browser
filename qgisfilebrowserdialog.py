"""
/***************************************************************************
QGISFileBrowserDialog
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_qgisfilebrowser import Ui_QGISFileBrowser
# create the dialog for zoom to point

#Should find a better way to do this rather then using regex
filters = {
    "ESRI Shapefiles (*.shp *.SHP)": "^.*\.(shp)$",
    "Mapinfo File (*.mif *.tab *.MIF *.TAB)":  "^.*\.(mif|tab)$",
    # Spatial Data Transfer Standard (*catd.ddf *CATD.DDF):  "^.*\.(shp)$"
    "S-57 Base file (*.000 *.000)":  "^.*\.(000)$",
    "Microstation DGN (*.dgn *.DGN)":  "^.*\.(dgn)$",
    "VRT - Virtual Datasource  (*.vrt *.VRT)":  "^.*\.(vrt)$",
    "Atlas BNA (*.bna *.BNA)":  "^.*\.(bna)$",
    "Comma Separated Value (*.csv *.CSV)":  "^.*\.(csv)$",
    "Geography Markup Language (*.gml *.GML)":  "^.*\.(gml)$",
    "GPX (*.gpx *.GPX)":  "^.*\.(gpx)$",
    "KML (*.kml *.KML)":  "^.*\.(kml)$",
    "GeoJSON (*.geojson *.GEOJSON)":  "^.*\.(geojson)$",
    "INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI)":  "^.*\.(itf|xml|ili)$",
    "INTERLIS 2 (*.itf *.xml *.ili *.ITF *.XML *.ILI)":  "^.*\.(itf|xml|ili)$",
    "GMT (*.gmt *.GMT)":  "^.*\.(gmt)$",
    "SQLite (*.sqlite *.SQLITE)":  "^.*\.(sqlite)$",
    "ESRI Personal GeoDatabase (*.mdb *.MDB)":  "^.*\.(mdb)$",
    # X-Plane/Flightgear (apt.dat nav.dat fix.dat awy.dat APT.DAT NAV.DAT FIX.DAT AWY.DAT)":  "^.*\.(shp)$"
    "Arc/Info ASCII Coverage (*.e00 *.E00)":  "^.*\.(e00)$",
    "AutoCAD DXF (*.dxf *.DXF)":  "^.*\.(dxf)$",
    "Geoconcept (*.gxt *.txt *.GXT *.TXT)":  "^.*\.(gxt|txt)$",
    "GeoRSS (*.xml *.XML)":  "^.*\.(xml)$",
    "QGIS Project File (*.qgs)" : "^.*\.(qgs)$",
    "All supported files (*)":  "^.*\.(shp|mif|tab|000|dgn|vrt|bna|csv|gml|gpx|kml|geojson|itf|xml|ili|gmt|sqlite|mdb|e00|dxf|gxt|txt|xml|qgs)$"
  }

class QGISFileBrowserDialog(QDockWidget):
  #Signal notify when a file needs to be opened
  fileOpenRequest = pyqtSignal(file)

  def __init__(self):
    QDockWidget.__init__(self)
    # Set up the user interface from Designer.
    self.ui = Ui_QGISFileBrowser()
    self.ui.setupUi(self)

    #Load the filter list
    for filter in filters:
        self.ui.filtercombobox.addItem(filter)

  def LoadFiles(self):
    self.model = QFileSystemModel(self.ui.fileTree)
    self.model.setRootPath(QDir.homePath())
    self.proxy = MyFilter()
    self.proxy.setSourceModel(self.model)
    self.proxy.setFilterKeyColumn(0)

    self.proxy.setFilterRegExp(QRegExp(filters[str(self.ui.filtercombobox.currentText())],Qt.CaseInsensitive,QRegExp.RegExp))

    self.ui.fileTree.setModel(self.proxy)
    self.ui.fileTree.hideColumn(1)
    self.ui.fileTree.hideColumn(2)
    self.ui.fileTree.hideColumn(3)
    #Hack to make sure the horizontal scroll bar shows up
    self.ui.fileTree.header().setStretchLastSection(False)
    self.ui.fileTree.header().setResizeMode(QHeaderView.ResizeToContents)
    self.ui.fileTree.setColumnWidth(0,280)
    #Just hide the header because we don't need to see it.
    self.ui.fileTree.header().hide()

    self.connect(self.ui.filtercombobox,SIGNAL("currentIndexChanged( const QString &)"),self.filterChanged)
    #self.ui.filtercombobox.currentIndexChanged.connect(self.filterChanged)
    self.connect(self.ui.fileTree,SIGNAL("doubleClicked( const QModelIndex &)"), self.itemClicked)

  def filterChanged(self, text):
    print self.proxy
    self.proxy.setFilterRegExp(QRegExp(filters[str(text)],Qt.CaseInsensitive,QRegExp.RegExp))

  def itemClicked(self, item):
    index = item.model().mapToSource(item)
    filepath = self.model.filePath(index)
    #self.emit(SIGNAL("fileOpenRequest",filepath))
    self.fileOpenRequest.emit(filepath)

  def updateFilter(self, text):
    self.proxy.setFilterRegExp(QRegExp(text,Qt.CaseInsensitive,QRegExp.RegExp))

class MyFilter(QSortFilterProxyModel):
    def __init__(self,parent=None):
        super(MyFilter, self).__init__(parent)

    def filterAcceptsRow (self, source_row, source_parent ):
        if self.filterRegExp() == "":
            return True #Shortcut for common case

        source_index = self.sourceModel().index(source_row, 0, source_parent)

        if self.sourceModel().isDir(source_index):
            return True

        return self.sourceModel().data(source_index).toString().contains(self.filterRegExp())


