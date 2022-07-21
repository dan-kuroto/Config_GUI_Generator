from typing import Dict, List

from bs4 import BeautifulSoup


class BaseGenerator:
    """
    base class for all generators
    """
    def __init__(self, input_file: str, output_file: str, data_name: str, window_name: str):
        """
        :param input_file: input file path (*.html)
        :param output_file: output file path (*.py)
        :param data_name: class name of ConfigData
        :param window_name: class name of ConfigWindow
        """
        self.input_file = input_file
        self.output_file = output_file
        self.data_name = data_name
        self.window_name = window_name

    def generate(self):
        """
        generate code
        """
        raise NotImplementedError()


class PyQt5Generator(BaseGenerator):
    """
    config code generator for GUI software written in Python3 and PyQt5
    """
    def __init__(self, input_file: str, output_file: str, data_name: str, window_name: str):
        super().__init__(input_file, output_file, data_name, window_name)
        self.module_name = 'PyQt5'

    def generate(self):
        """
        generate code
        """
        data = self.__get_data()
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.writelines(self.__get_code(data))

    def __get_code(self, data: Dict) -> List[str]:
        """
        generate code by `data` and return lines
        """
        lines = []

        # import
        lines.extend(self.__get_import_statement())
        lines.extend(['\n', '\n'])  # 2 empty lines
        # class ConfigData
        lines.extend(self.__get_data_class_statement(data))
        lines.extend(['\n', '\n'])  # 2 empty lines
        # class ConfigWindow
        lines.extend(self.__get_window_class_statement(data))

        return lines

    def __get_import_statement(self) -> List[str]:
        """
        generate code of import statement and return lines
        """
        return [
            'import json\n',
            'import os\n',
            'import traceback\n',
            'from typing import Callable\n',
            '\n',
            f'from {self.module_name}.QtWidgets import *\n',
            f'from {self.module_name}.QtCore import *\n',
            f'from {self.module_name}.QtGui import *\n',
        ]

    def __get_data_class_statement(self, data: Dict) -> List[str]:
        """
        generate code of class ConfigData and return lines
        """
        lines = [
            f'class {self.data_name}:\n',
            f'    """\n',
            f'    ATTENTION:\n',
            f'    1. Don\'t use current `{self.data_name}` in your own code. It can only be used in `{self.window_name}`\n',
            f'    2. Don\'t call `save` of any `{self.data_name}`. `{self.window_name}` will control it.\n',
            f'    """\n',
            # init
            f'    def __init__(self):\n',
            f'        # set config path\n',
            f"        self.__config_path = os.path.abspath(r'{data['config_path']}')\n",
            f'        # load config\n',
            f'        __config_data = {{}}\n',
            f'        file_exist = True\n',
            f'        try:\n',
            f"            with open(self.__config_path, 'r', encoding='utf-8') as f:\n",
            f'                __config_data = json.load(f)\n',
            f'        except FileNotFoundError:\n',
            f'            file_exist = False\n',
            f'        except Exception:\n',
            f'            traceback.print_exc()\n',
            f'        # init config data\n',
        ]
        for item in data['content']:
            if item['category'] == 'input':
                if item['type'] == 'number':
                    lines.append(f"        self.{item['id']} = __config_data.get('{item['name']}', {item['value']})\n")
                else:
                    lines.append(f"        self.{item['id']} = __config_data.get('{item['name']}', '{item['value']}')\n")
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    if item_['type'] == 'number':
                        lines.append(f"        self.{item_['id']} = __config_data.get('{item_['name']}', {item_['value']})\n")
                    else:
                        lines.append(f"        self.{item_['id']} = __config_data.get('{item_['name']}', '{item_['value']}')\n")
        lines.extend([
            "        # init config file\n",
            "        if not file_exist:\n",
            "            if not os.path.exists(os.path.dirname(self.__config_path)):\n",
            "                os.makedirs(os.path.dirname(self.__config_path))\n",
            "            self.save()\n",
            "\n",
            "    def save(self):\n",
            "        config_data = {\n",
        ])
        for item in data['content']:
            if item['category'] == 'input':
                lines.append(f"            '{item['name']}': self.{item['id']},\n")
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    lines.append(f"            '{item_['name']}': self.{item_['id']},\n")
        lines.append('        }\n')
        lines.extend([
            "        try:\n",
            "            with open(self.__config_path, 'w', encoding='utf-8') as f:\n",
            "                json.dump(config_data, f, ensure_ascii=False)\n",
            "        except Exception:\n",
            "            traceback.print_exc()\n",
        ])

        return lines

    def __get_window_class_statement(self, data: Dict) -> List[str]:
        """
        generate code of class ConfigWindow and return lines
        """
        lines = [
            f"class {self.window_name}(QWidget):\n",
            f'    """\n',
            f"    ATTENTION:\n",
            f"    1. Get config data by getters in `{self.window_name}` instead of `{self.data_name}.*`\n",
            f'    """\n',
            f"    def __init__(self, config_changed: Callable[[], None] = lambda: None):\n",
            f'        """\n',
            f"        :param config_changed: function to call when config is changed\n",
            f'        """\n',
            f"        super().__init__()\n",
            f"        self.__config_data = {self.data_name}()\n",
            f"        self.__config_changed = config_changed\n",
            f"        self.setWindowTitle('{data['title']}')\n",
            f"        self.resize({data['width']}, {data['height']})\n",
            f"        self.setFixedSize({data['width']}, {data['height']})\n",
            f"        self.setWindowModality(Qt.WindowModality.ApplicationModal)\n",
            f"\n",
        ]
        for item in data['content']:
            if item['category'] == 'input':
                if item['type'] == 'number':
                    lines.extend([
                        f"        self.__label_{item['id']} = QLabel('{item['text']}')\n",
                        f"        self.__spin_box_{item['id']} = QSpinBox()\n",
                        f"        self.__spin_box_{item['id']}.setRange({item['min']}, {item['max']})\n",
                        f"        self.__spin_box_{item['id']}.setValue(self.__config_data.{item['id']})\n",
                    ])
                elif item['type'] == 'text':
                    lines.extend([
                        f"        self.__label_{item['id']} = QLabel('{item['text']}')\n",
                        f"        self.__line_edit_{item['id']} = QLineEdit()\n",
                        f"        self.__line_edit_{item['id']}.setText(self.__config_data.{item['id']})\n",
                        f"        self.__line_edit_{item['id']}.setPlaceholderText('{item['placeholder']}')\n",
                        f"        self.__line_edit_{item['id']}.setMaxLength({item['maxlength']})\n",
                    ])
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    if item_['type'] == 'number':
                        lines.extend([
                            f"        self.__label_{item_['id']} = QLabel('{item_['text']}')\n",
                            f"        self.__spin_box_{item_['id']} = QSpinBox()\n",
                            f"        self.__spin_box_{item_['id']}.setRange({item_['min']}, {item_['max']})\n",
                            f"        self.__spin_box_{item_['id']}.setValue(self.__config_data.{item_['id']})\n",
                        ])
                    elif item_['type'] == 'text':
                        lines.extend([
                            f"        self.__label_{item_['id']} = QLabel('{item_['text']}')\n",
                            f"        self.__line_edit_{item_['id']} = QLineEdit()\n",
                            f"        self.__line_edit_{item_['id']}.setText(self.__config_data.{item_['id']})\n",
                            f"        self.__line_edit_{item_['id']}.setPlaceholderText('{item_['placeholder']}')\n",
                            f"        self.__line_edit_{item_['id']}.setMaxLength({item_['maxlength']})\n",
                        ])
        lines.extend([
            f"        self.__button_save = QPushButton()\n",
            f"        self.__button_save.setText('{'Save' if data['lang'] == 'en' else '保存'}')\n",
            f"        self.__button_save.clicked.connect(self.on_button_save_clicked)\n",
            f"        self.__button_cancel = QPushButton()\n",
            f"        self.__button_cancel.setText('{'Cancel' if data['lang'] == 'en' else '取消'}')\n",
            f"        self.__button_cancel.clicked.connect(self.on_button_cancel_clicked)\n",
            f"\n",
        ])
        for item in data['content']:
            if item['category'] == 'fieldset':
                lines.append(f"        self.__group_box_{item['id']} = QGroupBox('{item['text']}')\n")
                lines.append(f"        layout_group_box_{item['id']} = QFormLayout()\n")
                for item_ in item['items']:
                    type_ = {'number': 'spin_box', 'text': 'line_edit'}[item_['type']]
                    lines.append(f"        layout_group_box_{item['id']}.addRow(self.__label_{item_['id']}, self.__{type_}_{item_['id']})\n")
                lines.append(f"        self.__group_box_{item['id']}.setLayout(layout_group_box_{item['id']})\n")
                lines.append("\n")
        lines.append(f"        layout_main = QVBoxLayout()\n")
        for item in data['content']:
            if item['category'] == 'fieldset':
                lines.append(f"        layout_main.addWidget(self.__group_box_{item['id']})\n")
            elif item['category'] == 'input':
                type_ = {'number': 'spin_box', 'text': 'line_edit'}[item['type']]
                lines.append(f"        layout_{item['id']} = QFormLayout()\n")
                lines.append(f"        layout_{item['id']}.addRow(self.__label_{item['id']}, self.__{type_}_{item['id']})\n")
                lines.append(f"        layout_main.addLayout(layout_{item['id']})\n")
        lines.extend([
            "        layout_button = QHBoxLayout()\n",
            "        layout_button.setAlignment(Qt.AlignmentFlag.AlignRight)\n",
            "        layout_button.addWidget(self.__button_save)\n",
            "        layout_button.addWidget(self.__button_cancel)\n",
            "        layout_main.addLayout(layout_button)\n",
            "        self.setLayout(layout_main)\n",
            "\n",
            "    def on_button_save_clicked(self):\n",
            "        # check input\n",
            "        if not self.check():\n",
            "            return\n",
            "        # update config\n",
        ])
        for item in data['content']:
            if item['category'] == 'input':
                if item['type'] == 'number':
                    lines.append(f"        self.__config_data.{item['id']} = self.__spin_box_{item['id']}.value()\n")
                elif item['type'] == 'text':
                    lines.append(f"        self.__config_data.{item['id']} = self.__line_edit_{item['id']}.text()\n")
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    if item_['type'] == 'number':
                        lines.append(f"        self.__config_data.{item_['id']} = self.__spin_box_{item_['id']}.value()\n")
                    elif item_['type'] == 'text':
                        lines.append(f"        self.__config_data.{item_['id']} = self.__line_edit_{item_['id']}.text()\n")
        lines.extend([
            "        # save config\n",
            "        self.__config_data.save()\n",
            "        # call config_changed\n",
            "        self.__config_changed()\n",
            "        # close window\n",
            "        self.close()\n",
            "\n",
            "    def check(self) -> bool:\n",
            '        """\n',
            '        check input, show error message window and finally return whether input is valid\n',
            '        :return: True if input is valid, False otherwise\n',
            '        """\n',
        ])
        for item in data['content']:
            if item['category'] == 'input' and item['type'] == 'text' and item['minlength'] > 0:
                lines.append(f"        if len(self.__line_edit_{item['id']}.text()) < {item['minlength']}:\n")
                if data['lang'] == 'en':
                    lines.append(f"            QMessageBox.warning(self, 'Error', '{item['text']} must be at least {item['minlength']} characters long.')\n")
                elif data['lang'] == 'zh-CN':
                    lines.append(f"            QMessageBox.warning(self, '错误', '{item['text']}必须至少{item['minlength']}个字符')\n")
                lines.append("            return False\n")
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    if item_['type'] == 'text' and item_['minlength'] > 0:
                        lines.append(f"        if len(self.__line_edit_{item_['id']}.text()) < {item_['minlength']}:\n")
                        if data['lang'] == 'en':
                            lines.append(f"            QMessageBox.warning(self, 'Error', '{item_['text']} must be at least {item_['minlength']} characters long.')\n")
                        elif data['lang'] == 'zh-CN':
                            lines.append(f"            QMessageBox.warning(self, '错误', '{item_['text']}必须至少{item_['minlength']}个字符.')\n")
                        lines.append("            return False\n")
        lines.extend([
            "        return True\n",
            "\n",
            "    def on_button_cancel_clicked(self):\n",
            "        self.cancel()\n",
            "\n",
            "    def closeEvent(self, a0: QCloseEvent):\n",
            "        self.cancel()\n",
            "\n",
            "    def cancel(self):\n",
            "        # reset config\n",
        ])
        for item in data['content']:
            if item['category'] == 'input':
                if item['type'] == 'number':
                    lines.append(f"        self.__spin_box_{item['id']}.setValue(self.{item['id']}())\n")
                elif item['type'] == 'text':
                    lines.append(f"        self.__line_edit_{item['id']}.setText(self.{item['id']}())\n")
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    if item_['type'] == 'number':
                        lines.append(f"        self.__spin_box_{item_['id']}.setValue(self.{item_['id']}())\n")
                    elif item_['type'] == 'text':
                        lines.append(f"        self.__line_edit_{item_['id']}.setText(self.{item_['id']}())\n")
        lines.extend([
            "        # close window\n",
            "        self.close()\n",
        ])
        for item in data['content']:
            if item['category'] == 'input':
                if item['type'] == 'number':
                    lines.extend([
                        f"\n",
                        f"    def {item['id']}(self) -> int:\n",
                        f"        return self.__config_data.{item['id']}\n",
                    ])
                elif item['type'] == 'text':
                    lines.extend([
                        f"\n",
                        f"    def {item['id']}(self) -> str:\n",
                        f"        return self.__config_data.{item['id']}\n",
                    ])
            elif item['category'] == 'fieldset':
                for item_ in item['items']:
                    if item_['type'] == 'number':
                        lines.extend([
                            f"\n",
                            f"    def {item_['id']}(self) -> int:\n",
                            f"        return self.__config_data.{item_['id']}\n",
                        ])
                    elif item_['type'] == 'text':
                        lines.extend([
                            f"\n",
                            f"    def {item_['id']}(self) -> str:\n",
                            f"        return self.__config_data.{item_['id']}\n",
                        ])
        return lines

    def __get_data(self) -> Dict:
        """
        get data from input file
        """
        with open(self.input_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        data = {}

        # html.lang
        data['lang'] = soup.html.get('lang', 'en')
        # head.title
        data['title'] = soup.head.title.string
        # body.width, body.height, body.src
        data['width'] = int(soup.body.get('width', '800'))
        data['height'] = int(soup.body.get('height', '600'))
        data['config_path'] = soup.body.get('src', './res/config.json')
        # all input tags or fieldset tags in body
        # input tags: {'category': 'input', 'attr_name': 'attr_value', ...}
        # fieldset tags: {'category': 'fieldset', 'attr_name': 'attr_value', ..., 'items': [input tags]}
        data['content'] = []
        for tag in soup.body.children:
            if tag.name == 'p':  # input tag is wrapped in <p> tag with <span>
                data['content'].append(self.__get_input_tag_data_from(tag))
            elif tag.name == 'fieldset':
                data['content'].append(self.__get_fieldset_tag_data_from(tag))

        return data

    def __get_input_tag_data_from(self, tag: BeautifulSoup) -> Dict:
        """
        get data from:

        <p>
            <span>label</span>
            <input attr_name="attr_value" ...>
        </p>
        """
        data = {}
        # tags
        span_tag = tag.find('span')
        input_tag = tag.find('input')

        # common data
        data['category'] = 'input'  # input or fieldset
        data['text'] = span_tag.string  # label text, will be shown in window
        data['type'] = input_tag.get('type', 'text')  # input type
        data['id'] = input_tag.get('id', '')  # input id, will be used in code
        if not data['id']:
            raise ValueError('id is required')
        data['name'] = input_tag.get('name', data['id'])  # input name, will be used in config file

        # unique data for each type of input tag
        if data['type'] == 'text':
            data['placeholder'] = input_tag.get('placeholder', '')  # placeholder text, will be shown in window
            data['value'] = input_tag.get('value', '')  # initial value, will be used in config file
            data['minlength'] = int(input_tag.get('minlength', 0))  # minimum text length
            data['maxlength'] = int(input_tag.get('maxlength', 10))  # maximum text length
        elif data['type'] == 'number':
            data['value'] = int(input_tag.get('value', 0))  # initial value, will be used in config file
            data['min'] = int(input_tag.get('min', 0))  # minimum value
            data['max'] = int(input_tag.get('max', 10))  # maximum value
            data['step'] = int(input_tag.get('step', 1))  # step value
        else:
            raise Exception(f'unsupported input type: {data["type"]}')

        return data

    def __get_fieldset_tag_data_from(self, tag: BeautifulSoup) -> Dict:
        """
        get data from:

        <fieldset>
            <legend>label</legend>
            <p>input ...</p>
            ...
        </fieldset>
        """
        data = {}
        # tags
        legend_tag = tag.find('legend')
        p_tags = tag.find_all('p')

        # data
        data['category'] = 'fieldset'  # input or fieldset
        data['id'] = tag.get('id', '')  # fieldset id, will be used in code (QGroupBox)
        if not data['id']:
            raise ValueError('id is required')
        data['text'] = legend_tag.string  # label text, will be shown in window (QGroupBox)
        data['items'] = []  # input tags
        for p_tag in p_tags:
            data['items'].append(self.__get_input_tag_data_from(p_tag))

        return data


class PySide2Generator(PyQt5Generator):
    """
    config code generator for GUI software written in Python3 and PySide2
    
    Based on `PyQt5Generator` instead of `BaseGenerator`, because `PySide2` is similar to `PyQt5`.
    The only difference of source code will be the import statement.
    """
    def __init__(self, input_file: str, output_file: str, data_name: str, window_name: str):
        super().__init__(input_file, output_file, data_name, window_name)
        self.moduel_name = 'PySide2'
