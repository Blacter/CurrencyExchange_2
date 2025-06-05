from controller.post_data.base_post_data import BasePostData

from controller.controller_error.post_data_error import WrongExchangeRatesUpdateBody


class ExchangeRateUpdatePostData(BasePostData):
    def __init__(self, post_data: bytes):
        super().__init__(post_data)
        
    def get_parsed_parameters(self) -> dict[str, int | str]:
        self.get_base_parsed_parameters()
        self.check_parameters_structure()
        self.parse_parameters_with_type()
        return self.get_parameters_dict()
    
    def check_parameters_structure(self) -> None:
        self.check_rate()
        
    def parse_parameters_with_type(self) -> None:
        self.parse_rate()
        
    def get_parameters_dict(self) -> dict[str, int | str]:
        result_parameters_dict: dict[str, int | str] = {}
        result_parameters_dict['rate'] = self.parsed_rate
        
        return result_parameters_dict
    
    def check_rate(self) -> None:
        self.check_rate_key()
        self.check_rate_value()
        
    def parse_rate(self) -> None:
        self.parsed_rate: float = float(self._parameters_dict['rate'])
        
    def check_rate_key(self) -> None:
        if not self.is_key_in_body('rate'):
            raise WrongExchangeRatesUpdateBody('parameter rate doesn\'t exists.')
        
    def check_rate_value(self) -> None:
        self.check_rate_not_empty()
        self.check_rate_is_float()

    def check_rate_not_empty(self) -> None:
        if BasePostData.is_empty_str(self._parameters_dict['rate']):
            raise WrongExchangeRatesUpdateBody('rate value shouldn\'t be empty.')

    def check_rate_is_float(self) -> None:
        if not BasePostData.could_str_be_parsed_to_float(self._parameters_dict['rate']):
            raise WrongExchangeRatesUpdateBody('rate value should be float.')