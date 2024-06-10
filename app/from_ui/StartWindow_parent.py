# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\python\aspirantura_map\app\ui\start_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(974, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.main_tab = QtWidgets.QWidget()
        self.main_tab.setObjectName("main_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.main_tab)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(False)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.LE_file_path = QtWidgets.QLineEdit(self.main_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LE_file_path.sizePolicy().hasHeightForWidth())
        self.LE_file_path.setSizePolicy(sizePolicy)
        self.LE_file_path.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.LE_file_path.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.LE_file_path.setObjectName("LE_file_path")
        self.horizontalLayout_2.addWidget(self.LE_file_path)
        self.PB_open_file = QtWidgets.QPushButton(self.main_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PB_open_file.sizePolicy().hasHeightForWidth())
        self.PB_open_file.setSizePolicy(sizePolicy)
        self.PB_open_file.setObjectName("PB_open_file")
        self.horizontalLayout_2.addWidget(self.PB_open_file)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.widget = QtWidgets.QWidget(self.main_tab)
        self.widget.setMinimumSize(QtCore.QSize(0, 500))
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.TE_warning = QtWidgets.QTextEdit(self.main_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TE_warning.sizePolicy().hasHeightForWidth())
        self.TE_warning.setSizePolicy(sizePolicy)
        self.TE_warning.setMaximumSize(QtCore.QSize(16777215, 50))
        self.TE_warning.setObjectName("TE_warning")
        self.verticalLayout.addWidget(self.TE_warning)
        self.tabWidget.addTab(self.main_tab, "")
        self.map_tab = QtWidgets.QWidget()
        self.map_tab.setObjectName("map_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.map_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.PB_show_by_year = QtWidgets.QPushButton(self.map_tab)
        self.PB_show_by_year.setMaximumSize(QtCore.QSize(920, 30))
        self.PB_show_by_year.setObjectName("PB_show_by_year")
        self.horizontalLayout_3.addWidget(self.PB_show_by_year)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.map_tab, "")
        self.horizontalLayout_9.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "File path"))
        self.PB_open_file.setText(_translate("MainWindow", "Open"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_tab), _translate("MainWindow", "Main"))
        self.PB_show_by_year.setText(_translate("MainWindow", "Show"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.map_tab), _translate("MainWindow", "Map"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
