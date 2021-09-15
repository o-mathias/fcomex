import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import dash_table
import dash_table.FormatTemplate as FormatTemplate
from app.models import FComex, NCM, VIA

from django_plotly_dash import DjangoDash

from django.core.cache import cache

app = DjangoDash('dash_app_id', external_stylesheets=[dbc.themes.BOOTSTRAP])
'''
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
'''
anos = pd.DataFrame.from_records(FComex.objects.all().values('ano'))

#print('ANOOOS:', anos)
df_ncm = pd.DataFrame.from_records(NCM.objects.all().values())
df_via = pd.DataFrame.from_records(VIA.objects.all().values())

#print(df_ncm)

ano = [{'label':ano, 'value':ano} for ano in anos['ano'].unique()]
prd = [{'label':prd['no_ncm_por'], 'value':prd['id_ncm']} for idx,prd in df_ncm.iterrows()]
prd.append({'label':'Todos', 'value':'Todos'})



app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    html.H4(children='Filtros'),
    dcc.Dropdown(
        id='drop-ano',
        options=ano,
        value=2020
    ),
    html.Br(),
    dcc.Dropdown(
        id='drop-mov',
        options=[
            {'label': 'Importação', 'value': 'Importação'},
            {'label': 'Exportação', 'value': 'Exportação'}
        ],
        value='Importação'
    ),
    html.Br(),
    dcc.Dropdown(
        id='drop-prd',
        options=prd,
        value='Todos'
    ),
    html.Br(),
    dbc.Card(id='card-total',
        className="mb-3",
    ),
    html.Br(),
    html.H4(id='qnt-title'),
    dcc.Graph(
        id='qnt-graph',
    ),

    html.H4(id='via-title'),
    dcc.Graph(
        id='via-graph',
    ),

    html.H4(id='table-title'),
    dash_table.DataTable(
        id='table',
        sort_action='native',
        columns=[{"name": 'UF', "id": 'sg_uf'},
                 {"name": 'Valor', "id": 'vl_fob','type': 'numeric', 'format': FormatTemplate.money(0)},
                 {"name": 'Participação', "id": 'PART','type': 'numeric', 'format': FormatTemplate.percentage(2)}],
        style_cell={'padding': '5px'},
        style_header={
            'backgroundColor': 'darkblue',
            'fontWeight': 'bold',
            'color': 'white'
        },
    ),

    #html.Table(id='fob-table'),

])


def query_cache(ano, mov, prd):

    p_comex = f'comex-{ano}-{mov}'
    df_comex = cache.get(p_comex)

    if type(df_comex) == type(None):
        columns = ['ano', 
                    'movimentacao', 
                    'ncm', 
                    'via', 
                    'sg_uf', 
                    'vl_fob',
                    'mes',
                    'vl_quantidade']
        df_comex = pd.DataFrame.from_records(
            FComex.objects.filter(ano=ano, movimentacao=mov).values(
                                        *columns))

        if len(df_comex) == 0:
            df_comex = pd.DataFrame(columns=columns)

        cache.set(p_comex, df_comex)

    #print('---------------CACHED-------------', df_comex)
    p = f'{ano}-{mov}-{prd}'
    filtered_df = cache.get(p)
    #print('---------------CACHED-------------', filtered_df)

    if type(filtered_df) == type(None):
        
        if prd == 'Todos':
            filtered_df = df_comex[(df_comex.ano == ano) & \
                (df_comex.movimentacao == mov)]
        else:
            filtered_df = df_comex[(df_comex.ano == ano) & \
                (df_comex.movimentacao == mov) & \
                    (df_comex.ncm == prd)]

        cache.set(p, filtered_df, 200)
    
    return filtered_df



@app.callback(
    Output('qnt-graph', 'figure'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_figure(ano, mov, prd):
    filtered_df = query_cache(ano, mov, prd)

    qnt_df = filtered_df[['mes', 'vl_quantidade']].groupby(['mes']).sum().sort_values('mes')
    #print('qnt', qnt_df)

    ticks = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', \
        'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    tick_vals = [1,2,3,4,5,6,7,8,9,10,11,12]

    if len(qnt_df) == 0:
        qnt_df = pd.DataFrame(columns=['mes', 'vl_quantidade'])

    fig = px.bar(qnt_df, x=qnt_df.index, y="vl_quantidade", barmode="group")

    fig.update_layout(transition_duration=500,
                        xaxis = dict(
                            tickmode = 'array',
                            tickvals = tick_vals,
                            ticktext = ticks
                        ))

    cache.set('filtered_df', filtered_df)

    return fig

@app.callback(
    Output('via-graph', 'figure'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_figure(ano, mov, prd):
    #print(ano, mov, prd)
    filtered_df = query_cache(ano, mov, prd)

    qnt_df = filtered_df['via'].value_counts().sort_index()

    name_via = [df_via[df_via['id_via']==x]['no_via'] for x in qnt_df.index]


    fig = px.pie(qnt_df, names=name_via, values="via", title="")

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    #*table_callbacks_out,
    Output('table', 'data'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_table(ano, mov, prd):

    filtered_df = query_cache(ano, mov, prd)

    if len(filtered_df):
    
        qnt_df = filtered_df[['sg_uf', 'vl_fob']].groupby(['sg_uf'], as_index=False).sum()
        qnt_df['PART'] = (qnt_df['vl_fob']/qnt_df['vl_fob'].sum())

        return qnt_df.to_dict('records')

    else:
        return pd.DataFrame(columns=['sg_uf', 'vl_fob', 'PART']).to_dict('records')

@app.callback(
    Output('qnt-title', 'children'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_title_bar(ano, mov, prd):
    if prd == 'Todos':
        title = f'Quantidade total de {mov} por mês em {ano}'
    else:
        prod = df_ncm[df_ncm['id_ncm']==prd]['no_ncm_por'].iloc[0]
        title = f'Quantidade de {mov} de {prod} por mês em {ano}'
    return title

@app.callback(
    Output('via-title', 'children'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_title_via(ano, mov, prd):
    if prd == 'Todos':
        title = f'Percentual de utilização de via para {mov} por estado em {ano}'
    else:
        prod = df_ncm[df_ncm['id_ncm']==prd]['no_ncm_por'].iloc[0]
        title = f'Percentual de utilização de via para {mov} de {prod} por estado em {ano}'
    return title

@app.callback(
    Output('table-title', 'children'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_title_table(ano, mov, prd):
    if prd == 'Todos':
        title = f'Total de {mov} por estado em {ano}'
    else:
        prod = df_ncm[df_ncm['id_ncm']==prd]['no_ncm_por'].iloc[0]
        title = f'Total de {mov} de {prod} por estado em {ano}'
    return title

@app.callback(
    Output('card-total', 'children'),
    Input('drop-ano', 'value'),
    Input('drop-mov', 'value'),
    Input('drop-prd', 'value'))
def update_card(ano, mov, prd):

    filtered_df = query_cache(ano, mov, prd)

    qnt_df = filtered_df['vl_quantidade'].sum()
    total = '{0:,} unidades'.format(qnt_df).replace(',','.')


    if prd == 'Todos':
        title = f'Total de {mov} em {ano}'
    else:
        prod = df_ncm[df_ncm['id_ncm']==prd]['no_ncm_por'].iloc[0]
        title = f'Total de {mov} de {prod} em {ano}'
    cb = dbc.CardBody(
        [
            html.H4(title, className="card-title"),
            html.H5(total, className="card-subtitle")
        ])
    return cb



if __name__ == '__main__':
    app.run_server(8052, debug=False)