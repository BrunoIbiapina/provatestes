# Roteiro de Demo - Quebrar e Arrumar

Demo dirigida pra apresentação. **Tempo total: ~5 minutos.**
Objetivo: provar que CI funciona ao vivo, não só que existe.

---

## Antes de começar (na sua casa, com calma)

1. Garanta que o repo está **público** no GitHub
2. Garanta que a pipeline mais recente está **verde**
3. Crie um branch local pra demo: `git checkout -b demo-aula`
4. Volte pra `main`: `git checkout main`
5. Tenha as abas abertas:
   - **Aba 1:** terminal no projeto, com `git status` rodado
   - **Aba 2:** GitHub Actions do repo (lista de runs recentes)
   - **Aba 3:** README do GitHub (pra mostrar o badge)
   - **Aba 4:** VS Code com `web/tests/test_login.py` aberto
6. Faça login no GitHub na aba do navegador (pra commit ficar com seu avatar)

---

## Roteiro passo-a-passo (na hora da apresentação)

### Passo 0 - Setup (10s)
> "Antes de quebrar, vou mostrar que tá tudo verde."

**Faça:**
- Mostra a aba do GitHub Actions com a última execução verde
- Mostra o badge no README

---

### Passo 1 - Quebrar de propósito (30s)
> "Agora vou quebrar um teste de propósito - vou pegar o de login."

**Faça no VS Code:**
Abre `web/tests/test_login.py`, encontra o `test_standard_user_login`, troca a URL esperada de `inventory` pra `xpto`:

```python
# Antes:
assert "inventory" in driver.current_url

# Depois:
assert "xpto" in driver.current_url
```

**Faça no terminal:**

```bash
git add web/tests/test_login.py
git commit -m "test: simular falha intencional para demo"
git push
```

---

### Passo 2 - Ver pipeline rodando (60s)
> "O push acabou de disparar o workflow. Veem aqui no GitHub - já tá rodando."

**Faça:**
- Volta pra aba do GitHub Actions
- F5 - aparece a execução nova com bolinha amarela (em progresso)
- Clica nela pra mostrar os jobs rodando
- Enquanto roda, explica:

> "A pipeline tá fazendo: checkout do código, setup do Python, instalação das dependências, e agora vai rodar o pytest. Em uns 2 minutos a gente sabe."

**Enquanto espera:** abre rapidamente o `.github/workflows/web-tests.yml` e mostra a estrutura.

---

### Passo 3 - Pipeline falha (30s)
> "Olha lá - falhou."

**Faça:**
- Refresh, mostra o ❌ vermelho
- Clica no job `web-tests`
- Mostra a saída do pytest com o assert falhando
- Scrolla até o final mostrando o passo "Upload screenshots on failure" - **artifact criado**
- Volta pro README e atualiza - **badge ficou vermelho**

> "Cada vez que um teste falha, a pipeline guarda o relatório HTML, os resultados do Allure e os screenshots do momento da falha. Tudo aqui, disponível pra download."

**Mostra:**
- Faz download do artifact `web-failure-screenshots`
- Abre o ZIP - mostra o PNG do navegador no momento exato do erro

---

### Passo 4 - Arrumar (30s)
> "Bora arrumar."

**Faça no VS Code:**
Reverte a mudança - volta o `xpto` pra `inventory`:

```python
assert "inventory" in driver.current_url
```

**Faça no terminal:**

```bash
git add web/tests/test_login.py
git commit -m "fix: revert demo intencional"
git push
```

---

### Passo 5 - Voltar ao verde (60s)
> "Pipeline rodando de novo. Vamos esperar."

**Faça:**
- Aba do GitHub Actions, F5
- Mostra o run novo em amarelo
- Aguarda completar (~2 min - se quiser, segue falando do projeto durante esse tempo)
- Run fica verde ✅
- Volta pro README - badge **verde**

> "Pronto. Em 5 minutos vocês viram o ciclo completo: detecção de erro, relatório de falha automático, correção, validação. Isso é o que CI faz no dia a dia."

---

## Plano B (se a internet falhar)

Tenha **gravado em vídeo** a execução completa rodando localmente:

```bash
# Gravar video com OBS / Kap / quicktime:
# 1. pytest web/tests/test_login.py (passa)
# 2. modificar o assert
# 3. pytest web/tests/test_login.py (falha + screenshot)
# 4. reverter
# 5. pytest novamente (passa)
```

Se o GitHub não responder na hora, mostra o vídeo. **Nunca improvise sem backup.**

---

## Anti-roteiro (NÃO fazer)

- Não tentar editar arquivo do projeto sozinha **sem** ter testado o passo antes
- Não escolher um teste que dependa de fixture complexa (use `test_standard_user_login` que é simples)
- Não fazer push direto na `main` se o repo tiver branch protection (use uma branch `demo-aula`)
- Não esperar mais de 2 minutos em silêncio - sempre fala algo do projeto enquanto a pipeline roda
- Não revelar a senha de nada na tela (a senha do SauceDemo é pública: `secret_sauce`, mas qualquer credencial real esconde)

---

## Frases-chave pra usar

- "Em vez de descrever o que CI faz, deixa eu mostrar."
- "Aqui o teste falhou - **a pipeline detectou**, **gerou o artifact**, **mudou o badge**."
- "Se isso fosse produção, o time de dev seria notificado antes do bug chegar no usuário."
- "O screenshot anexado no Allure é o que diferencia debug de chute."

---

## Pós-demo

Depois da apresentação, rode `git log --oneline -3` pra mostrar que ficou:

```
abc1234 fix: revert demo intencional
def5678 test: simular falha intencional para demo
9876543 ... (commit anterior real)
```

Os commits semânticos e os emojis do badge são parte da pegada do projeto - deixa lá. **Não faça squash**.

---

**Boa demo!**
