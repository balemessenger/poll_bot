from os import path

from polling_bot.excel_reader import ExcelReader


HERE = path.abspath(path.dirname(__file__))


class ExcelQuestions:

    def __init__(self):
        excel_reader = ExcelReader(path.join(HERE, 'data/polling.xlsx'))
        excel_reader.read_excel_data(sheets=['questions', 'answers'])
        self.data = excel_reader.get_data
    #
    # def read_excell(self):
    #     excel_reader = ExcelReader(path.join(HERE, 'data/polling.xlsx'))
    #     excel_reader.read_excel_data(sheets=['questions', 'answers'])
    #     return excel_reader.get_data

    def get_question_list(self):

        return self.data['questions'][0]

    def get_question_answer(self, question_number):
        return self.data['answers'][0][question_number]
        # excel_reader = ExcelReader(path.join(HERE, 'tests/data/polling.xlsx'))
        # excel_reader.read_excel_data(sheets=['questions', 'answers'])
        # return excel_reader.get_data['answers'][0][question_number]


