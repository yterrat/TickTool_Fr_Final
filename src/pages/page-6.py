#!/usr/bin/env python3

# Importation des packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-6')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Confiance', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    ######
    ######
    html.Br(),
    html.Br(),
    html.P("Veuillez indiquer votre niveau d’accord avec les quatre affirmations suivantes :", \
           style={'font-size': '25px'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.B("Je suis capable de pouvoir prévenir une morsure de tique."),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d’accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d’accord", 'value': "Somewhat agree"},
                {'label': "Ni d’accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt pas d’accord", 'value': "Somewhat disagree"},
                {'label': "Pas du tout d’accord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='confidence_prevent_tick_bite'
        )
    ], style={'font-size': '20px', 'marginLeft': '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ######
    ######
    html.Div([
        html.B("Je suis capable de pouvoir repérer une jeune tique (nymphe, illustrée) sur mes vêtements ou ma peau.", className='question_style2'),
        html.Br(),
        html.Br(),
        html.Img(src='/assets/Tick1.jpg', style={'width': '30vw', 'height': 'auto'}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d’accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d’accord", 'value': "Somewhat agree"},
                {'label': "Ni d’accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt pas d’accord", 'value': "Somewhat disagree"},
                {'label': "Pas du tout d’accord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='confidence_young_tick'
        )
    ], style={'font-size': '20px', 'marginLeft': '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ######
    ######
    html.Div([
        html.B("Je suis capable de pouvoir repérer une tique adulte (illustrée) sur mes vêtements ou ma peau."),
        html.Br(),
        html.Br(),
        html.Img(src='/assets/tick2.jpg', style={'width': '30vw', 'height': 'auto'}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d’accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d’accord", 'value': "Somewhat agree"},
                {'label': "Ni d’accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt pas d’accord", 'value': "Somewhat disagree"},
                {'label': "Pas du tout d’accord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='confidence_adult_tick'
        )
    ], style={'font-size': '20px', 'marginLeft': '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ######
    ######
    html.Div([
        html.B("Je suis capable d’enlever en toute sécurité et efficacement une tique incrustée dans la peau.", className='question_style2'),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d’accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d’accord", 'value': "Somewhat agree"},
                {'label': "Ni d’accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt pas d’accord", 'value': "Somewhat disagree"},
                {'label': "Pas du tout d’accord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='safely_remove_a_tick'
        )
    ], style={'font-size': '20px', 'marginLeft': '30px'}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Link('Précédent', href='/page-5', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Suivant', href='/page-7', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '40px'
        }
    ),
    html.Br(),
    html.Br(),
    dbc.Progress(value=90, style={"height": "15px"}, className="mb-3", label="90% complété"),
])


@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('confidence_prevent_tick_bite', 'value'),
    Input('confidence_young_tick', 'value'),
    Input('confidence_adult_tick', 'value'),
    Input('safely_remove_a_tick', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)
def update_dic_p6(Q1, Q2, Q3, Q4, data):
    data = data or {}
    if Q1 is not None:
        data['confidence_prevent_tick_bite'] = Q1
    if Q2 is not None:
        data['confidence_young_tick'] = Q2
    if Q3 is not None:
        data['confidence_adult_tick'] = Q3
    if Q4 is not None:
        data['safely_remove_a_tick'] = Q4
    return data


@callback(
    Output('confidence_prevent_tick_bite', 'value'),
    Output('confidence_young_tick', 'value'),
    Output('confidence_adult_tick', 'value'),
    Output('safely_remove_a_tick', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('confidence_prevent_tick_bite', None),
        data.get('confidence_young_tick', None),
        data.get('confidence_adult_tick', None),
        data.get('safely_remove_a_tick', None)
    )
