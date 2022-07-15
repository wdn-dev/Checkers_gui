# 1.简介

使用PyQt5开发国际跳棋界面

# 2.环境

- PyQt5

# 3.运行

主窗口类中，实例化`ChessController`类时，传入不同的参数，可切换国跳100和国跳64

## 国跳100

```python
self.game = ChessController(CheckerType.CHECKER100)
```

## 国跳64

```python
self.game = ChessController(CheckerType.CHECKER64)
```
