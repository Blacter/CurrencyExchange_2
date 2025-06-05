class ExchangeRatesCurrenciesNotInUrl(Exception):
    def __str__(self) -> str:
        return 'Error: no exchange rates currencies in url should be /exchangeRate/USDEUR'
    
class ExchangeRatesUpdateCurrenciesNotInUrl(Exception):
    def __str__(self) -> str:
        return 'Error: no exchange rates currencies in url should be /exchangeRate/USDEUR'
    
