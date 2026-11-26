# Sistema de Biblioteca

API REST para administrar o acervo e as operações de uma biblioteca.

**Tema recebido:** sistema de biblioteca com gestão de acervo e circulação de exemplares.  
**Objetivo:** centralizar os cadastros, acompanhar empréstimos e atrasos e disponibilizar consultas e indicadores para apoiar a administração da biblioteca.

**Integrantes:** José Mayson, Matheus Eugênio e Isaque Abraão.

<p align="center">
  <a href="#tecnologias-utilizadas">Tecnologias</a> ·
  <a href="#instalação-e-configuração">Instalação</a> ·
  <a href="#-api">Endpoints</a> ·
  <a href="#entidades-relacionamentos-e-diagrama">Modelo de dados</a> ·
  <a href="#regras-de-negócio">Regras de negócio</a> ·
  <a href="#funcionalidade-específica-do-tema">Funcionalidades</a> ·
  <a href="#consultas-simples-e-complexas">Consultas e filtros</a>
</p>

## Tecnologias utilizadas

- **Python 3.12+**
- **FastAPI** para a API e documentação OpenAPI.
- **Pydantic** para validação e serialização.
- **SQLAlchemy** para persistência relacional.
- **SQLite** como banco de dados.
- **Alembic** para migrações.

## Instalação e configuração

### Criar o ambiente e instalar dependências

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install alembic
```

O banco usado pela aplicação é SQLite, localizado por padrão em `alembic/biblioteca.db`. A API não cria o esquema automaticamente. O arquivo `scripts/schema.sql` contém a definição do esquema para configuração manual.

### Configurar SQLite

SQLite não exige um servidor separado. Para usar outro arquivo, defina `DATABASE_URL` no PowerShell:

```powershell
$env:DATABASE_URL = "sqlite:///C:/caminho/para/biblioteca.db"
```

`DATABASE_URL` altera o banco usado pela aplicação. Sem essa variável, ela usa `alembic/biblioteca.db`. O Alembic não lê essa variável.

### Executar migrações

Como a URL do Alembic é `sqlite:///./biblioteca.db`, execute as migrações a partir da pasta `alembic`. Assim, elas usam `alembic/biblioteca.db`, o mesmo arquivo padrão da aplicação:

```powershell
Set-Location .\alembic
alembic upgrade head
Set-Location ..
```

Se definir `DATABASE_URL` para apontar a aplicação a outro arquivo, ajuste também a URL em `alembic.ini` antes de executar as migrações. O Alembic não lê essa variável automaticamente.

### Carregar dados de exemplo

Depois de criar o esquema, carregue os dados uma única vez em um banco SQLite vazio:

```powershell
python scripts/povoar_banco.py
```

### Executar a aplicação

```powershell
uvicorn app.main:app --reload
```

O servidor fica disponível em <http://127.0.0.1:8000>. A documentação interativa da API fica em <http://127.0.0.1:8000/docs>.

## 🔌 API

Todas as rotas trocam dados em JSON. Os exemplos usam `http://127.0.0.1:8000` como endereço base.

<details open>
<summary><strong>Acervo e cadastros</strong></summary>

| Recurso | Rotas principais |
|---|---|
| **Livros** | `GET /livros/`, `POST /livros/`, `GET /livros/{id}`, `PUT /livros/{id}`, `DELETE /livros/{id}` |
| **Exemplares** | `GET /exemplares/`, `POST /exemplares/`, `GET /exemplares/{id}`, `PUT /exemplares/{id}`, `DELETE /exemplares/{id}` |
| **Usuários** | `GET /usuarios/`, `POST /usuarios/`, `GET /usuarios/{id}`, `PATCH /usuarios/{id}`, `DELETE /usuarios/{id}` |
| **Autores** | `GET /autores/`, `POST /autores/`, `GET /autores/{id}`, `PUT /autores/{id}`, `DELETE /autores/{id}` |
| **Editoras** | `GET /editoras/`, `POST /editoras/`, `GET /editoras/{id}`, `PUT /editoras/{id}`, `DELETE /editoras/{id}` |
| **Categorias** | `GET /categorias/`, `POST /categorias/`, `GET /categorias/{id}`, `PUT /categorias/{id}`, `DELETE /categorias/{id}` |

Rotas relacionadas:

- `GET /livros/{livro_id}/exemplares` — exemplares associados a um livro.
- `GET /autores/{autor_id}/livros` — livros associados a um autor.
- `GET /usuarios/{usuario_id}/emprestimos` — histórico de empréstimos de um usuário.

</details>

<details>
<summary><strong>Empréstimos</strong></summary>

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/emprestimos/` | Lista empréstimos com filtros e paginação. |
| `POST` | `/emprestimos/` | Cadastra um empréstimo. |
| `GET` | `/emprestimos/{id}` | Consulta um empréstimo. |
| `PUT` | `/emprestimos/{id}` | Atualiza os dados de um empréstimo. |
| `DELETE` | `/emprestimos/{id}` | Remove um empréstimo. |
| `GET` | `/emprestimos/vencidos/` | Identifica e lista empréstimos em atraso. |
| `GET` | `/usuarios/{id_usuario}/situacao` | Consulta a situação da conta do usuário e seus atrasos. |

Na listagem, `page` começa em `1` e `page_size` aceita valores de `1` a `100`. Livros aceitam filtros por `titulo`, `id_categoria`, `id_editora` e `ano_publicacao`. Empréstimos aceitam filtros por `id_usuario`, `id_exemplar` e `situacao_emprestimo`.

</details>

<details>
<summary><strong>Estatísticas e relatórios</strong></summary>

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/estatisticas/estatisticas` | Indicadores de acervo, empréstimos e páginas por categoria. |
| `GET` | `/relatorios/obras-autores-categorias` | Ranking da quantidade de obras por autor e categoria. |
| `GET` | `/relatorios/atrasos-categorias` | Quantidade de empréstimos atrasados por categoria. |

