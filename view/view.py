import json

class CurrencyView:
    @staticmethod
    def get_all_currencies(all_currencies: dict[int, dict]) -> str:
        return json.dumps(all_currencies)
    
    @staticmethod
    def get_currency(currency_info: dict) -> str:
        return json.dumps(currency_info)
    
    @staticmethod
    def get_all_exchange_rates(all_exchange_rates: dict[int, dict]) -> str:
        return json.dumps(all_exchange_rates)
        
    @staticmethod
    def get_exchange_rate(exchange_rate_info: dict[str, int|float|dict]) -> str:
        return json.dumps(exchange_rate_info)
    
    @staticmethod
    def get_path_not_found(path: str) -> str:
        return json.dumps({'error': f'path {path} not found'})
    
    @staticmethod
    def get_error_info(directory: str) -> str:
        error_description: str = ''
        if directory == '/currency':
            error_description = 'wrong currency code'
        elif directory == '/exchangeRate':
            error_description = 'wrong exchange rate code'
        elif directory == '/exchange':
            error_description = 'wrong query parameters, should be like "?from=USD&to=EUR&amount=10"'
            
        return json.dumps({'error_info': error_description})
    
    @staticmethod
    def get_add_currencies_result(result_add_currencies: str) -> str:
        return json.dumps({'add_currencies_result': result_add_currencies})
        
    @staticmethod
    def get_add_exchange_rates_result(result_add_exchange_rates: dict[str, int|str]) -> str:
        return json.dumps({'add_exchange_rates_result': result_add_exchange_rates})
    