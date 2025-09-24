import sqlite3 as sq

from config.config import Config


class DBCreator:
    def __init__(self):
        self.config: Config = Config()
        
    def create_currency_exchange_db(self):
        self.create_tables()
        self.insert_data_into_tables()

    def create_tables(self):
        with sq.connect(self.config.db_path_name) as con:
        # with sq.connect('del.db') as con:
            cur = con.cursor()
            cur.executescript(self.get_currencies_create_executescript())
            cur.executescript(self.get_exchange_rate_create_executescript())
            
    def insert_data_into_tables(self):
        with sq.connect(self.config.db_path_name) as con:
            cur = con.cursor()
            cur.executescript(self.get_currencies_data_insert_executescript())
            cur.executescript(self.get_exchange_rates_data_insert_executescript())
            
    def get_currencies_create_executescript(self) -> str:
        with open(self.config.script_path_create_currencies_table, mode='r') as executescript_file:
            return executescript_file.read()

    def get_exchange_rate_create_executescript(self) -> str:
        with open(self.config.script_path_create_exchange_rates_table, mode='r') as executescript_file:
            return executescript_file.read()
        
    def get_currencies_data_insert_executescript(self) -> str:
        with open(self.config.script_path_insert_data_into_currencies_table, mode='r') as executescript_file:
            return executescript_file.read()
    
    def get_exchange_rates_data_insert_executescript(self) -> str:
        with open(self.config.script_path_insert_data_into_exchange_table, mode='r') as executescript_file:
            return executescript_file.read()


if __name__ == '__main__':
    db_creator: DBCreator = DBCreator()
    db_creator.create_currency_exchange_db()
