import json

class CurrencyView:
    @staticmethod
    def get_all_currencies(all_currencies: list[dict] | None) -> str:
        all_currencies = CurrencyView.write_all_currencies_in_response_format(all_currencies)
        return json.dumps(all_currencies)
    
    @staticmethod
    def write_all_currencies_in_response_format(all_currencies: list[dict] | None) -> list[dict]:
        all_currencies_result: list[dict] = []
        for currency in all_currencies:
            all_currencies_result.append(CurrencyView.write_currency_in_response_format(currency))
        return all_currencies_result    
    
    @staticmethod
    def get_currency(currency_info: dict) -> str:
        currency_info: dict = CurrencyView.write_currency_in_response_format(currency_info)
        return json.dumps(currency_info)
    
    @staticmethod
    def write_currency_in_response_format(currency_info: dict) -> dict:
        result_currency: dict = {}
        result_currency['id'] = currency_info['ID']
        result_currency['name'] = currency_info['FullName']
        result_currency['code'] = currency_info['Code']
        result_currency['sign'] = currency_info['Sign']
        return result_currency
    
    @staticmethod
    def get_all_exchange_rates(all_exchange_rates: list[dict[str, int|float|dict]]) -> str:
        all_exchange_rates: list[dict[str, int|float|dict]] = CurrencyView.write_all_exchange_rates_in_response_form(all_exchange_rates)
        return json.dumps(all_exchange_rates)
    
    @staticmethod
    def write_all_exchange_rates_in_response_form(all_exchange_rates: list[dict[str, int|float|dict]]) -> list[dict[str, int|float|dict]]:
        result_all_exchange_rates: list[dict[str, int|float|dict]] = []
        for exchange_rate in all_exchange_rates:
            result_all_exchange_rates.append(CurrencyView.write_exchange_rate_in_response_format(exchange_rate))
        return result_all_exchange_rates            
        
    @staticmethod
    def get_exchange_rate(exchange_rate_info: dict[str, int|float|dict]) -> str:
        exchange_rate_info: dict[str, int|float|dict] = CurrencyView.write_exchange_rate_in_response_format(exchange_rate_info)
        return json.dumps(exchange_rate_info)
    
    @staticmethod
    def write_exchange_rate_in_response_format(exchange_rate_info: dict[str, int|float|dict]) -> dict[str, int|float|dict]:
        result_exchange_rate: dict[str, int|float|dict] = {}
        result_exchange_rate['id'] = exchange_rate_info['ID']
        result_exchange_rate['baseCurrency'] = CurrencyView.write_currency_in_response_format(exchange_rate_info['BaseCurrency'])
        result_exchange_rate['targetCurrency'] = CurrencyView.write_currency_in_response_format(exchange_rate_info['TargetCurrency'])
        result_exchange_rate['rate'] = exchange_rate_info['Rate']
        return result_exchange_rate
    
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
    
    @staticmethod
    def get_add_exchange_rates_update_result(result_update_exchange_rates: dict[str, int|str]) -> str:
        return json.dumps({'get_add_exchange_rates_update_result': result_update_exchange_rates})
    
    @staticmethod
    def get_error_description(error_key: str, error_description: str) -> str:
        return json.dumps({error_key: error_description})
    
    @staticmethod
    def get_exchange_result(message: str) -> str:
        return json.dumps({'currency_exchange_result': message})
    
    @staticmethod
    def get_json_result(error_key: str, message: str) -> str:
        return json.dumps({error_key: message})
       