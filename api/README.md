# Automacao de API - Swagger Petstore

Suite de testes automatizados para os endpoints **Pet**, **Store** e **User** da API publica [Swagger Petstore](https://petstore.swagger.io/).

## Stack

- Python 3.11+
- pytest 8
- requests
- jsonschema (validacao de contrato)
- Faker (geracao de massa de teste)
- Allure Report
- pytest-html

## Estrutura

```
api/
├── clients/         # Camada de clientes HTTP por recurso
├── schemas/         # JSON Schemas para validacao de contrato
├── data/            # Factories de dados (Faker)
├── tests/           # Casos de teste por recurso
├── config.py        # Configuracao via .env
├── pytest.ini       # Markers e opcoes do pytest
└── requirements.txt
```

## Instalacao

```bash
cd api
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Execucao

```bash
# Todos os testes
pytest

# Apenas smoke
pytest -m smoke

# Por recurso
pytest -m pet
pytest -m store
pytest -m user

# Cenarios negativos
pytest -m negative

# Em paralelo
pytest -n auto

# Relatorio Allure
pytest --alluredir=allure-results
allure serve allure-results
```

## Cobertura

| Recurso | Endpoints cobertos |
|---------|-------------------|
| Pet | POST, GET por ID, PUT, POST form, DELETE, findByStatus, negativos |
| Store | GET inventory, POST order, GET order, DELETE order, negativos |
| User | POST, GET, PUT, DELETE, login, logout, createWithList, negativos |

## Padroes adotados

- **Service/Client pattern**: cada recurso tem seu cliente HTTP isolado
- **Factory pattern**: massa de teste via Faker (sem hardcode)
- **Schema validation**: toda resposta de sucesso tem contrato validado
- **Setup/Teardown**: fixtures criam e deletam dados pra nao deixar lixo
- **Markers**: `smoke`, `regression`, `negative`, `pet`, `store`, `user`
