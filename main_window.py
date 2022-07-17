# -*- coding: utf-8 -*-
#  @file        - main_window.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 界面主窗口
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 


from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QToolButton, QPlainTextEdit, QTextEdit, QMainWindow, QToolBar, QMenu
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, QSize, QDateTime, QTimer, pyqtSignal, QRect, QPoint, QTime, pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor, QImage, QMouseEvent, QResizeEvent, QPainter

from PyQt5 import uic
from functools import partial

from chess_state import ChessState, ChessType
from chess_board import ChessBoard
from chess_controller import ChessController, CheckerType

# 导入ui
from ui.main_windows_ui import Ui_MainWindow
from ui.rule_show_ui import Ui_ChessRule

class GameRule(Ui_ChessRule, QWidget):
    """ 游戏规则界面
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("游戏规则")

class MainWindow(Ui_MainWindow, QMainWindow):
    """ 主窗口类
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setupUi(self)

        self.setWindowTitle("国际跳棋")  # 窗口名称
        self.setWindowIcon(QIcon("res/icons/icon.png"))  # 窗口图标

        # 工具栏设置
        tool_new_game = QToolButton(self)
        tool_new_game.setIcon(QIcon("res/icons/icon.png"))
        tool_new_game.setToolTip("新游戏")
        tool_setting = QToolButton(self)
        tool_setting.setIcon(QIcon("res/icons/setting.png"))
        tool_setting.setToolTip("设置")
        tool_rule = QToolButton(self)
        tool_rule.setIcon(QIcon("res/icons/setting.png"))
        tool_rule.setToolTip("规则")
        tool_rule.clicked.connect(self.game_rule)
        tool_test = QToolButton(self)
        tool_test.setIcon(QIcon("res/icons/setting.png"))
        tool_test.setToolTip("测试")
        tool_test.clicked.connect(self.chess_state_test)
        tool_test2 = QToolButton(self)
        tool_test2.setIcon(QIcon("res/icons/setting.png"))
        tool_test2.setToolTip("测试2")
        tool_test2.clicked.connect(self.chess_state_test2)

        self.toolBar.addWidget(tool_new_game)
        self.toolBar.addWidget(tool_setting)
        self.toolBar.addWidget(tool_rule)
        self.toolBar.addWidget(tool_test)
        self.toolBar.addWidget(tool_test2)

        # 状态栏
        self.white_icon = QLabel()
        self.white_icon.setPixmap(QPixmap("res/icons/whitelabel.png"))
        self.statusbar.addWidget(self.white_icon)

        self.white_label = QLabel()
        self.statusbar.addWidget(self.white_label)

        self.black_icon = QLabel()
        self.black_icon.setPixmap(QPixmap("res/icons/blacklabel.png"))
        self.statusbar.addWidget(self.black_icon)

        self.black_label = QLabel()
        self.statusbar.addWidget(self.black_label)

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.statusbar.addWidget(self.spacer, 1)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.statusbar.addWidget(self.time_label)
        self.time_label.setStyleSheet("color: black;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.time_changed_slot)
        self.timer.start(1000)
        self.red_time_label.setText("00:00")
        self.red_time_label.setStyleSheet("color: red")

        self.black_time_label.setText("00:00")
        self.black_time_label.setStyleSheet("color: black")

        # 信号连接
        self.game_rule_act.triggered.connect(self.game_rule)

        
        

        # # 改变此类的输入参数，切换跳棋类型
        self.game = ChessController(CheckerType.CHECKER100)

        # self.game_board.mouse_clicked_signal.connect(partial(self.game.set_clicked_slot))
        self.game.state_change_signal.connect(partial(self.game_board.set_state_slot))
        # self.game.state_change_signal.connect(partial(self.updata_chess_num))

        # self.game.game_end_signal.connect(partial(self.game_ended))
        # self.game.start_thinking_signal.connect(partial(self.game_board.start_thinking_slot))
        # self.game.stop_thinking_signal.connect(partial(self.game_board.stop_thinking_slot))

        self.start_new_game_slot()

        self.pushButton_regret.clicked.connect(self.game.regret_chess_slot)
        
    @pyqtSlot()
    def time_changed_slot(self):
        """ 显示时间槽函数
        """
        self.time_label.setText(QTime.currentTime().toString("HH:mm:ss"))

    @pyqtSlot()
    def start_new_game_slot(self):
        """ 开始新的游戏
        """
        self.my_chess_color = ChessType.WHITE
        rival_chess_color = None
        if self.my_chess_color == ChessType.WHITE:
            rival_chess_color = ChessType.BLACK
        else:
            rival_chess_color = ChessType.WHITE
        
        self.game_board.set_rival_chess_color(rival_chess_color)
        self.game_board.set_show_hour_glass(True)

        self.game.start_game(rival_chess_color)

    @pyqtSlot()
    def updata_chess_num(self, state:ChessState):
        """ 更新棋子计数器
        """
        if len(state.chess_counts) != 0:
            white_num = state.counts()[0] + state.counts()[1]
            black_num = state.counts()[4] + state.counts()[5]
            self.white_label.setText("<b><font color=red>{}</font></b>".format(white_num))
            self.black_label.setText("<b><font color=red>{}</font></b>".format(black_num))

    @pyqtSlot()
    def gameover(self):
        """ 程序结束
        """
        self.game.end_game
        self.game_board.stop_thinking_slot()
        self.close()

    @pyqtSlot()
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

    @pyqtSlot()
    def game_rule(self):
        """ 游戏规则槽函数
        """
        self.rule_ui = GameRule()
        rule_str = open("res/checkers_rule3.html" ,'r', encoding='utf-8').read()
        self.rule_ui.textBrowser.setText(rule_str)
        self.rule_ui.pushButton.clicked.connect(lambda:self.rule_ui.close())

        self.rule_ui.show()

    @pyqtSlot()
    def chess_state_test(self):
        """ 游戏规则槽函数
        """
        # test_state = ChessState(10)
        # for i in range(0, 10):
        #     for j in range(0, 10):
        #         if i%2 == j%2:
        #             test_state.set_chess_type(i, j, ChessType.WHITE)
        #     for j in range(6, 10):
        #         if i%2 == j%2:
        #             test_state.set_chess_type(i, j, ChessType.BLACK)
        test_state = self.game.curr_state
        i, j = self.game.row_col_to_pix(5, 2)
        test_state.set_chess_type(i, j, ChessType.WHITE)
        i, j = self.game.row_col_to_pix(6, 1)
        test_state.set_chess_type(i, j, ChessType.EMPTY)
        self.game.change_state(test_state)
        # pass
    @pyqtSlot()
    def chess_state_test2(self):
        """ 游戏规则槽函数
        """
        test_state = self.game.first_state.copy()
        # test_state = self.game.curr_state
        # i, j = self.game.row_col_to_pix(5, 2)
        # test_state.set_chess_type(i, j, ChessType.WHITE)
        # i, j = self.game.row_col_to_pix(6, 1)
        # test_state.set_chess_type(i, j, ChessType.EMPTY)
        self.game.change_state(test_state)

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
    import sys
    app = QApplication(sys.argv)
    # app.setStyleSheet(get_app_qss_str("res/style/style.qss"))
    # app.setFont(get_app_font("res/style/FZLTZHUNHJW.TTF"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())