import sys
import random
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Program(QWidget):
    def __init__(self, parent=None):
        super(Program, self).__init__(parent)
        self.setStyleSheet("background-color: white")

        self.Game_over = 0
        self.init_ui()

    def init_ui(self):
        # self.setGeometry(800, 150, 350, 500)
        self.setFixedSize(350, 500)
        self.setWindowTitle("PyQt5_2048")
        # self.setWindowOpacity(0.9)
        self.show()

    def set_map(self, mx, my, value):
        if self.exist_map(mx, my):
            _map[mx][my] = value

    def get_map(self, mx, my):
        if self.exist_map(mx, my):
            return _map[mx][my]
        return -1

    @staticmethod
    def exist_map(mx, my):
        return 0 <= mx < _size and 0 <= my < _size

    def turn(self, ex, ey, sx, sy):  # движение на одну клетку

        if self.get_map(ex, ey) > 0:
            while self.get_map(ex + sx, ey + sy) == 0:
                _map[ex + sx][ey + sy] = self.get_map(ex, ey)
                _map[ex][ey] = 0

                ex += sx
                ey += sy
                self.moved = 1

    def join(self, ex, ey, sx, sy):
        global _bill
        if self.get_map(ex, ey) > 0:
            if self.get_map(ex + sx, ey + sy) == self.get_map(ex, ey):
                self.set_map(ex + sx, ey + sy, self.get_map(ex, ey) << 1)  # сдвигаем на битовую еденицу влево
                _bill[1] += self.get_map(ex, ey) << 1  # увеличение счёта
                while self.get_map(ex - sx, ey - sy) > 0:
                    # устанавливаем значение предыдущего в текущий
                    self.set_map(ex, ey, self.get_map(ex - sx, ey - sy))
                    ex -= sx
                    ey -= sy
                self.set_map(ex, ey, 0)
                self.moved = 1

    global moved

    def game_over(self):
        for ex in range(_size):
            for ey in range(_size):
                if self.get_map(ex, ey) == 0:
                    return 0
        for ex in range(_size):
            for ey in range(_size):
                if self.get_map(ex, ey) == self.get_map(ex + 1, ey) or self.get_map(ex, ey) == self.get_map(ex, ey + 1):
                    return 0
        return 1

    def clicked(self, k):
        global _map
        if k == -1:
            sys.stdout.write('\rleft')
            self.moved = 0
            for ey in range(_size):
                for ex in range(-1, _size):
                    self.turn(ex, ey, -1, 0)
                for ex in range(-1, _size):
                    self.join(ex, ey, -1, 0)
            if self.moved == 1:
                self.random_new_numbers()

        elif k == 2:
            sys.stdout.write('\rup')
            self.moved = 0
            for ex in range(_size):
                for ey in range(-1, _size):
                    self.turn(ex, ey, 0, -1)
                for ey in range(-1, _size):
                    self.join(ex, ey, 0, -1)
            if self.moved == 1:
                self.random_new_numbers()

        elif k == 1:
            sys.stdout.write('\rright')
            self.moved = 0
            # sys.stdout.write(str(bin(map[1][1])))
            for ey in range(_size):
                for ex in range(2, -1, -1):
                    self.turn(ex, ey, 1, 0)
                for ex in range(2, -1, -1):
                    self.join(ex, ey, 1, 0)
            if self.moved == 1:
                self.random_new_numbers()

        elif k == 0:
            sys.stdout.write('\rdown')
            self.moved = 0
            for ex in range(_size):
                for ey in range(2, -1, -1):
                    self.turn(ex, ey, 0, 1)
                for ey in range(2, -1, -1):
                    self.join(ex, ey, 0, 1)
            if self.moved == 1:
                self.random_new_numbers()

        elif k == 3:
            if self.game_over() == 1:
                for ex in range(_size):
                    for ey in range(_size):
                        self.set_map(ex, ey, 0)
                _bill[1] = 0
            if np.sum(_map) == 0:
                self.random_new_numbers()
                self.random_new_numbers()

        self.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            self.clicked(-1)
        elif e.key() == Qt.Key_Right:
            self.clicked(1)
        elif e.key() == Qt.Key_Down:
            self.clicked(0)
        elif e.key() == Qt.Key_Up:
            self.clicked(2)
        elif e.key() == Qt.Key_Plus:
            self.clicked(3)

    def paintEvent(self, event):
        qp = QPainter()
        qp.setRenderHint(QPainter.Antialiasing)

        qp.begin(self)
        pen = QPen(QColor(colors[0]))
        qp.setPen(pen)
        for ex in range(_size):
            for ey in range(_size):
                qp.setFont(QFont('Decorative', self.font_size(len(str(_map[ex][ey])))))  # ~30
                if self.game_over() == 0:
                    qp.fillRect(ex * x * 1.2 + x, ey * x * 1.2 + x, x, x,
                                QBrush(QColor(colors[len(str(bin(_map[ex][ey]))) - 2])))
                else:
                    qp.fillRect(ex * x * 1.2 + x, ey * x * 1.2 + x, x, x, QBrush(QColor(colors[12])))
                qp.drawText(ex * x * 1.2 + x, ey * x * 1.2 + x, x, x,
                            Qt.AlignHCenter | Qt.AlignVCenter, str(_map[ex][ey]))

        qp.setFont(QFont('Decorative', self.font_size(len(str(_bill[1])))))
        qp.drawText(121.9, 318, 106, 53, Qt.AlignHCenter | Qt.AlignVCenter, str(_bill[1]))
        if self.game_over() == 1:
            qp.drawText(121.9, 318, 106, 53, Qt.AlignHCenter | Qt.AlignVCenter, "Game Over")
            qp.fillRect(x, x, x*4.6, x*4.6, QBrush(QColor(0, 0, 0, 50)))
        qp.end()

    @staticmethod
    def font_size(count):
        if count < 2:
            return 30
        elif count < 3:
            return 26
        elif count < 4:
            return 22
        elif count < 6:
            return 18
        else:
            return 14

    @staticmethod
    def random_new_numbers():
        what_times = 0
        for i in range(50):
            eex = random.randrange(0, _size)
            eey = random.randrange(0, _size)
            if _map[eex][eey] == 0:
                _map[eex][eey] = random.choice((0b_10, 0b_10, 0b_10, 0b_10, 0b_100))  # 10% fortune for 4
                what_times += 1
            if what_times == 1:
                break


colors = ['#34486a', '#f6f4f5',
          '#cad877', '#d7ddea', '#FEC77F', '#FFB3B1',
          '#c0eb7e', '#c2e4eb', '#ffea97', '#f9c0c9',
          '#778046', '#757980', '#c78b89']
_size = 5
x = _size * 9  # размер сетки и отступы 13 9
_map = [[0 for i in range(_size)] for ii in range(_size)]  # частная переменная map
_bill = [0, 0]  # счёт рекордный и настоящий

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()

    sys.exit(app.exec_())
