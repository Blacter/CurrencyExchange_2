class WrongCurrenciesBody(Exception):
    def __init__(self, description: str):
        self.description: str = description
        
    def __str__(self) -> str:
        return f'Error: {self.description} should be id=6&name=Renminbi&code=CNY&sign=%C2%A5'
    
    
class BodySizeTooLarge(Exception):
    def __str__(self) -> str:
        return f'Error: body size too big'
    
class WrongExchangeRatesBody(Exception):
    def __init__(self, description: str):
        self.description: str = description
        
    def __str__(self) -> str:
        return f'Error: {self.description} should be baseCurrencyCode=Code1&targetCurrencyCode=Code2&rate=float_rate'