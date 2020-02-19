import os
import sys
from datetime import datetime
from collections import OrderedDict

import pandas as pd

from loguru import logger


DATA_INDEX = 0
TRANSLATION_INDEX = 1


def convert_dataframe_to_matrix(data_frame_list):
    converted_data = OrderedDict()
    converted_data.setdefault('peer_id', [])
    for value in data_frame_list[0]['question_number']:
        converted_data.setdefault(int(value) + 1, [])

    for data in data_frame_list:
        for key, value in data.items():
            if key == 'peer_id':
                for item in set(value):
                    converted_data[key].append(item)

        for i in range(len(data['answer'])):
            converted_data[int(data['question_number'][i])+1].append(data['answer'][i])

    return [converted_data]


class ResultWriter:

    def __init__(self, exel_file_path):
        self.path = exel_file_path

    def _create_data_frame(self, data_tuple):
        result = OrderedDict()
        for data in data_tuple[DATA_INDEX]:
            for key, value in data.__dict__.items():
                if key == '_sa_instance_state' or key == 'question_answer_flag':
                    continue

                result.setdefault(key, []).append(value) if len(data_tuple) == 1 \
                    else result.setdefault(
                    data_tuple[TRANSLATION_INDEX][key], []
                ).append(value)

        return result

    def write_to_excel(self, data_list, sheet_name_list):
        data_frame_list = []
        if os.path.exists(self.path):
            os.remove(self.path)


        # for data_tuple in data_list:
        #     data_frame_list.append(self._create_data_frame(data_tuple))

        # data_frame_list = convert_dataframe_to_matrix(data_frame_list)

        writer = pd.ExcelWriter(self.path, engine='xlsxwriter')
        try:
            pandas_dataframe = pd.DataFrame(data_list)
        except ValueError as e:
            logger.error(
                'Data Is Malform',
                extra={
                    'step': sys._getframe().f_code.co_name,
                    'time': datetime.now()
                }
            )
            raise RuntimeError('Data Is Malform')
        pandas_dataframe.to_excel(writer, "report")

        writer.save()
