from view.view import CurrencyView
from model.model import CurrencyModel

from controller.post_data.exchange_rate_post_data import ExchangeRatePostData

from model.db_error import DBError
from controller.controller_error.currency_error import CurrencyNotExists
from model.db_error import ExchangeRatesAlreadyExists
from model.db_error import CurrencyNotInDB
from controller.controller_error.post_data_error import BodySizeTooLarge, WrongExchangeRatesBody


class ExchangeRateAddController:
    def __init__(self, view: CurrencyView, model: CurrencyModel, post_data: bytes):
        self.view: CurrencyView = view
        self.model: CurrencyModel = model
        self.exchenge_rate_post_data: ExchangeRatePostData = ExchangeRatePostData(post_data)
        
    def add_exchange_rate(self) -> tuple[int, str]:
        try:
            exchange_rate: dict[str, int|float|str] = self.exchenge_rate_post_data.get_parsed_parameters()
            self.model.add_exchange_rate(exchange_rate)
            exchange_rate_result: dict[str, int|str] = self.get_exchange_rates_result(exchange_rate) # FIXME: в таком состоянии блок try не похож на транзакцию.    
        except BodySizeTooLarge:
            response_code: int = 400
            response_str: str = self.view.get_json_result('add_exchange_error', str(e))
        except WrongExchangeRatesBody as e:
            response_code: int = 400
            response_str: str = self.view.get_json_result('add_exchange_error', str(e))
        except ExchangeRatesAlreadyExists as e:
            response_code: int = 409
            response_str: str = self.view.get_json_result('add_exchange_error', str(e))
        except CurrencyNotInDB as e: # 
            response_code: int = 404
            response_str: str = self.view.get_json_result('add_exchange_error', str(e))
        except DBError as e:
            response_code: int = 500
            response_str = self.view.get_json_result('add_exchange_error', str(e))
        else:
            response_code: int = 201            
            response_str: str = self.view.get_add_exchange_rates_result(exchange_rate_result)
        return (response_code, response_str)
        
    def get_exchange_rates_result(self, exchange_rate: dict[str, int|str]) -> dict[str, int|str]:
        base_currency_code, target_currency_code = exchange_rate['baseCurrencyCode'], exchange_rate['targetCurrencyCode']
        base_currency: int = self.model.get_currency_by_code(base_currency_code)
        target_currency: int = self.model.get_currency_by_code(target_currency_code)        
        
        exchange_rate: str = self.model.get_exchange_rate_by_currencies(base_currency, target_currency)
        exchange_rate_result: dict[str, int|float|dict] = {}
        exchange_rate_result['id'] = exchange_rate['ID']
        exchange_rate_result['baseCurrency'] = base_currency
        exchange_rate_result['targetCurrency'] = target_currency
        exchange_rate_result['rate'] = exchange_rate['Rate'] 
        
        return exchange_rate_result