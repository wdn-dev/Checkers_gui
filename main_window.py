# -*- coding: utf-8 -*-
#  @file        - main_window.py
#  @author      - dongnian.wang
#  @brief       - 界面主窗口
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QToolButton, QPlainTextEdit, QTextEdit, QMainWindow, QToolBar, QMenu
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, QSize, QDateTime, QTimer, pyqtSignal, QRect, QPoint, QTime
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor, QImage, QMouseEvent, QResizeEvent, QPainter

from chess_state import ChessState, ChessType
from chess_board import ChessBoard
from chess_controller import ChessController, CheckerType

from functools import partial

class MainWindow(QMainWindow):
    """ 主窗口类
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.window:ChessBoard
        self.my_chess_color:ChessType
        self.init_ui()

        # 改变此类的输入参数，切换跳棋类型
        self.game = ChessController(CheckerType.CHECKER64)

        self.window.mouse_clicked_signal.connect(partial(self.game.set_clicked_slot))
        self.game.state_change_signal.connect(partial(self.window.set_state_slot))
        self.game.state_change_signal.connect(partial(self.updata_chess_num))


        self.game.game_end_signal.connect(partial(self.game_ended))
        self.game.start_thinking_signal.connect(partial(self.window.start_thinking_slot))
        self.game.stop_thinking_signal.connect(partial(self.window.stop_thinking_slot))

        self.start_new_game_slot()


    def init_ui(self):
        # 窗口大小: 430*400
        self.resize(700, 780)                                   # 窗口大小: 430*400,  窗口可以随着内容自动变化长度
        self.setMinimumSize(QtCore.QSize(0, 0))                 # 窗口最小的大小
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))   # 窗口最大的大小
        # 窗口初始化
        self.setWindowTitle("国际跳棋")  # 窗口名称
        self.setWindowIcon(QIcon("res/icons/icon.png"))  # 窗口图标

        # 菜单栏设置
        self.menuBar = self.menuBar()
        game_menu = self.menuBar.addMenu("游戏")
        game_menu.addAction(QIcon("res/icons/icon1.png"), "新游戏", self.start_new_game_slot)
        game_menu.addAction(QIcon("res/icons/reset.png"), "重新开始", self.start_new_game_slot)
        game_menu.addAction(QIcon("res/icons/close.png"), "退出", self.gameover)

        setting_menu = self.menuBar.addMenu("设置")

        help_menu = self.menuBar.addMenu("帮助")
        help_menu.addAction(QIcon(""), "游戏规则")
        help_menu.addAction(QIcon(""), "关于")
        self.menuBar.addMenu(help_menu)
        
        # 工具栏设置
        lift_tool_bar = QToolBar(self)
        pointer_reset = QToolButton(self)
        pointer_reset.setIcon(QIcon("res/icons/icon.png"))
        pointer_reset.setToolTip("新游戏")
        pointer_reset2 = QToolButton(self)
        pointer_reset2.setIcon(QIcon("res/icons/setting.png"))
        pointer_reset2.setToolTip("设置")

        lift_tool_bar.addWidget(pointer_reset)
        lift_tool_bar.addWidget(pointer_reset2)
        lift_tool_bar.setAllowedAreas(Qt.ToolBarArea.LeftToolBarArea)
        self.addToolBar(lift_tool_bar)


        # 中央组件设置
        self.window = ChessBoard()
        # first = ChessState(10)
        # for i in range(0, 10):
        #     for j in range(0, 4):
        #         if i%2 == j%2:
        #             first.set_chess_type(i, j, ChessType.WHITE)
        #     for j in range(6, 10):
        #         if i%2 == j%2:
        #             first.set_chess_type(i, j, ChessType.BLACK)
        # self.window.set_state_slot(first)
        self.setCentralWidget(self.window)

        # 状态栏
        self.statusBar = self.statusBar()

        self.white_icon = QLabel()
        self.white_icon.setPixmap(QPixmap("res/icons/whitelabel.png"))
        self.statusBar.addWidget(self.white_icon)

        self.white_label = QLabel()
        self.statusBar.addWidget(self.white_label)

        self.black_icon = QLabel()
        self.black_icon.setPixmap(QPixmap("res/icons/blacklabel.png"))
        self.statusBar.addWidget(self.black_icon)

        self.black_label = QLabel()
        self.statusBar.addWidget(self.black_label)

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.statusBar.addWidget(self.spacer, 1)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.statusBar.addWidget(self.time_label)
        self.time_label.setStyleSheet("color: black;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.time_changed_slot)
        self.timer.start(1000)





        

    def time_changed_slot(self):
        """ 显示时间槽函数
        """
        self.time_label.setText(QTime.currentTime().toString("HH:mm:ss"))

    def start_new_game_slot(self):
        """ 开始新的游戏
        """
        self.my_chess_color = ChessType.WHITE
        rival_chess_color = None
        if self.my_chess_color == ChessType.WHITE:
            rival_chess_color = ChessType.BLACK
        else:
            rival_chess_color = ChessType.WHITE
        
        self.window.set_rival_chess_color(rival_chess_color)
        self.window.set_show_hour_glass(True)

        self.game.start_game(rival_chess_color)

    def updata_chess_num(self, state:ChessState):
        """ 更新棋子计数器
        """
        if len(state.chess_counts) != 0:
            white_num = state.counts()[0] + state.counts()[1]
            black_num = state.counts()[4] + state.counts()[5]
            self.white_label.setText("<b><font color=red>{}</font></b>".format(white_num))
            self.black_label.setText("<b><font color=red>{}</font></b>".format(black_num))

    def gameover(self):
        """ 程序结束
        """
        self.game.end_game
        self.window.stop_thinking_slot()
        self.close()
    
    def game_ended(self, win_color:ChessType):
        """ 游戏结束
        """
        string = None
        if win_color == self.my_chess_color:
            string = "我方胜利！ \n再来一局？"
        else:
            string = "对方胜利！ \n再来一局？"
        ret = QMessageBox.question(self, '结果', string, QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.start_new_game_slot()
        else:
            self.gameover()

from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtGui import QFontDatabase, QFont
def get_app_qss_str(qss_path) -> str:
    """ 从文件加载qss
    """
    qss_str = None
    qss = QFile(qss_path)
    if qss.open(QIODevice.OpenModeFlag.ReadOnly):
        qss_str = str(qss.readAll(), encoding= 'utf-8')
        qss.close()
    return qss_str
   
def get_app_font(font_path) -> QFont:
    """ 加载字体文件
    """
    font_str = None
    font_file = QFile(font_path)
    if not font_file.open(QIODevice.OpenModeFlag.ReadOnly):
        font_file.close()
        return None
    load_font_id = QFontDatabase.addApplicationFontFromData(font_file.readAll())
    load_font_families = QFontDatabase.applicationFontFamilies(load_font_id)
    if len(load_font_families) == 0:
        font_file.close()
        return None
    font_str = load_font_families[0]
    font_file.close()
    if font_str == "":
        return None
    return QFont(font_str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(get_app_qss_str("res/style/style.qss"))
    app.setFont(get_app_font("res/style/FZLTZHUNHJW.TTF"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())