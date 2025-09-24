from copy import copy, deepcopy

from config.config import Config
from model.db_data_work import DBDataWork
from model.db_error import CurrencyNotInDB, ExchangeRateNotInDB, CurrencyAlreadyExists, ExchangeRatesAlreadyExists


class CurrencyModel:
    def __init__(self):
        self.__config: Config = Config()
        self.db_data_work: DBDataWork = DBDataWork()
        
    def get_all_currencies(self) -> dict:
        return deepcopy(self.db_data_work.get_all_currencies())
    
    def get_all_exchange_rates(self) -> dict[int, dict]:
        return deepcopy(self.db_data_work.get_all_exchange_rates())
    
    def get_currency_by_code(self, code: str) -> dict[str, int|float|str]:
        result_currency: dict[str, int|float] | None = None
        result_currency: dict[str, int|float] = self.db_data_work.get_currency_by_code(code)  
        return result_currency    
    
    def get_currency_id_by_code(self, code: str) -> int | None:
        currency: dict[str, int|float] | None = self.get_currency_by_code(code)
        return currency['ID']
    
    def get_currency_by_id(self, id: int) -> dict[str, int|float]:
        result_currency: dict[str, int|float] | None = None
        result_currency = self.db_data_work.get_currency_by_id(id)
        return result_currency
    
    def get_exchange_rate_by_currencies(self, base_currency: dict[str, int|float|str], target_currency: dict[str, int|float|str]) -> dict[str, int|float]:        
        result_exchange_rate: dict[str, int|float] | None = None
        result_exchange_rate = self.db_data_work.get_exchange_rate_by_currencies_ids(base_currency['ID'], target_currency['ID'])        
        if result_exchange_rate is None:
            raise ExchangeRateNotInDB(base_currency['Code'], target_currency['Code'])        
        return result_exchange_rate
    
    def add_currency(self, currency: dict[str, int|str]) -> None:
        if self.is_currency_with_code_exists(currency['code']):
            raise CurrencyAlreadyExists(currency['code'])        
        # new_currency_id = max(self.currencies.keys()) + 1
        
        currency_to_add: dict[str, int|str] = CurrencyModel.get_currency_to_add(currency)        
        self.db_data_work.add_currency(currency_to_add)        
        
    def is_currency_with_code_exists(self, code: str) -> None:
        is_exists: bool = self.db_data_work.is_currency_with_code(code)
        return is_exists
    
    @staticmethod
    def get_currency_to_add(currency: dict[str, int|str]) -> dict[str, int|str]:
        currency_with_right_keys: dict[str, int|str] = {}
        currency_with_right_keys['Code'] = currency['code']
        currency_with_right_keys['FullName'] = currency['name']
        currency_with_right_keys['Sign'] = currency['sign']
        return currency_with_right_keys        
    
    def add_exchange_rate(self, exchange_rate: dict[str, int|str]) -> None:
        base_currency_code: str = exchange_rate['baseCurrencyCode']
        target_currency_code: str = exchange_rate['targetCurrencyCode']
        
        base_currency_id: int = self.get_currency_id_by_code(base_currency_code)
        target_currency_id: int = self.get_currency_id_by_code(target_currency_code)
                
        if self.is_exchange_rates_exists(base_currency_id, target_currency_id):
            raise ExchangeRatesAlreadyExists(base_currency_code, target_currency_code)        

        exchange_rates_to_add: int = CurrencyModel.get_exchange_rates_to_add(base_currency_id, target_currency_id, exchange_rate['rate'])
        self.db_data_work.add_exchange_rate(exchange_rates_to_add)
        
    def is_exchange_rates_exists(self, base_currency_id: int, target_currency_id: int) -> bool:
        if self.db_data_work.is_exchange_rates_exists(base_currency_id, target_currency_id):        
                return True
        return False
    
    def get_exchange_rate_by_codes(self, base_currency_code: str, target_currency_code: str) -> float | None:
        try:
            base_currency: dict[str, int|float|str] = self.get_currency_by_code(base_currency_code)
            target_currency: dict[str, int|float|str] = self.get_currency_by_code(target_currency_code)
            
            exchange_rate_info: dict[str, int|float] = self.get_exchange_rate_by_currencies(base_currency, target_currency)
        except ExchangeRateNotInDB:
            result_exchange_rate = None
        else:
            result_exchange_rate = exchange_rate_info['Rate']
            
        return result_exchange_rate
            
    def get_exchange_rate_to_usd(self, base_currency_code: str) -> float | None:
        return self.get_exchange_rate_by_codes(base_currency_code, 'USD')

    def get_exchange_rate_from_usd(self, target_currency_code: str) -> float | None:
        return self.get_exchange_rate_by_codes('USD', target_currency_code)
    
    @staticmethod
    def get_exchange_rates_to_add(base_currency_id: int, target_currency_id: int, rate: float) -> dict[str, int|str]:
        result_exchange_rate: dict[str, int|str] = {}
        result_exchange_rate['BaseCurrencyId'] = base_currency_id
        result_exchange_rate['TargetCurrencyId'] = target_currency_id
        result_exchange_rate['Rate'] = rate
        
        return result_exchange_rate
        
    def update_exchange_rate(self, base_currency: dict[str, int|float|str], target_currency: dict[str, int|float|str], new_rate: float) -> None:
        exchange_rate_to_update: dict[str, int|float] = self.get_exchange_rate_by_currencies(base_currency, target_currency)
        exchange_rate_to_update['Rate'] = new_rate
        
        if not self.db_data_work.is_exchange_rates_exists(base_currency['ID'], target_currency['ID']):
            raise ExchangeRateNotInDB(base_currency['Code'], target_currency['Code'])
        
        self.db_data_work.update_exchange_rate(base_currency['ID'], target_currency['ID'], new_rate)
         