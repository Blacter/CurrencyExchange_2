from urllib.parse import unquote

from controller.post_data.base_post_data import BasePostData
from controller.controller_error.post_data_error import WrongCurrenciesBody

class CurrencyPostData(BasePostData):
    def __init__(self, post_data: bytes):
        super().__init__(post_data)

    def get_parsed_parameters(self) -> dict[str, int | str]:
        self.get_base_parsed_parameters()
        self.check_parameters_structure()
        self.parse_parameters_with_type()

        return self.get_parameters_dict()

    def check_parameters_structure(self) -> None:
        self.check_name()
        self.check_code()
        self.check_sign()

    def check_name(self) -> None:
        if 'name' not in self._parameters_dict.keys():
            raise WrongCurrenciesBody('parameter name doesn\'t exists.')
        if len(self._parameters_dict['name']) == 0:
            raise WrongCurrenciesBody('name value shouldn\'t be empty.')

    def check_code(self) -> None:
        if 'code' not in self._parameters_dict.keys():
            raise WrongCurrenciesBody('parameter code doesn\'t exists.')
        if len(self._parameters_dict['code']) == 0:
            raise WrongCurrenciesBody('code value shouldn\'t be empty.')

    def check_sign(self) -> None:
        if 'sign' not in self._parameters_dict.keys():
            raise WrongCurrenciesBody('parameter sign doesn\'t exists.')
        if len(self._parameters_dict['sign']) == 0:
            raise WrongCurrenciesBody('sign value shouldn\'t be empty.')

    def parse_parameters_with_type(self) -> None:
        self.parse_name()
        self.parse_code()
        self.parse_sign()

    def parse_name(self) -> None:
        self.parsed_name: str = self._parameters_dict['name']

    def parse_code(self) -> None:
        self.parsed_code: str = self._parameters_dict['code']

    def parse_sign(self) -> None:
        self.parsed_sign: str = unquote(self._parameters_dict['sign'])

    def get_parameters_dict(self) -> dict[str, int | str]:
        result_parameters_dict: dict[str, int | str] = {}
        result_parameters_dict['name'] = self.parsed_name
        result_parameters_dict['code'] = self.parsed_code
        result_parameters_dict['sign'] = self.parsed_sign
        return result_parameters_dict