from abc import ABC, abstractmethod


class DBError(Exception, ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class CurrencyNotInDB(DBError):
    def __init__(self, *args):
        self.currency_code = args[0]

    def __str__(self) -> str:
        return f'Error: currency with code "{self.currency_code}" not found'


class ExchangeRateNotInDB(DBError):
    def __init__(self, *args):
        self.base_currency_code = args[0]
        self.target_currency_code = args[1]

    def __str__(self, *args):
        return f'Error: exchange rate from "{self.base_currency_code}" to "{self.target_currency_code}" not found'


class CurrencyCodeNoExists(Exception):
    pass


class DBUnavailable(DBError):
    def __str__(self):
        return f'Error: database unvavailable.'


class CurrencyAlreadyExists(Exception):
    def __init__(self, *args):
        self.currency_code: str = args[0]

    def __str__(self) -> str:
        return f'Error: currency with code "{self.currency_code}" already exists.'


class ExchangeRatesAlreadyExists(Exception):
    def __init__(self, baseCurrencyCode: str, targetCurrencyCode: str):
        self.baseCurrencyCode: str = baseCurrencyCode
        self.targetCurrencyCode: str = targetCurrencyCode

    def __str__(self) -> str:
        return f'Error: exchange rate "{self.baseCurrencyCode} {self.targetCurrencyCode}" already exists.'
