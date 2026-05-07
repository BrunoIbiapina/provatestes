# Arquitetura

Documento de referência técnica do projeto de automação de testes. Detalha os padrões de projeto adotados, a separação em camadas e o racional por trás de cada escolha.

> Complementa o [README.md](./README.md) (visão geral) e o [TEST_STRATEGY.md](./TEST_STRATEGY.md) (estratégia de testes).

---

## 1. Visão geral

O repositório é um **monorepo** com dois projetos de automação independentes que compartilham apenas a estratégia geral e o pipeline de CI:

```
.
├── api/      # Testes de API REST (Swagger Petstore)
└── web/      # Testes E2E de interface web (SauceDemo)
```

Os dois projetos foram desenhados para serem **independentes**:

- Cada um tem seu próprio `requirements.txt`, `pytest.ini`, `config.py` e `conftest.py`.
- Cada um roda em um workflow separado no GitHub Actions.
- Cada um tem seu próprio relatório (HTML + Allure).

**Motivação**: a suite web é mais lenta (Selenium + browser real) e tem dependências de sistema (Chrome, drivers). Mantê-la separada da API permite rodar a suite rápida (API) com mais frequência sem pagar o custo do browser, e isolar falhas (uma quebra de driver não derruba o pipeline da API).

---

## 2. Projeto API — Service / Client Pattern

### 2.1 Camadas

```
┌─────────────────────────────────────────────────┐
│  tests/        (test_pet, test_store, test_user)│  ← cenários
├─────────────────────────────────────────────────┤
│  schemas/      (PET_SCHEMA, ORDER_SCHEMA, ...)  │  ← contrato
├─────────────────────────────────────────────────┤
│  data/         (build_pet, build_order, ...)    │  ← massa de teste
├─────────────────────────────────────────────────┤
│  clients/      (PetClient, StoreClient, ...)    │  ← chamadas HTTP
├─────────────────────────────────────────────────┤
│  config.py     (BASE_URL, TIMEOUT, ...)         │  ← configuração
└─────────────────────────────────────────────────┘
```

Cada camada tem **uma única responsabilidade** e nunca pula camadas (um teste não fala com `requests` direto, sempre passa por um client).

### 2.2 BaseClient + clients especializados

`api/clients/base_client.py` centraliza:

- Sessão `requests.Session` reaproveitada entre chamadas (keep-alive)
- Headers padrão (`Content-Type`, `Accept`)
- Timeout configurável via `.env`
- Logging estruturado (método, URL, status, tempo de resposta)

Cada recurso da API tem seu próprio cliente herdando de `BaseClient`:

| Cliente | Responsabilidade |
|---|---|
| `PetClient` | CRUD de pets, busca por status/tags, update via formulário |
| `StoreClient` | Inventário e CRUD de orders |
| `UserClient` | CRUD de users, login/logout, criação em lote |

**Por que não usar `requests` direto nos testes?**

1. **DRY** — header e timeout ficam num lugar só.
2. **Trocabilidade** — se trocarmos `requests` por `httpx`, mexemos em 1 arquivo.
3. **Legibilidade** — `pet_client.find_by_status("sold")` lê melhor que `requests.get(BASE_URL + "/pet/findByStatus", params={"status": "sold"}, headers=..., timeout=...)`.
4. **Logging consistente** — todo request loga do mesmo jeito, sem duplicar código no teste.

### 2.3 Schema validation com `jsonschema`

Em `api/schemas/`, cada recurso tem um schema JSON declarativo:

- `PET_SCHEMA` — strict, com `id`, `name`, `photoUrls` obrigatórios. Usado em endpoints individuais que **nós controlamos** (POST, GET por id).
- `PET_LIST_ITEM_SCHEMA` — frouxo, só `id` obrigatório. Usado no `findByStatus`, que retorna dados poluídos da API pública compartilhada.
- `ORDER_SCHEMA`, `INVENTORY_SCHEMA`, `USER_SCHEMA` — strict, recursos sob nosso controle.

**Decisão arquitetural relevante**: separamos `PET_SCHEMA` de `PET_LIST_ITEM_SCHEMA` porque a API `petstore.swagger.io` é compartilhada entre milhares de usuários. O `findByStatus` retorna pets criados por terceiros, frequentemente sem `name`. Validar com `PET_SCHEMA` resultaria em falhas flaky por dados externos. A separação preserva o rigor onde temos controle.

### 2.4 Factories de dados (Faker)

