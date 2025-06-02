from controller.controller import CurrencyController
from model.model import CurrencyModel
from view.view import CurrencyView

from settings.settings import Settings

from currency_exchange import CurrencyExchange

if __name__ == '__main__':
    currency_exchange: CurrencyExchange = CurrencyExchange()
    currency_exchange.start_server()