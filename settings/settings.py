ENCODING_TYPE: str = 'UTF-8'

class Settings:
    def __init__(self):
        self.__encoding_type: str = ENCODING_TYPE
        
    @property
    def encoding_type(self) -> str:
        return self.__encoding_type
    
    
# settings = Settings()