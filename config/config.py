ENCODING_TYPE: str = 'UTF-8'

DATABASE_ERROR_KEY: str = 'data_base_error'

class Config:
    def __init__(self):
        self.__encoding_type: str = ENCODING_TYPE
        self.__database_error_key: str = DATABASE_ERROR_KEY
        
    @property
    def encoding_type(self) -> str:
        return self.__encoding_type
    
    @property
    def database_error_key(self) -> str:
        return self.__database_error_key
    
