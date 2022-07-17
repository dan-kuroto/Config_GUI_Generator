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
        
    def generate(self):
        print('test')
