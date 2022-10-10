
from datetime import datetime
from this import d
import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO


#importando e tratamento dos dados
df = pd.read_table("C:/projetos/meus/meus_dash/meu-dash-preco-combustivel/2004-2021.tsv")

df["DATA INICIAL"] = pd.to_datetime(df["DATA INICIAL"])
df["DATA FINAL"] = pd.to_datetime(df["DATA FINAL"])
df["MES"] = df["DATA INICIAL"].dt.month
df["ANO"] = df["DATA INICIAL"].dt.year
df['MES/ANO'] = df['DATA INICIAL'].dt.strftime('%m/%Y')


df.rename(columns={"DATA INICIAL":"DATA", "PREÇO MÉDIO REVENDA": "VALOR REVENDA"},inplace = True)

df_gasolina = df[df["PRODUTO"] == "GASOLINA COMUM"].reset_index(drop = ["index"])
df_gasolina = df_gasolina[["DATA", "REGIÃO", "ESTADO", "VALOR REVENDA", "ANO", "MES", "MES/ANO"]]

df_gasolina["ANO"] = df_gasolina["ANO"].astype(str)
df_gasolina.at[df_gasolina.index[1], "ANO"]

df_store = df_gasolina.to_dict()

# ========= App ============== #
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css])
app.scripts.config.serve_locally = True
server = app.server

# ========== Styles ============ #

template_theme1 = "flatly"
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR

tab_card = {"height":"100%"}

main_config = {
    "hovermode":"x unified",
    "legend": {"yanchor":"top",
                "y":0.9,
                "xanchor":"left",
                "x":0.1,
                "title":{"text":None},
                "font":{"color":"white"},
                "bgcolor":"rgba(0,0,0,0.5)"},
    "margin": {"l":0, "r":0, "t":10, "b":0}

}

# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    dcc.Store(id = "dataset", data = df_store),
    dcc.Store(id = "dataset_fixed", data = df_store),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([

                    dbc.Row([
                        dbc.Col([
                            html.Legend("Gas Prices Analysis")
                        ], sm = 8),
                        dbc.Col([
                            html.I(className="fa fa-filter", style= {"font-size":"300%"})
                        ], sm = 4, align = "center")

                    ]),

                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("JC PASTORIL")
                        ])
                    ], style = {"margin-top":"10px"}),

                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Visite o site", href="https://fontawesome.com/icons/filter?s=solid&f=classic", target="_blank")
                        ], style={"margin-top": "10px"})
                    ])
                ])
            ], style = tab_card)

        ], sm = 4, lg = 2),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3("MÁXIMOS E MÍNIMOS"),
                            dcc.Graph(id = "static-maxmin", config = {"displayModeBar":False, "showTips":False})
                        ])
                    ])
                ])
            ], style = tab_card)          
        ], sm = 8, lg = 3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("ANO DE ANÁLISE"),
                            dcc.Dropdown(
                                id="select_ano",
                                value = df_gasolina.at[df_gasolina.index[1], "ANO"],
                                clearable=False,
                                className="dbc",
                                options=[{"label":x, "value":x} for x in df_gasolina["ANO"].unique()]
                            )
                        ], sm = 6),

                        dbc.Col([
                            html.H6("REGIÃO DE ANÁLISE"),
                            dcc.Dropdown(
                                id="select_regiao",
                                value = df_gasolina.at[df_gasolina.index[1], "REGIÃO"],
                                clearable=False,
                                className="dbc",
                                options=[{"label":x, "value":x} for x in df_gasolina["REGIÃO"].unique()])
                        ], sm = 6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="regiaobar_graph", config = {"displayModeBar":False, "showTips":False})
                        ], sm = 12, md=6),
                        dbc.Col([
                            dcc.Graph(id = "estadobar_graph", config = {"displayModeBar":False, "showTips":False})
                        ], sm = 12, md = 6)
                    ], style = {"column-gap":"0px"})
                ])
            ], style = tab_card)
        ], sm = 12, lg = 7)
    
    ], className = "g-2 my-auto"),

    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("PREÇO X ESTADO"),
                    html.H6("COMPARAÇÃO TEMPORAL ENTRE ESTADOS"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_estado0",
                                value = [df_gasolina.at[df_gasolina.index[3], "ESTADO"], 
                                        df_gasolina.at[df_gasolina.index[13], "ESTADO"],
                                        df_gasolina.at[df_gasolina.index[6], "ESTADO"]],
                                clearable = False,
                                className="dbc",
                                multi = True,
                                options=[{"label":x, "value":x} for x in df_gasolina.ESTADO.sort_values().unique()]
                                )
                        ], sm = 10),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id= "animation_graph", config = {"displayModeBar":False, "showTips":False})
                        ])
                    ])                
                ])
            ], style = tab_card)
        ], sm = 12, md = 6, lg = 5),

        dbc.Col([

            dbc.Card([
                dbc.CardBody([
                    html.H3("COMPARAÇÃO DIRETA"),
                    html.H6("QUAL PREÇO É MENOR EM UM DADO PERÍODO DE TEMPO?"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_estado1",
                                value = df_gasolina.at[df_gasolina.index[3], "ESTADO"],
                                clearable = False,
                                className="dbc",
                                options=[{"label":x, "value":x} for x in df_gasolina.ESTADO.sort_values().unique()]
                            )
                        ], sm = 10, md = 5),
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_estado2",
                                value = df_gasolina.at[df_gasolina.index[1], "ESTADO"],
                                clearable = False,
                                className="dbc",
                                options=[{"label":x, "value":x} for x in df_gasolina.ESTADO.sort_values().unique()]
                            )
                        ], sm = 10, md = 6)
                    
                        ], style = {"margin-top":"20px"}, justify = "center"),
                    dcc.Graph(id = "direct_comparison_graph", config = {"displayModeBar":False, "showTips":False}),
                    html.P(id = "desc_comparison", style = {"color":"gray", "font-size":"80%"})
                ]),
            ], style = tab_card),
        ], sm = 12, md =6, lg = 4),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id = "card1_indicators", config = {"displayModeBar":False, "showTips":False}, style = {"margin-top":"30px"})
                        ])                                                    
                    ], style = tab_card)
                ])
            ], justify = "center", style = {"padding-bottom":"7px", "height":"50%"}),  
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id = "card2_indicators", config={"displayModeBar":False, "showTips":False}, style = {"margin-top":"30px"})
                        ])
                    ], style = tab_card)
                ])
            ], justify="center", style = {"height":"50%"})                           
        ], sm = 12, lg = 3, style = {"height":"100%"})

    ], className = "g-2 my-auto"),


    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        dbc.Button([html.I(className="fa fa-play")], id = "play-button", style = {"margin-right":"15px"}),
                        dbc.Button([html.I(className = "fa fa-stop")], id = "stop-button")
                    ], sm = 12, md = 1, style = {"justify-content":"center", "margin-top":"10px"}),
                dbc.Col([
                    dcc.RangeSlider(
                        id = "rangeslider",
                        marks = {int(x):f'{x}' for x in df_gasolina["ANO"].unique()},
                        step = 3,
                        min = 2004,
                        max = 2021,
                        className="dbc",
                        value = [2004, 2021],
                        dots = True,
                        pushable=3,
                        tooltip = {"always_visible":False, "placement":"bottom"}
                    )
                ], sm = 12, md = 10, style = {"margin-top":"15px"}),

                dcc.Interval(id = "interval", interval=200)
                ], className="g-1", style = {"height":"20%", "justify-content":"center"})
            ], style = tab_card)
        ])
    ], className = "g-2 my-auto")


], fluid=True, style={'height': '100%'})

# ======== Callbacks ========== #

