from view.view import CurrencyView
from model.db_emulation import DBEmulator

from model.db_error import DBError


class AllCurrenciesController:
    def __init__(self, view: CurrencyView, model: DBEmulator):
        self.view: CurrencyView = view
        self.model: DBEmulator = model

    def get_all_currencies(self) -> tuple[int, str]:
        response_code, response_str = self.get_all_currencies_from_db()

        return (response_code, response_str)

    def get_all_currencies_from_db(self) -> tuple[int, str]:
        try:
            all_currencies_info: dict[int,
                                      dict] = self.model.get_all_currencies()
        except DBError as e:  # Ошибка БД.
            response_code: int = 500
            response_str = self.view.get_json_result('data_base_error', str(e))
            pass
        else:
            response_code: int = 200
            response_str = self.view.get_all_currencies(all_currencies_info)
            
        return (response_code, response_str)
