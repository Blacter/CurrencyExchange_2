from view.view import CurrencyView
from model.model import CurrencyModel

from url_path.url_path import UrlPath

from controller.all_currencies_controller import AllCurrenciesController
from controller.currency_controller import CurrencyController
from controller.all_exchange_rates_controller import AllExchangeRatesController
from controller.exchange_rate_controller import ExchangeRateController
from controller.currency_add_controller import CurrencyAddController
from controller.exchange_rate_add_controller import ExchangeRateAddController
from controller.exchange_controller import ExchangeController
from controller.exchange_rate_update_controller import ExchangeRateUpdateController

class Controller:
    def __init__(self, view: CurrencyView, model: CurrencyModel):
        self.view: CurrencyView = view
        self.model: CurrencyModel = model
    
    def get_all_currencies_controller(self) -> AllCurrenciesController:
        return AllCurrenciesController(self.view, self.model)
    
    def get_currency_controller(self, url_path: UrlPath) -> CurrencyController:
        return CurrencyController(self.view, self.model, url_path)
    
    def get_all_exchange_rates_controller(self) -> AllExchangeRatesController:
        return AllExchangeRatesController(self.view, self.model)
    
    def get_exchange_rate_controller(self, url_path: UrlPath) -> ExchangeRateController:
        return ExchangeRateController(self.view, self.model, url_path)
    
    def get_currency_add_controller(self, post_data: bytes) -> CurrencyAddController:
        return CurrencyAddController(self.view, self.model, post_data)
    
    def get_exchange_rate_add_controller(self, post_data: bytes) -> ExchangeRateAddController:
        return ExchangeRateAddController(self.view, self.model, post_data)
    
    def get_exchange_controller(self, url_path: UrlPath) -> ExchangeController:
        return ExchangeController(self.view, self.model, url_path)
    
    def get_exchange_rate_update_controller(self, url_path: UrlPath, post_data: bytes) -> ExchangeRateUpdateController:
        return ExchangeRateUpdateController(self.view, self.model, url_path, post_data)