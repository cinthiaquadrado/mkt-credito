import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Simulação de dados mais realista (com métricas de crédito)
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
campaigns = ['Promoção A', 'Promoção B', 'Promoção C', 'Promoção D']
channels = ['Email', 'Redes Sociais', 'TV', 'Google Ads']

# Dados simulados com a lógica de que Aprovações Crédito >= Aprovações Cartão
data = {
    'Data': np.random.choice(dates, 1000),
    'Campanha': np.random.choice(campaigns, 1000),
    'Canal': np.random.choice(channels, 1000),
    'Orçamento': np.random.randint(1000, 5000, 1000),
    'Acessos': np.random.randint(500, 5000, 1000),
    'Cliques': np.random.randint(100, 2000, 1000),
    'Aplicações': np.random.randint(50, 1000, 1000),
    'Aprovações_Crédito': np.random.randint(10, 500, 1000),
    'Aprovações_Cartão': np.random.randint(5, 300, 1000),
    'Churn': np.random.randint(5, 200, 1000)
}

# Garantir que as Aprovações_Cartão sejam sempre menores ou iguais a Aprovações_Crédito
df = pd.DataFrame(data)
df['Aprovações_Cartão'] = df.apply(lambda row: min(row['Aprovações_Crédito'], row['Aprovações_Cartão']), axis=1)
df = df.sort_values('Data')

# Cálculo de métricas derivadas
df['Taxa_Clique'] = df['Cliques'] / df['Acessos']
df['Taxa_Aplicação'] = df['Aplicações'] / df['Cliques']
df['Taxa_Aprovação_Crédito'] = df['Aprovações_Crédito'] / df['Aplicações']
df['Taxa_Aprovação_Cartão'] = df['Aprovações_Cartão'] / df['Aprovações_Crédito']
df['Custo_Por_Aprovação'] = df['Orçamento'] / df['Aprovações_Crédito']

# Layout Streamlit
st.title("Performance de Campanhas de Crédito")

# Seleção de abas
page = st.selectbox("Escolha uma página", ["Dashboard", "Explicações de métricas"])

if page == "Dashboard":
    # Seleção de datas e canais
    start_date = st.date_input('Início', df['Data'].min())
    end_date = st.date_input('Fim', df['Data'].max())
    selected_channels = st.multiselect('Canal', channels, default=channels)
    selected_campaigns = st.multiselect('Campanha', campaigns, default=campaigns)

    # Garantir que as datas selecionadas sejam convertidas para datetime64
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filtragem de dados
    filtered_df = df[
        (df['Data'] >= start_date) & 
        (df['Data'] <= end_date)
    ]

    if selected_channels:
        filtered_df = filtered_df[filtered_df['Canal'].isin(selected_channels)]

    if selected_campaigns:
        filtered_df = filtered_df[filtered_df['Campanha'].isin(selected_campaigns)]

    # Cálculo de KPIs
    kpis = {
        'Aplicações': filtered_df['Aplicações'].sum(),
        'Aprovações Crédito': filtered_df['Aprovações_Crédito'].sum(),
        'Aprovações Cartão': filtered_df['Aprovações_Cartão'].sum(),
        'Taxa Conversão Crédito': f"{(filtered_df['Aprovações_Crédito'].sum() / filtered_df['Acessos'].sum() * 100):.1f}%",
        'Taxa Conversão Cartão': f"{(filtered_df['Aprovações_Cartão'].sum() / filtered_df['Aprovações_Crédito'].sum() * 100):.1f}%",
        'Custo Médio por Aprovação': f"R${filtered_df['Custo_Por_Aprovação'].mean():.2f}",
        'Churn Rate': f"{(filtered_df['Churn'].sum() / filtered_df['Aprovações_Crédito'].sum() * 100):.1f}%"
    }

    # Exibição dos KPIs em colunas
    col1, col2, col3 = st.columns(3)  # Cria 3 colunas para exibição lado a lado

    with col1:
        st.metric(label="Aplicações", value=kpis['Aplicações'])
        st.metric(label="Aprovações Crédito", value=kpis['Aprovações Crédito'])

    with col2:
        st.metric(label="Aprovações Cartão", value=kpis['Aprovações Cartão'])
        st.metric(label="Taxa Conversão Crédito", value=kpis['Taxa Conversão Crédito'])

    with col3:
        st.metric(label="Custo Médio por Aprovação", value=kpis['Custo Médio por Aprovação'])
        st.metric(label="Churn Rate", value=kpis['Churn Rate'])

    # Gráfico de Funil de Conversão
    st.subheader('Funil de Conversão por Campanha')
    funnel_fig = px.funnel(
        filtered_df.groupby('Campanha').agg({
            'Acessos': 'sum',
            'Cliques': 'sum',
            'Aplicações': 'sum',
            'Aprovações_Crédito': 'sum',
            'Aprovações_Cartão': 'sum'
        }).reset_index(),
        x=['Acessos', 'Cliques', 'Aplicações', 'Aprovações_Crédito', 'Aprovações_Cartão'],
        y='Campanha',
        title='Funil de Conversão por Campanha'
    )
    st.plotly_chart(funnel_fig)

    # Gráfico de Tendência de Aprovações
    st.subheader('Tendência de Aprovações')
    trend_fig = px.line(
        filtered_df.groupby('Data').agg({
            'Aprovações_Crédito': 'sum',
            'Aprovações_Cartão': 'sum'
        }).reset_index(),
        x='Data',
        y=['Aprovações_Crédito', 'Aprovações_Cartão'],
        title='Tendência de Aprovações',
        markers=True
    )
    st.plotly_chart(trend_fig)

    # Gráfico de Heatmap de ROI
    st.subheader('Eficiência de Custo por Canal/Campanha')
    roi_fig = px.density_heatmap(
        filtered_df,
        x='Canal',
        y='Campanha',
        z='Custo_Por_Aprovação',
        title='Eficiência de Custo por Canal/Campanha',
        histfunc="avg"
    )
    st.plotly_chart(roi_fig)

    # Tabela Detalhada
    st.subheader('Tabela Detalhada')
    st.dataframe(filtered_df)

elif page == "Explicações de métricas":
    # Explicação sobre as métricas
    st.subheader("Explicação das Métricas")

    with st.expander("Clique aqui para ver as explicações"):
        st.write(""" 
            ### 1. **Aplicações**
            Refere-se ao número total de aplicações realizadas pelos usuários que visualizaram a campanha.

            ### 2. **Aprovações Crédito**
            Número total de aprovações de crédito realizadas com sucesso após uma aplicação.

            ### 3. **Aprovações Cartão**
            Número total de aprovações de cartão realizadas com sucesso após a aprovação de crédito. Essa é uma fase seguinte do processo e pode ser menor que as aprovações de crédito.

            ### 4. **Taxa Conversão Crédito**
            Taxa que mede a porcentagem de acessos que resultaram em aprovações de crédito. A fórmula é:
            ```
            (Aprovações Crédito / Acessos) * 100
            ```

            ### 5. **Taxa Conversão Cartão**
            Taxa que mede a porcentagem de aprovações de crédito que resultaram em aprovações de cartão. A fórmula é:
            ```
            (Aprovações Cartão / Aprovações Crédito) * 100
            ```

            ### 6. **Custo Médio por Aprovação**
            O custo médio gasto por cada aprovação de crédito. A fórmula é:
            ```
            Orçamento / Aprovações Crédito
            ```

            ### 7. **Churn Rate**
            Taxa de churn que mede o percentual de desistências no processo, sendo calculado da seguinte forma:
            ```
            (Churn / Aprovações Crédito) * 100
            """)

