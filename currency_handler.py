from http.server import HTTPServer, BaseHTTPRequestHandler
from copy import deepcopy

from model.model import CurrencyModel
from model.db_emulation import DBEmulator
from view.view import CurrencyView
from url_path.url_path import UrlPath

from controller.controller import Controller
from controller.all_currencies_controller import AllCurrenciesController
from controller.currency_controller import CurrencyController
from controller.all_exchange_rates_controller import AllExchangeRatesController
from controller.exchange_rate_controller import ExchangeRateController
from controller.currency_add_controller import CurrencyAddController
from controller.exchange_rate_add_controller import ExchangeRateAddController
from controller.exchange_controller import ExchangeController
from controller.exchange_rate_update_controller import ExchangeRateUpdateController

from config.config import Config


class CurrencyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        # self.model: CurrencyModel = CurrencyModel()
        self.view: CurrencyView = CurrencyView()
        self.model: CurrencyModel = DBEmulator()
        self.controller: Controller = Controller(self.view, self.model)
        self.config: Config = Config()
        super().__init__(request, client_address, server)        
                    
    def do_GET(self):
        self.url_path: UrlPath | None = UrlPath(self.path)
        
        if self.url_path.is_in_directory('/currencies'): 
            all_currencies_controller: AllCurrenciesController = self.controller.get_all_currencies_controller()
            responde_code, responde_str = all_currencies_controller.get_all_currencies()
            
        elif self.url_path.is_in_directory('/currency'):
            currency_controller: CurrencyController = self.controller.get_currency_controller(self.url_path)
            responde_code, responde_str = currency_controller.get_currency()
        elif self.url_path.is_in_directory('/exchangeRates'):
            all_exchange_rates_controller: AllExchangeRatesController = self.controller.get_all_exchange_rates_controller()
            responde_code, responde_str = all_exchange_rates_controller.get_all_exchange_rates()
        elif self.url_path.is_in_directory('/exchangeRate'):
            exchange_rate_controller: ExchangeRateController = self.controller.get_exchange_rate_controller(self.url_path)
            responde_code, responde_str = exchange_rate_controller.get_exchange_rate()
        elif self.url_path.is_in_directory('/exchange'):
            exchange_controller: ExchangeController = self.controller.get_exchange_controller(self.url_path)
            responde_code, responde_str = exchange_controller.get_exchange()
        else:
            responde_code: int = 200
            responde_str: str = self.page_not_found()
            
            
        self.send_response(responde_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
            
        self.wfile.write(responde_str.encode(self.config.encoding_type))
        
    def do_POST(self):
        self.url_path: UrlPath | None = UrlPath(self.path)        
        
        content_length = int(self.headers['Content-Length']) # FIXME: Выделить в метод read_post_data
        self.post_data: bytes = self.rfile.read(content_length) # FIXME: Выделить в метод read_post_data 
                
        if self.url_path.is_in_directory('/currencies'):                        
            currency_add_controller: CurrencyAddController = self.controller.get_currency_add_controller(self.post_data)
            responde_code, responde_str = currency_add_controller.add_currency()            
        elif self.url_path.is_in_directory('/exchangeRates'):            
            exchange_rate_add_controller: ExchangeRateAddController = self.controller.get_exchange_rate_add_controller(self.post_data)
            responde_code, responde_str = exchange_rate_add_controller.add_exchange_rate()
        else:
            responde_code: int = 404
            responde_str: str = self.page_not_found()
            
        self.send_response(responde_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(responde_str.encode(self.config.encoding_type))
        
    def do_PATCH(self):
        self.url_path: UrlPath | None = UrlPath(self.path) 
        
        content_length = int(self.headers.get('Content-Length', 0))
        self.patch_data = self.rfile.read(content_length)
        
        if self.url_path.is_in_directory('/exchangeRate'):
            exchange_rate_update_controller: ExchangeRateUpdateController = self.controller.get_exchange_rate_update_controller(self.url_path, self.patch_data)
            responde_code, responde_str = exchange_rate_update_controller.update_exchange_rate()
        else:
            responde_code: int = 404
            responde_str: str = self.page_not_found()

        self.send_response(responde_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(responde_str.encode(self.config.encoding_type))
    
    def page_not_found(self) -> str: # FIXME ? Убрать ли эту функцию в controller, если да то в какой класс ?
        return self.view.get_path_not_found(self.url_path.initial_url_path)
               