@app.callback(
    Output("static-maxmin", "figure"),
    Input("dataset", "data"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def func(data, toggle):

    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)
    max = dff.groupby(["ANO"])["VALOR REVENDA"].max()
    min = dff.groupby(["ANO"])["VALOR REVENDA"].min()

    final_df = pd.concat([max, min], axis = 1)
    final_df.columns = ["MÁXIMO", "MÍNIMO"]

    fig = px.line(final_df, x = final_df.index, y = final_df.columns, template = template)

    fig.update_layout(main_config, height=150, xaxis_title = None, yaxis_title = None)


    return fig
# região de barras horizontais

@app.callback(
    [Output("regiaobar_graph", "figure"),
    Output("estadobar_graph", "figure")],
    [Input("dataset", "data"),
    Input("select_ano", "value"),
    Input("select_regiao", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)

def func(data, ano, regiao, toggle):

    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)

    df_filtered = dff[dff.ANO.isin([ano])]


    df_regiao = df_filtered.groupby(["ANO", "REGIÃO"])["VALOR REVENDA"].mean().reset_index()
    df_estado = df_filtered.groupby(["ANO", "ESTADO", "REGIÃO"])["VALOR REVENDA"].mean().reset_index()
    df_estado = df_estado[df_estado.REGIÃO.isin([regiao])]

    df_regiao = df_regiao.sort_values(by=["VALOR REVENDA"], ascending= True)
    df_estado = df_estado.sort_values(by=["VALOR REVENDA"], ascending= True)

    
    df_regiao["VALOR REVENDA"] = df_regiao["VALOR REVENDA"].round(2)
    df_estado["VALOR REVENDA"] = df_estado["VALOR REVENDA"].round(2)

    fig1_text = [f'{x} - R${y}' for x, y in zip(df_regiao.REGIÃO.unique(), df_regiao["VALOR REVENDA"].unique())]
    fig2_text = [f'R${y} - {x}' for x, y in zip(df_estado.ESTADO.unique(), df_estado["VALOR REVENDA"].unique())]


    fig1 = go.Figure(go.Bar(
        x = df_regiao["VALOR REVENDA"],
        y = df_regiao["REGIÃO"],
        orientation="h",
        text = fig1_text,
        textposition="auto",
        insidetextanchor="end",
        insidetextfont=dict(family = "Times", size = 12)
    ))

    fig1.update_layout(main_config, height=140, yaxis = {"showticklabels":False}, template=template, xaxis_range = [df_regiao["VALOR REVENDA"].max(), df_regiao["VALOR REVENDA"].min() - 0.15])
    

    fig2 = go.Figure(go.Bar(
        x = df_estado["VALOR REVENDA"],
        y = df_estado["ESTADO"],
        orientation="h",
        text = fig2_text,
        insidetextanchor="end",
        insidetextfont=dict(family = "Times", size = 12)
    ))
    fig2.update_xaxes(autorange = "reversed")
    fig2.update_layout(main_config, height=140, yaxis = {"showticklabels":False}, template=template, xaxis_range = [df_estado["VALOR REVENDA"].max() - 0.15, df_estado["VALOR REVENDA"].min()])


    return [fig1, fig2]

@app.callback(
    Output("animation_graph", "figure"),
    Input("dataset", "data"),
    Input("select_estado0", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def animation(data, estados, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)
    mask = dff.ESTADO.isin(estados)
    fig = px.line(dff[mask], x = 'DATA', y = "VALOR REVENDA",
        color = "ESTADO", template = template)
    
    fig.update_layout(main_config, height=425, xaxis_title = None, template=template)

    return fig


@app.callback(
    [Output("direct_comparison_graph", "figure"),
    Output("desc_comparison", "children")],
    [Input("dataset", "data"),
    Input("select_estado1", "value"),
    Input("select_estado2", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)

def func(data, est1, est2, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)
    df1 = dff[dff["ESTADO"].isin([est1])]
    df2 = dff[dff["ESTADO"].isin([est2])]

    df_final = pd.DataFrame()

    df_estado1 = df1.groupby(pd.PeriodIndex(df1["DATA"], freq = "M"))["VALOR REVENDA"].mean().reset_index()
    df_estado2 = df2.groupby(pd.PeriodIndex(df2["DATA"], freq = "M"))["VALOR REVENDA"].mean().reset_index()


    df_estado1["DATA"] = pd.PeriodIndex(df_estado1["DATA"], freq = "M")
    df_estado2["DATA"] = pd.PeriodIndex(df_estado2["DATA"], freq = "M")


    df_final["DATA"] = df_estado1["DATA"].astype("datetime64[ns]")
    df_final["VALOR REVENDA"] = df_estado1["VALOR REVENDA"] - df_estado2["VALOR REVENDA"]

    fig = go.Figure()

    fig.add_scatter(name = est1, x = df_final["DATA"], y = df_final["VALOR REVENDA"])
    
    fig.add_scatter(name = est2, x = df_final["DATA"], y = df_final["VALOR REVENDA"].where(df_final["VALOR REVENDA"] > 0.0))

    fig.update_layout(main_config, height=350, template=template)

    fig.update_yaxes(range = [-0.7, 0.7])

    fig.add_annotation(text = f'{est2} MAIS BARATO', 
                        xref = "paper", yref = "paper",
                        font = dict(
                            family = "Courier New, monospace",
                            size = 12,
                            color = "#ffffff"),                            
                        align = "center", bgcolor = "rgba(0,0,0,0.5)",
                        opacity = 0.8, x = 0.1, y = 0.75, showarrow = False)

    fig.add_annotation(text = f'{est1} MAIS BARATO', 
                    xref = "paper", yref = "paper",
                    font = dict(
                        family = "Courier New, monospace",
                        size = 12,
                        color = "#ffffff"),                            
                    align = "center", bgcolor = "rgba(0,0,0,0.5)",
                    opacity = 0.8, x = 0.1, y = 0.25, showarrow = False)

    text = f"Comparando {est1} e {est2}. Se a linha estiver acima do eixo X, {est2} tinha menor preço, do contrário, {est1} tinha um valor inferior"

    return [fig, text]


@app.callback(
    Output("card1_indicators", "figure"),
    [Input("dataset", "data"),
    Input("select_estado1", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)

def card1(data, estado, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)

    df_final = dff[dff.ESTADO.isin([estado])]

    data1 = str(int(dff.ANO.min()))
    data2 = dff.ANO.max()

    fig = go.Figure()

    fig.add_trace(go.Indicator(
                mode = "number+delta",
                title = {"text": f"<span style ='size:60%'>{estado}</span><br><span style = 'font-size:0.7em'>{data1} - {data2}</span>"},
                value = df_final.at[df_final.index[-1], "VALOR REVENDA"],
                number = {"prefix":"R$", "valueformat":".2f"},
                delta = {"relative":True, "valueformat": ".1%", "reference": df_final.at[df_final.index[0], "VALOR REVENDA"]}

    ))

    fig.update_layout(main_config, height=250, template=template)

    return fig


@app.callback(
Output("card2_indicators", "figure"),
[Input("dataset", "data"),
Input("select_estado2", "value"),
Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)

def card2(data, estado, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)

    df_final = dff[dff.ESTADO.isin([estado])]

    data1 = str(int(dff.ANO.min()))
    data2 = dff.ANO.max()

    fig = go.Figure()

    fig.add_trace(go.Indicator(
                mode = "number+delta",
                title = {"text": f"<span style ='size:60%'>{estado}</span><br><span style = 'font-size:0.7em'>{data1} - {data2}</span>"},
                value = df_final.at[df_final.index[-1], "VALOR REVENDA"],
                number = {"prefix":"R$", "valueformat":".2f"},
                delta = {"relative":True, "valueformat": ".1%", "reference": df_final.at[df_final.index[0], "VALOR REVENDA"]}

    ))
    fig.update_layout(main_config, height=250, template=template)

    return fig

@app.callback(
Output("dataset", "data"),
[Input("rangeslider", "value"),
Input("dataset_fixed", "data")], prevent_initial_call = True
)

def range_slider(range, data):
    dff = pd.DataFrame(data)
    dff = dff[(dff["ANO"] >= f'{str(int(range[0]) - 1)}-01-01') & (dff["ANO"] <= f'{range[1]}-31-12')] 
    data = dff.to_dict()

    return data
# Run server
if __name__ == '__main__':
    app.run_server(debug=True, 
                    port=8080, 
                    use_reloader = False)

