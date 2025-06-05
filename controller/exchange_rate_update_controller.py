from copy import copy

from view.view import CurrencyView
from model.db_emulation import DBEmulator
from url_path.url_path import UrlPath
from controller.post_data.exchange_rate_update_post_data import ExchangeRateUpdatePostData

from model.db_error import DBError
from controller.controller_error.exchange_rates_error import ExchangeRatesUpdateCurrenciesNotInUrl
from controller.controller_error.post_data_error import BodySizeTooLarge, WrongExchangeRatesBody
from controller.controller_error.currency_error import CurrencyNotExists
from model.db_error import ExchangeRatesAlreadyExists



class ExchangeRateUpdateController:
    def __init__(self, view: CurrencyView, model: DBEmulator, url_path: UrlPath, post_data: bytes):
        self.view: CurrencyView = view
        self.model: DBEmulator = model
        self.url_path: UrlPath = url_path
        self.exchenge_rate_update_post_data: ExchangeRateUpdatePostData = ExchangeRateUpdatePostData(post_data)
        
    def update_exchange_rate(self) -> tuple[int, str]:
        try:
            self.get_exchange_rate_update_info()
            self.update_exchane_rate_in_db()
            exchange_rate_result: dict[str, int|str] = self.get_exchange_rates_update_result() # FIXME: в таком состоянии блок try не похож на транзакцию.
        except ExchangeRatesUpdateCurrenciesNotInUrl as e:
            response_code: int = 400
            response_str: str = self.view.get_json_result('update_exchange_error', str(e))
        except BodySizeTooLarge:
            response_code: int = 400
            response_str: str = self.view.get_json_result('update_exchange_error', str(e))
        except WrongExchangeRatesBody as e:
            response_code: int = 400
            response_str: str = self.view.get_json_result('update_exchange_error', str(e))
        except ExchangeRatesAlreadyExists as e:
            response_code: int = 409
            response_str: str = self.view.get_json_result('update_exchange_error', str(e))
        except CurrencyNotExists as e:
            response_code: int = 404
            response_str: str = self.view.get_json_result('update_exchange_error', str(e))
        except DBError as e: # DBError
            response_code: int = 500
            response_str: str = self.view.get_json_result('update_exchange_error', str(e))
        else:
            response_code: int = 200            
            response_str: str = self.view.get_add_exchange_rates_update_result(exchange_rate_result)
        
        return (response_code, response_str)
        
    def get_exchange_rate_update_info(self) -> None:
        self.exchange_rate_update_info: ExchangeRateUpdateInfo = ExchangeRateUpdateInfo()
        
        base_currency_code, target_currency_code = self.get_parsed_exchange_rate_currencies_from_url()
        self.exchange_rate_update_info.base_currency = self.model.get_currency_by_code(base_currency_code)
        self.exchange_rate_update_info.target_currency = self.model.get_currency_by_code(target_currency_code)     
        
        self.exchange_rate_update_info.rate = self.exchenge_rate_update_post_data.get_parsed_parameters()['rate']
        
    def get_parsed_exchange_rate_currencies_from_url(self) -> tuple[str, str]:
        if len(self.url_path.path_directories_list) < 2:
            raise ExchangeRatesUpdateCurrenciesNotInUrl()
        else:
            base_currency_code: int = self.url_path.path_directories_list[1][:3]
            target_currency_code: int = self.url_path.path_directories_list[1][3:]
        return (base_currency_code, target_currency_code)
        
    def update_exchane_rate_in_db(self) -> None:
        base_currency: str = self.exchange_rate_update_info.base_currency
        target_currency: str = self.exchange_rate_update_info.target_currency
        new_rate: float = self.exchange_rate_update_info.rate
        self.model.update_exchange_rate(base_currency, target_currency, new_rate)
        
    def get_exchange_rates_update_result(self) -> dict[str, int|str]:        
        base_currency = self.exchange_rate_update_info.base_currency
        target_currency = self.exchange_rate_update_info.target_currency
        
        exchange_rate: str = self.model.get_exchange_rate_by_currencies(base_currency, target_currency)
        exchange_rate_result: dict[str, int|float|dict] = {}
        exchange_rate_result['id'] = exchange_rate['ID']
        exchange_rate_result['baseCurrency'] = base_currency
        exchange_rate_result['targetCurrency'] = target_currency
        exchange_rate_result['rate'] = exchange_rate['Rate'] 
        
        return exchange_rate_result
    
class ExchangeRateUpdateInfo:
    def __init__(self):
        self.__base_currency: dict[str, int|float|str] | None = None
        self.__target_currency: dict[str, int|float|str] | None = None
        self.__rate: float | None = None
        
    @property
    def base_currency(self) -> dict[str, int|float|str] | None:
        return copy(self.__base_currency)
        
    @base_currency.setter
    def base_currency(self, base_currency: dict[str, int|float|str]) -> None:
        self.__base_currency = copy(base_currency)
        
    @property
    def target_currency(self) -> dict[str, int|float|str] | None:
        return copy(self.__target_currency)
    
    @target_currency.setter
    def target_currency(self, target_currency: dict[str, int|float|str]) -> None:
        self.__target_currency = copy(target_currency)
        
    @property
    def rate(self) -> float | None:
        return self.__rate
    
    @rate.setter
    def rate(self, rate_value: float) -> None:
        self.__rate = rate_value
        
    def get_base_currency_code(self) -> str:
        return self.__base_currency['Code']
    
    def get_target_currency_code(self) -> str:
        return self.__target_currency['Code']
        