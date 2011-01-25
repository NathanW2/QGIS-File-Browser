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

class QGISFileBrowserDialog(QDockWidget):
  def __init__(self):
    QDockWidget.__init__(self)
    # Set up the user interface from Designer.
    self.ui = Ui_QGISFileBrowser()
    self.ui.setupUi(self)

  def LoadFiles(self):
    self.model = QFileSystemModel(self.ui.fileTree)
    self.model.setRootPath(QDir.homePath())
    self.proxy = MyFilter()
    self.proxy.setSourceModel(self.model)
    self.proxy.setFilterKeyColumn(0)
    filter = "^.*\.(tab|shp)$"
    self.ui.filterText.setText(filter)
    self.proxy.setFilterRegExp(QRegExp(filter,Qt.CaseInsensitive,QRegExp.RegExp))

    self.ui.fileTree.setModel(self.proxy)
    self.ui.fileTree.hideColumn(1)
    self.ui.fileTree.hideColumn(2)
    self.ui.fileTree.hideColumn(3)
    
    self.connect(self.ui.filterText,SIGNAL("textChanged( const QString &)"),self.updateFilter)
    self.connect(self.ui.fileTree,SIGNAL("doubleClicked( const QModelIndex &)"), self.itemClicked)

  def itemClicked(self, item):
    index = item.model().mapToSource(item)
    print self.model.filePath(index)

  def updateFilter(self, text):
    self.proxy.setFilterRegExp(QRegExp(text,Qt.CaseInsensitive,QRegExp.RegExp))

class MyFilter(QSortFilterProxyModel):
    def __init__(self,parent=None):
        super(MyFilter, self).__init__(parent)

    def filterAcceptsRow (self, source_row, source_parent ):
        if self.filterRegExp() == "" :
            return True #Shortcut for common case

        source_index = self.sourceModel().index(source_row, 0, source_parent)

        if self.sourceModel().isDir(source_index):
            return True

        return self.sourceModel().data(source_index).toString().contains(self.filterRegExp())


