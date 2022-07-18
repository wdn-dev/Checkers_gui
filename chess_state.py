# -*- coding: utf-8 -*-
#  @file        - chess_state.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 棋子状态类
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 

import copy
from enum import Enum

class ChessType(enumerate):
    """ 棋子类型
    """
    GOON = -1,                  # 未赢，继续下棋
    EMPTY = 0,                  # 没放棋子的格子, i%2 == j%2
    WHITE = 1,                  # 白棋
    BLACK = 2,                  # 黑棋
    WHITEKING = 3,              # 白王棋
    BLACKKING = 4,              # 黑王棋

    MOVEDFROM = 20,
    MOVEDTO = 21,
    MOVEDTHROUGH = 22,
    DELETED = 23,
    MARKDELETED = 24,
    TOKING = 25

class ChessPoint(object):
    """
        棋子坐标
    """
    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type
        

    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y and self.type == other.type :
            return True
        return False
    
    def get_point(self):
        return self.x, self.y, self.type

class ChessState(object):
    """
        棋子类
    """
    def __init__(self, size:int) -> None:
        self.chess_size = size
        self.chess_state = [[ChessType.EMPTY for n in range(int(self.chess_size))] for m in range(self.chess_size)]
        self.chess_counts = [0] * 8    # 不同类型棋子的数量，包括空棋 [白棋，白王棋，白棋可移动数，，黑棋， 黑王棋， 黑色棋子可移动数， ]
        # print(len(self.chess_state))
        # print(len(self.chess_state[2]))

    def size(self) -> int:
        return self.chess_size

    def counts(self):
        """ 返回不同类型棋子的数量，包括空棋
        """
        return self.chess_counts
    
    def clear_chess_counts(self):
        """ 清除所有棋子的数量
        """
        self.chess_counts.clear()
        self.chess_counts = [0] * 8

    def copy(self):
        """ 深拷贝
        """
        return copy.deepcopy(self)

    def gen_next_state(self, board:list):
        """ 生成走一步棋后的状态
        """
        state = ChessState()
        tmp_type = None
        for k in range(0, len(board)):
            i = board[k][0]
            j = board[k][1]
            if board[k][2] == ChessType.MOVEDFROM:
                tmp_type = state.at(i, j)
                state.set_chess_type(i, j, ChessType.EMPTY)
            elif board[k][2] == ChessType.MOVEDTO:
                state.set_chess_type(i, j, tmp_type)
            elif board[k][2] == ChessType.MARKDELETED:
                state.set_chess_type(i, j, ChessType.MARKDELETED)
            elif board[k][2] == ChessType.DELETED:
                state.set_chess_type(i, j, ChessType.EMPTY)
            elif board[k][2] == ChessType.TOKING:
                if tmp_type == ChessType.WHITE:
                    state.set_chess_type(i, j, ChessType.WHITEKING)
                if tmp_type == ChessType.BLACK:
                    state.set_chess_type(i, j, ChessType.BLACKKING)

        return state


    def set_chess_type(self, i:int, j:int, type:ChessType):
        self.chess_state[i][j] = type

    def at(self, i:int, j:int):
        """ 返回点的属性
        """
        if i % 2 == j % 2:
            return ChessType.EMPTY
        return self.chess_state[i][j]

    def color(self, i:int, j:int):
        """ 返回棋子颜色
        """
        if self.at(i, j) == ChessType.WHITE or self.at(i, j) == ChessType.WHITEKING:
            return ChessType.WHITE
        if self.at(i, j) == ChessType.BLACK or self.at(i, j) == ChessType.BLACKKING:
            return ChessType.BLACK
        return ChessType.EMPTY
    
    def is_white(self, i:int, j:int):
        """ 是否为白色棋子
        """
        if self.at(i, j) == ChessType.WHITE or self.at(i, j) == ChessType.WHITEKING:
            return True
        return False
    
    def is_black(self, i:int, j:int):
        """ 是否为黑色棋子
        """
        if self.at(i, j) == ChessType.BLACK or self.at(i, j) == ChessType.BLACKKING:
            return True
        return False

    def is_king(self, i:int, j:int):
        """ 是否为王棋
        """
        if self.at(i, j) == ChessType.BLACKKING or self.at(i, j) == ChessType.WHITEKING:
            return True
        return False
    
    def is_empty(self, i:int, j:int):
        """ 是否存在棋子
        """
        if self.at(i, j) == ChessType.EMPTY:
            return True
        return False


if __name__ == "__main__":
    
    checker_state = ChessState(10)
    print(checker_state.chess_state)
    print(checker_state.size())
    print(checker_state.at(1,1))
