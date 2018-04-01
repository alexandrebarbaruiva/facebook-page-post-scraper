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

## Modelo para arquivo Token

O armazenamento do token está ocorrendo em um arquivo chamado config.ini para
evitar falhas de segurança como compartilhamento indevido de tokens

```
[DEFAULT]
token={SEUTOKENGIGANTEAQUI}
```
