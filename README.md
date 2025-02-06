# Dashboard de Análise de Campanhas de Crédito

Este é um aplicativo interativo criado com **Streamlit** para visualizar o desempenho de campanhas de crédito, analisando métricas de marketing digital e métricas financeiras. O dashboard permite filtrar dados por período, canal de marketing e campanha, além de exibir gráficos e KPIs relevantes.

## Funcionalidades

- **Filtros Interativos**:
  - Selecione o período para visualizar os dados de campanhas.
  - Filtre os dados por canal (Email, Redes Sociais, TV, Google Ads).
  - Filtre os dados por campanha (Promoção A, Promoção B, etc.).

- **KPIs**:
  - Acompanhamento de métricas como número de aplicações, aprovações de crédito, taxa de conversão, custo por aprovação e churn rate.

- **Gráficos**:
  - **Funil de Conversão**: Exibe as conversões de cada campanha em diferentes estágios (Acessos, Cliques, Aplicações, Aprovações).
  - **Tendência de Aprovações**: Exibe a evolução das aprovações de crédito e de cartão ao longo do tempo.
  - **Heatmap de ROI**: Exibe a eficiência de custo por canal/campanha, baseado no custo médio por aprovação.

- **Tabela Detalhada**:
  - Exibe uma tabela com todos os dados filtrados.

## Requisitos

Antes de rodar o projeto, certifique-se de ter as bibliotecas necessárias instaladas. Use o arquivo `requirements.txt` para instalar as dependências:

```bash
pip install -r requirements.txt
