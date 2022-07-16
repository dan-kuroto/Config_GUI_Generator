import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from config import ConfigWindow


class __TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.config_window = ConfigWindow(self.config_changed)
        self.setWindowTitle('Config Test for {}({})'.format(self.config_window.user_name(), self.config_window.age()))

        self.button = QPushButton(self)
        self.button.setText('Config')
        self.button.setGeometry(0, 0, 100, 50)
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.config_window.show()

    def config_changed(self):
        self.setWindowTitle('Config Test for {}({})'.format(self.config_window.user_name(), self.config_window.age()))


if __name__ == '__main__':
    # 防止从奇怪的路径启动程序导致程序内使用的相对路径出错，先cd过去
    os.chdir(os.path.split(os.path.realpath(__file__))[0])

    app = QApplication(sys.argv)
    window = __TestWindow()
    window.show()
    sys.exit(app.exec_())
