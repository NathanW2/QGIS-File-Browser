# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgisfilebrowser.ui'
#
# Created: Tue Jan 25 15:22:55 2011
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
        self.fileTree = QtGui.QTreeView(self.dockWidgetContents)
        self.fileTree.setGeometry(QtCore.QRect(10, 50, 281, 701))
        self.fileTree.setObjectName("fileTree")
        self.plainTextEdit = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 281, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        QGISFileBrowser.setWidget(self.dockWidgetContents)

        self.retranslateUi(QGISFileBrowser)
        QtCore.QMetaObject.connectSlotsByName(QGISFileBrowser)

    def retranslateUi(self, QGISFileBrowser):
        QGISFileBrowser.setWindowTitle(QtGui.QApplication.translate("QGISFileBrowser", "QGISFileBrowser", None, QtGui.QApplication.UnicodeUTF8))

