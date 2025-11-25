# Sistema de Recomendação — Trabalho Final DSIA
Desenvolvimento de um sistema completo de recomendação utilizando Python, FastAPI e testes automatizados.

---

## 1. Visão Geral do Projeto

Este projeto implementa um sistema de recomendação baseado em dados reais do MovieLens. Ele utiliza técnicas de filtragem colaborativa e análise estatística para recomendar filmes com base em similaridade e preferências de usuários. A aplicação oferece:

- API REST desenvolvida com FastAPI.
- Interface web simples para interação com a API.
- Testes automatizados com pytest.
- Organização modular seguindo boas práticas de engenharia.
- Carregamento e manipulação de dados via pandas.

---

## 2. Objetivo da Aplicação

A aplicação tem como objetivos principais:

1. Ler, tratar e utilizar dois datasets (ratings e movies) para construir recomendações.
2. Implementar diferentes abordagens de recomendação:
   - Recomendação baseada em itens (item-based).
   - Recomendação baseada em usuários (user-based).
   - Rankings estatísticos (mais bem avaliados, mais assistidos).
3. Disponibilizar essas funcionalidades via API.
4. Permitir cadastro de novos usuários, filmes e avaliações.
5. Garantir confiabilidade por meio de testes automatizados.

---

## 3. Arquitetura da Aplicação

A arquitetura é composta pelos seguintes componentes:

- **FastAPI**: responsável pelo backend e disponibilização dos endpoints.
- **Templates HTML + CSS**: interface visual do dashboard.
- **Pandas + Scikit-Learn**: processamento dos dados e cálculo de similaridades.
- **TestClient (pytest)**: automação dos testes e validação da API.

Toda a lógica é centralizada no módulo `main.py`, com estruturas bem definidas para endpoints, funções de recomendação e modelos Pydantic.

---

## 4. Estrutura do Repositório

A estrutura foi organizada conforme padrões de projetos FastAPI:

recomender-system/
│
├── app/
│ ├── data/
│ │ ├── movies.csv
│ │ └── ratings.csv
│ ├── static/
│ │ └── style.css
│ ├── templates/
│ │ └── index.html
│ ├── init.py
│ └── main.py
│
├── tests/
│ ├── init.py
│ └── test_api.py
│
├── requirements.txt
└── README.md


Descrição dos diretórios:

- `app/data/` → arquivos CSV utilizados pelo modelo.
- `app/static/` → arquivos CSS e recursos da interface.
- `app/templates/` → página HTML utilizada no dashboard.
- `app/main.py` → código principal da API e lógica das recomendações.
- `tests/` → suíte de testes automatizados.
- `requirements.txt` → dependências necessárias.

---

## 5. Dataset Utilizado

A base de dados é composta pelos arquivos:

### 5.1 movies.csv
Contém informações dos filmes:

- movieId  
- title  
- genres  

Total: 9.742 filmes.

### 5.2 ratings.csv
Contém avaliações dos usuários:

- userId  
- movieId  
- rating  
- timestamp  

Total: 100.836 avaliações.

Os arquivos possuem relação 1:N através de `movieId`.

---

## 6. Técnicas de Recomendação Implementadas

### 6.1 Recomendação Baseada em Itens (Item-Based)
Utiliza a matriz usuário-filme para calcular similaridade entre filmes.  
A similaridade é calculada por meio de **Cosine Similarity**.

### 6.2 Recomendação Baseada em Usuários (User-Based)
Identifica usuários semelhantes (comportamento de avaliação) e recomenda itens não assistidos.

### 6.3 Rankings Estatísticos
- Filmes mais bem avaliados (média ponderada com número mínimo de avaliações).
- Filmes mais assistidos (contagem de avaliações).

---

## 7. Instalação e Execução

### 7.1 Ativar ambiente virtual
..venv\Scripts\activate

### 7.2 Instalar dependências
pip install -r requirements.txt

### 7.3 Executar o servidor
uvicorn app.main:app --reload --port 8081


### 7.4 Acessar aplicação
- Dashboard: http://localhost:8081  
- Documentação Swagger: http://localhost:8081/docs  

---

## 8. Testes Automatizados

Todos os principais endpoints possuem testes automatizados com pytest.

### Executar testes:
pytest -v


Os testes cobrem:

- Página inicial
- Top rated
- Most viewed
- Similaridade
- User-based
- Cadastro de usuário
- Cadastro de filme
- Atualização de avaliações
- Busca por nome

Resultado esperado:

9 passed


---

## 9. Documentação dos Endpoints

### GET /
Retorna o dashboard HTML.

### GET /best-seller/ratings/
Lista filmes mais bem avaliados.

### GET /best-seller/views/
Lista filmes mais assistidos.

### GET /similarity/{movie_id}
Retorna filmes semelhantes ao item informado.

### GET /user-based/{user_id}
Recomenda filmes com base em usuários similares.

### GET /search/movie/{name}
Busca filmes pelo título.

### POST /users/
Cadastra um novo usuário.

### POST /movies/
Cadastra um novo filme.

### POST /ratings/
Registra ou atualiza a avaliação de um usuário.

---

## 10. Docker (a ser incluído)
O projeto está preparado para receber:

- Dockerfile
- docker-compose.yml
- Configuração de ambiente para execução containerizada

A containerização será documentada na próxima etapa.

---

## 11. Autores

Alice Moreira
Eduardo Hirle
Isadora Poppi
Gabriel Poppi 

Trabalho desenvolvido para a disciplina DSIA.

---
