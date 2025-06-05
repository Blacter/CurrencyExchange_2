from abc import ABC, abstractmethod


class WrongAmountValue(Exception):
    def __str__(self) -> str:
        return f'Error: amount should be int'


class ExchangeImpossible(Exception):
    def __init__(self, from_currency_code: str, to_currency_code: str):
        self.from_currency_code: str = from_currency_code
        self.to_currency_code: str = to_currency_code
        
    def __str__(self) -> str:
        return f'Error: Can not exchange from {self.from_currency_code} to {self.to_currency_code}'
    

class WrongCurrencyParameters(Exception, ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass


class WrongCurrencyUrlKey(WrongCurrencyParameters):
    def __init__(self, parameter_name: str):
        self.parameter_name: str = parameter_name
    
    def __str__(self) -> str:
        return f'Error: parameter_name "{self.parameter_name}" should be "/exchange/fr=CODE1&to=CODE2&amoun=number"'
    
    
class WrongCurrencyUrlValue(WrongCurrencyParameters):
    def __init__(self, key: str):
        self.key: str = key
    
    def __str__(self) -> str:
        return f'Error: value with key "{self.key}" should not be empty, should be "/exchange/fr=CODE1&to=CODE2&amoun=number"'
    