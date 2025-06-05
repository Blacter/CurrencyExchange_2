from http.server import HTTPServer, BaseHTTPRequestHandler

from currency_handler import CurrencyHandler
from model.model import CurrencyModel
from view.view import CurrencyView

from config.config import Config

class CurrencyExchange:
        
    def start_server(self):
        self.port: int = 8000
        self.host: str = 'localhost'
        server_address: tuple = ('', self.port)
        httpd = HTTPServer(server_address, CurrencyHandler)
        print(f"Server running on http://{self.host}:{self.port}")        
        httpd.serve_forever()        
        