</details>

## Entidades, relacionamentos e diagrama

![Diagrama original do esquema relacional do banco de dados](docs/images/esquema-relacional.png)

### Entidades e relacionamentos

| Entidade | Responsabilidade e relações |
|---|---|
| **Usuário** | Representa quem pode realizar empréstimos. Armazena nome, data de cadastro, e-mail, matrícula, telefone e tipo (`ALUNO`, `PROFESSOR`, `SERVIDOR` ou `ADMINISTRADOR`). E-mail, matrícula e telefone são únicos. Um usuário pode ter vários empréstimos. |
| **Empréstimo** | Registra a circulação de um exemplar por um usuário. Guarda as datas do empréstimo, do prazo de devolução e, quando informado, da devolução efetiva, além da situação (`PENDENTE`, `DEVOLVIDO` ou `ATRASADO`). Cada registro referencia exatamente um usuário e um exemplar. |
| **Exemplar** | Representa uma cópia física disponível no acervo. Está associado a um livro e possui uma situação (`DISPONIVEL`, `DANIFICADO`, `EM_EMPRESTIMO` ou `RETIRADO_DE_CIRCULACAO`). Um exemplar pode estar relacionado a vários registros de empréstimo ao longo do tempo. |
| **Livro** | Descreve uma obra pelo título, ano de publicação e número de páginas. Cada livro referencia uma editora e uma categoria, pode ter vários autores e pode possuir vários exemplares. |
| **Autor** | Guarda o nome de quem escreveu uma ou mais obras. A relação com livros é muitos-para-muitos e fica registrada na tabela de associação `livro_autor`. |
| **Editora** | Guarda o nome da editora responsável pela publicação. Uma editora pode estar associada a vários livros. |
| **Categoria** | Classifica os livros por assunto. O nome da categoria é único e uma categoria pode agrupar vários livros. |

## Regras de negócio

- Um empréstimo deve referenciar um usuário e um exemplar existentes.
- A camada de serviços define validações de disponibilidade do exemplar e do período de devolução. Essas validações ainda não são chamadas pelo endpoint de criação, que verifica a existência do usuário e do exemplar.
- As rotas `DELETE` não apagam automaticamente os registros dependentes. Remova empréstimos antes de usuários ou exemplares, exemplares antes de livros e livros antes de editoras ou categorias. Ao excluir um autor, o vínculo em `livro_autor` é removido sem apagar os livros. Violações de chaves estrangeiras retornam **HTTP 409 Conflict**. Excluir empréstimos também apaga o histórico de circulação.

## Funcionalidade específica do tema

- `GET /emprestimos/vencidos/` procura empréstimos pendentes, ainda sem devolução efetiva e com prazo anterior à data atual. Atualiza esses registros para `ATRASADO` e retorna o total e os empréstimos atrasados:

  ```json
  {
    "total_atrasados": 1,
    "emprestimos": [
      {
        "id_emprestimo": "id-do-emprestimo",
        "id_usuario": "id-do-usuario",
        "id_exemplar": "id-do-exemplar",
        "data_prazo": "15/11/2026",
        "dias_atraso": 11
      }
    ]
  }
  ```

- `GET /usuarios/{id_usuario}/situacao` recebe o ID do usuário na URL. Conta os empréstimos sem devolução efetiva cujo prazo já passou, atualiza a situação para `ATRASADO` e retorna a situação da conta:

  ```json
  {
    "id_usuario": "id-do-usuario",
    "nome": "Nome do usuário",
    "tipo_usuario": "ALUNO",
    "situacao_conta": "BLOQUEADO",
    "livros_em_atraso": 1,
    "dias_totais_de_atraso_acumulados": 11
  }
  ```

- `GET /estatisticas/estatisticas` retorna quantidade de livros por categoria, quantidade de exemplares por situação, tempo médio dos empréstimos devolvidos, datas do primeiro e do último empréstimo e total de páginas por categoria.
- Os relatórios apresentam o ranking de quantidade de obras de cada autor por categoria e a quantidade de empréstimos em atraso por categoria.

## Consultas simples e complexas

### Consultas simples

- As operações CRUD e as buscas por ID dos recursos **editoras**, **usuários**, **livros**, **autores**, **categorias**, **empréstimos** e **exemplares**.
- `GET /estatisticas/estatisticas` — consulta os indicadores do acervo e dos empréstimos.
- `GET /usuarios/{usuario_id}/emprestimos` — consulta o histórico de empréstimos de um usuário.
- `GET /autores/{autor_id}/livros` — lista os livros de um autor.
- `GET /livros/{livro_id}/exemplares` — lista os exemplares de um livro.
- `GET /emprestimos/vencidos/` e `GET /usuarios/{id_usuario}/situacao` — identificam empréstimos atrasados e calculam a situação do usuário.

### Consultas complexas

- `GET /relatorios/obras-autores-categorias` — relaciona livros, categorias e autores para contar e ordenar as obras por autor e categoria.
- `GET /relatorios/atrasos-categorias` — relaciona categorias, livros, exemplares e empréstimos para contar os atrasos por categoria.

### Filtros disponíveis

- **Livros:** `titulo`, `id_categoria`, `id_editora` e `ano_publicacao`.
- **Empréstimos:** `id_usuario`, `id_exemplar` e `situacao_emprestimo`.

