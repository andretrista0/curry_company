# Projeto Curry Company

#### PROBLEMA DE NEGÓCIO

A Cury Company é uma empresa de tecnologia que desenvolveu um aplicativo que conecta restaurantes, entregadores e pessoas, permitindo que os clientes façam pedidos de refeições de restaurantes cadastrados e os recebam em casa através dos entregadores também cadastrados no aplicativo.

Apesar do crescimento no número de entregas, o CEO da empresa não possui uma visão completa dos indicadores-chave de crescimento (KPIs) da empresa. O modelo de negócio da Cury Company é do tipo Marketplace, atuando como intermediário entre três grupos principais de clientes: restaurantes, entregadores e consumidores.

O objetivo deste projeto é apresentar ao CEO as seguintes métricas de crescimento para cada grupo:

#### Métricas para o lado da empresa:

- Quantidade de pedidos por dia.
- Quantidade de pedidos por semana.
- Distribuição dos pedidos de acordo com o tipo de tráfego.
- Comparação do volume de pedidos por cidade e tipo de tráfego.
- Quantidade de pedidos por entregador por semana.
- Localização central de cada cidade, segmentada por tipo de tráfego.

#### Métricas para o lado dos entregadores:

- Faixa etária dos entregadores (menor e maior idade).
- Condição dos veículos (pior e melhor condição).
- Avaliação média por entregador.
- Avaliação média e desvio padrão por tipo de tráfego.
- Avaliação média e desvio padrão de acordo com as condições climáticas.
- Top 10 dos entregadores mais rápidos por cidade.
- Top 10 dos entregadores mais lentos por cidade.

#### Métricas para o lado dos restaurantes:

- Quantidade de entregadores únicos.
- Distância média entre os restaurantes e os locais de entrega.
- Tempo médio e desvio padrão de entrega por cidade.
- Tempo médio e desvio padrão de entrega por cidade e tipo de pedido.
- Tempo médio e desvio padrão de entrega por cidade e tipo de tráfego.
- Tempo médio de entrega durante os Festivais.

O objetivo final é apresentar um conjunto de gráficos e tabelas que mostrem essas métricas de forma clara e compreensível para o CEO. Isso permitirá que ele acompanhe o crescimento dos negócios da empresa e tome decisões estratégicas informadas.


#### PREMISSAS PARA A ANÁLISE

Para a realização desta análise, foram consideradas as seguintes premissas:

Período de Dados: Os dados utilizados abrangem o período de 11 de fevereiro de 2022 a 06 de abril de 2022. Essa janela de tempo permitirá uma visão representativa do desempenho da Cury Company e suas métricas de crescimento ao longo desse intervalo.

Modelo de Negócio: A análise é baseada no pressuposto de que a Cury Company adota o modelo de negócio chamado "Marketplace". Nesse modelo, a empresa atua como intermediária entre restaurantes, entregadores e consumidores, facilitando a conexão entre eles.

#### Três Principais Visões:

a) Visão Transação de Pedidos: Métricas relacionadas à quantidade de pedidos, distribuição por tipo de tráfego, volume por cidade e tipo de tráfego, entre outros.

b) Visão dos Restaurantes: Métricas referentes aos restaurantes parceiros, como quantidade de entregadores únicos, distância média das entregas, tempo médio de entrega por cidade e tipo de pedido, dentre outras.

c) Visão dos Entregadores: Métricas relacionadas aos entregadores, como faixa etária, condição dos veículos, avaliação média, desempenho por tipo de tráfego e condições climáticas, além dos entregadores mais rápidos e lentos por cidade.

Essas premissas formam a base para a análise dos dados e fornecerão insights valiosos para o CEO da Cury Company tomar decisões estratégicas informadas e acompanhar o crescimento do negócio de maneira mais abrangente.


#### ESTRATÉGIA DA SOLUÇÃO

Para criar um painel estratégico que abranja as três principais visões do modelo de negócio da Cury Company, foram utilizadas métricas relevantes para cada uma delas. Abaixo está o conjunto de métricas representando cada visão:

#### Visão do Crescimento da Empresa:
a. Quantidade de pedidos por dia.
b. Porcentagem de pedidos por condições de trânsito.
c. Quantidade de pedidos por tipo e por cidade.
d. Pedidos por semana.
e. Quantidade de pedidos por tipo de entrega.
f. Quantidade de pedidos por condições de trânsito e tipo de cidade.

#### Visão do Crescimento dos Restaurantes:
a. Quantidade de pedidos únicos.
b. Distância média percorrida.
c. Tempo médio de entrega durante festivais e dias normais.
d. Desvio padrão do tempo de entrega durante festivais e dias normais.
e. Tempo de entrega médio por cidade.
f. Distribuição do tempo médio de entrega por cidade.
g. Tempo médio de entrega por tipo de pedido.

#### Visão do Crescimento dos Entregadores:
a. Idade do entregador mais velho e do mais novo.
b. Avaliação do melhor e do pior veículo.
c. Avaliação média por entregador.
d. Avaliação média por condições de trânsito.
e. Avaliação média por condições climáticas.
f. Tempo médio do entregador mais rápido.
g. Tempo médio do entregador mais rápido por cidade.

Essas métricas foram cuidadosamente selecionadas para fornecer ao CEO uma visão abrangente do crescimento da empresa, dos restaurantes parceiros e dos entregadores que utilizam o aplicativo. O painel estratégico permitirá ao CEO tomar decisões informadas e identificar áreas de oportunidade para aprimorar o desempenho do negócio em cada uma dessas perspectivas.

#### TOP 3 INSIGHTS DE DADOS

