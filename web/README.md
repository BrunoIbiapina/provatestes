# Automacao Web - SauceDemo

Suite de testes E2E para [SauceDemo](https://www.saucedemo.com/) usando Selenium WebDriver com Page Object Model.

## Stack

- Python 3.11+
- pytest 8
- Selenium 4 (driver via Selenium Manager embutido)
- Allure Report
- pytest-html

## Estrutura

```
web/
├── pages/           # Page Objects (BasePage + uma por tela)
├── tests/           # Testes organizados por feature
├── utils/           # DriverFactory
├── config.py        # Configuracao via .env
├── pytest.ini       # Markers e opcoes
└── requirements.txt
```

## Instalacao

```bash
cd web
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Chrome ou Firefox precisa estar instalado. O Selenium Manager (embutido no Selenium 4.6+) baixa o driver automaticamente.

## Execucao

```bash
# Tudo (modo visual)
pytest

# Headless (CI)
HEADLESS=true pytest

# Smoke
pytest -m smoke

# Por feature
pytest -m login
pytest -m cart
pytest -m checkout

# Em paralelo
pytest -n 2

# Allure
pytest --alluredir=allure-results
allure serve allure-results
```

## Cenarios cobertos

**Login**: usuario padrao, locked_out, senha errada, campos vazios, logout.
**Carrinho**: adicionar 1, adicionar varios, remover, persistir entre paginas, ordenacao por preco.
**Checkout**: fluxo completo E2E, validacao de nome obrigatorio, validacao de CEP obrigatorio.

## Padroes adotados

- **Page Object Model**: cada tela isolada em sua classe, herdando de `BasePage`
- **DriverFactory**: criacao centralizada do WebDriver, suporta Chrome/Firefox e headless
- **Esperas explicitas**: `WebDriverWait` em vez de sleeps
- **Screenshot em falha**: hook automatico anexa print no Allure quando teste quebra
- **Markers**: `smoke`, `regression`, `negative`, `login`, `cart`, `checkout`
