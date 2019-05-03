import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class Game(QWidget):

    def __init__(self, parent=None):
        super(Game, self).__init__(parent)
        self.initUI()

    def start_game(self):
        self.dialog = MainGame()
        self.dialog.show()
        #self.setFixedSize(x/2, y/1.5)
        self.move(40, 150)
        #self.butt(10, 20)

    def initUI(self):

        #НАЧАЛО ИГРЫ
        QToolTip.setFont(QFont('Raleway', 10))

        # self.setFixedSize(x, y)
        self.resize(x, y)
        self.center()
        self.setWindowTitle('Logic_Game')
        self.setWindowIcon(QIcon('LOGO.png'))
        self.butt(x, y)
        #self.show()

        # установка фонового изображения
        oImage = QImage("2.jpg")
        sImage = oImage.scaled(QSize(x, y))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def butt(self, x_local, y_local):
        button = QPushButton('Start', self)
        button.setFont(QFont('Raleway', 20))
        button.setToolTip('Click <b>Start</b> to start game.')

        # ЗАВЕРШЕНИЕ ИГРЫ
        exit = QPushButton('Exit', self)
        exit.resize(exit.sizeHint())
        exit.move(x_local/2.0, y_local/1.5)
        exit.clicked.connect(QCoreApplication.instance().quit)

        button.resize(150, 40)
        button.move(x_local/3.0, y_local/2.5)
        button.clicked.connect(self.start_game)



    # Автоматическое централизирование окна игры
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        # двигаем левый верхний угол окна игры в тот-же угол qr
        self.move(qr.topLeft())

class MainGame(QWidget):
    def __init__(self, parent=None):
        super(MainGame, self).__init__(parent)
        self.initUI2()

        # текст lable
        self.layout = QVBoxLayout()
        self.label = QLabel("My text")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    global num, color, sqx, sqy
    # массив изображений
    global px1, px2
    global SQUARE

    def initUI2(self):
        global x, y
        self.setFixedSize(x, y)
        self.setWindowTitle('Simple play')
        self.setWindowIcon(QIcon('LOGO.png'))
        self.show()

        oImage = QImage("2.jpg")
        sImage = oImage.scaled(QSize(x, y))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    # переопределение метода закрытия окна- сообщение

    #def closeEvent(self, QCloseEvent):
    #    reply = QMessageBox.question(self, 'Remark',
    #                                 'Exit?', QMessageBox.Yes | QMessageBox.No,
    #                                 QMessageBox.No)
    #    if reply == QMessageBox.Yes:
    #        QCloseEvent.accept()
    #    else:
    #        QCloseEvent.ignore()



    def paintEvent(self, event):
        qp = QPainter()
        qp.setRenderHint(QPainter.Antialiasing)
        qp.begin(self)

        qp.fillRect(SQUARE[0][0], SQUARE[0][1], SQUARE[0][2], SQUARE[0][3], QBrush(QColor(color)))
        pen = QPen(QColor('#7cb2d1'))
        pen.setWidth(1)
        qp.setPen(pen)

        #for e in SQUARE:
            #qp.drawRect(SQUARE[e][0], SQUARE[e][1], SQUARE[e][2], SQUARE[e][3])
        qp.drawRect(SQUARE[0][0], SQUARE[0][1], SQUARE[0][2], SQUARE[0][3])
        qp.drawText(SQUARE[0][0], SQUARE[0][1], SQUARE[0][2], SQUARE[0][3], Qt.AlignHCenter | Qt.AlignVCenter, str(num))
        qp.drawRect(SQUARE[1][0], SQUARE[1][1], SQUARE[1][2], SQUARE[1][3])
        qp.drawRect(SQUARE[2][0], SQUARE[2][1], SQUARE[2][2], SQUARE[2][3])
        qp.drawRect(SQUARE[3][0], SQUARE[3][1], SQUARE[3][2], SQUARE[3][3])

        qp.end()

        # QTextEdit().setText('one<b>two</b>three<br>')
        # QTextBlock('one<b>two</b>three<br>')




    # отклик на нажатие управляющих клавиш
    def updateValues(self, value):

        if value == 1:
            self.num *= 4

        elif value == 2:
            self.num *= 4
        elif value == 3:
            self.num = 20
            self.color = '#bed3c3'
            self.sqx = 40
        elif value == 4:
            self.num *= 4


        self.update()  # <-- update the window!

    # отслеживание нажима клавиш
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.updateValues(1)
        if e.key() == Qt.Key_Left:
            self.updateValues(2)
        if e.key() == Qt.Key_Up:
            self.updateValues(3)
        if e.key() == Qt.Key_Down:
            self.updateValues(4)




#PARAMETERS

num = 2
color = '#212e53'


# размеры окон
x = 300
y = 450

# массив изображений
px1 = './images/1.png'
px2 = './images/2.png'

# размеры прямоугольников
sqx = 25
sqy = 55
sq = 65

# массив координат прямоугольников
SQUARE_1 = [sq - 40, sqx, sqy, sqy]
SQUARE_2 = [sq + 25, sqx, sqy, sqy]
SQUARE_3 = [sq + 90, sqx, sqy, sqy]
SQUARE_4 = [sq + 155, sqx, sqy, sqy]

# массив квадратов
SQUARE = [SQUARE_1, SQUARE_2, SQUARE_3, SQUARE_4]

D_SQUARE = SQUARE_1[2] - SQUARE_1[0]

if __name__ == '__main__':
    # Каждое приложение должно создать объект QApplication
    # sys.argv - список аргументов командной строки
    app = QApplication(sys.argv)
    ex = Game()
    ex1 = MainGame()
    sys.exit(app.exec_())