from view.view import CurrencyView
from model.model import CurrencyModel

from url_path.url_path import UrlPath

from controller.controller_error.exchange_rates_error import ExchangeRatesCurrenciesNotInUrl
from model.db_error import DBError

class ExchangeRateController():
    def __init__(self, view: CurrencyView, model: CurrencyModel, url_path: UrlPath):
        self.view: CurrencyView = view
        self.model: CurrencyModel = model
        self.url_path: UrlPath = url_path
        
    def get_exchange_rate(self) -> tuple[int, str]:
        try:
            base_currency_code, target_currency_code = self.get_parsed_exchange_rate_currencies_from_url()            
            base_currency: int = self.model.get_currency_by_code(base_currency_code)
            target_currency: int = self.model.get_currency_by_code(target_currency_code)
            
            exchange_rate: str = self.model.get_exchange_rate_by_currencies(base_currency, target_currency)            
        except ExchangeRatesCurrenciesNotInUrl as e:
            response_code: int = 400
            response_str: str = self.view.get_json_result('get_exchange_error', str(e))
        except DBError as e: # DBError
            response_code: int = 500
            response_str: str = self.view.get_json_result('get_exchange_error', str(e))
        else:
            response_code: int = 200
            exchange_rate_info: dict[str, int|float|dict] = self.put_currencies_in_response(exchange_rate)
            response_str: str = self.view.get_exchange_rate(exchange_rate_info)
            
        return (response_code, response_str)
    
    def get_parsed_exchange_rate_currencies_from_url(self) -> tuple[str, str]:
        if len(self.url_path.path_directories_list) < 2:
            raise ExchangeRatesCurrenciesNotInUrl()
        else:
            base_currency_code: int = self.url_path.path_directories_list[1][:3]
            target_currency_code: int = self.url_path.path_directories_list[1][3:]
        return (base_currency_code, target_currency_code)
    
    def put_currencies_in_response(self, exchange_rate) -> dict[str, int|float|dict]: # FIXME: Дублируется с get_exchange_rate_response_form из all_exchange_rates_controller.
        tmp_exchange_rate: dict = {}
        tmp_exchange_rate['ID'] = exchange_rate['ID']
        tmp_exchange_rate['BaseCurrency'] = self.model.get_currency_by_id(exchange_rate['BaseCurrencyId'])
        tmp_exchange_rate['TargetCurrency'] = self.model.get_currency_by_id(exchange_rate['TargetCurrencyId'])
        tmp_exchange_rate['Rate'] = exchange_rate['Rate']        
        return tmp_exchange_rate