# 1. Problema de negócio

Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa
iRango Food Company, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!

A empresa iRango Food Company é um marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da iRango Food Company que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

A iRango Food Company possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre três clientes principais: restaurantes e pessoas compradoras. Para
acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

## Visão Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## Visão Países

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Visão Cidades

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

## Visão Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

## Visão Cozinhas

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. O CEO precisa
dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa iRango Food Company para conseguir tomar decisões mais assertivas. Seu trabalho é utilizar os dados que a empresa iRango Food Company possui e responder as perguntas feitas do CEO e criar o dashboard solicitado.

Seu trabalho é utilizar os dados que a empresa iRango Food Company possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

# 2. Premissas do negócio

1. Para esta análise foram utilizados dados públicos disponibilizados no Kaggle através deste link: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
2. Marketplace foi o modelo de negócio assumido.
3. As 4 principais visões do negócio foram: visão geral, visão países, visão cidades e visão restaurantes.

# 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:

1. Visão Geral.
2. Visão Países.
3. Visão Cidades.
4. Visão Restaurantes.

Cada visão é representada pelo seguinte conjunto de métricas:

1. Visão Geral.
    1. Quantidade de restaurantes registrados.
    2. Quantidade de países registrados.
    3. Quantidade de cidades registradas.
    4. Quantidade de avaliações registradas.
    5. Quantidade de culinárias registradas.
    6. Mapa com a localização central dos restaurantes, clusterizados por região e categorizados (cor dor marcador) pela avaliação média.
2. Visão Países.
    1. Quantidade de restaurantes registrados por país.
    2. Quantidade de cidades registradas por país.
    3. Média de avaliações feitas por país.
    4. Custo médio de um prato para duas pessoas.
3. Visão Cidades.
    1. Top 10 cidades com mais restaurantes registrados por país.
    2. Cidades com mais restaurantes com média acima de 4.
    3. Cidades com mais restaurantes com média baixo de 2.5.
    4. Top 10 cidades com mais tipos de culinárias distintas.
4. Visão Cozinhas
    1. Avaliação média dos Top 5 melhores restaurantes dos tipos culinárias mais bem avaliados.
    2. Top 10 restaurantes mais bem avaliados da plataforma.
    3. Top 10 culinárias mais bem avaliadas.
    4. Top 10 culinárias menos bem avaliadas.

# 4. Top 3 Insights de dados

1. O país com mais restaurantes registrados é também o que possui uma das menores médias de avaliações registradas.
2. A cidade que possui maior número de restaurantes com média de avaliação acima de 4, corresponde ao país da cidade que tem o maior número de restaurantes com média de avaliação abaixo de 2.5
3. Os restaurantes com maior custo médio do prato para 2 pessoas não estão entre os top 10 mais bem avaliados da plataforma

# 5. O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através desse link: https://ftcprojetoaluno-irangofoodcompany.streamlit.app/

# 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
que exibam essas métricas da melhor forma possível para o CEO.

No geral, podemos concluir que o país com maior número restaurantes registrados não possui uma das maiores média de avaliações registradas, porém contém a maior quantidade de culinárias distintas. Além disso, concentra em suas cidades a maior quantidade de restaurantes com avaliação acima de 4 e abaixo de 2.5. Os restaurantes que possuem os pratos mais caros, não são necessariamente os mais bem avaliados.

# 7. Próximos passos

1. Aumentar o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.
