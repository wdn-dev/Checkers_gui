# -*- coding: utf-8 -*-
#  @file        - chess_controller.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 国际跳棋逻辑控制类
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 

from chess_board import ChessBoard
from chess_state import ChessState, ChessPoint, ChessType

from PyQt5.QtCore import QObject, QPoint, pyqtSignal
from PyQt5 import QtCore

class CheckerType:
    """ 国际跳棋种类
    """
    CHECKER100 = 1,     # 国际跳棋100
    CHECKER64 = 2       # 国际跳棋64


class ChessController(QObject):
    """ 游戏控制类
    """

    """ 信号
    """
    state_change_signal = pyqtSignal(ChessState)
    game_end_signal = pyqtSignal(ChessType)
    start_thinking_signal = pyqtSignal()
    stop_thinking_signal = pyqtSignal()
    chess_list_change_signal = pyqtSignal(list)
    chess_list_del_signal = pyqtSignal()

    def __init__(self, checker_type:CheckerType, parent=None) -> None:
        super().__init__(parent)
        """ 初始化
            当 chess_size = 10, chess_row = 4 为国际跳棋 100；
            当 chess_size = 8, chess_row = 3 为国际跳棋 64；
        """
        self.chess_size = 0     # 棋盘格子数
        self.chess_row = 0      # 棋子行数
        self.checker_type = checker_type
        if checker_type == CheckerType.CHECKER100:
            self.chess_size = 10     # 棋盘格子数
            self.chess_row = 4      # 棋子行数
        else:
            self.chess_size = 8     # 棋盘格子数
            self.chess_row = 3      # 棋子行数

        self.rival_chess_color = ChessType.BLACK    # 对手棋子颜色
        self.my_chess_color = ChessType.WHITE       # 我方棋子颜色

        self.first_state = None     # 游戏初始状态
        self.curr_state= None      # 当前游戏状态

        # 定义方向
        self.ix = [None] * 4
        self.jx = [None] * 4
        self.gamerunning = False

        # 鼠标点击次数标志
        self.click_flag = 0

    def start_game(self, rival_chess_color):
        """ 游戏开始
        """
        self.rival_chess_color = rival_chess_color
        if self.rival_chess_color == ChessType.BLACK:
            self.my_chess_color = ChessType.WHITE
        else:
            self.my_chess_color = ChessType.BLACK
        self.first_state = ChessState(self.chess_size)
        for i in range(0, self.chess_size):
            for j in range(0, self.chess_row):
                if i%2 == j%2:
                    self.first_state.set_chess_type(i, j, ChessType.WHITE)
            for j in range(self.chess_size - self.chess_row, self.chess_size):
                if i%2 == j%2:
                    self.first_state.set_chess_type(i, j, ChessType.BLACK)
        
        if self.curr_state is not None:
            self.curr_state = None
        self.curr_state = self.first_state.copy()

        # 旁路的方向
        self.ix[0] = -1     # 左下
        self.ix[1] = 1      # 右下
        self.ix[2] = -1     # 左上
        self.ix[3] = 1      # 右上

        self.jx[0] = 1
        self.jx[1] = 1
        self.jx[2] = -1
        self.jx[3] = -1
        
        self.click_flag = 0
        self.gamerunning = True

        self.check_terminate_pos(self.curr_state)

        if self.rival_chess_color == ChessType.WHITE:
            pass
        else:
            self.state_change_signal.emit(self.curr_state)
            pass

    def end_game(self):
        """ 游戏结束
        """
        self.gamerunning = False
        if self.curr_state is not None:
            self.curr_state = None
        self.first_state = None

    def who_win(self, state:ChessState) -> ChessType:
        """ 判断输赢
        """
        if state.counts()[0] + state.counts()[1] == 0 or state.counts()[2] == 0:
            return ChessType.BLACK
        if state.counts()[4] + state.counts()[5] == 0 or state.counts()[6] == 0:
            return ChessType.WHITE

        return ChessType.GOON

    def _check_coord(self, coord) -> bool:
        """ 检查坐标是否正确
        """
        if coord >= 0 and coord < self.chess_size:
            return True
        return False

    def moves_count(self, state:ChessState, i:int, j:int):
        """ 计算棋子可移动的数
        """
        chess_color = state.color(i, j)
        move_num = 0        # 移动数量
        sidx = 0            # 方向：左
        eidx = 0            # 方向:右
        pidx = 1            # 方向上的移动数量
        if chess_color == ChessType.WHITE:
            # 方向为左下和右下
            sidx = 0
            eidx = 0
        if chess_color == ChessType.BLACK:
            # 方向为左上和右上
            sidx = 2
            eidx = 3
        if state.is_king(i, j):
            # 方向全激活，攻击距离全开
            sidx = 0
            eidx = 3
            pidx = self.chess_size
        
        for k in range(sidx, eidx+1):
            for pk in range(1, pidx+1):
                xi = i + pk * self.ix[k]
                xj = j + pk * self.jx[k]
                # 如果坐标超出棋盘则跳出该方向
                if self._check_coord(xi) == False or self._check_coord(xj) == False:
                    break
                # 如果该点没放棋子，moves加1，否则跳出该方向
                if state.is_empty(xi, xj):
                    move_num += 1
                else:
                    break
        
        for k in range(0, 4):
            capture_flag = False
            # 考虑捕获攻击距离要加1
            for pk in range(1, pidx+1+1):
                xi = i + pk * self.ix[k]
                xj = j + pk * self.jx[k]
                # 如果坐标超出棋盘则跳出该方向
                if self._check_coord(xi) == False or self._check_coord(xj) == False:
                    break
                # 如果预捕获为假而且无棋子，跳至该方向下一点
                if  not capture_flag and state.is_empty(xi, xj):
                    continue
                # 如果该点棋子颜色是本色或者该点属性为目标删除，则跳出该方向
                if state.color(xi, xj) == chess_color or state.color(xi, xj) == ChessType.MARKDELETED:
                    break
                # 如果预捕获为假且棋子颜色为反色，则标记预捕获，跳至该方向下一点
                if not capture_flag and state.color(xi, xj) != chess_color:
                    capture_flag = True
                    continue
                if capture_flag:
                    if state.is_empty(xi, xj):
                        capture_flag = False
                        break
                    move_num += 1

        return move_num

    def calc_chess_counts(self, state:ChessState):
        """ 统计各类棋子数目以及可移动数
        """
        state.clear_chess_counts()
        moves_num = 0
        for i in range(self.chess_size):
            for j in range(self.chess_size):
                # 如果是不能放棋子的点，直接跳过
                if i % 2 != j % 2:
                    continue
                moves_num = self.moves_count(state, i, j)
                if state.at(i, j) == ChessType.WHITE:
                    # 白色普通棋子个数
                    state.chess_counts[0] += 1
                    # 白方的移动数
                    state.chess_counts[2] += moves_num
                elif state.at(i, j) == ChessType.WHITEKING:
                    # 白色王棋的个数
                    state.chess_counts[1] += 1
                    state.chess_counts[2] += moves_num
                elif state.at(i, j) == ChessType.BLACK:
                    # 黑色普通棋子的个数
                    state.chess_counts[4] += 1
                    # 黑方的移动数
                    state.chess_counts[6] += moves_num
                elif state.at(i, j) == ChessType.BLACKKING:
                    # 黑色王棋的个数
                    state.chess_counts[5] += 1
                    state.chess_counts[6] += moves_num
                    
    def check_terminate_pos(self, state:ChessState)->bool:
        """ 判断是否达到最终节点
        """                 
        if len(state.chess_counts) != 0:
            self.calc_chess_counts(state)
        if state.chess_counts[0] + state.chess_counts[1] == 0   \
            or state.chess_counts[4] + state.chess_counts[5] == 0 :
            return True
        if state.chess_counts[2] == 0 or state.chess_counts[6] == 0:
            return True
        return False

    def move(self, p1:ChessPoint, p2:ChessPoint):
        """ 棋子移动
        """
        tmp_state = self.curr_state.copy()
        tmp_state.set_chess_type(p1.x, p1.y, ChessType.EMPTY)
        tmp_state.set_chess_type(p2.x, p2.y, p2.type)

        self.curr_state = tmp_state
        self.state_change_signal.emit(self.curr_state)
        self.stop_thinking_signal()

        if self.check_terminate_pos(self.curr_state):
            self.gamerunning = False
            self.game_end_signal.emit(self.who_win(self.curr_state))

    def change_state(self, state:ChessState):
        """ 棋子移动
        """
        self.curr_state = state
        self.state_change_signal.emit(self.curr_state)
        self.stop_thinking_signal()

        if self.check_terminate_pos(self.curr_state):
            self.gamerunning = False
            self.game_end_signal.emit(self.who_win(self.curr_state))

    def set_clicked_slot(self, i:int, j:int):
        """ 鼠标点击事件
        """
        print("recv: i:{}, j:{}".format(i, j))
        if i >= 0 and i < self.chess_size and j >= 0 and j < self.chess_size \
            and i % 2 == j % 2 and self.gamerunning:
            tmp_point = None
            if self.click_flag == 0:
                tmp_point = self.first_click(i, j)
            else :
                self.second_click(i, j, tmp_point)
        else:
            self.chess_list_del_signal.emit()
            self.click_flag = 0

    def first_click(self, i, j):
        """ 第一次点击鼠标
        """
        if self.rival_chess_color == self.curr_state.color(i, j):
            return ChessPoint(i, j, ChessType.MOVEDFROM)


    def second_click(self, i, j, point):
        """ 第二次点击鼠标
        """
        if self.curr_state.is_empty(i, j) and  point is not None \
            and point.x != i and point.y != j:
            self.move(point, ChessPoint(i, j, ChessType.MOVEDTO))
            


        

