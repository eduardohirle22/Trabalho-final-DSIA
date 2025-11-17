# Trabalho-final-DSIA
Desenvolvimento de uma aplicação completa de recomendação 
Documentação da Base de Dados (Introdução do Projeto)

A base de dados utilizada neste projeto é composta por dois arquivos principais — movies.csv e ratings.csv — que juntos formam um conjunto clássico utilizado em sistemas de recomendação, semelhante ao MovieLens. O objetivo dessa base é permitir análises sobre comportamentos de usuários, preferências de filmes e avaliar modelos de filtragem colaborativa ou conteúdo.

1. Arquivo: movies.csv

Este arquivo contém informações descritivas sobre os filmes presentes no catálogo.

Quantidade de registros: 9.742 filmes
Colunas:

movieId (int) — Identificador único do filme, usado como chave principal.

title (string) — Título do filme, geralmente contendo o ano de lançamento.

genres (string) — Lista de gêneros do filme separados pelo caractere | (ex.: Comedy|Drama).

Exemplos de uso no projeto

Enriquecimento de recomendações pela similaridade de gêneros.

Análises por categorias (comédia, ação, romance etc.).

Junção com as avaliações para contextualização dos resultados.

2. Arquivo: ratings.csv

Este arquivo armazena as avaliações feitas por usuários para os filmes cadastrados.

Quantidade de registros: 100.836 avaliações
Colunas:

userId (int) — Identificador do usuário que avaliou o filme.

movieId (int) — Identificador do filme avaliado (chave estrangeira ligada a movies.csv).

rating (float) — Nota atribuída ao filme, variando de 0.5 a 5.0.

timestamp (int) — Momento da avaliação em formato Unix Time.

Exemplos de uso no projeto

Treinamento de modelos de recomendação (CF baseado em usuários/itens).

Análise de padrões de comportamento de usuários.

Cálculo de métricas como média de notas, dispersão e rankings.

3. Relação entre os arquivos

A base possui uma relação 1:N, onde o arquivo movies.csv contém os filmes e o arquivo ratings.csv registra múltiplas avaliações desses filmes. A chave que conecta os dois é movieId.

Isso permite análises integradas, tais como:

Identificar quais filmes são mais populares.

Medir quais gêneros recebem melhores avaliações.

Estimar perfis de usuários para recomendações personalizadas.
