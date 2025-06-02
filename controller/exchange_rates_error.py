class CurrencyNotExists(Exception):
    def __init__(self, currency_code: str):
        self.currency_code: str = currency_code
    
    def __str__(self) -> str:
        return f'Error: currency code "{self.currency_code}" does not exist.'