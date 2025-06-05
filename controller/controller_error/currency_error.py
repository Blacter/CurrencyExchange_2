class CurrencyCodeNotInUrl(Exception):
    def __str__(self) -> str:
        return 'Error: no currency code in url, should be /currency/CODE'
    
class CurrencyNotExists(Exception): # FIXME: возможно лучше переместить в currency_error.
    def __init__(self, currency_code: str):
        self.currency_code: str = currency_code
    
    def __str__(self) -> str:
        return f'Error: currency code "{self.currency_code}" does not exist.'