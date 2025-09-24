import sqlite3 as sq

from model.db_error import CurrencyNotInDB
from config.config import Config


class DBDataWork:
    def __init__(self):
        self.__config: Config = Config()  # self.__config.db_path_name

    def get_all_currencies(self) -> list[dict[str, int | str]]:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM Currencies;')

        all_currencies_result: list[dict[str, int | str]] = []
        for currency in cur:
            all_currencies_result.append(dict(currency))

        return all_currencies_result

    def get_all_exchange_rates(self) -> list[dict[str, int | float]]:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM ExchangeRates;')

        all_currencies_result: list[dict[str, int | float]] = []
        for currency in cur:
            all_currencies_result.append(dict(currency))

        return all_currencies_result

    def get_currency_by_id(self, id: int) -> dict[str, int | str]:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM Currencies WHERE ID = ?;', (id, ))
        currency = cur.fetchone()
        if currency is None:
            raise CurrencyNotInDB(id)  # FIXME should be id, not code.
        else:
            currency_result: dict[str, int | str] = dict(currency)
        return currency_result

    def get_currency_by_code(self, code: str) -> dict[str, int | str]:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM Currencies WHERE Code = ?;', (code, ))
        currency = cur.fetchone()
        if currency is None:
            raise CurrencyNotInDB(code)
        else:
            currency_result: dict[str, int | str] = dict(currency)
        return currency_result

    def get_exchange_rate_by_currencies_ids(self, base_currency_id: int, target_currency_id: int) -> dict[str, int | float] | None:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?',
                        (base_currency_id, target_currency_id))
        exchange_rate = cur.fetchone()
        if exchange_rate is None:
            exchange_rate_result = None
            print(f'{exchange_rate_result=}')
        else:
            exchange_rate_result: dict[str, int | str] = dict(exchange_rate)
        return exchange_rate_result

    def is_currency_with_code(self, code: str) -> bool:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM Currencies WHERE Code = ?;', (code, ))
        currency = cur.fetchone()
        if currency is None:
            return False
        else:
            return True

    def add_currency(self, currency_to_add: dict[str, int | str]) -> None:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)',
                        (currency_to_add['Code'],
                         currency_to_add['FullName'],
                         currency_to_add['Sign']))
            con.commit()

    def add_exchange_rate(self, exchange_rates_to_add) -> None:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)',
                        (exchange_rates_to_add['BaseCurrencyId'],
                         exchange_rates_to_add['TargetCurrencyId'],
                         exchange_rates_to_add['Rate']))
            con.commit()

    def is_exchange_rates_exists(self, base_currency_id: int, target_currency_id: int) -> bool:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?',
                        (base_currency_id,
                         target_currency_id))
        exchange_rate = cur.fetchone()
        if exchange_rate is None:
            return False
        return True
    
    def update_exchange_rate(self, base_currency_id: int, target_currency_id: int, new_rate: float) -> None:
        with sq.connect(self.__config.db_path_name) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute('UPDATE ExchangeRates SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?',
                        (new_rate, base_currency_id, target_currency_id))
            con.commit()


if __name__ == '__main__':
    db_data_extractor: DBDataWork = DBDataWork()
    res = db_data_extractor.get_currency_by_id(10)
    print(f'{res=}')
