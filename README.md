# **Análise de Performance de Campanhas de Crédito**

## **Descrição**

Este projeto tem como objetivo analisar o desempenho de campanhas voltadas para a aquisição de cartões de crédito. A análise é realizada com base em métricas de conversão, custo por aprovação e churn, utilizando dados simulados para as principais etapas do processo de aquisição:

1. **Acessos**: Número total de visitantes nas campanhas.
2. **Cliques**: Total de cliques nas campanhas.
3. **Aplicações**: Total de aplicações feitas pelos usuários.
4. **Aprovações de Crédito**: Aprovações de crédito realizadas após a aplicação.
5. **Aprovações de Cartão**: Aprovações de cartão realizadas após a aprovação de crédito (sempre menor ou igual a aprovações de crédito).
6. **Churn**: Taxa de desistência durante o processo de aquisição do cartão.

Através dessas métricas, buscamos entender a eficiência das campanhas, as taxas de conversão em cada etapa do funil e o impacto do churn no processo de aquisição.

---

## **Estrutura do Projeto**

### **1. Geração de Dados Simulados**

A geração dos dados simulados considera as métricas chave de cada campanha. Os dados incluem:

- **Data da campanha**: Variando entre janeiro e fevereiro de 2024.
- **Campanhas**: Nome das campanhas que estão sendo analisadas.
- **Canais de divulgação**: Canais como Email, Redes Sociais, TV e Google Ads.
- **Orçamento**: O valor investido em cada campanha.
- **Acessos, Cliques, Aplicações, Aprovações de Crédito e Aprovações de Cartão**: Contagem de cada um dos eventos que fazem parte do processo de aquisição do cartão.
- **Churn**: Número de desistências durante o processo.

### **2. Métricas Calculadas**

As principais métricas calculadas são:

- **Taxa de Clique**: Percentual de cliques em relação ao total de acessos.
- **Taxa de Aplicação**: Percentual de aplicações em relação aos cliques.
- **Taxa de Aprovação de Crédito**: Percentual de aprovações de crédito em relação às aplicações.
- **Taxa de Aprovação de Cartão**: Percentual de aprovações de cartão em relação às aprovações de crédito.
- **Custo por Aprovação**: Custo médio por cada aprovação de crédito.
- **Taxa de Churn**: Percentual de desistências no processo de aquisição.


### **3. Visualizações e Gráficos**

O projeto também oferece gráficos interativos utilizando **Plotly** e **Streamlit** para facilitar a análise dos dados:

- **Funil de Conversão por Campanha**: Mostra a jornada do cliente desde os acessos até a aprovação do cartão, destacando a taxa de conversão em cada etapa.
- **Tendência de Aprovações**: Exibe a evolução das aprovações de crédito e cartão ao longo do tempo.
- **Eficiência de Custo por Canal/Campanha**: Um gráfico de heatmap para analisar a eficiência do custo por aprovação em cada canal de divulgação e campanha.
