#!/usr/bin/env bash
# Setup completo de Git + commits semanticos para o trabalho de QA
# Uso: bash scripts/setup_git.sh

set -e  # para na primeira falha
cd "$(dirname "$0")/.."

echo "=========================================="
echo "  Setup de Git + Commits Semanticos"
echo "=========================================="
echo

# 1) Limpa qualquer .git anterior (se existir um meio-iniciado)
if [ -d .git ]; then
  echo "→ Removendo .git anterior..."
  rm -rf .git
fi

# 2) Limpa leftovers de sessoes antigas (se existirem)
[ -d test-automation ] && rm -rf test-automation && echo "→ Pasta test-automation antiga removida"
[ -f Automacao_de_Testes_Guia_Completo.pdf ] && rm -f Automacao_de_Testes_Guia_Completo.pdf && echo "→ PDF antigo removido"
find . -name ".DS_Store" -delete 2>/dev/null || true

# 3) Inicializa
echo "→ Inicializando repo..."
git init -b main >/dev/null
git config user.name "Bruno Ibiapina"
git config user.email "brunoibiapina@me.com"

# 4) Sequencia de commits semanticos
commit() {
  local msg="$1"; shift
  git add "$@"
  git commit -m "$msg" >/dev/null
  echo "  ✓ $msg"
}

echo
echo "→ Fazendo commits semanticos..."

commit "chore: setup inicial do repositorio" \
  .gitignore LICENSE Makefile

commit "chore(api): estrutura inicial do projeto api petstore" \
  api/config.py api/.env.example api/pytest.ini api/requirements.txt

commit "feat(api): clientes http base, pet, store e user" \
  api/clients/ api/schemas/

commit "feat(api): factories de massa de teste com Faker" \
  api/data/

commit "feat(api): suite de testes para pet, store e user" \
  api/tests/ api/README.md

commit "chore(web): estrutura inicial do projeto web saucedemo" \
  web/config.py web/.env.example web/pytest.ini web/requirements.txt

commit "feat(web): page object model e driver factory" \
  web/pages/ web/utils/

commit "feat(web): testes e2e de login, carrinho e checkout" \
  web/tests/ web/README.md

commit "ci: workflows de testes api, web e lint no github actions" \
  .github/

commit "docs: estrategia de testes e readme principal" \
  TEST_STRATEGY.md README.md

commit "feat(docs): dashboard interativo com grafo de topologia 3d" \
  docs/dashboard.html docs/architecture.svg

commit "docs: roteiro da demo quebrar e arrumar" \
  docs/DEMO_SCRIPT.md

commit "docs: guia de estudo e apresentacao da banca" \
  Apresentacao.pptx Guia_de_Estudo.docx Guia_de_Estudo.pdf

commit "chore: script de setup do git" \
  scripts/setup_git.sh

echo
echo "=========================================="
echo "  Resumo:"
echo "=========================================="
git log --oneline
echo
echo "Pronto! Proximos passos:"
echo
echo "  1) Vai em https://github.com/new"
echo "     - Repository name: trabalho-qa-automacao"
echo "     - Public"
echo "     - NAO marque 'Add README', 'gitignore', 'license' (deixa tudo desmarcado)"
echo "     - Create repository"
echo
echo "  2) Cole no terminal:"
echo
echo "     git remote add origin https://github.com/brunoibiapina/trabalho-qa-automacao.git"
echo "     git push -u origin main"
echo
echo "  3) Espera ~3min: as pipelines comecam a rodar sozinhas."
echo "     Veja em: https://github.com/brunoibiapina/trabalho-qa-automacao/actions"
echo
