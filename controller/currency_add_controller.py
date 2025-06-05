from view.view import CurrencyView
from model.db_emulation import DBEmulator

from controller.post_data.currency_post_data import CurrencyPostData

from model.db_error import DBError
from model.db_error import CurrencyAlreadyExists
from controller.controller_error.post_data_error import BodySizeTooLarge, WrongCurrenciesBody

class CurrencyAddController:
    def __init__(self, view: CurrencyView, model: DBEmulator, post_data: bytes):
        self.view: CurrencyView = view
        self.model: DBEmulator = model
        self.currency_post_data: CurrencyPostData = CurrencyPostData(post_data)
        
    def add_currency(self) -> tuple[int, str]:
        try :
            currency: dict[str, int|str] = self.currency_post_data.get_parsed_parameters()
            self.model.add_currency(currency)            
        except BodySizeTooLarge as e:
            response_code: int = 400
            result_add_currencies: str = self.view.get_json_result('currency_add_error', str(e))
        except WrongCurrenciesBody as e:
            response_code: int = 400
            result_add_currencies: str = self.view.get_json_result('currency_add_error', str(e))
        except CurrencyAlreadyExists as e:
            response_code: int = 409
            result_add_currencies: str = self.view.get_json_result('currency_add_error', str(e))
        except DBError as e:
            response_code: int = 500
            result_add_currencies: str = self.view.get_json_result('currency_add_error', str(e))
        else:
            response_code: int = 201
            result_add_currencies: str = self.view.get_json_result('result', 'currency successfully added.')
        
        response_str = self.view.get_add_currencies_result(result_add_currencies)
        return (response_code, response_str)