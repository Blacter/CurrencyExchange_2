from http.server import HTTPServer, BaseHTTPRequestHandler

from controller.controller import CurrencyController
from model.model import CurrencyModel
from view.view import CurrencyView

from settings.settings import Settings

class CurrencyExchange:
    def __init__(self):
        # self.view: CurrencyView = CurrencyView()
        # self.model: CurrencyModel = CurrencyModel()
        # self.settings: Settings = Settings()
        # self.controller: CurrencyController = CurrencyController(self.view, self.model, self.settings)
        pass
        
    def start_server(self):
        self.port: int = 8000
        self.host: str = 'localhost'
        server_address: tuple = ('', self.port)
        httpd = HTTPServer(server_address, CurrencyController)
        print(f"Server running on http://{self.host}:{self.port}")        
        httpd.serve_forever()        
        