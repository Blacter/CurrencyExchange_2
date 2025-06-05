from copy import copy, deepcopy

from model.db_error import CurrencyNotInDB, ExchangeRateNotInDB, CurrencyAlreadyExists, ExchangeRatesAlreadyExists

CURRENCIES: dict[int, dict] = {
    1 : {
            'ID': 1,
            'Code': 'USD',
            'FullName': 'US Dollar',
            'Sign': '$',
                        
        },
    2 : {
            'ID': 2,
            'Code': 'EUR',
            'FullName': 'Euro',
            'Sign': '€',
        },
    3 : {
            'ID': 3,
            'Code': 'RUB',
            'FullName': 'Russian Ruble',
            'Sign': '₽',
        },
    4 : {
            'ID': 4,
            'Code': 'CHF',
            'FullName': 'Swiss Franc',
            'Sign': '-',
        },
    5 : {
            'ID': 5,
            'Code': 'GBP',
            'FullName': 'Pound Sterling',
            'Sign': '£',
        },
}

EXCHANGE_RATES: dict[int, dict] = {
    1: {
        'ID': 1,
        'BaseCurrencyId': 2,
        'TargetCurrencyId': 1,
        'Rate': 1.1365
    },
    2: {
        'ID': 2,
        'BaseCurrencyId': 5,
        'TargetCurrencyId': 1,
        'Rate': 1.3538
    },
    3: {
        'ID': 3,
        'BaseCurrencyId': 1,
        'TargetCurrencyId': 4,
        'Rate': 0.8214
    },
    4: {
        'ID': 4,
        'BaseCurrencyId': 1,
        'TargetCurrencyId': 3,
        'Rate': 79.5
    },
    5: {
        'ID': 5,
        'BaseCurrencyId': 2,
        'TargetCurrencyId': 3,
        'Rate': 90.352
    }, 
}


class DBEmulator:
    def __init__(self):
        self.currencies: dict[int, dict] = CURRENCIES
        self.exchange_rates: dict[int, dict] = EXCHANGE_RATES
        
    def get_all_currencies(self) -> dict:
        return deepcopy(self.currencies)
    
    def get_all_exchange_rates(self) -> dict[int, dict]:
        return deepcopy(self.exchange_rates)
    
    def get_currency_by_code(self, code: str) -> dict[str, int|float|str]:
        result_currency: dict[str, int|float] | None = None
        for currency in self.currencies.values():
            if currency['Code'] == code:
                result_currency = copy(currency)
                break
        else:            
            raise CurrencyNotInDB(code)        
        return result_currency    
    
    def get_currency_id_by_code(self, code: str) -> int | None:
        currency: dict[str, int|float] | None = self.get_currency_by_code(code)
        return currency['ID']
    
    def get_currency_by_id(self, id: int) -> dict[str, int|float]:
        result_currency: dict[str, int|float] | None = None
        for currency in self.currencies.values():
            if currency['ID'] == id:
                result_currency = copy(currency)
                break
        else:            
            raise CurrencyNotInDB(id)        
        return result_currency
    
    def get_exchange_rate_by_currencies(self, base_currency: dict[str, int|float|str], target_currency: dict[str, int|float|str]) -> dict[str, int|float]:        
        result_exchange_rate: dict[str, int|float] | None = None
        for exchange_rate in self.exchange_rates.values():
            print(f'{exchange_rate = }')
            if exchange_rate['BaseCurrencyId'] == base_currency['ID'] and exchange_rate['TargetCurrencyId'] == target_currency['ID']:
                result_exchange_rate = copy(exchange_rate)
                break
        else:
            raise ExchangeRateNotInDB(base_currency['Code'], target_currency['Code'])        
        return result_exchange_rate
    
    def add_currency(self, currency: dict[str, int|str]) -> None:
        if self.is_currency_with_code_exists(currency['code']):
            raise CurrencyAlreadyExists(currency['code'])        
        new_currency_id = max(self.currencies.keys()) + 1
        currency_to_add: dict[str, int|str] = DBEmulator.get_currency_to_add(currency, new_currency_id)        
        self.currencies[new_currency_id] = copy(currency_to_add)        
        
    def is_currency_with_code_exists(self, code: str) -> None:
        is_exists: bool = False
        for currency in self.currencies.values():
            # print(f'{currency = }')
            if code == currency['Code']:
                is_exists = True
                break        
        return is_exists
    
    @staticmethod
    def get_currency_to_add(currency: dict[str, int|str], new_currency_id: int) -> dict[str, int|str]:
        currency_with_right_keys: dict[str, int|str] = {}
        currency_with_right_keys['ID'] = new_currency_id
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
        
        new_exchange_rates_id: int = self.get_new_exchange_rates_id()
        exchange_rates_to_add: int = DBEmulator.get_exchange_rates_to_add(new_exchange_rates_id, base_currency_id, target_currency_id, exchange_rate['rate'])
        
        self.exchange_rates[new_exchange_rates_id] = copy(exchange_rates_to_add)
        
    def is_exchange_rates_exists(self, base_currency_id: int, target_currency_id: int) -> bool:
        for exchange_rate in self.exchange_rates.values():
            if exchange_rate['BaseCurrencyId'] == base_currency_id and exchange_rate['TargetCurrencyId'] == target_currency_id:
                return True
        return False
    
    def get_new_exchange_rates_id(self) -> int:
        max_existing_id: int = 0
        for exchange_rate in self.exchange_rates.values():
            if max_existing_id < exchange_rate['ID']:
                max_existing_id = exchange_rate['ID']
                
        return 1 + max_existing_id
    
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
    def get_exchange_rates_to_add(new_exchange_rates_id: int, base_currency_id: int, target_currency_id: int, rate: float) -> dict[str, int|str]:
        result_exchange_rate: dict[str, int|str] = {}
        result_exchange_rate['ID'] = new_exchange_rates_id
        result_exchange_rate['BaseCurrencyId'] = base_currency_id
        result_exchange_rate['TargetCurrencyId'] = target_currency_id
        result_exchange_rate['Rate'] = rate
        
        return result_exchange_rate
        
    def update_exchange_rate(self, base_currency: dict[str, int|float|str], target_currency: dict[str, int|float|str], new_rate: float) -> None:
        exchange_rate_to_update: dict[str, int|float] = self.get_exchange_rate_by_currencies(base_currency, target_currency)
        exchange_rate_to_update['Rate'] = new_rate
        
        exchange_rate_to_update_id: int = exchange_rate_to_update['ID']
        self.exchange_rates[exchange_rate_to_update_id] = exchange_rate_to_update    