#### Sazonalidade Diária nos Pedidos: 
Foi identificada uma sazonalidade diária nos pedidos, com uma variação de aproximadamente 10% na quantidade de pedidos entre dias sequenciais. Isso sugere que há padrões regulares ao longo dos dias da semana, com períodos de maior e menor demanda. Essa informação pode ser valiosa para o planejamento das operações da empresa, como alocação de recursos e gerenciamento da logística de entregas.

#### Cidades Semi-Urbanas e Condições de Trânsito: 
Um padrão interessante surgiu nas cidades classificadas como Semi-Urbanas, onde não são encontradas condições baixas de trânsito. Esse dado pode indicar que as cidades semi-urbanas possuem infraestrutura de transporte mais eficiente em comparação com áreas urbanas. Esse insight pode ser relevante para a empresa ao considerar estratégias de expansão ou foco em áreas específicas.

#### Variações no Tempo de Entrega e Condições Climáticas:
Foi observado que as maiores variações no tempo de entrega ocorrem durante condições climáticas ensolaradas. Isso pode ser explicado por diversos fatores, como maior fluxo de tráfego nas ruas em dias ensolarados, possíveis eventos ou festivais que influenciam o tráfego, entre outros. Entender essa relação permitirá à empresa tomar medidas para otimizar as entregas em diferentes condições climáticas, melhorando a experiência do cliente.

Esses insights fornecem informações valiosas sobre o comportamento do negócio e dos clientes, além de permitir que a Cury Company tome decisões estratégicas mais embasadas. Essa análise dos dados pode impulsionar a eficiência operacional e a satisfação dos clientes, aumentando o sucesso geral da empresa no mercado.
PRODUTO FINAL DO PROJETO 

É um painel online, hospedado em uma plataforma de nuvem (Cloud), que está disponível para acesso em qualquer dispositivo conectado à internet.

Para acessar o painel, basta utilizar o seguinte link: https://currycompany.streamlit.app/

#### CONCLUSÃO:

O projeto foi desenvolvido com o objetivo de criar um conjunto de gráficos e tabelas para exibir as métricas de crescimento da Cury Company de forma clara e compreensível para o CEO. Através do painel online hospedado na nuvem, o CEO agora tem acesso fácil e interativo a informações valiosas que refletem as três principais visões do modelo de negócio da empresa: crescimento da empresa, crescimento dos restaurantes e crescimento dos entregadores.

Ao analisar a visão da Empresa, identificamos uma conclusão significativa: o número de pedidos apresentou crescimento entre a semana 06 e a semana 13 do ano de 2022. Esse dado é crucial para o CEO, pois indica uma tendência positiva de aumento nas transações da empresa durante esse período específico.

No entanto, vale ressaltar que o painel oferece uma variedade de outras métricas para uma análise mais aprofundada. Ao explorar os diferentes gráficos e tabelas, o CEO poderá descobrir insights adicionais e identificar áreas de oportunidade e otimização.

Em suma, o projeto proporcionou à Cury Company uma ferramenta valiosa para acompanhar e compreender o desempenho do negócio de forma mais abrangente e informada. Com uma visão mais clara das métricas de crescimento, o CEO estará melhor equipado para tomar decisões estratégicas, impulsionar a eficiência operacional e aprimorar a experiência do cliente, garantindo o contínuo sucesso da empresa no mercado de tecnologia e delivery.

#### PRÓXIMOS PASSOS:

Após a conclusão do projeto e a implementação do painel online, existem várias ações que podem ser consideradas para aprimorar ainda mais a ferramenta e obter insights adicionais. 

Os próximos passos incluem:

#### Reduzir o Número de Métricas:
É importante revisar as métricas apresentadas no painel e avaliar sua relevância em relação aos objetivos estratégicos da empresa. Remover métricas menos significativas ou redundantes pode tornar o painel mais conciso e focado, facilitando a interpretação dos dados pelos usuários, incluindo o CEO.

#### Criar Novos Filtros:
Considerar a adição de novos filtros ao painel permitirá uma análise mais personalizada dos dados. Novos filtros podem incluir segmentação por região geográfica, faixa de datas específicas, tipo de restaurante ou entregador, entre outros. Essa flexibilidade ajudará o CEO a explorar diferentes cenários e entender melhor o comportamento do negócio em situações específicas.

#### Adicionar Novas Visões de Negócio:
Além das três principais visões já implementadas, pode ser valioso incorporar novas visões de negócio que fornecem insights adicionais sobre o desempenho da empresa. Por exemplo, uma visão relacionada à satisfação do cliente, análise de custos operacionais ou métricas financeiras pode trazer informações valiosas para a tomada de decisões.

#### Coletar e Integrar Novos Dados:
Para enriquecer ainda mais a análise, considerar a coleta e integração de novos dados relevantes ao painel. Isso pode incluir dados demográficos dos clientes, feedbacks de clientes e entregadores, informações sobre a concorrência, entre outros. A expansão da fonte de dados ajudará a empresa a ter uma visão mais completa do seu ecossistema.

#### Aperfeiçoar a Interface do Painel:
Aprimorar a interface do painel em termos de design e usabilidade pode torná-lo mais atraente e intuitivo para os usuários. Uma interface clara e amigável facilitará a navegação e a compreensão dos dados, tornando a experiência do usuário mais agradável.

Esses próximos passos garantirão que o painel de análise continue sendo uma ferramenta valiosa para a Cury Company, capacitando o CEO e outros usuários a tomar decisões estratégicas informadas e impulsionando o crescimento e sucesso contínuo da empresa no mercado de tecnologia e delivery.

