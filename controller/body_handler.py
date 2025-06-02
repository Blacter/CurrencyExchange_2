from abc import ABC, abstractmethod
from markupsafe import escape
from urllib.parse import unquote
import re

from controller.body_error_handler import BodySizeTooLarge
from controller.body_error_handler import WrongCurrenciesBody
from controller.body_error_handler import WrongExchangeRatesBody


class BodyHandler:
    def __init__(self, parameters_row: str):
        if len(parameters_row) > 1000:
            raise BodySizeTooLarge()
        self._parameters_row: str = parameters_row.decode('UTF-8')

    @abstractmethod
    def get_parsed_parameters(self):
        pass

    def get_base_parsed_parameters(self) -> dict[str, str]:
        print(f'{self._parameters_row=}')
        key_value_list: list[str] = self._parameters_row.split('&')
        self._parameters_dict: dict[str, str] = {}

        for key_value in key_value_list:
            # TODO: отлавливать случай отсутствия =.
            key, value = key_value.split('=')
            self._parameters_dict[key] = value

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


class CurrenciesBodyHandler(BodyHandler):
    def __init__(self, parameters_row: str):
        super().__init__(parameters_row)

    def get_parsed_parameters(self) -> dict[str, int | str]:
        self.get_base_parsed_parameters()
        self.check_parameters_structure()
        self.parse_parameters_with_type()

        # parameters_dict: dict[str, int|str] = {}
        return self.get_parameters_dict()

    def check_parameters_structure(self) -> None:
        self.check_id()
        self.check_name()
        self.check_code()
        self.check_sign()

    def check_id(self) -> None:
        if 'id' not in self._parameters_dict.keys():
            raise WrongCurrenciesBody('parameter id doesn\'t exists.')
        if not self._parameters_dict['id'].isdigit():
            raise WrongCurrenciesBody('id should be number.')

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
        self.parse_id()
        self.parse_name()
        self.parse_code()
        self.parse_sign()

    def parse_id(self) -> None:
        self.parsed_id: int = int(self._parameters_dict['id'])

    def parse_name(self) -> None:
        self.parsed_name: str = self._parameters_dict['name']

    def parse_code(self) -> None:
        self.parsed_code: str = self._parameters_dict['code']

    def parse_sign(self) -> None:
        self.parsed_sign: str = unquote(self._parameters_dict['sign'])

    def get_parameters_dict(self) -> dict[str, int | str]:
        result_parameters_dict: dict[str, int | str] = {}
        result_parameters_dict['id'] = self.parsed_id
        result_parameters_dict['name'] = self.parsed_name
        result_parameters_dict['code'] = self.parsed_code
        result_parameters_dict['sign'] = self.parsed_sign
        return result_parameters_dict


class ExchangeRatesBodyHandler(BodyHandler):
    def __init__(self, parameters_row: str):
        super().__init__(parameters_row)

    def get_parsed_parameters(self) -> dict[str, int | str]:
        self.get_base_parsed_parameters()
        self.check_parameters_structure()
        self.parse_parameters_with_type()
        return self.get_parameters_dict()

    def check_parameters_structure(self) -> None:
        self.check_base_currency_code()
        self.check_target_currency_code()
        self.check_rate()
        
    def parse_parameters_with_type(self) -> None:
        self.parse_base_currency_code()
        self.parse_target_currency_code()
        self.parse_rate()
    
    def get_parameters_dict(self) -> dict[str, int | str]:
        result_parameters_dict: dict[str, int | str] = {}
        result_parameters_dict['baseCurrencyCode'] = self.parsed_base_currency_code
        result_parameters_dict['targetCurrencyCode'] = self.parsed_target_currency_code
        result_parameters_dict['rate'] = self.parsed_rate
        
        return result_parameters_dict

    def check_base_currency_code(self) -> None:
        self.check_base_currency_code_key()
        self.check_base_currency_code_value()
        
    def check_target_currency_code(self) -> None:
        self.check_target_currency_code_key()
        self.check_target_currency_code_value()
        
    def check_rate(self) -> None:
        self.check_rate_key()
        self.check_rate_value()
        
    def parse_base_currency_code(self) -> None:
        self.parsed_base_currency_code: str = self._parameters_dict['baseCurrencyCode']
    
    def parse_target_currency_code(self) -> None:
        self.parsed_target_currency_code: str = self._parameters_dict['targetCurrencyCode']
    
    def parse_rate(self) -> None:
        self.parsed_rate: float = self._parameters_dict['rate']

    def check_base_currency_code_key(self) -> None:
        if not self.is_key_in_body('baseCurrencyCode'):
            raise WrongExchangeRatesBody(
                'parameter baseCurrencyCode doesn\'t exists.')

    def check_base_currency_code_value(self) -> None:
        if BodyHandler.is_empty_str(self._parameters_dict['baseCurrencyCode']):
            raise WrongExchangeRatesBody(
                'baseCurrencyCode value shouldn\'t be empty.')

    def check_target_currency_code_key(self) -> None:
        if not self.is_key_in_body('targetCurrencyCode'):
            raise WrongExchangeRatesBody(
                'parameter targetCurrencyCode doesn\'t exists.')
            
    def check_target_currency_code_value(self) -> None:
        if BodyHandler.is_empty_str(self._parameters_dict['targetCurrencyCode']):
            raise WrongExchangeRatesBody(
                'targetCurrencyCode value shouldn\'t be empty.')

    def check_rate_key(self) -> None:
        if not self.is_key_in_body('rate'):
            raise WrongExchangeRatesBody('parameter rate doesn\'t exists.')
        
    def check_rate_value(self) -> None:
        self.check_rate_not_empty()
        self.check_rate_is_float()

    def check_rate_not_empty(self) -> None:
        if BodyHandler.is_empty_str(self._parameters_dict['rate']):
            raise WrongExchangeRatesBody('rate value shouldn\'t be empty.')

    def check_rate_is_float(self) -> None:
        if not BodyHandler.could_str_be_parsed_to_float(self._parameters_dict['rate']):
            raise WrongExchangeRatesBody('rate value should be float.')

    
