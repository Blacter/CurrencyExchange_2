ENCODING_TYPE: str = 'UTF-8'

DATABASE_ERROR_KEY: str = 'data_base_error'
DB_PATH: str = 'model'
DB_NAME: str = 'currency_exchange_db.db'
SCRIPT_PATH_CREATE_CURRENCIES_TABLE = 'create_db/create_currencies.sql'
SCRIPT_PATH_CREATE_EXCHANGE_RATES = 'create_db/create_exchange_rates.sql'
SCRIPT_PATH_INSERT_DATA_INTO_CURRENCIES_TABLE = 'create_db/insert_data_into_currencies.sql'
SCRIPT_PATH_INSERT_DATA_INTO_EXCHANGE_TABLE = 'create_db/insert_data_into_exchange_rates.sql'
ACCESS_CONTROLL_ALLOW_ORIGIN_VALUE = 'http://localhost'



class Config:
    def __init__(self):
        self.__encoding_type: str = ENCODING_TYPE
        self.__database_error_key: str = DATABASE_ERROR_KEY
        self.__db_path: str = DB_PATH
        self.__db_name: str = DB_NAME
        self.__db_path_name: str = DB_PATH + '/' + DB_NAME
        self.__script_path_create_currencies_table : str = SCRIPT_PATH_CREATE_CURRENCIES_TABLE
        self.__script_path_create_exchange_rates : str = SCRIPT_PATH_CREATE_EXCHANGE_RATES
        self.__script_path_insert_data_into_currencies_table : str = SCRIPT_PATH_INSERT_DATA_INTO_CURRENCIES_TABLE
        self.__script_path_insert_data_into_exchange_table : str = SCRIPT_PATH_INSERT_DATA_INTO_EXCHANGE_TABLE
        self.__access_controll_allow_origin_value: str = ACCESS_CONTROLL_ALLOW_ORIGIN_VALUE
        
    @property
    def encoding_type(self) -> str:
        return self.__encoding_type
    
    @property
    def database_error_key(self) -> str:
        return self.__database_error_key
    
    @property
    def db_path(self) -> str:
        return self.__db_path
    
    @property
    def db_name(self) -> str:
        return self.__db_name
    
    @property
    def db_path_name(self) -> str:
        return self.__db_path_name
    
    @property
    def script_path_create_currencies_table(self) -> str:
        return self.__script_path_create_currencies_table
    
    @property
    def script_path_create_exchange_rates_table(self) -> str:
        return self.__script_path_create_exchange_rates
    
    @property
    def script_path_insert_data_into_currencies_table(self) -> str:
        return self.__script_path_insert_data_into_currencies_table
    
    @property
    def script_path_insert_data_into_exchange_table(self) -> str:
        return self.__script_path_insert_data_into_exchange_table
    
    @property
    def access_controll_allow_origin_value(self) -> str:
        return self.__access_controll_allow_origin_value