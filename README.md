# Facebook Scraper

[![Build Status](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper.svg?branch=master)](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper)

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
Para isso devemos baixar o ChromeDriver seguindo as instruções do Splinter para cada sistema operacional:([Instruções para baixar ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)).
Uma vez com o ChromeDriver instalado corretamente,para a aquisição do Token basta digitar
```
make autotoken
```
e seguir as instruções do programa.

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