`api/data/factories.py` expõe `build_pet()`, `build_order()`, `build_user()`. Cada chamada gera dados únicos (IDs aleatórios, nomes randômicos via `Faker`).

**Por quê?**

- **Isolamento entre execuções** — sem ID hardcoded, dois pipelines rodando em paralelo não colidem.
- **Sem lixo cruzado** — cada teste limpa o que criou (fixture com teardown).
- **Sem hardcode** — facilita rodar a suite contra outro ambiente sem editar código.

### 2.5 Fixtures (setup / teardown)

`api/tests/conftest.py` define fixtures de dois tipos:

- **Sessão** (`pet_client`, `store_client`, `user_client`) — uma instância única por execução. Reaproveita conexão HTTP.
- **Função** (`new_pet`, `new_order`, `new_user`) — cria recurso → entrega ao teste → deleta no teardown. Garante que cada teste começa limpo e não deixa lixo.

```python
@pytest.fixture
def new_pet(pet_client):
    payload = build_pet()
    response = pet_client.create(payload)
    assert response.status_code == 200
    yield response.json()
    pet_client.delete_by_id(payload["id"])  # teardown
```

---

## 3. Projeto Web — Page Object Model

### 3.1 Camadas

```
┌─────────────────────────────────────────────────┐
│  tests/    (test_login, test_cart, test_checkout)│  ← cenários
├─────────────────────────────────────────────────┤
│  pages/    (LoginPage, InventoryPage, ...)      │  ← interação UI
├─────────────────────────────────────────────────┤
│  pages/base_page.py  (BasePage)                 │  ← primitivas Selenium
├─────────────────────────────────────────────────┤
│  utils/driver_factory.py                         │  ← criação do driver
├─────────────────────────────────────────────────┤
│  config.py                                       │  ← URL, browser, timeouts
└─────────────────────────────────────────────────┘
```

### 3.2 Page Object Model

Cada tela do SauceDemo tem uma classe em `web/pages/` que herda de `BasePage`:

| Page Object | Tela coberta |
|---|---|
| `LoginPage` | `/` (login) |
| `InventoryPage` | `/inventory.html` (catálogo) |
| `CartPage` | `/cart.html` (carrinho) |
| `CheckoutPage` | `/checkout-step-one.html` e seguintes |

Cada classe expõe:

- **Locators** como atributos de classe (`USERNAME = (By.ID, "user-name")`)
- **Ações de negócio** como métodos (`login()`, `add_to_cart()`, `fill_info()`)

**Por quê?**

1. **Manutenção** — se o seletor muda, edita em um lugar só.
2. **Legibilidade** — `login_page.login(user, pass)` esconde os detalhes do Selenium.
3. **Reuso** — `add_to_cart()` é chamado em testes de carrinho e de checkout sem duplicação.

### 3.3 BasePage

`web/pages/base_page.py` encapsula as primitivas de Selenium com **espera explícita embutida**:

- `find(locator)` — espera o elemento aparecer e retorna
- `click(locator)` — espera ser clicável e clica
- `type(locator, text)` — espera, limpa e digita
- `is_visible(locator)` — true/false sem quebrar se não achar

**Decisão arquitetural**: nenhum Page Object usa `time.sleep()`. Toda espera é via `WebDriverWait` + `expected_conditions`. Isso elimina sleeps arbitrários e torna os testes mais rápidos e confiáveis.

### 3.4 DriverFactory

`web/utils/driver_factory.py` centraliza a criação do `WebDriver`:

- Suporta Chrome e Firefox (via `Config.BROWSER`)
- Headless toggle via `HEADLESS=true`
- Flags padrão (`--no-sandbox`, `--disable-dev-shm-usage`, resolução fixa) pra estabilidade em CI
- `webdriver-manager` baixa o driver compatível com o browser instalado — zero setup manual

### 3.5 Hook de screenshot em falha

`web/tests/conftest.py` tem um `pytest_runtest_makereport` que, em caso de falha, salva o screenshot em `screenshots/` e anexa no Allure automaticamente. Evidência visual gratuita pra debug e relatório.

---

## 4. Aspectos transversais

### 4.1 Configuração via `.env`

Tanto API quanto Web usam `python-dotenv` em `config.py`. Toda string de URL, timeout, credencial e toggle de comportamento vem de variável de ambiente, com default sensato pra rodar localmente.

**Benefício**: o mesmo código roda local, em CI e contra ambientes diferentes (staging/prod) sem alteração.

