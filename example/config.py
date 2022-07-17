import json
import os
import traceback
from typing import Callable

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ConfigData:
    """
    ATTENTION:
    1. Don't use current `ConfigData` in your own code. It can only be used in `ConfigWindow`
    2. Don't call `save` of any `ConfigData`. `ConfigWindow` will control it.
    """
    def __init__(self):
        # set config path
        self.__config_path = os.path.abspath(r'res\config.json')
        # load config
        __config_data = {}
        file_exist = True
        try:
            with open(self.__config_path, 'r', encoding='utf-8') as f:
                __config_data = json.load(f)
        except FileNotFoundError:
            file_exist = False
        except Exception:
            traceback.print_exc()
        # init config data
        self.user_name = __config_data.get('user_name', 'user')
        self.age = __config_data.get('age', 0)
        # init config file
        if not file_exist:
            if not os.path.exists(os.path.dirname(self.__config_path)):
                os.makedirs(os.path.dirname(self.__config_path))
            self.save()

    def save(self):
        config_data = {
            'user_name': self.user_name,
            'age': self.age
        }
        try:
            with open(self.__config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False)
        except Exception:
            traceback.print_exc()


class ConfigWindow(QWidget):
    """
    ATTENTION:
    1. Get config data by getters in `ConfigWindow` instead of `__config_data.*`
    """
    def __init__(self, config_changed: Callable[[], None]):
        """
        :param config_changed: function to call when config is changed
        """
        super().__init__()
        self.__config_data = ConfigData()
        self.__config_changed = config_changed
        self.setWindowTitle('Config Window')
        self.resize(300, 200)
        self.setFixedSize(300, 200)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.__label_user_name = QLabel('用户名')
        self.__text_edit_user_name = QLineEdit(self)
        self.__text_edit_user_name.setText(self.__config_data.user_name)
        self.__text_edit_user_name.setPlaceholderText('请输入用户名')
        self.__text_edit_user_name.setMaxLength(10)
        self.__label_age = QLabel('年龄')
        self.__spin_box_age = QSpinBox()  # 只能整数，要浮点数就得用QDoubleSpinBox
        self.__spin_box_age.setRange(0, 100)
        self.__spin_box_age.setValue(self.__config_data.age)
        self.__button_save = QPushButton()
        self.__button_save.setText('保存')
        self.__button_save.clicked.connect(self.on_button_save_clicked)
        self.__button_cancel = QPushButton()
        self.__button_cancel.setText('取消')
        self.__button_cancel.clicked.connect(self.on_button_cancel_clicked)

        self.__group_box_user = QGroupBox('用户')
        layout_group_box_user = QFormLayout()
        layout_group_box_user.addRow(self.__label_user_name, self.__text_edit_user_name)
        layout_group_box_user.addRow(self.__label_age, self.__spin_box_age)
        self.__group_box_user.setLayout(layout_group_box_user)

        layout_self = QVBoxLayout()
        layout_self.addWidget(self.__group_box_user)
        layout_button = QHBoxLayout()
        layout_button.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_button.addWidget(self.__button_save)
        layout_button.addWidget(self.__button_cancel)
        layout_self.addLayout(layout_button)
        self.setLayout(layout_self)

    def on_button_save_clicked(self):
        # check input
        if not self.check():
            return
        # update config
        self.__config_data.user_name = self.__text_edit_user_name.text()
        self.__config_data.age = self.__spin_box_age.value()
        # save config
        self.__config_data.save()
        # call config_changed
        self.__config_changed()
        # close window
        self.close()

    def check(self) -> bool:
        """
        check input, show error message window and finally return whether input is valid
        :return: True if input is valid, False otherwise
        """
        raise NotImplementedError("You should implement this method by yourself!")
        return True

    def on_button_cancel_clicked(self):
        self.cancel()

    def closeEvent(self, a0: QCloseEvent):
        self.cancel()

    def cancel(self):
        # reset config
        self.__text_edit_user_name.setText(self.user_name())
        self.__spin_box_age.setValue(self.age())
        # close window
        self.close()

    def user_name(self) -> str:
        return self.__config_data.user_name

    def age(self) -> int:
        return self.__config_data.age
