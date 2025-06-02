class CurrencyCodeNotInUrl(Exception):
    def __str__(self) -> str:
        return 'Error: no currency code in url, should be /currency/CODE'
    
class ExchangeRatesCurrenciesNotInUrl(Exception):
    def __str__(self) -> str:
        return 'Error: no exchange rates currencies in url should be /exchangeRate/USDEUR'