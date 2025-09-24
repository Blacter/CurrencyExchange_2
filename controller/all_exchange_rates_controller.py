from copy import deepcopy

from view.view import CurrencyView
from model.model import CurrencyModel

from model.db_error import DBError
from model.db_error import CurrencyNotInDB

class AllExchangeRatesController:
    def __init__(self, view: CurrencyView, model: CurrencyModel):
        self.view: CurrencyView = view
        self.model: CurrencyModel = model
    
    def get_all_exchange_rates(self) -> tuple[int, str]:
        try:            
            all_exchange_rates: dict[str, int|float] = self.model.get_all_exchange_rates()                       
            result_all_exchange_rates: list[dict] = self.get_all_exchange_rates_in_response_form(all_exchange_rates)
        except DBError as e:
            response_code: int = 500
            response_str: str = self.view.get_json_result('data_base_error', str(e))
        else: # FIXME уменьшить блок else
            response_code: int = 200
            response_str: str = self.view.get_all_exchange_rates(result_all_exchange_rates)            
        return (response_code, response_str)
    
    def get_all_exchange_rates_in_response_form(self, all_exchange_rates: list[dict[str, int|float]]) -> list[dict]:
        result_all_exchange_rates: list = []
        for exchange_rate in all_exchange_rates:
                tmp_exchange_rate: dict = self.get_exchange_rate_response_form(exchange_rate)
                result_all_exchange_rates.append(deepcopy(tmp_exchange_rate))
        return result_all_exchange_rates
    
    def get_exchange_rate_response_form(self, exchange_rate: dict[str, int|float]) -> dict[str, int|float|dict]:
        tmp_exchange_rate: dict = {}
        tmp_exchange_rate['ID'] = exchange_rate['ID']
        tmp_exchange_rate['BaseCurrency'] = self.model.get_currency_by_id(exchange_rate['BaseCurrencyId'])
        tmp_exchange_rate['TargetCurrency'] = self.model.get_currency_by_id(exchange_rate['TargetCurrencyId'])
        tmp_exchange_rate['Rate'] = exchange_rate['Rate']        
        return tmp_exchange_rate