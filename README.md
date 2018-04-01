# Facebook Scraper

## Fazendo tudo rodar

Uma vez que se tenha instalado python 3 e Git, baixado o repositório e
esteja com um editor de texto adequado (Atom, VSCode, Sublime ou Pycharm), deve-se
seguir os seguintes passos

Criar o ambiente virtual (venv) e entrar no mesmo
```
python3 -m venv venv
source venv/bin/activate
```

Para aqueles no Linux ou Mac
```
make install
```

Para windows
```
pip install -r requirements.txt
```

Uma vez instalados todos os módulos, é necessário configurar o token.
Por enquanto é preciso ir à Graph API do Facebook pegar o token
([link](https://developers.facebook.com/tools/explorer/)). Uma vez em posse do
token, deve-se criar um arquivo chamado `config.ini` dentro da pasta `scraper`.



## Modelo para arquivo Token

O armazenamento do token está ocorrendo em um arquivo chamado config.ini para
evitar falhas de segurança como compartilhamento indevido de tokens

```
[DEFAULT]
token={SEUTOKENGIGANTEAQUI}
```

## Rodando testes

Por enquanto rodar testes é a principal funcionalidade. Em breve serão adicionadas mais funções. Portanto, para testes

```
make
```
E para saber qual a cobertura dos testes, use
```
make cov
```

## Verificando estilo

Para verificar se o seu código encontra-se bem indentado e bonito, use o seguinte comando

```
make style
```
Importante usar este comando antes de mandar uma PR para garantir código mais legível.
