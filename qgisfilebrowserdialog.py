"""
/***************************************************************************
QGISFileBrowserDialog
A QGIS plugin
A tree like file browser that can open any qgis supported format into qgis.
                             -------------------
begin                 :  2011-01-20
copyright             :  (C) 2011 by Nathan Woodrow
email                 :  woodrow.nathan@gmail.com
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
import os
from qgis.core import QgsVectorFileWriter

#Should find a better way to do this rather then using regex
#Needs to be refactored into different lists.
# Need to add these with correct regex
# Spatial Data Transfer Standard (*catd.ddf *CATD.DDF) :  "^.*\.(shp)$"
# X-Plane/Flightgear (apt.dat nav.dat fix.dat awy.dat APT.DAT NAV.DAT FIX.DAT AWY.DAT)" :  "^.*\.(shp)$"
filters = {
   '[Vector] ESRI Shapefiles (*.shp *.SHP)' : '^.*\.(shp)$',
   '[Vector] Mapinfo File (*.mif *.tab *.MIF *.TAB)' :  '^.*\.(mif|tab)$',
   '[Vector] S-57 Base file (*.000 *.000)' :  '^.*\.(000)$',
   '[Vector] Microstation DGN (*.dgn *.DGN)' :  '^.*\.(dgn)$',
   '[Vector] VRT - Virtual Datasource  (*.vrt *.VRT)' :  '^.*\.(vrt)$',
   '[Vector] Atlas BNA (*.bna *.BNA)' :  '^.*\.(bna)$',
   '[Vector] Comma Separated Value (*.csv *.CSV)' :  '^.*\.(csv)$',
   '[Vector] GeVectoraphy Markup Language (*.gml *.GML)' :  '^.*\.(gml)$',
   '[Vector] GPX (*.gpx *.GPX)' :  '^.*\.(gpx)$',
   '[Vector] KML (*.kml *.KML)' :  '^.*\.(kml)$',
   '[Vector] GeoJSON (*.geojson *.GEOJSON)' :  '^.*\.(geojson)$',
   '[Vector] INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI)' :  '^.*\.(itf|xml|ili)$',
   '[Vector] INTERLIS 2 (*.itf *.xml *.ili *.ITF *.XML *.ILI)' :  '^.*\.(itf|xml|ili)$',
   '[Vector] GMT (*.gmt *.GMT)' :  '^.*\.(gmt)$',
   '[Vector] SQLite (*.sqlite *.SQLITE)' :  '^.*\.(sqlite)$',
   '[Vector] ESRI Personal GeoDatabase (*.mdb *.MDB)' :  '^.*\.(mdb)$',
   '[Vector] Arc/Info ASCII Coverage (*.e00 *.E00)' :  '^.*\.(e00)$',
   '[Vector] AutoCAD DXF (*.dxf *.DXF)' :  '^.*\.(dxf)$',
   '[Vector] Geoconcept (*.gxt *.txt *.GXT *.TXT)' :  '^.*\.(gxt|txt)$',
   '[Vector] GeoRSS (*.xml *.XML)' :  '^.*\.(xml)$',
   '[Vector] QGIS Project File (*.qgs)'  : '^.*\.(qgs)$',
   'All supported files' :  '^.*\.(shp|mif|tab|000|dgn|vrt|bna|csv|gml|gpx|kml|geojson|itf|xml|ili|gmt|sqlite|mdb|e00|dxf|gxt|txt|xml|qgs|vrt|tiff|tif|ntf|toc|img|gff|asc|ddf|dt0|dt1|dt2|png|jpg|jpeg|mem|gif|n1|xpm|bmp|pix|map|mpr|mpl|rgb|hgt|ter|nc|grb|hdr|rda|bt|lcp|rik|dem|gxf|hdf5|grd|grc|gen|img|blx|blx|sqlite|sdat)$',
   'All vector files' :  '^.*\.(shp|mif|tab|000|dgn|vrt|bna|csv|gml|gpx|kml|geojson|itf|xml|ili|gmt|sqlite|mdb|e00|dxf|gxt|txt|xml)$',
   'All raster files' : '^.*\.(sid|ecw|vrt|tiff|tif|ntf|toc|img|gff|asc|ddf|dt0|dt1|dt2|png|jpg|jpeg|mem|gif|n1|xpm|bmp|pix|map|mpr|mpl|rgb|hgt|ter|nc|grb|hdr|rda|bt|lcp|rik|dem|gxf|hdf5|grd|grc|gen|img|blx|blx|sqlite|sdat)$',
   '[Raster] MrSID (*.sid)' : '^.*\.(sid)$',
   '[Raster] Enhanced Compression Wavelet (*.ecw)' : '^.*\.(ecw)$',
   '[Raster] Virtual Raster (*.vrt *.VRT)'  :  '^.*\.(vrt)$',
   '[Raster] GeoTIFF (*.tif *.tiff *.TIF *.TIFF)'  :  '^.*\.(tiff|tif)$',
   '[Raster] National Imagery Transmission Format (*.ntf *.NTF)'  :  '^.*\.(ntf)$',
   '[Raster] Raster Product Format TOC format (*.toc *.TOC)'  :  '^.*\.(toc)$',
   '[Raster] Erdas Imagine Images  (*.img *.IMG)'  :  '^.*\.(img)$',
   '[Raster] Ground-based SAR Applications Testbed File Format  (*.gff *.GFF)'  :  '^.*\.(gff)$',
   '[Raster] Arc/Info ASCII Grid (*.asc *.ASC)'  :  '^.*\.(asc)$',
   '[Raster] SDTS Raster (*.ddf *.DDF)'  :  '^.*\.(ddf)$',
   '[Raster] DTED Elevation Raster (*.dt0 *.dt1 *.dt2 *.DT0 *.DT1 *.DT2)'  :  '^.*\.(dt0|dt1|dt2)$',
   '[Raster] Portable Network Graphics (*.png *.PNG)'  :  '^.*\.(png)$',
   '[Raster] JPEG JFIF (*.jpg *.jpeg *.JPG *.JPEG)'  :  '^.*\.(jpg|jpeg)$',
   '[Raster] Japanese DEM  (*.mem *.MEM)'  :  '^.*\.(mem)$',
   '[Raster] Graphics Interchange Format  (*.gif *.GIF)'  :  '^.*\.(gif)$',
   '[Raster] Envisat Image Format (*.n1 *.N1)'  :  '^.*\.(n1)$',
   '[Raster] X11 PixMap Format (*.xpm *.XPM)'  :  '^.*\.(xpm)$',
   '[Raster] MS Windows Device Independent Bitmap (*.bmp *.BMP)'  :  '^.*\.(bmp)$',
   '[Raster] PCIDSK Database File (*.pix *.PIX)'  :  '^.*\.(pix)$',
   '[Raster] PCRaster Raster File (*.map *.MAP)'  :  '^.*\.(map)$',
   '[Raster] ILWIS Raster Map (*.mpr *.mpl *.MPR *.MPL)'  :  '^.*\.(mpr|mpl)$',
   '[Raster] SGI Image File Format 1.0 (*.rgb *.RGB)'  :  '^.*\.(rgb)$',
   '[Raster] SRTMHGT File Format (*.hgt *.HGT)'  :  '^.*\.(hgt)$',
   '[Raster] Leveller heightfield (*.ter *.TER)'  :  '^.*\.(ter)$',
   '[Raster] Terragen heightfield (*.ter *.TER)'  :  '^.*\.(ter)$',
   '[Raster] GMT NetCDF Grid Format (*.nc *.NC)'  :  '^.*\.(nc)$',
   '[Raster] Network Common Data Format (*.nc *.NC)'  :  '^.*\.(nc)$',
   '[Raster] GRIdded Binary  (*.grb *.GRB)'  :  '^.*\.(grb)$',
   '[Raster] Raster Matrix Format (*.rsw *.RSW)'  :  '^.*\.(rsw)$',
   '[Raster] EUMETSAT Archive native  (*.nat *.NAT)'  :  '^.*\.(nat)$',
   '[Raster] Idrisi Raster A.1 (*.rst *.RST)'  :  '^.*\.(rst)$',
   '[Raster] Golden Software ASCII Grid  (*.grd *.GRD)'  :  '^.*\.(grd)$',
   '[Raster] Golden Software Binary Grid  (*.grd *.GRD)'  :  '^.*\.(grd)$',
   '[Raster] Golden Software 7 Binary Grid  (*.grd *.GRD)'  :  '^.*\.(grd)$',
   '[Raster] DRDC COASP SAR Processor Raster (*.hdr *.HDR)'  :  '^.*\.(hdr)$',
   '[Raster] R Object Data Store (*.rda *.RDA)'  :  '^.*\.(rda)$',
   '[Raster] Portable Pixmap Format  (*.pnm *.PNM)'  :  '^.*\.(pnm)$',
   '[Raster] Vexcel MFF Raster (*.hdr *.HDR)'  :  '^.*\.(hdr)$',
   '[Raster] VTP .bt (Binary Terrain) 1.3 Format (*.bt *.BT)'  :  '^.*\.(bt)$',
   '[Raster] FARSITE v.4 Landscape File  (*.lcp *.LCP)'  :  '^.*\.(lcp)$',
   '[Raster] Swedish Grid RIK  (*.rik *.RIK)'  :  '^.*\.(rik)$',
   '[Raster] USGS Optional ASCII DEM  (*.dem *.DEM)'  :  '^.*\.(dem)$',
   '[Raster] GeoSoft Grid Exchange Format (*.gxf *.GXF)'  :  '^.*\.(gxf)$',
   '[Raster] Hierarchical Data Format Release 5 (*.hdf5 *.HDF5)'  :  '^.*\.(hdf5)$',
   '[Raster] Northwood Numeric Grid Format .grd/.tab (*.grd *.GRD)'  :  '^.*\.(grd)$',
   '[Raster] Northwood Classified Grid Format .grc/.tab (*.grc *.GRC)'  :  '^.*\.(grc)$',
   '[Raster] ARC Digitized Raster Graphics (*.gen *.GEN)'  :  '^.*\.(gen)$',
   '[Raster] Standard Raster Product  (*.img *.IMG)'  :  '^.*\.(img)$',
   '[Raster] Magellan topo  (*.blx *.BLX)'  :  '^.*\.(blx)$',
   '[Raster] Rasterlite (*.sqlite *.SQLITE)'  :  '^.*\.(sqlite)$',
   '[Raster] SAGA GIS Binary Grid  (*.sdat)'  :  '^.*\.(sdat)$'
  }


class QGISFileBrowserDialog(QDockWidget):
    #Signal notify when a file needs to be opened
    fileOpenRequest = pyqtSignal(QString)

    def __init__(self):
        QDockWidget.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_QGISFileBrowser()
        self.ui.setupUi(self)

        #Load the filter list
        for key in sorted(filters.iterkeys()):
            self.ui.filtercombobox.addItem(key)
            
        self.openFileAction = QAction("Open Layer",  self)
        self.openFileAction.triggered.connect(self.openFile)
        self.deleteFileAction = QAction("Delete Layer",  self)
        self.deleteFileAction.triggered.connect(self.deleteFile)

    def LoadFiles(self):
        self.model = QFileSystemModel(self.ui.fileTree)
        self.model.setRootPath(QDir.homePath())
        self.proxy = MyFilter()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(0)

        self.proxy.setFilterRegExp(QRegExp(filters[unicode(self.ui.filtercombobox.currentText())],Qt.CaseInsensitive,QRegExp.RegExp))

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

        self.ui.filtercombobox.currentIndexChanged[QString].connect(self.filterChanged)
        self.ui.fileTree.doubleClicked.connect(self.itemClicked)
        self.ui.fileTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.fileTree.customContextMenuRequested.connect(self.customContext)

    def filterChanged(self, text):
        self.proxy.setFilterRegExp(QRegExp(filters[str(text)],Qt.CaseInsensitive,QRegExp.RegExp))

    def itemClicked(self, item):
        index = item.model().mapToSource(item)
        filepath = unicode(self.model.filePath(index).toUtf8(),"utf-8")
        #We don't need to do anything if filepath is a directory.
        if os.path.isdir(filepath):
            return

        self.fileOpenRequest.emit(filepath)
        
    def openFile(self):
        index = self.ui.fileTree.currentIndex()
        self.itemClicked(index)
        
    def deleteFile(self):
        index = self.ui.fileTree.currentIndex()
        index = index.model().mapToSource(index)
        filepath = unicode(self.model.filePath(index).toUtf8(), "utf-8")
        if os.path.isdir(filepath):
            return
        else:
            # careful... maybe we should double check with the user?
            ok = QMessageBox.warning(self.ui.fileTree, "QGIS File Browser", 
            "Are you sure you want to \ndelete this layer and associated files?",
            QMessageBox.Yes|QMessageBox.Cancel)
            if ok == QMessageBox.Yes:
                if filepath.endswith(".shp"):
                    QgsVectorFileWriter.deleteShapeFile(filepath)
                else:
                    self.model.remove(index)

    def customContext(self, point):
        index = self.ui.fileTree.indexAt(point)
        # Don't show the menu if we don't have a vaild tree item. 
        if not index.isValid():
            return

        self.ui.fileTree.setCurrentIndex(index)

        menu = QMenu("Menu")
        menu.addAction(self.openFileAction)
        menu.addAction(self.deleteFileAction)
        menu.exec_(self.ui.fileTree.mapToGlobal(point))

    def updateFilter(self, text):
        self.proxy.setFilterRegExp(QRegExp(text,Qt.CaseInsensitive,QRegExp.RegExp))


class MyFilter(QSortFilterProxyModel):
    def __init__(self,parent=None):
        super(MyFilter, self).__init__(parent)

    def filterAcceptsRow (self, source_row, source_parent ):
        if self.filterRegExp() =="":
            return True #Shortcut for common case

        source_index = self.sourceModel().index(source_row, 0, source_parent)

        if self.sourceModel().isDir(source_index):
            return True

        return self.sourceModel().data(source_index).toString().contains(self.filterRegExp())

