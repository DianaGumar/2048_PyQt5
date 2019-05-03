import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Program(QWidget):
    def __init__(self, parent=None):
        super(Program, self).__init__(parent)
        self.setStyleSheet("background-color: white")

        self.initUI()

    def initUI(self):
        self.setGeometry(800, 150, 350, 500)
        self.show()

    def set_map(self, mx, my, value):
        if mx > -1 and mx < 4 and my > -1 and my < 4:
            map[mx][my] = value

    def exist_map(self,mx, my):
        if mx > -1 and mx < 4 and my > -1 and my < 4:
            return map[mx][my]

    # ex > -1 and ex < 4 and ey > -1 and ey < 4 and map[ex + sx][ey + sy] == 0
    def Turn(self, ex, ey, sx, sy):  # движение на одну клетку
        if map[ex][ey] > 0:
            while ex > -1 and ex < 4 and ey > -1 and ey < 4 and map[ex + sx][ey + sy] == 0:
                print(ex," ",ey)
                map[ex + sx][ey + sy] = map[ex][ey]
                map[ex][ey] = 0
                # self.set_map(ex + sx, ey + sy, map[ex][ey])
                # map[ex][ey] = 0

                ex -= sx
                ey -= sy


    def kliked(self, k):
        global map
        if k == -1:
            print('left')
            for ey in range(4):
                for ex in range(1, 4):
                    self.Turn(ex, ey, -1, 0)
            self.random_new_numbers()

        elif k == 1:
            print('right')
            for ey in range(4):
                for ex in range(2, -1, -1):
                    self.Turn(ex, ey, 1, 0)
            self.random_new_numbers()

        elif k == 2:
            print('up')
            for ex in range(4):
                for ey in range(1, 4):
                    self.Turn(ex, ey, 0, -1)
            self.random_new_numbers()

        elif k == 0:
            print('down')
            for ex in range(4):
                for ey in range(2, -1, -1):
                    self.Turn(ex, ey, 0, 1)
            self.random_new_numbers()

        self.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            self.kliked(-1)
        elif e.key() == Qt.Key_Right:
            self.kliked(1)
        elif e.key() == Qt.Key_Down:
            self.kliked(0)
        elif e.key() == Qt.Key_Up:
            self.kliked(2)

    def paintEvent(self, event):
        qp = QPainter()
        qp.setRenderHint(QPainter.Antialiasing)

        qp.begin(self)
        pen = QPen(QColor('#34486a'))
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', 30))
        for ex in range(4):
            for ey in range(4):
                qp.fillRect(ex*x*1.2+x, ey*x*1.2+x, x, x, QBrush(QColor(color[int(map[ex][ey]/2)])))  # несовершенно
                qp.drawText(ex*x*1.2+x, ey*x*1.2+x, x, x, Qt.AlignHCenter | Qt.AlignVCenter, str(map[ex][ey]))
        qp.end()


    def random_new_numbers(self):
        what_times = 0
        for i in range(50):
            eex = random.randrange(0, 4)
            eey = random.randrange(0, 4)
            if map[eex][eey] == 0:
                map[eex][eey] = random.choice((2, 2, 4))
                what_times += 1
            if what_times == 1:
                break


color = ['#f6f4f5', '#d7ddea', '#cad877']
x = 53
map = [[0 for i in range(4)] for ii in range(4)]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    sys.exit(app.exec_())
