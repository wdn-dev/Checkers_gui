# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\05Code\ComputerGames\surakarta_gui\ui\main_window2.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(737, 516)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.game_board_widget = QtWidgets.QWidget(self.centralwidget)
        self.game_board_widget.setGeometry(QtCore.QRect(0, 0, 470, 470))
        self.game_board_widget.setObjectName("game_board_widget")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(480, 0, 261, 471))
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.black_time_label = QtWidgets.QLabel(self.widget_2)
        self.black_time_label.setObjectName("black_time_label")
        self.horizontalLayout.addWidget(self.black_time_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.red_time_label = QtWidgets.QLabel(self.widget_2)
        self.red_time_label.setObjectName("red_time_label")
        self.horizontalLayout_2.addWidget(self.red_time_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.log_text_browser = QtWidgets.QTextBrowser(self.widget_2)
        self.log_text_browser.setObjectName("log_text_browser")
        self.gridLayout.addWidget(self.log_text_browser, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 737, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.game_rule_act = QtWidgets.QAction(MainWindow)
        self.game_rule_act.setObjectName("game_rule_act")
        self.game_about_act = QtWidgets.QAction(MainWindow)
        self.game_about_act.setObjectName("game_about_act")
        self.new_game_act = QtWidgets.QAction(MainWindow)
        self.new_game_act.setObjectName("new_game_act")
        self.quit_game_act = QtWidgets.QAction(MainWindow)
        self.quit_game_act.setObjectName("quit_game_act")
        self.game_setting_act = QtWidgets.QAction(MainWindow)
        self.game_setting_act.setObjectName("game_setting_act")
        self.menu.addAction(self.new_game_act)
        self.menu.addAction(self.quit_game_act)
        self.menu_2.addAction(self.game_setting_act)
        self.menu_3.addAction(self.game_rule_act)
        self.menu_3.addAction(self.game_about_act)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "???????????????    "))
        self.black_time_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "???????????????    "))
        self.red_time_label.setText(_translate("MainWindow", "TextLabel"))
        self.menu.setTitle(_translate("MainWindow", "??????"))
        self.menu_2.setTitle(_translate("MainWindow", "??????"))
        self.menu_3.setTitle(_translate("MainWindow", "??????"))
        self.game_rule_act.setText(_translate("MainWindow", "????????????"))
        self.game_about_act.setText(_translate("MainWindow", "??????"))
        self.new_game_act.setText(_translate("MainWindow", "?????????"))
        self.quit_game_act.setText(_translate("MainWindow", "??????"))
        self.game_setting_act.setText(_translate("MainWindow", "????????????"))
