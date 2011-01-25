# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgisfilebrowser.ui'
#
# Created: Wed Jan 26 01:06:24 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QGISFileBrowser(object):
    def setupUi(self, QGISFileBrowser):
        QGISFileBrowser.setObjectName("QGISFileBrowser")
        QGISFileBrowser.resize(300, 777)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(4, 9, -1, 7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filterText = QtGui.QLineEdit(self.dockWidgetContents)
        self.filterText.setObjectName("filterText")
        self.verticalLayout.addWidget(self.filterText)
        self.fileTree = QtGui.QTreeView(self.dockWidgetContents)
        self.fileTree.setObjectName("fileTree")
        self.verticalLayout.addWidget(self.fileTree)
        QGISFileBrowser.setWidget(self.dockWidgetContents)

        self.retranslateUi(QGISFileBrowser)
        QtCore.QMetaObject.connectSlotsByName(QGISFileBrowser)

    def retranslateUi(self, QGISFileBrowser):
        QGISFileBrowser.setWindowTitle(QtGui.QApplication.translate("QGISFileBrowser", "File Browser", None, QtGui.QApplication.UnicodeUTF8))

