# API de Gerenciamento Escolar

Este projeto implementa uma API RESTful completa para o gerenciamento de Professores, Turmas e Alunos, conforme a estrutura solicitada.

## 👥 Integrantes do Grupo

* **Grupo:** 9
* Ana Carolina Guedes
* Maria Eduarda Gomes
* Suzana Kelly Guedes

## 🛠️ Arquitetura e Tecnologias

O projeto foi construído seguindo uma arquitetura modularizada para promover a organização e escalabilidade:

1.  **Estrutura MVC (Model-View-Controller/Routes):** O código é dividido para separar a lógica de negócio (Modelos) da manipulação de dados (Routes/Controllers) e da representação (Serialização/Schemas).
2.  **Framework:** **Flask** (Python).
3.  **Banco de Dados:** **SQLite** para persistência, gerenciado pelo **SQLAlchemy (ORM)**.
4.  **Serialização/Validação:** **Marshmallow**.
5.  **Rotas e Documentação:** **Flask-RESTx** para endpoints REST e **Swagger** para documentação automática.
6.  **Containerização:** O serviço está empacotado e rodando com **Docker** e orquestrado por **Docker Compose**.

## 🚀 Como Rodar a Aplicação

A forma mais simples e recomendada de rodar a aplicação é utilizando o Docker Compose.

### Pré-requisitos

* Docker Desktop instalado e rodando.

### Comandos de Execução

1.  **Navegue** até a pasta raiz do projeto (`Gerenciamento-Escolar/`).
2.  **Construa a imagem** Docker:
    ```bash
    docker-compose build
    ```
3.  **Inicie o container** em modo detached (segundo plano):
    ```bash
    docker-compose up -d
    ```

### Acessando a API

Após iniciar o container, a API estará acessível no endereço abaixo:

* **Documentação Interativa (Swagger UI):** `http://localhost:5000/doc/`

---

## 🗄️ Endpoints Principais (CRUD)

A API suporta as seguintes operações completas (GET, POST, PUT, DELETE) para as três entidades:

| Entidade | Prefixo da Rota |
| :--- | :--- |
| **Professor** | `/professores` |
| **Turma** | `/turmas` |
| **Aluno** | `/alunos` |

O modelo `Aluno` calcula e armazena automaticamente a `media_final` com base nas `notas` fornecidas.