!pip install pandas plotly dash

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State

# Simulação de dados mais realista (com métricas de crédito)
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
campaigns = ['Promoção A', 'Promoção B', 'Promoção C', 'Promoção D']
channels = ['Email', 'Redes Sociais', 'TV', 'Google Ads']

data = {
    'Data': np.random.choice(dates, 1000),
    'Campanha': np.random.choice(campaigns, 1000),
    'Canal': np.random.choice(channels, 1000),
    'Orçamento': np.random.randint(1000, 5000, 1000),  # Novo campo
    'Acessos': np.random.randint(500, 5000, 1000),
    'Cliques': np.random.randint(100, 2000, 1000),
    'Aplicações': np.random.randint(50, 1000, 1000),
    'Aprovações_Crédito': np.random.randint(10, 500, 1000),
    'Aprovações_Cartão': np.random.randint(5, 300, 1000),
    'Churn': np.random.randint(5, 200, 1000)
}

df = pd.DataFrame(data).sort_values('Data')

# Cálculo de métricas derivadas
df['Taxa_Clique'] = df['Cliques'] / df['Acessos']
df['Taxa_Aplicação'] = df['Aplicações'] / df['Cliques']
df['Taxa_Aprovação'] = df['Aprovações_Crédito'] / df['Aplicações']
df['Custo_Por_Aprovação'] = df['Orçamento'] / df['Aprovações_Crédito']

# Inicialização do Dash
app = dash.Dash(__name__)
app.title = "Analytics de Campanhas de Crédito"

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Performance de Campanhas de Crédito", style={'textAlign': 'center'}),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label("Período:"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['Data'].min(),
                end_date=df['Data'].max()
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Canal:"),
            dcc.Dropdown(
                id='channel-filter',
                options=[{'label': c, 'value': c} for c in channels],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Campanha:"),
            dcc.Dropdown(
                id='campaign-filter',
                options=[{'label': c, 'value': c} for c in campaigns],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ]),
    
    # KPIs
    html.Div(id='kpi-container', style={'marginTop': 20}),
    
    # Gráficos
    dcc.Graph(id='conversion-funnel'),
    dcc.Graph(id='approval-trend'),
    dcc.Graph(id='roi-heatmap'),
    
    # Tabela Detalhada
    html.Div(id='data-table', style={'marginTop': 20})
])

# Callbacks
@app.callback(
    [Output('kpi-container', 'children'),
     Output('conversion-funnel', 'figure'),
     Output('approval-trend', 'figure'),
     Output('roi-heatmap', 'figure'),
     Output('data-table', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('channel-filter', 'value'),
     Input('campaign-filter', 'value')]
)
def update_dashboard(start_date, end_date, selected_channels, selected_campaigns):
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
        'Taxa Conversão Total': f"{(filtered_df['Aprovações_Crédito'].sum() / filtered_df['Acessos'].sum() * 100):.1f}%",
        'Custo Médio por Aprovação': f"R${filtered_df['Custo_Por_Aprovação'].mean():.2f}",
        'Churn Rate': f"{(filtered_df['Churn'].sum() / filtered_df['Aprovações_Crédito'].sum() * 100):.1f}%"
    }
    
    # Layout dos KPIs
    kpi_container = html.Div([
        html.Div([
            html.H4(k),
            html.P(str(v)),
        ], style={
            'width': '16%', 
            'display': 'inline-block',
            'textAlign': 'center',
            'border': '1px solid #ddd',
            'padding': '10px',
            'margin': '5px'
        }) for k, v in kpis.items()
    ])
    
    # Funil de Conversão
    funnel_fig = px.funnel(
        filtered_df.groupby('Campanha').agg({
            'Acessos': 'sum',
            'Cliques': 'sum',
            'Aplicações': 'sum',
            'Aprovações_Crédito': 'sum'
        }).reset_index(),
        x=['Acessos', 'Cliques', 'Aplicações', 'Aprovações_Crédito'],
        y='Campanha',
        title='Funil de Conversão por Campanha'
    )
    
    # Tendência de Aprovações
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
    
    # Heatmap de ROI
    roi_fig = px.density_heatmap(
        filtered_df,
        x='Canal',
        y='Campanha',
        z='Custo_Por_Aprovação',
        title='Eficiência de Custo por Canal/Campanha',
        histfunc="avg"
    )
    
    # Tabela Detalhada
    table = dash.dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in filtered_df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'}
    )
    
    return kpi_container, funnel_fig, trend_fig, roi_fig, table

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
