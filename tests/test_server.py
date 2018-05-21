import json
import unittest

def test_get_actor_name_example(self):
    # Envia uma requisição HTTP GET para a aplicação
    result = self.app.get('/actor/example')

    self.assertEqual(result.data.decode("utf-8") , "actor name : example")

def test_get_actor_name_json_example(self):
    # Envia uma requisição HTTP GET para a aplicação
    result = self.app.get('/actorjson/example')
    r = json.loads(result.data.decode('utf8'))
        
    self.assertEqual(r , {'actor_name' : 'example'})


if __name__ == '__main__':
    unittest.main()
