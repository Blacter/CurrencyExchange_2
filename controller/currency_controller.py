from view.view import CurrencyView
from model.db_emulation import DBEmulator

from url_path.url_path import UrlPath

from controller.controller_error.currency_error import CurrencyCodeNotInUrl
from model.db_error import CurrencyNotInDB

class CurrencyController:
    def __init__(self, view: CurrencyView, model: DBEmulator, url_path: UrlPath):
        self.view: CurrencyView = view
        self.model: DBEmulator = model
        self.url_path: UrlPath = url_path
        
    def get_currency(self) -> tuple[int, str]:
        try:
            currency_code: str = self.get_currency_code()
            currency_info: dict[str, int|float] = self.model.get_currency_by_code(currency_code)                
        except CurrencyCodeNotInUrl as e:
            response_code: int = 400
            response_str: str = self.view.get_json_result('currency_get_error', str(e))
        except CurrencyNotInDB as e:
            response_code: int = 404
            response_str: str = self.view.get_json_result('currency_get_error', str(e))
        else:            
            response_code: int = 200
            response_str: str = self.view.get_currency(currency_info)
            
        return (response_code, response_str)
    
    def get_currency_code(self) -> str:
        if len(self.url_path.path_directories_list) < 2:
            raise CurrencyCodeNotInUrl()
        else:
            currency_code = self.url_path.path_directories_list[1].upper()
        return currency_code