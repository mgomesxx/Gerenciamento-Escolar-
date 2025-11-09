__Sistema de Gerenciamento Escolar com Microsserviços (Flask)__


Este projeto implementa um sistema de gerenciamento escolar baseado em microsserviços, desenvolvido com Flask, SQLAlchemy e Docker Compose.

O sistema é dividido em três partes: Gerenciamento, Reservas e Atividades, que se comunicam entre si por meio de requisições HTTP usando a biblioteca requests.

Cada serviço é independente e possui seu próprio banco de dados SQLite.

__🔗 Estrutura dos Microsserviços__

Responsável por cadastrar e gerenciar alunos, professores e turmas.

É o serviço principal, que fornece os IDs usados pelos outros microsserviços.

Não lida diretamente com reservas ou atividades.

Gerencia as reservas de salas feitas pelas turmas.

Usa o ID da turma, obtido do serviço de Gerenciamento, para criar e validar as reservas.

Não gerencia dados de turmas diretamente.

Controla atividades e notas dos alunos.

Cada atividade é associada a um professor e uma turma, validados por meio do serviço de Gerenciamento.

Não administra professores ou turmas diretamente.

__🔗 Comunicação entre Serviços__


Os microsserviços se comunicam de forma síncrona utilizando a biblioteca requests.

Por exemplo, antes de criar uma reserva, o serviço de Reservas verifica se o ID da turma existe no Gerenciamento:

import requests

def validar_turma(turma_id):
 response = requests.get(f"http://gerenciamento:5000/turmas/{turma_id}")
 return response.status_code == 200

 __🔗 Execução com Docker__

 __*Estrutura do projeto*__

 /projeto-microsservicos
│
├── gerenciamento/
│ ├── app.py
│ ├── models.py
│ ├── controllers/
│ ├── views/
│ ├── Dockerfile
│
├── reservas/
│ ├── app.py
│ ├── models.py
│ ├── controllers/
│ ├── views/
│ ├── Dockerfile
│
├── atividades/
│ ├── app.py
│ ├── models.py
│ ├── controllers/
│ ├── views/
│ ├── Dockerfile
│
└── docker-compose.yml

__*Passos para execução*__

__1. Clonar o repositório:__

git clone https://github.com/mgomesxx/Gerenciamento-Escolar-.git

__2. Subir containers:__

docker compose up --build

__3. Acessar os serviços:__

Gerenciamento -> http://localhost:5000
Reservas -> http://localhost:5001
Atividades -> http://localhost:5002

__🔗 Integrantes:__

- Ana Carolina Guedes Bueno
- Maria Eduarda Gomes Romera
- Suzana Kelly Guedes Vieira 