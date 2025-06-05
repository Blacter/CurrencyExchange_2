from copy import copy

class UrlPath:
    # https://user:pass@sub.example.com:8080/p/a/t/h?query=string
    # path == '/p/a/t/h?query=string'
    # url_path_name == '/p/a/t/h'
    # query == 'query=string'
    
    def __init__(self, initial_url_path: str):
        self.__initial_url_path: str = initial_url_path
        self.__url_path_name: str | None = None
        self.__path_directories_list: list[str] | None = None
        self.__query: str | None = None
        self.__query_parameters: dict[str, str] | None = None
        
        self.split_initial_url_path()
        self.__get_url_path_directories_list()
        self.parse_query_parameters()
        
    @property
    def initial_url_path(self) -> str:
        return self.__initial_url_path
        
    @property
    def url_path_name(self) -> str | None:
        return self.__url_path_name
    
    @property
    def path_directories_list(self) -> list[str] | None:
        return copy(self.__path_directories_list)
    
    @property
    def query(self) -> str | None:
        return self.__query
    
    @property
    def query_parameters(self) -> dict[str, str] | None:
        return copy(self.__query_parameters)
        
    def split_initial_url_path(self) -> None:
        url_path = self.__initial_url_path.split('?')        
        if len(url_path) == 0:
            self.__url_path_name, self.__query = (None, None)
        elif len(url_path) == 1:
            self.__url_path_name, self.__query = (url_path[0],None)
        elif len(url_path) == 2:
            self.__url_path_name, self.__query = url_path
        
    def __get_url_path_directories_list(self) -> None:
        self.__path_directories_list = None
        if not self.is_url_path_name_empty():
            self.__path_directories_list = self.__url_path_name.split('/')
            self.__path_directories_list.pop(0)    
                    
    def is_url_path_name_empty(self) -> bool:
        return self.__url_path_name == '' or self.__url_path_name is None
        
    def parse_query_parameters(self) -> None:        
        if not self.is_url_query_empty():
            self.__query_parameters = dict()
            query_parameters_list: list[str, str] = {parameters for parameters in self.__query.split('&')}
            for parameter in query_parameters_list:                
                key, value = self.get_query_parameter_key_and_value(parameter)
                self.__query_parameters[key] = value
            
    def is_url_query_empty(self) -> bool:
        return self.__query == '' or self.__query is None
    
    def get_query_parameter_key_and_value(self, query_parameters: str) -> tuple[str, str|int]:
        key, value = query_parameters.split('=')
        return (key, value)
        
    def __str__(self):
        return f'path_name: {self.__url_path_name}\npath_directories_list: {self.__path_directories_list}\n\
    query: {self.__query}\nquery_parameters: {self.__query_parameters}'        
        
    def get_currency(self) -> str:
        return self.path_directories_list[1]    
    
    def is_in_directory(self, directory: str) -> bool:        
        if self.__path_directories_list[0] == directory.strip('/'):
            return True
        return False
    