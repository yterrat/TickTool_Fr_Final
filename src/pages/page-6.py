#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-6')

layout = html.Div([
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Confiance', style={'font-size': '60px'})
    ]),
    html.Br(),
    html.Br(),
    html.P("Veuillez indiquer votre niveau d'accord avec les quatre énoncés suivants :", style={'font-size': '25px'}),
    html.Br(),
    html.Br(),

    html.Div([
        html.B('1. Je suis confiant(e) de pouvoir prévenir une piqûre de tique.'),
        html.Br(), html.Br(),
        html.Div(
            dcc.Dropdown(
                options=[
                    {'label': 'Tout à fait d\'accord', 'value': 'Strongly agree'},
                    {'label': "Plutôt d'accord", 'value': "Somewhat agree"},
                    {'label': "Ni d'accord ni en désaccord", 'value': "Neither agree nor disagree"},
                    {'label': "Plutôt en désaccord", 'value': "Somewhat disagree"},
                    {'label': "Tout à fait en désaccord", 'value': "Strongly disagree"}
                ],
                style={'width': '300px'},
                id='confidence_prevent_tick_bite'
            ),
            style={'display': 'flex', 'justifyContent': 'center'}
            )
        ], style={'font-size': '20px'}),
    
    html.Br(),
    html.Hr(className='grey_blue_line'),
    
    
    ######
    

    html.Div([
    html.B("2. Je suis confiant(e) de pouvoir trouver une jeune tique (nymphe, illustrée) sur mes vêtements ou ma peau.", className='question_style2'),
    html.Br(), html.Br(),

    html.Div(
        html.Img(src='/assets/Tick1.jpg', style={'width': '30vw', 'height': 'auto'}),
        style={'textAlign': 'center'}
    ),

    html.Br(), html.Br(),
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d\'accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d'accord", 'value': "Somewhat agree"},
                {'label': "Ni d'accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt en désaccord", 'value': "Somewhat disagree"},
                {'label': "Tout à fait en désaccord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='confidence_young_tick'
        ),
        style={'display': 'flex', 'justifyContent': 'center'}
        )
    ], style={'font-size': '20px'}),

    html.Br(),
    html.Hr(className='grey_blue_line'),
    

    #######
    #######
    
    html.Div([
    html.B("3. Je suis confiant(e) de pouvoir trouver une tique adulte (illustrée) sur mes vêtements ou ma peau.", className='question_style2'),
    html.Br(), html.Br(),

    html.Div(
        html.Img(src='/assets/tick2.jpg', style={'width': '30vw', 'height': 'auto'}),
        style={'textAlign': 'center'}
    ),

    html.Br(), html.Br(),
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d\'accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d'accord", 'value': "Somewhat agree"},
                {'label': "Ni d'accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt en désaccord", 'value': "Somewhat disagree"},
                {'label': "Tout à fait en désaccord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='confidence_adult_tick'
        ),
        style={'display': 'flex', 'justifyContent': 'center'}
        )
    ], style={'font-size': '20px'}),

    html.Br(),
    html.Hr(className='grey_blue_line'),
    
    #######
    #######
    
    html.Div([
    html.B("4. Je pourrais retirer de manière sécuritaire et efficace une tique qui s'est enfoncée dans la peau.", className='question_style2'),
    html.Br(), html.Br(),
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Tout à fait d\'accord', 'value': 'Strongly agree'},
                {'label': "Plutôt d'accord", 'value': "Somewhat agree"},
                {'label': "Ni d'accord ni en désaccord", 'value': "Neither agree nor disagree"},
                {'label': "Plutôt en désaccord", 'value': "Somewhat disagree"},
                {'label': "Tout à fait en désaccord", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            id='safely_remove_a_tick'
        ),
        style={'display': 'flex', 'justifyContent': 'center'}
        )
    ], style={'font-size': '20px'}),

    html.Br(), html.Br(),
    html.Br(), html.Br(),
    html.Div([
        dcc.Link('Précédent', href='/page-5', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Suivant', href='/page-7', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '40px'
    }),

    html.Br(), html.Br(),
    dbc.Progress(value=90, style={"height": "15px", "width": "60%"}, className="mb-3", label="90% terminé"),

], style={
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'center',
    'width': '100%',
    'textAlign': 'center'
})

    

@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('confidence_prevent_tick_bite', 'value'),
    Input('confidence_young_tick', 'value'),
    Input('confidence_adult_tick', 'value'),
    Input('safely_remove_a_tick', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p6(Q1,Q2,Q3,Q4,data):
    data = data or {}
    if Q1 is not None :
        data['confidence_prevent_tick_bite'] = Q1
    if Q2 is not None :
        data['confidence_young_tick'] = Q2
    if Q3 is not None :
        data['confidence_adult_tick'] = Q3
    if Q4 is not None :
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


# @callback(
#     [Output('confidence_prevent_tick_bite', 'value'),
#      Output('confidence_young_tick', 'value'),
#      Output('confidence_adult_tick', 'value'),
#      Output('safely_remove_a_tick', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page6(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('confidence_prevent_tick_bite', None),
#      data.get('confidence_young_tick', None),
#      data.get('confidence_adult_tick', None),
#      data.get('safely_remove_a_tick', None)
#      ]

# Dynamic link depending on the 'consent' answer (we skip the sociodemographic questions)