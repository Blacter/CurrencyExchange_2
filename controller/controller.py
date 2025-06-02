from http.server import HTTPServer, BaseHTTPRequestHandler
from copy import deepcopy

from model.model import CurrencyModel
from model.db_emulation import DBEmulator
from model.db_error_handler import DBUnavailable, DBErrorHandler, CurrencyNotInDB, ExchangeRateNotInDB, CurrencyAlreadyExists
from model.db_error_handler import ExchangeRatesAlreadyExists, CurrencyCodeNoExists
from view.view import CurrencyView
from controller.url_path_processing import UrlPathProcessing
from controller.url_path_error_handler import CurrencyCodeNotInUrl, ExchangeRatesCurrenciesNotInUrl
from controller.body_handler import BodyHandler, CurrenciesBodyHandler, ExchangeRatesBodyHandler
from controller.body_error_handler import BodySizeTooLarge, WrongCurrenciesBody, WrongExchangeRatesBody
from controller.exchange_rates_error import CurrencyNotExists
from settings.settings import Settings


class CurrencyController(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.model: CurrencyModel = CurrencyModel()
        self.view: CurrencyView = CurrencyView()
        self.setting: Settings = Settings()
        super().__init__(request, client_address, server)
        
    def get_currency_code(self) -> str:
        if len(self.url_path.path_directories_list) < 2: # or len(self.url_path.path_directories_list[1]) != 0
            raise CurrencyCodeNotInUrl()
        else:
            currency_code = self.url_path.path_directories_list[1].upper()
        return currency_code
    
    def get_parsed_exchange_rate_currencies(self) -> tuple[str]:
        if len(self.url_path.path_directories_list) < 2:
            raise ExchangeRatesCurrenciesNotInUrl()
        else:
            base_currency_code: int = self.url_path.path_directories_list[1][:3]
            target_currency_code: int = self.url_path.path_directories_list[1][3:]
        return (base_currency_code, target_currency_code)
        
                
    def do_GET(self):
        self.model: DBEmulator = DBEmulator()
        self.view: CurrencyView = CurrencyView()
        self.setting: Settings = Settings()        
        
        self.url_path: UrlPathProcessing | None = UrlPathProcessing(self.path)
        print('GET', (self.url_path))
        
        if self.url_path.is_in_directory('/currencies'): 
            responde_str: str = self.get_all_currencies()
        elif self.url_path.is_in_directory('/currency'):            
            responde_str: str = self.get_currency()            
        elif self.url_path.is_in_directory('/exchangeRates'):
            responde_str: str = self.get_all_exchange_rates()
        elif self.url_path.is_in_directory('/exchangeRate'): # and len(self.url_path.path_directories_list) == 2   
            responde_str: str = self.get_exchange_rate()  
        elif self.url_path.is_in_directory('/exchange'):
            pass
        else:
            responde_str: str = self.page_not_found()
            
        self.send_header('Content-type', 'application/json')
        self.end_headers()
            
        self.wfile.write(responde_str.encode(Settings().encoding_type))
        
    def do_POST(self):
        self.model: DBEmulator = DBEmulator()
        self.view: CurrencyView = CurrencyView()
        self.setting: Settings = Settings()
                
        self.url_path: UrlPathProcessing | None = UrlPathProcessing(self.path)
        
        content_length = int(self.headers['Content-Length'])
        self.post_data = self.rfile.read(content_length)
                
        if self.url_path.is_in_directory('/currencies'):            
            result_add_currencies: str = self.add_currencies()
            responde_str: str = self.view.get_add_currencies_result(result_add_currencies)
        elif self.url_path.is_in_directory('/exchangeRates'):
            result_add_exchange_rates: str = self.add_exchange_rates()
            responde_str: str = self.view.get_add_exchange_rates_result(result_add_exchange_rates)
        else:
            responde_str: str = self.page_not_found()
            
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(responde_str.encode(Settings().encoding_type))
        
    def do_PATCH(self):
        content_length = int(self.headers.get('Content-Length', 0))
        patch_data = self.rfile.read(content_length)

        # Здесь можно обновить нужные данные
        print("Получены данные PATCH:", patch_data.decode())

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"PATCH ")    
    
    def get_all_currencies(self) -> str:
        try:
            all_currencies_info: dict[int, dict] = self.model.get_all_currencies()
            responde_str: str = self.view.get_all_currencies(all_currencies_info)   
        except : # Ошибка БД.
            pass
        else:
            self.send_response(200)
            
        return responde_str
                
    def get_currency(self) -> str:
        try:
            currency_code: str = self.get_currency_code()
            if currency_code is not None:
                currency_info: dict[str, int|float] = self.model.get_currency_by_code(currency_code)
                responde_str: str = self.view.get_currency(currency_info)
        except CurrencyCodeNotInUrl as e:
            self.send_response(400)
            responde_str: str = str(e)
        except CurrencyNotInDB as e:
            self.send_response(404)
            responde_str: str = str(e)
        else:            
            self.send_response(200)  
        return responde_str
    
    def get_all_exchange_rates(self) -> str:
        try:
            result_all_exchange_rates: list = []
            all_exchange_rates: dict[str, int|float] = self.model.get_all_exchange_rates()
            tmp_exchange_rate: dict = {}
            for exchange_rate in all_exchange_rates.values():
                tmp_exchange_rate['id'] = exchange_rate['ID']
                tmp_exchange_rate['baseCurrency'] = self.model.get_currency_by_id(exchange_rate['BaseCurrencyId'])
                tmp_exchange_rate['targetCurrency'] = self.model.get_currency_by_id(exchange_rate['TargetCurrencyId'])
                tmp_exchange_rate['rate'] = exchange_rate['Rate']
                result_all_exchange_rates.append(deepcopy(tmp_exchange_rate))
            responde_str: str = self.view.get_all_exchange_rates(result_all_exchange_rates)
        except CurrencyNotInDB as e:
            self.send_response(404)
            responde_str: str = str(e)
        else:
            self.send_response(200)         
        return responde_str
    
    def get_exchange_rate(self) -> str:
        try:
            base_currency_code, target_currency_code = self.get_parsed_exchange_rate_currencies()            
            base_currency: int = self.model.get_currency_by_code(base_currency_code)
            target_currency: int = self.model.get_currency_by_code(target_currency_code)           
            
            exchange_rate: str = self.model.get_exchange_rate_by_currencies(base_currency, target_currency)
            exchange_rate_info: dict[str, int|float|dict] = {}
            exchange_rate_info['id'] = exchange_rate['ID']
            exchange_rate_info['baseCurrency'] = base_currency
            exchange_rate_info['targetCurrency'] = target_currency
            exchange_rate_info['rate'] = exchange_rate['Rate']            
            
            respond_str: str = self.view.get_exchange_rate(exchange_rate_info)
        except ExchangeRatesCurrenciesNotInUrl as e:
            self.send_response(400)
            respond_str: str = str(e)
        except CurrencyNotInDB as e:
            self.send_response(404)
            respond_str: str = str(e)        
        except ExchangeRateNotInDB as e:
            self.send_response(404)
            respond_str: str = str(e)            
        else:
            self.send_response(200)
        return respond_str
    
    def page_not_found(self) -> str:
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        return self.view.get_path_not_found(self.url_path.initial_url_path)
    
    def add_currencies(self) -> str:
        try:
            self.body_handler: CurrenciesBodyHandler = CurrenciesBodyHandler(self.post_data)
            currency: dict[str, int|str] = self.body_handler.get_parsed_parameters()
            self.model.add_currency(currency)
            respond_str: str = 'currency successfully added.'
        except BodySizeTooLarge as e:
            self.send_response(400)
            respond_str: str = str(e)
        except WrongCurrenciesBody as e:
            self.send_response(400)
            respond_str: str = str(e)
        except CurrencyAlreadyExists as e:
            self.send_response(409)
            respond_str: str = str(e)
        except DBUnavailable as e:
            respond_str: str = str(e)
        else:
            self.send_response(201)            
        return respond_str
            
    def add_exchange_rates(self) -> dict[str, int|str] | str:
        try:
            self.body_handler: ExchangeRatesBodyHandler = ExchangeRatesBodyHandler(self.post_data)
            exchange_rate: dict[str, int|str] = self.body_handler.get_parsed_parameters()
            self.check_currency_code_exists(exchange_rate)
            self.model.add_exchange_rate(exchange_rate)
            exchange_rate_result: dict[str, int|str] = self.get_exchange_rates_result(exchange_rate)
        except BodySizeTooLarge:
            self.send_response(400)
            exchange_rate_result: str = str(e)
        except WrongExchangeRatesBody as e:
            self.send_response(400)
            exchange_rate_result: str = str(e)
        except ExchangeRatesAlreadyExists as e:
            self.send_response(409)
            exchange_rate_result: str = str(e)
        except CurrencyNotExists as e:
            self.send_response(404)
            exchange_rate_result: str = str(e)
        else:
            self.send_response(201)
        return exchange_rate_result
    
    def check_currency_code_exists(self, exchange_rate: dict[str, int|str]) -> None:
        if not self.model.is_currency_with_code_exists(exchange_rate['baseCurrencyCode']):
            raise CurrencyNotExists(exchange_rate['baseCurrencyCode'])
        if not self.model.is_currency_with_code_exists(exchange_rate['targetCurrencyCode']):
            raise CurrencyNotExists(exchange_rate['targetCurrencyCode'])
        
    def get_exchange_rates_result(self, exchange_rate: dict[str, int|str]) -> dict[str, int|str]:
        base_currency_code, target_currency_code = exchange_rate['baseCurrencyCode'], exchange_rate['targetCurrencyCode']
        base_currency: int = self.model.get_currency_by_code(base_currency_code)
        target_currency: int = self.model.get_currency_by_code(target_currency_code)        
        
        exchange_rate: str = self.model.get_exchange_rate_by_currencies(base_currency, target_currency)
        exchange_rate_result: dict[str, int|float|dict] = {}
        exchange_rate_result['id'] = exchange_rate['ID']
        exchange_rate_result['baseCurrency'] = base_currency
        exchange_rate_result['targetCurrency'] = target_currency
        exchange_rate_result['rate'] = exchange_rate['Rate'] 
        
        return exchange_rate_result