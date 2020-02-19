from collections import defaultdict

import pandas


class ExcelReader:

    def __init__(self, file_path):
        self.file = file_path
        self.data_list = defaultdict(list)
        self.data = list

    def read_excel_data(self, sheets=None):
        if sheets and isinstance(sheets, list):
            for sheet_number in sheets:
                self.data = []
                data_frame = pandas.read_excel(self.file, sheet_name=sheet_number, header=None)
                # keys = data_frame.keys()
                for value_list in data_frame.values:
                    inner_data = []
                    for value in value_list:
                        inner_data.append(value)

                    self.data.append(inner_data)
                self.data_list[sheet_number].append(self.data)

    def validate_fields(self, data: dict):
        raise NotImplementedError()
    #
    @property
    def get_data(self):
        return self.data_list