### 4.2 Markers de pytest

Definidos em `pytest.ini` com `--strict-markers` (typo em marker quebra a coleta):

- `smoke` — fumaça mínima, roda em todo push
- `regression` — suite completa, roda em PR e agendado
- `negative` — cenários de erro
- Marcadores por recurso: `pet`, `store`, `user` (API) / `login`, `cart`, `checkout` (Web)

Permite seleção por sub-suite (`pytest -m smoke`, `pytest -m "checkout and not negative"`).

### 4.3 Allure Report

Todo teste tem três níveis de hierarquia Allure:

- `@allure.epic("...")` — projeto (Petstore API / SauceDemo)
- `@allure.feature("...")` — recurso (Pet, Store, Login, Cart...)
- `@allure.story("...")` — cenário específico

Permite filtrar e agrupar no relatório por contexto de negócio, não só por arquivo.

### 4.4 CI/CD — GitHub Actions

Três workflows independentes em `.github/workflows/`:

| Workflow | Quando | O que faz |
|---|---|---|
| `api-tests.yml` | push, PR, agendado | Matriz Python 3.11/3.12, suite API |
| `web-tests.yml` | push, PR, agendado | Chrome headless, suite Web |
| `lint.yml` | push, PR | flake8 |

Os artifacts (HTML + Allure + screenshots de falha) ficam disponíveis pra download em cada execução.

---

## 5. Fluxo de uma execução típica

### Teste de API (ex.: `test_create_pet`)

```
1. pytest coleta testes em api/tests/
2. Fixture pet_client cria PetClient com session HTTP
3. build_pet() gera payload com ID/nome aleatórios
4. pet_client.create(payload) → POST /pet
5. Validação: status 200, schema do body, name/status batem
6. pet_client.delete_by_id(payload["id"]) → cleanup
7. Allure registra steps; pytest-html gera report.html
```

### Teste E2E Web (ex.: `test_full_checkout`)

```
1. pytest coleta testes em web/tests/
2. DriverFactory.create() abre Chrome (headless ou visual)
3. login_page.load() + .login(user, pass) → autentica
4. InventoryPage: add_to_cart(produto_a), add_to_cart(produto_b)
5. go_to_cart() → CartPage.go_to_checkout()
6. CheckoutPage.fill_info(...) → .finish()
7. Assert "Thank you for your order"
8. Em falha: screenshot anexado no Allure
9. Driver.quit() no teardown
```

---

## 6. Decisões e trade-offs

| Decisão | Alternativa | Por que escolhemos esta |
|---|---|---|
| Service/Client (API) | Helpers funcionais soltos | Encapsula estado (session, base_url), facilita extensão |
| `jsonschema` (API) | Pydantic | Schema declarativo é mais leve e independe da versão do Python |
| Page Object (Web) | Testes "scriptados" com Selenium puro | Manutenção centralizada de seletores |
| `webdriver-manager` | Baixar driver manualmente | Zero setup, sempre compatível com browser instalado |
| `requests.Session` | `requests.get/post` direto | Connection pooling + headers persistentes |
| Fixtures com teardown | Suite "criar e esquecer" | Isolamento entre testes, sem dados poluídos |
| `pytest-html` + Allure | Só Allure | HTML simples roda sem CLI extra (útil em CI), Allure é o detalhado |
| Monorepo | Dois repos separados | Pipeline de QA único, contexto compartilhado, releases sincronizadas |

---

## 7. Onde adicionar coisas novas

| Quero... | Onde mexo |
|---|---|
| Novo endpoint da API | `api/clients/<recurso>_client.py` (método novo) + `api/tests/test_<recurso>.py` |
| Nova validação de contrato | `api/schemas/<recurso>_schema.py` |
| Novo dado de teste | `api/data/factories.py` |
| Nova tela do app web | `web/pages/<nova>_page.py` herdando de `BasePage` |
| Nova suite E2E | `web/tests/test_<feature>.py` |
| Suporte a outro browser | `web/utils/driver_factory.py` (nova `if browser ==`) |
| Variável de configuração | `config.py` (api/ ou web/) + `.env.example` |

---

## 8. Referências

- [pytest docs](https://docs.pytest.org/)
- [Selenium Python](https://selenium-python.readthedocs.io/)
- [JSON Schema](https://json-schema.org/)
- [Allure pytest](https://docs.qameta.io/allure/#_pytest)
- [Page Object Model — Martin Fowler](https://martinfowler.com/bliki/PageObject.html)
