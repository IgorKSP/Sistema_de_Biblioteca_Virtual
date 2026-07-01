# 📚 Gerenciador de Livros

Um aplicativo de linha de comando em Python para cadastrar, listar, pesquisar, excluir e exportar livros usando SQLite como banco de dados e Pydantic para validação de dados. Ideal para organizar sua leitura de forma prática e simples.

## 🚀 Funcionalidades

- ✅ Adicionar livros com validação de dados
- 📋 Listar todos os livros cadastrados
- 🔍 Pesquisar por nome ou categoria
- 🔄 Alterar o status de leitura ("Na fila" ou "Lido")
- 🗑️ Remover livros por ID ou nome
- 📂 Exportar lista de livros para um arquivo `.csv`
- ♻️ Resetar o banco de dados (com recriação da tabela)

## 🛠️ Tecnologias Utilizadas

- Python 3
- SQLite3 (banco de dados local)
- CSV (exportação)

## 📦 Estrutura de Arquivos

```
proj-livro/
│
├── modelos/
│   └── livro.py       # Classe Livro com lógica e integração com SQLite
├── main.py            # Menu interativo e controle de execução
└── README.md          # Este arquivo
```

## ⚙️ Requisitos

- Python 3.8+
- Biblioteca Pydantic (instale com o pip abaixo)

```bash
pip install pydantic
```

## ▶️ Como usar

1. Clone o repositório ou copie os arquivos para sua máquina:

```bash
git clone https://github.com/seuusuario/proj-livro.git
cd proj-livro
```

2. Execute o script principal:

```bash
python main.py
```

3. Siga as instruções no menu:

```
Escolha o que deseja fazer:

1 - Adicionar livro
2 - Listar livro(s)
3 - Mudar status
4 - Pesquisar livro
5 - Transformar em .CSV
6 - Remover item
7 - Resetar banco de dados
```

## 🧪 Exemplo de uso

- Ao escolher `1`, o programa pedirá:
  - Nome do livro
  - Número de páginas
  - Categoria
  - Status (1 = Lido, 2 = Na fila)

- Com `2`, você verá uma tabela com os livros cadastrados.
- Com `3`, você atualizara os status do livro.
- Com `4`, você pesquisa um livro especifico.
- com `5`, você exporta para um arquivo excel (.csv).
- Com `6`, você remove determinado item.
- Com `7`, reinicia o banco de dados.

## 📤 Exportação para CSV

Com a opção 5 do menu, a lista de livros é exportada para `livros_exportado.csv` no mesmo diretório do projeto.

## 🔄 Resetar Banco de Dados

A opção 7 apaga o banco `livros.db` e recria a estrutura da tabela do zero.

⚠️ **Aviso:** essa ação remove todos os livros cadastrados!

