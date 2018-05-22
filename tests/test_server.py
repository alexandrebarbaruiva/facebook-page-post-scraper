from server.main import app
import unittest


class TestFlask(unittest.TestCase):
    def setUp(self):
        # Cria um cliente de teste
        self.app = app.test_client()
        # Propaga as exceções para o cliente de teste
        self.app.testing = True

    def test_home_status_code(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/')

        # Verifica o código de estado da resposta da requisição
        #   Se for sucesso irá retornar 200
        self.assertEqual(result.status_code, 200)

    def test_actors_status_code(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/actors')

        # Verifica o código de estado da resposta da requisição
        #   Se for sucesso irá retornar 200
        self.assertEqual(result.status_code, 200)
    
    def test_dates_status_code(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/date')

        # Verifica o código de estado da resposta da requisição
        #   Se for sucesso irá retornar 200
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/')

        # Verifica o dado da resposta do caminho da página inicial
        self.assertEqual(result.data.decode("utf-8"), "Facebook Scraper.")


if __name__ == '__main__':
    unittest.main()
