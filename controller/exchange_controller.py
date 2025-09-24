from view.view import CurrencyView
from model.model import CurrencyModel

from url_path.url_path import UrlPath

from controller.controller_error.exchange_error import WrongCurrencyParameters
from controller.controller_error.exchange_error import WrongCurrencyUrlKey
from controller.controller_error.exchange_error import WrongCurrencyUrlValue
from controller.controller_error.exchange_error import ExchangeImpossible


class ExchangeController:
    def __init__(self, view: CurrencyView, model: CurrencyModel, url_path: UrlPath):
        self.view: CurrencyView = view
        self.model: CurrencyModel = model
        self.url_path: UrlPath = url_path

    def get_exchange(self) -> tuple[int, str]:
        try:
            self.check_exchange_parameters()
            self.parce_exchange_data()
            exchange_result: str = self.do_exchange()
        except WrongCurrencyParameters as e:
            response_code: int = 400
            response_str: str = self.view.get_json_result('exchange_error', str(e))
        except ExchangeImpossible as e:
            response_code: int = 200
            response_str: str = self.view.get_json_result('exchange_error', str(e))
        else:
            response_code: int = 200
            response_str: str = self.view.get_exchange_result(exchange_result)

        return (response_code, response_str)

    def check_exchange_parameters(self) -> None:
        self.row_query_parameters: dict[str,
                                        str] = self.url_path.query_parameters
        self.check_from_currency_code()
        self.check_to_currency_code()
        self.check_amount()

    def parce_exchange_data(self) -> None:
        parced_exchange_data_tmp: dict[str, str | int] = {}
        parced_exchange_data_tmp['fr'] = self.url_path.query_parameters['fr']
        parced_exchange_data_tmp['to'] = self.url_path.query_parameters['to']
        parced_exchange_data_tmp['amount'] = int(
            self.url_path.query_parameters['amount'])

        self.parced_exchange_data: ExchangeData = ExchangeData.from_dict(
            parced_exchange_data_tmp)

    def do_exchange(self) -> str:
        exchange_result: str | None = self.exchange_straight_pair()
        if exchange_result is None:
            exchange_result = self.exchange_reverse_pair()
        if exchange_result is None:
            exchange_result = self.exchange_usd_pair()
        if exchange_result is None:
            raise ExchangeImpossible(
                self.parced_exchange_data.base_currency_code, self.parced_exchange_data.target_currency_code)

        return exchange_result

    def check_from_currency_code(self) -> None:
        if 'fr' not in self.row_query_parameters:
            raise WrongCurrencyUrlKey('fr')
        if ExchangeController.is_empty(self.row_query_parameters['fr']):
            raise WrongCurrencyUrlValue('fr')

    def check_to_currency_code(self) -> None:
        if 'to' not in self.row_query_parameters:
            raise WrongCurrencyUrlKey('to')
        if ExchangeController.is_empty(self.row_query_parameters['to']):
            raise WrongCurrencyUrlValue('to')

    def check_amount(self) -> None:
        if 'amount' not in self.row_query_parameters:
            raise WrongCurrencyUrlKey('amount')
        if ExchangeController.is_empty(self.row_query_parameters['amount']):
            raise WrongCurrencyUrlValue('amount')

    def exchange_straight_pair(self) -> str | None:
        straight_exchange_rate: float | None = self.model.get_exchange_rate_by_codes(
            self.parced_exchange_data.base_currency_code, self.parced_exchange_data.target_currency_code)
        if straight_exchange_rate is None:
            return None
        return str(self.parced_exchange_data.amount * straight_exchange_rate)

    def exchange_reverse_pair(self) -> str | None:
        reverse_exchange_rate: float | None = self.model.get_exchange_rate_by_codes(
            self.parced_exchange_data.target_currency_code, self.parced_exchange_data.base_currency_code)
        if reverse_exchange_rate is None:
            return None
        straight_exchange_rate: float = 1 / reverse_exchange_rate
        return str(self.parced_exchange_data.amount * straight_exchange_rate)

    def exchange_usd_pair(self) -> str | None:
        base_to_usd_exchange_rate: float | None = self.get_exchange_rate_from_base_to_usd()
        if base_to_usd_exchange_rate is None:
            return None

        usd_to_target_exchange_rate: float | None = self.get_exchange_rate_from_usd_to_target()
        if usd_to_target_exchange_rate is None:
            return None

        return str(self.parced_exchange_data.amount * base_to_usd_exchange_rate * usd_to_target_exchange_rate)

    def get_exchange_rate_from_base_to_usd(self) -> float | None:
        base_to_usd_exchange_rate: float | None = self.model.get_exchange_rate_to_usd(
            self.parced_exchange_data.base_currency_code)
        if base_to_usd_exchange_rate is not None:
            return base_to_usd_exchange_rate

        usd_to_base_exchange_rate: float | None = self.model.get_exchange_rate_from_usd(
            self.parced_exchange_data.base_currency_code)
        if usd_to_base_exchange_rate is not None:
            return 1 / usd_to_base_exchange_rate

        return None

    def get_exchange_rate_from_usd_to_target(self) -> float | None:
        usd_to_target_exchange_rate: float | None = self.model.get_exchange_rate_from_usd(
            self.parced_exchange_data.target_currency_code)
        if usd_to_target_exchange_rate is not None:
            return usd_to_target_exchange_rate

        target_to_usd_exchange_rate = self.model.get_exchange_rate_to_usd(
            self.parced_exchange_data.target_currency_code)
        if target_to_usd_exchange_rate is not None:
            return 1 / target_to_usd_exchange_rate

        return None

    @staticmethod
    def is_empty(value: str) -> bool:
        if len(value) == 0:
            return True
        return False


class ExchangeData:
    def __init__(self, from_code: str, to_code: str, amount: int):
        self.base_currency_code: str = from_code
        self.target_currency_code: str = to_code
        self.amount: int = amount

    @staticmethod
    def from_dict(exchange_data_dict: dict):
        return ExchangeData(exchange_data_dict['fr'], exchange_data_dict['to'], exchange_data_dict['amount'])

    def exchange_data_to_dict(self) -> dict[str, str | int]:
        exchange_data_dict: dict[str, str | int] = {}
        exchange_data_dict['currency_from_code'] = self.base_currency_code
        exchange_data_dict['currency_to_code'] = self.target_currency_code
        exchange_data_dict['amount'] = self.amount
