# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgisfilebrowser.ui'
#
# Created: Thu Jan 27 09:57:45 2011
#      by: PyQt4 UI code generator 4.5.2
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.filtercombobox = QtGui.QComboBox(self.dockWidgetContents)
        self.filtercombobox.setAutoFillBackground(False)
        self.filtercombobox.setObjectName("filtercombobox")
        self.horizontalLayout.addWidget(self.filtercombobox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.fileTree = QtGui.QTreeView(self.dockWidgetContents)
        self.fileTree.setObjectName("fileTree")
        self.verticalLayout.addWidget(self.fileTree)
        QGISFileBrowser.setWidget(self.dockWidgetContents)

        self.retranslateUi(QGISFileBrowser)
        QtCore.QMetaObject.connectSlotsByName(QGISFileBrowser)

    def retranslateUi(self, QGISFileBrowser):
        QGISFileBrowser.setWindowTitle(QtGui.QApplication.translate("QGISFileBrowser", "File Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("QGISFileBrowser", "Filter", None, QtGui.QApplication.UnicodeUTF8))

