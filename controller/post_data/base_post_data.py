from abc import ABC, abstractmethod
import re
import urllib.parse


from controller.controller_error.post_data_error import BodySizeTooLarge

class BasePostData(ABC):
    def __init__(self, post_data: str):
        if len(post_data) > 1000:
            raise BodySizeTooLarge()
        self._post_data: str = urllib.parse.unquote(post_data)

    @abstractmethod
    def get_parsed_parameters(self):
        pass

    def get_base_parsed_parameters(self) -> dict[str, str]:
        print(f'{self._post_data=}')
        key_value_list: list[str] = self._post_data.split('&')
        self._parameters_dict: dict[str, str] = {}

        for key_value in key_value_list:
            key, value = key_value.split('=')
            self._parameters_dict[key] = value.strip()

    def is_key_in_body(self, key: str) -> bool:
        if key in self._parameters_dict.keys():
            return True
        return False

    @staticmethod
    def is_empty_str(value: str) -> bool:
        if len(value) == 0:
            return True
        return False

    @staticmethod
    def could_str_be_parsed_to_float(value: str) -> bool:
        return re.match(r'^\d+\.\d+$', value)