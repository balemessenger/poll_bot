from os import path
from polling_bot.excel_reader import ExcelReader


HERE = path.abspath(path.dirname(__file__))


class TestExcelReaderWithValidation(ExcelReader):

    def __init__(self, file_path):
        super().__init__(file_path)

    def validate_fields(self):
        for key, value in self.data.items():
            for index, element in enumerate(value):
                if key == 'national_id' and not self.validate_national_id(element):
                    value[index] = 'Invalid'

    @staticmethod
    def validate_national_id(national_id):
        if len(str(national_id)) != 10:
            return False

        return True


class TestExcelReader:

    def test_excel_reader(self):
        excel_reader = TestExcelReaderWithValidation(path.join(HERE, 'data/polling.xlsx'))
        excel_reader.read_excel_data(sheets=[1, 2])


if __name__ == '__main__':
    excel_reader = TestExcelReaderWithValidation(path.join(HERE, 'data/polling.xlsx'))
    excel_reader.read_excel_data(sheets=['questions', 'answers'])
    excel_reader.get_data
