# Estrategia de Testes

Este documento descreve as decisoes de testes tomadas neste repositorio: o que foi testado, por que, e como.

## Piramide de testes

Como os dois projetos sao **suites de teste de caixa-preta** sobre sistemas externos (API publica e site publico), o foco da piramide aqui e:

```
        /\
       /E2E\         <- web/ (SauceDemo) - fluxo completo de usuario
      /------\
     / API    \      <- api/  (Petstore) - testes de servico
    /----------\
   / Unit (n/a) \    <- nao se aplica: nao temos codigo de producao para testar
  /--------------\
```

## Selecao de cenarios

### API - Petstore

Estrategia: cobrir o **CRUD completo** de cada recurso + ao menos um cenario negativo por recurso + validacao de **contrato** (JSON Schema).

| Recurso | Caminho feliz | Cenarios negativos |
|---------|--------------|-------------------|
| Pet | Create, Read, Update (PUT), Update (form), Delete, FindByStatus | GET inexistente, DELETE inexistente |
| Store | Inventory, Place Order, Get Order, Delete Order | GET inexistente, GET ID invalido |
| User | Create, Get, Update, Delete, Login, Logout, CreateWithList | GET inexistente |

Alem disso:
- **Schema validation** em toda resposta de sucesso (garante contrato estavel)
- **Tempo de resposta** asserted em pelo menos 1 endpoint (basico de SLA)
- **Cleanup automatico** via fixtures - nada fica orfao na base

### Web - SauceDemo

Estrategia: cobrir o **fluxo principal de e-commerce** (login -> carrinho -> checkout) + variacoes negativas em cada etapa.

| Feature | Cenarios |
|---------|---------|
| Login | usuario padrao (smoke), locked_out, senha errada, campos vazios, logout |
| Carrinho | adicionar 1, adicionar varios, remover, persistencia entre paginas, ordenacao por preco |
| Checkout | E2E completo (smoke), validacao de campos obrigatorios |

## Markers do pytest

Permitem rodar subconjuntos:

```bash
pytest -m smoke        # rapido, validacao basica - usado em PRs
pytest -m regression   # completo - usado no schedule semanal
pytest -m negative     # apenas cenarios de erro
pytest -m pet          # filtra por feature/recurso
```

## Dados de teste

- **Sem hardcode**: tudo via Faker (factories) ou via configuracao (.env)
- **Isolamento**: cada teste cria seus proprios dados e limpa no teardown
- **IDs grandes**: usamos `random.randint(10**8, 10**9)` para evitar colisao com a base publica do Petstore

## Padroes de codigo

### API
- **Service/Client pattern**: cada recurso tem seu cliente (`PetClient`, `StoreClient`, `UserClient`) que herda de `BaseClient`
- `BaseClient` centraliza: sessao, headers, timeout, log da request
- Os testes nao falam diretamente com `requests` - sempre via cliente

### Web
- **Page Object Model rigoroso**: cada tela = uma classe, expoe acoes (nao elementos)
- `BasePage` centraliza esperas e operacoes comuns (`click`, `type`, `find`)
- Testes nao usam `By` nem `WebDriverWait` - tudo encapsulado nas pages
- **Sem `time.sleep`**: apenas esperas explicitas

## Por que essas escolhas?

1. **Camada de abstracao**: se a API ou o site mudarem (ex: novo seletor, novo header), o impacto e isolado em **um arquivo** e nao em todos os testes.
2. **Reusabilidade**: os mesmos clients/pages servem pra qualquer teste novo.
3. **Leitura clara**: um teste se le como uma historia de usuario - nao como codigo de baixo nivel.
4. **Evita flakiness**: esperas explicitas + cleanup robusto = pipeline estavel.

## Gaps conscientes

- Nao foi feita **autenticacao OAuth** (Petstore nao expoe)
- Nao foi feito **upload de imagem** no Pet (`uploadImage`) por inconsistencia da API publica
- Nao foi feito **teste de carga** (escopo definido foi funcional)
- Nao foi feito **cross-browser** alem de Chrome (Firefox esta suportado mas nao agendado no CI)

## Como expandir

- Adicionar cliente novo: crie em `api/clients/` herdando de `BaseClient`
- Adicionar page nova: crie em `web/pages/` herdando de `BasePage`
- Adicionar teste novo: use as fixtures existentes em `conftest.py`
