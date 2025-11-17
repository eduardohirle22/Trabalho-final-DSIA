# Sistema de Recomendação — Trabalho Final DSIA  
**Desenvolvimento de uma aplicação completa de recomendação**

---

## Documentação da Base de Dados

A base de dados utilizada no projeto é formada por dois arquivos principais — **`movies.csv`** e **`ratings.csv`**.  
Juntos, eles compõem um dataset amplamente utilizado em estudos de sistemas de recomendação, inspirado no **MovieLens**.

Esse conjunto possibilita análises sobre preferências de usuários, características dos filmes e avaliação de modelos colaborativos, de conteúdo ou híbridos.

---

## 1. `movies.csv`

Arquivo contendo informações descritivas sobre os filmes do catálogo.

**Quantidade de registros:** **9.742 filmes**

### Colunas
- **`movieId` (int)** — Identificador único do filme (chave primária).  
- **`title` (string)** — Título do filme (incluindo o ano de lançamento).  
- **`genres` (string)** — Lista de gêneros separados por `|`  

### Exemplos de uso no projeto
- Enriquecimento das recomendações por **similaridade de gêneros**.  
- Análises por categoria (comédia, ação, romance, etc.).  
- Junção com o arquivo de avaliações para contextualização dos resultados.

---

## 2. `ratings.csv`

Contém as avaliações realizadas pelos usuários sobre cada filme.

**Quantidade de registros:** **100.836 avaliações**

### Colunas
- **`userId` (int)** — Identificador do usuário.  
- **`movieId` (int)** — Filme avaliado (chave estrangeira para `movies.csv`).  
- **`rating` (float)** — Nota de 0.5 a 5.0.  
- **`timestamp` (int)** — Momento da avaliação (Unix Time).

### Exemplos de uso no projeto
- Treinamento de modelos de recomendação (User-Based, Item-Based, Híbridos).  
- Análise de padrões e preferências de usuários.  
- Cálculo de estatísticas: média de notas, popularidade, rankings, etc.

---

## 3. Relação entre os arquivos

Os dois arquivos possuem uma relação **1 : N**:

- `movies.csv` → contém cada filme apenas uma vez;  
- `ratings.csv` → contém múltiplas avaliações para cada filme.

A conexão ocorre por meio da chave **`movieId`**.

### Isso permite análises integradas como:
- Identificar filmes mais populares e mais bem avaliados.  
- Medir quais gêneros possuem melhor aceitação.  
- Criar perfis personalizados de usuários para recomendações.

---
