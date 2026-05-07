# Catálogo de Casos de Teste

Referência formal de todos os casos automatizados no projeto. Cada teste tem ID, descrição, marcadores, dados utilizados e resultado esperado.

> Documento de evidência de QA. Útil como anexo pra apresentação acadêmica e para rastreabilidade entre requisito e teste.

---

## Sumário

- [Convenções](#convenções)
- [API — Petstore (25 casos)](#api--petstore)
  - [Pet (10 casos)](#pet-apits-pet)
  - [Store (6 casos)](#store-apits-store)
  - [User (8 casos)](#user-apits-user)
- [Web — SauceDemo (13 casos)](#web--saucedemo)
  - [Login (5 casos)](#login-webts-login)
  - [Cart (5 casos)](#cart-webts-cart)
  - [Checkout (3 casos)](#checkout-webts-checkout)
- [Resumo quantitativo](#resumo-quantitativo)

---

## Convenções

### IDs

Formato `<PROJETO>-<RECURSO>-<NN>`:

- `API-PET-01` → caso 01 de Pet na API
- `WEB-LOGIN-03` → caso 03 de Login na Web

### Tipos

| Tipo | Descrição |
|---|---|
| **Smoke** | Cenários críticos do happy path. Roda em todo push. |
| **Regression** | Cobertura completa, incluindo variações. Roda em PR. |
| **Negative** | Cenários de erro / dados inválidos / casos limite. |

### Marcadores pytest

- API: `smoke`, `regression`, `negative`, `pet`, `store`, `user`
- Web: `smoke`, `regression`, `negative`, `login`, `cart`, `checkout`

Definidos em `api/pytest.ini` e `web/pytest.ini` com `--strict-markers`.

---

## API — Petstore

> Base URL: `https://petstore.swagger.io/v2`
> Arquivos: `api/tests/test_pet.py`, `test_store.py`, `test_user.py`

### Pet (`api/tests/test_pet.py`)

| ID | Caso | Tipo | Markers | Pré-condições | Passos | Resultado esperado |
|---|---|---|---|---|---|---|
| API-PET-01 | `test_create_pet` | Smoke | `smoke`, `pet` | — | `POST /pet` com payload de `build_pet()` | 200; body bate com `PET_SCHEMA`; `name` e `status` corretos; pet deletado no teardown |
| API-PET-02 | `test_get_pet_by_id` | Smoke | `smoke`, `pet` | Pet criado via fixture `new_pet` | `GET /pet/{id}` | 200; body bate com `PET_SCHEMA`; `id` retornado é o esperado |
| API-PET-03 | `test_update_pet` | Regression | `regression`, `pet` | Pet criado via `new_pet` | `PUT /pet` alterando `name` e `status="sold"` | 200; body confirma `name="PetAtualizado"` e `status="sold"` |
| API-PET-04 | `test_update_pet_with_form` | Regression | `regression`, `pet` | Pet criado via `new_pet` | `POST /pet/{id}` com form-urlencoded (`name`, `status`) | 200 |
| API-PET-05 | `test_delete_pet` | Smoke | `smoke`, `pet` | — | Cria pet → `DELETE /pet/{id}` → `GET /pet/{id}` | DELETE retorna 200; GET seguinte retorna 404 |
| API-PET-06 | `test_find_by_status[available]` | Regression | `regression`, `pet` | — | `GET /pet/findByStatus?status=available` | 200; body é array que bate com `PET_LIST_SCHEMA`; todos os pets têm `status="available"` |
| API-PET-07 | `test_find_by_status[pending]` | Regression | `regression`, `pet` | — | `GET /pet/findByStatus?status=pending` | 200; idem com `status="pending"` |
| API-PET-08 | `test_find_by_status[sold]` | Regression | `regression`, `pet` | — | `GET /pet/findByStatus?status=sold` | 200; idem com `status="sold"` |
| API-PET-09 | `test_get_pet_not_found` | Negative | `negative`, `pet` | — | `GET /pet/0` | 404 |
| API-PET-10 | `test_delete_pet_not_found` | Negative | `negative`, `pet` | — | `DELETE /pet/0` | 404 ou 400 |
| API-PET-11 | `test_response_time` | Regression | `regression`, `pet` | — | `GET /pet/findByStatus?status=available` | Tempo de resposta < 5s |

### Store (`api/tests/test_store.py`)

| ID | Caso | Tipo | Markers | Pré-condições | Passos | Resultado esperado |
|---|---|---|---|---|---|---|
| API-STORE-01 | `test_get_inventory` | Smoke | `smoke`, `store` | — | `GET /store/inventory` | 200; body bate com `INVENTORY_SCHEMA` (objeto com valores inteiros) |
| API-STORE-02 | `test_place_order` | Smoke | `smoke`, `store` | Pet criado via `new_pet` | `POST /store/order` com payload de `build_order(pet.id)` | 200; body bate com `ORDER_SCHEMA`; `petId` corresponde |
| API-STORE-03 | `test_get_order` | Smoke | `smoke`, `store` | Order criada via fixture `new_order` | `GET /store/order/{id}` | 200; body bate com `ORDER_SCHEMA`; `id` corresponde |
| API-STORE-04 | `test_delete_order` | Regression | `regression`, `store` | Pet criado via `new_pet` | Cria order → `DELETE /store/order/{id}` → `GET /store/order/{id}` | DELETE 200; GET seguinte 404 |
| API-STORE-05 | `test_get_order_not_found` | Negative | `negative`, `store` | — | `GET /store/order/99999999` | 404 |
| API-STORE-06 | `test_get_order_invalid_id` | Negative | `negative`, `store` | — | `GET /store/order/-1` | 400 ou 404 |

### User (`api/tests/test_user.py`)

| ID | Caso | Tipo | Markers | Pré-condições | Passos | Resultado esperado |
|---|---|---|---|---|---|---|
| API-USER-01 | `test_create_user` | Smoke | `smoke`, `user` | — | `POST /user` com payload de `build_user()` | 200; `message` retornada é o ID criado; user deletado no teardown |
| API-USER-02 | `test_get_user` | Smoke | `smoke`, `user` | User criado via fixture `new_user` | `GET /user/{username}` | 200; body bate com `USER_SCHEMA`; `username` corresponde |
| API-USER-03 | `test_update_user` | Regression | `regression`, `user` | User criado via `new_user` | `PUT /user/{username}` alterando `firstName`/`email` → `GET /user/{username}` | PUT 200; GET retorna `firstName="NovoNome"` |
| API-USER-04 | `test_delete_user` | Regression | `regression`, `user` | — | Cria user → `DELETE /user/{username}` → `GET /user/{username}` | DELETE 200; GET seguinte 404 |
| API-USER-05 | `test_login` | Smoke | `smoke`, `user` | User criado via `new_user` | `GET /user/login?username=...&password=...` | 200; mensagem contém "logged in user session" |
| API-USER-06 | `test_logout` | Regression | `regression`, `user` | — | `GET /user/logout` | 200 |
| API-USER-07 | `test_create_with_list` | Regression | `regression`, `user` | — | `POST /user/createWithList` com 3 users | 200; users deletados no teardown |
| API-USER-08 | `test_get_user_not_found` | Negative | `negative`, `user` | — | `GET /user/usuario_inexistente_12345` | 404 |

---

## Web — SauceDemo

> Base URL: `https://www.saucedemo.com`
> Arquivos: `web/tests/test_login.py`, `test_cart.py`, `test_checkout.py`
> Browser padrão: Chrome (headless via `HEADLESS=true`)

### Login (`web/tests/test_login.py`)

| ID | Caso | Tipo | Markers | Pré-condições | Passos | Resultado esperado |
|---|---|---|---|---|---|---|
| WEB-LOGIN-01 | `test_standard_user_login` | Smoke | `smoke`, `login` | Página de login carregada | Login com `standard_user` / `secret_sauce` | Inventário carrega; URL contém `inventory` |
| WEB-LOGIN-02 | `test_locked_out_user` | Negative | `negative`, `login` | Página de login carregada | Login com `locked_out_user` / `secret_sauce` | Mensagem contém "locked out" |
| WEB-LOGIN-03 | `test_wrong_password` | Negative | `negative`, `login` | Página de login carregada | Login com `standard_user` / `senha_errada` | Mensagem contém "do not match" |
| WEB-LOGIN-04 | `test_empty_fields` | Negative | `negative`, `login` | Página de login carregada | Login com username e senha vazios | Mensagem contém "username is required" |
| WEB-LOGIN-05 | `test_logout` | Regression | `regression`, `login` | Logado via fixture `logged_in` | Abrir menu burger → clicar em Logout | URL volta para `saucedemo.com` |

### Cart (`web/tests/test_cart.py`)

| ID | Caso | Tipo | Markers | Pré-condições | Passos | Resultado esperado |
|---|---|---|---|---|---|---|
| WEB-CART-01 | `test_add_single_product` | Smoke | `smoke`, `cart` | Logado | Adicionar "Sauce Labs Backpack" | Badge do carrinho mostra 1 |
| WEB-CART-02 | `test_add_multiple_products` | Regression | `regression`, `cart` | Logado | Adicionar 3 produtos | Badge mostra 3 |
| WEB-CART-03 | `test_remove_product` | Regression | `regression`, `cart` | Logado | Adicionar produto → remover mesmo produto | Badge zera |
| WEB-CART-04 | `test_cart_persists` | Regression | `regression`, `cart` | Logado | Adicionar 2 produtos → ir pro carrinho | `cart_item_count == 2`; "Sauce Labs Backpack" na lista |
| WEB-CART-05 | `test_sort_price_low_high` | Regression | `regression`, `cart` | Logado | Selecionar ordenação "Price (low to high)" | Lista de preços está em ordem crescente |

### Checkout (`web/tests/test_checkout.py`)

| ID | Caso | Tipo | Markers | Pré-condições | Passos | Resultado esperado |
|---|---|---|---|---|---|---|
| WEB-CHECK-01 | `test_full_checkout` | Smoke | `smoke`, `checkout` | Logado | Adicionar 2 produtos → ir ao carrinho → checkout → preencher (Bruno, Ibiapina, 60000-000) → finalizar | Tela de resumo mostra "Total"; confirmação contém "Thank you for your order" |
| WEB-CHECK-02 | `test_checkout_missing_first_name` | Negative | `negative`, `checkout` | Logado | Adicionar produto → checkout → preencher sem `first_name` | Mensagem contém "First Name is required" |
| WEB-CHECK-03 | `test_checkout_missing_postal` | Negative | `negative`, `checkout` | Logado | Adicionar produto → checkout → preencher sem CEP | Mensagem contém "Postal Code is required" |

---

## Resumo quantitativo

### Por projeto

| Projeto | Total | Smoke | Regression | Negative |
|---|---|---|---|---|
| API | 25 | 10 | 11 | 4 |
| Web | 13 | 3 | 5 | 5 |
| **Total** | **38** | **13** | **16** | **9** |

### Por recurso

| Projeto | Recurso | Total |
|---|---|---|
| API | Pet | 11 |
| API | Store | 6 |
| API | User | 8 |
| Web | Login | 5 |
| Web | Cart | 5 |
| Web | Checkout | 3 |

### Cobertura por método HTTP (API)

| Método | Endpoints cobertos |
|---|---|
| GET | `/pet/{id}`, `/pet/findByStatus`, `/store/inventory`, `/store/order/{id}`, `/user/{username}`, `/user/login`, `/user/logout` |
| POST | `/pet`, `/pet/{id}` (form), `/store/order`, `/user`, `/user/createWithList` |
| PUT | `/pet`, `/user/{username}` |
| DELETE | `/pet/{id}`, `/store/order/{id}`, `/user/{username}` |

---

## Como executar uma seleção

```bash
# Apenas smoke (qualquer projeto)
make smoke

# Recurso específico (API)
cd api && pytest -m pet
cd api && pytest -m "user and not negative"

# Recurso específico (Web)
cd web && pytest -m checkout

# Caso individual por ID do pytest
cd api && pytest tests/test_pet.py::TestPet::test_create_pet -v
cd web && pytest tests/test_checkout.py::TestCheckout::test_full_checkout -v
```

---

## Rastreabilidade

| Origem | Onde está |
|---|---|
| **Estratégia geral de testes** | [TEST_STRATEGY.md](./TEST_STRATEGY.md) |
| **Arquitetura técnica** | [ARCHITECTURE.md](./ARCHITECTURE.md) |
| **Schemas de validação** | `api/schemas/*.py` |
| **Factories de dados** | `api/data/factories.py` |
| **Page Objects** | `web/pages/*.py` |
| **Configuração** | `api/config.py`, `web/config.py` (via `.env`) |
