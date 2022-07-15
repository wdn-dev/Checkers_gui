# -*- coding: utf-8 -*-
#  @file        - chess_board.py
#  @author      - dongnian.wang
#  @brief       - 国际跳棋棋盘类
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 

from copy import deepcopy
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QPlainTextEdit, QTextEdit, QMainWindow
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, QSize, QDateTime, QTimer, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor, QImage, QMouseEvent, QResizeEvent, QPainter, QPen, QBrush
from numpy import double

from chess_state import ChessState, ChessType

class ChessBoard(QWidget):
    """ 棋盘类
    """

    """ 信号
    """
    mouse_clicked_signal = pyqtSignal(int, int)
    def __init__(self):
        super().__init__()

        # init
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Light, QColor(0x4c,0x7a,0x79, 200))
        self.setPalette(pal)
        self.setBackgroundRole(QPalette.ColorRole.Light)
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)

        self.zoom = 16
        self.chess_size = 10             # 棋盘大小
        self.thinking = False
        self.show_hour_glass = False
        self.hour_glass = QImage("res/icons/hourglass.png")

        self.setMinimumSize(self.zoom * (self.chess_size + 1), self.zoom * (self.chess_size + 1))

        self.curr_state = None          # 当前棋盘状态
        self.rival_chess_color = None
        self.chess_list = []           # 棋子集合
        self.base_point = QPoint(0, 0)        # 棋盘的原点
        self.side = 0                   # 棋盘边长

    def copy(self):
        return deepcopy(self)


    def state(self) -> ChessState:
        """ 返回现在的状态
        """
        return self.curr_state

    def set_rival_chess_color(self, color: ChessType):
        """ 设置对手棋子颜色
        """
        self.rival_chess_color = color

    def set_show_hour_glass(self, show_flag:bool):
        """ 设置显示标志位
        """
        self.show_hour_glass = show_flag

    def set_state_slot(self, state:ChessState):
        """ 设置棋局状态
        """
        # print(state.size())
        if state != None:
            self.curr_state = state
            # print(state.size())
            self.chess_size = state.size()
            self.chess_list.clear()
            self.repaint()
        else :
            self.clear()

    def set_chess_size_slot(self, size):
        """ 设置棋盘大小
        """
        self.chess_size = size
    
    def del_chess_set_slot(self):
        """ 清除点集
        """
        if len(self.chess_list) != 0:
            self.chess_list.clear()
            self.update()
    
    def set_chess_set_slot(self, chess_list:list):
        """ 设置点集
        """
        self.chess_list = chess_list
        self.update()

    def clear_slot(self):
        """ 清除点集和当前状态
        """
        self.curr_state = None
        self.chess_list.clear()
        self.update()

    def start_thinking_slot(self):
        """ 开始思考
        """
        self.thinking = True
        self.repaint()

    def stop_thinking_slot(self):
        """ 停止思考
        """
        self.thinking = False
        self.repaint()

    def mousePressEvent(self, event:QMouseEvent) -> None:
        """ 左击鼠标事件
        """
        if event.button() == Qt.LeftButton: 
            # print("base_point: ", self.base_point)
            # print("event.pos:", event.pos())
            # print("self.chess_size:", self.chess_size)
            # print("aaaaaaaa: ", (event.pos().y() - self.base_point.y()) * (self.chess_size) / self.side)
            i = int((event.pos().x() - self.base_point.x()) * (self.chess_size) / self.side)
            j = int(self.chess_size - int((event.pos().y() - self.base_point.y()) * (self.chess_size) / self.side) - 1)
            print("i: {}, j: {}".format(i, j))
            # self.mouse_clicked_signal.emit(int(1),int(1))
            if(self.rival_chess_color == ChessType.BLACK):
                self.mouse_clicked_signal.emit(int(i), int(j))
            else :
                self.mouse_clicked_signal.emit(self.chess_size - 1 - int(i), self.chess_size - 1 - int(j))

    def paintEvent(self, event:QMouseEvent) -> None:
        """ 绘制棋盘
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setViewport(self.base_point.x(), self.base_point.y(), self.side, self.side)
        painter.setWindow(0, 0, self.zoom * (self.chess_size), self.zoom * (self.chess_size))

        dark = QColor(0xcc,0xcc,0xcc,200)           # 终点颜色
        end_color = QColor(0x78,0xff,0x21,200)      # 起点颜色
        start_color = QColor(0xea,0x76,0x0f,200)   # 捕获颜色
        captured_color = QColor(0xed,0x50,0x62,200) # 正常色
        normal_color = QColor(0xd6,0xb8,0x2c,200)
        black = QColor(0x00, 0x00, 0x00, 200)
        white = QColor(0xff, 0xff, 0xff, 220)
        light = QColor(0xed,0xfc,0xdf,200)
        deep = QColor(0x5a,0x61,0x54,200)

        # 绘制棋盘
        # print(self.chess_size)
        for i in range(0, self.chess_size):
            for j in range(0, self.chess_size):
                rect = self._pixe_rect(i, j)
                if (i+j%2)%2 == 0:
                    painter.fillRect(rect, deep)
                else:
                    painter.fillRect(rect, light)
        ix = 0
        jx = 0
        if len(self.chess_list) != 0:
            tmp_type = None
            for i in range(0, len(self.chess_list)):
                if self.rival_chess_color == ChessType.WHITE:
                    ix = self.chess_size - 1 - self.chess_list[i].x
                    jx = self.chess_size - 1 - self.chess_list[i].y
                else:
                    ix = self.chess_list[i].x
                    jx = self.chess_list[i].y
                rect = self._pixe_rect(ix, jx)
                tmp_type = self.chess_list[i].type
                if tmp_type == ChessType.MOVEDFROM:
                    painter.fillRect(rect, start_color)
                elif tmp_type == ChessType.MOVEDTO or tmp_type == ChessType.TOKING:
                    painter.fillRect(rect, end_color)
                elif tmp_type == ChessType.MOVEDTHROUGH:
                    painter.fillRect(rect, normal_color)
                elif tmp_type == ChessType.DELETED:
                    painter.fillRect(rect, captured_color)

        s = self.zoom * 0.4
        sd = self.zoom * 0.3
        # 如果棋局状态发生了改变
        if self.curr_state is not None:
            painter.setPen(QPen(black, self.zoom * 0.025))
            # 画白棋, 白色则从最后一行开始画
            painter.setBrush(QBrush(white))
            for i in range(0, self.chess_size):
                for j in range(0, self.chess_size):
                    if self.rival_chess_color == ChessType.WHITE:
                        ix = self.chess_size - 1
                        jx = j + 1
                    else:
                        ix = i + 1
                        jx = self.chess_size - j
                    if self.curr_state.at(i, j) == ChessType.WHITE:
                        painter.drawEllipse(QPoint(self.zoom*(ix-0.5), self.zoom*(jx-0.5)), s, s)
                    if self.curr_state.at(i, j) == ChessType.WHITEKING:
                        painter.drawEllipse(QPoint(self.zoom*(ix-0.5), self.zoom*(jx-0.5)), s, s)
                        painter.drawEllipse(QPoint(self.zoom*(ix-0.5), self.zoom*(jx-0.5)), sd, sd)

            # 画黑棋
            painter.setBrush(QBrush(black))
            for i in range(0, self.chess_size):
                for j in range(0, self.chess_size):
                    if self.rival_chess_color == ChessType.WHITE:
                        ix = self.chess_size - 1
                        jx = j + 1
                    else:
                        ix = i + 1
                        jx = self.chess_size - j
                    if self.curr_state.at(i, j) == ChessType.BLACK:
                        painter.drawEllipse(QPoint(self.zoom*(ix-0.5), self.zoom*(jx-0.5)), s, s)
                    if self.curr_state.at(i, j) == ChessType.BLACKKING:
                        painter.drawEllipse(QPoint(self.zoom*(ix-0.5), self.zoom*(jx-0.5)), s, s)
                        painter.drawEllipse(QPoint(self.zoom*(ix-0.5), self.zoom*(jx-0.5)), sd, sd)

        if self.thinking and self.show_hour_glass:
            painter.setWindow(painter.viewport())
            painter.drawImage(self.width() - self.hour_glass.width() / 2,
                              self.height() - self.hour_glass.height() / 2,
                              self.hour_glass)


    def resizeEvent(self, event:QResizeEvent) -> None:
        """ 拖动改变大小
        """
        if event.oldSize() != event.size():
            self.update()
            self.side = min(self.width(), self.height())
            # print("w:{},h:{}, side:{}".format(self.width(), self.height(), self.side))
            self.base_point = QPoint((self.width() - self.side) / 2, (self.height() - self.side) / 2)
            # print("222base_point: ", self.base_point)
            self.hour_glass = QImage("res/icons/hourglass.png")
        else:
            event.ignore()

    def _pixe_rect(self, i:int, j:int):
        """ 返回一个矩形
        """
        return QRect(self.zoom * (i - 0.5) + self.zoom * 0.5, 
                     self.zoom * (self.chess_size - 1.0) - self.zoom * j,
                     self.zoom,
                     self.zoom)






# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     # window = MainWindow()
#     # window.show()

#     sys.exit(app.exec_())