#!/usr/bin/env python3

# Import des packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-5')

layout = html.Div([
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    ######
    ######
    html.Div([
        html.B('Exposition antérieure aux tiques', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.B("Au cours de la dernière année, à quelle fréquence avez-vous trouvé des tiques dans les contextes suivants ?", className='question_style2'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label('Fixée à votre peau', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Quotidiennement', 'value': 'Daily'},
                    {'label': "Hebdomadairement", 'value': "Weekly"},
                    {'label': "Mensuellement", 'value': "Monthly"},
                    {'label': "Moins d'une fois par mois", 'value': "Less than once a month"},
                    {'label': "Une ou deux fois par saison", 'value': "Once or twice a season"},
                    {'label': "Jamais", 'value': "Never"},
                    {'label': "Non applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                id='attached_to_your_skin'
            ),
            html.Br(),
            html.Label('Libre sur votre peau ou vos vêtements', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Quotidiennement', 'value': 'Daily'},
                    {'label': "Hebdomadairement", 'value': "Weekly"},
                    {'label': "Mensuellement", 'value': "Monthly"},
                    {'label': "Moins d'une fois par mois", 'value': "Less than once a month"},
                    {'label': "Une ou deux fois par saison", 'value': "Once or twice a season"},
                    {'label': "Jamais", 'value': "Never"},
                    {'label': "Non applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                id='Freely_moving'
            ),
            html.Br(),
            html.Label('Libre dans l’environnement extérieur', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Quotidiennement', 'value': 'Daily'},
                    {'label': "Hebdomadairement", 'value': "Weekly"},
                    {'label': "Mensuellement", 'value': "Monthly"},
                    {'label': "Moins d'une fois par mois", 'value': "Less than once a month"},
                    {'label': "Une ou deux fois par saison", 'value': "Once or twice a season"},
                    {'label': "Jamais", 'value': "Never"},
                    {'label': "Non applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                id='Freely_moving_outside'
            ),
        ], style={'font-size': '15px', 'marginLeft': '30px'})
    ]),
    html.Br(),
    html.Div(
        id='On_a_pet_question1',
        children=[
            html.Label('Sur un animal de compagnie', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Quotidiennement', 'value': 'Daily'},
                    {'label': "Hebdomadairement", 'value': "Weekly"},
                    {'label': "Mensuellement", 'value': "Monthly"},
                    {'label': "Moins d'une fois par mois", 'value': "Less than once a month"},
                    {'label': "Une ou deux fois par saison", 'value': "Once or twice a season"},
                    {'label': "Jamais", 'value': "Never"},
                    {'label': "Non applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                id='On_a_pet'
            )
        ], style={'font-size': '15px', 'marginLeft': '30px', 'marginRight': '30px'}),
    html.Br(),

    html.Div(
        id='How_many_question',
        children=[
            html.Hr(className='grey_blue_line'),
            html.B('Environ combien de tiques avez-vous trouvé dans les contextes suivants l’année dernière, entre avril et novembre ?', className='question_style2'),
            html.Br(),
            html.Br(),
            html.Div([
                html.Label('Fixée à votre peau', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': "Je ne m'en souviens pas", 'value': "I don't remember"},
                        {'label': "0", 'value': "0"},
                        {'label': "1-5", 'value': "1-5"},
                        {'label': "6-25", 'value': "6-25"},
                        {'label': "> 25", 'value': "> 25"},
                        {'label': "Non applicable", 'value': "Not applicable"}
                    ],
                    style={'width': '200px'},
                    id='How_many_embedded_in_your_skin'
                ),
                html.Br(),
                html.Label('Libre sur votre peau ou vos vêtements', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': "Je ne m'en souviens pas", 'value': "I don't remmber"},
                        {'label': "0", 'value': "0"},
                        {'label': "1-5", 'value': "1-5"},
                        {'label': "6-25", 'value': "6-25"},
                        {'label': "> 25", 'value': "> 25"},
                        {'label': "Non applicable", 'value': "Not applicable"}
                    ],
                    style={'width': '200px'},
                    id='How_many_freely_moving_on_your_skin'
                ),
                html.Br(),
            ], style={'font-size': '15px', 'marginLeft': '30px', 'marginRight': '30px'}),
            html.Div(
                id='On_a_pet_question2',
                children=[
                    html.Label('Sur un animal de compagnie', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': "Je ne m'en souviens pas", 'value': "I don’t remember"},
                            {'label': "0", 'value': "0"},
                            {'label': "1-5", 'value': "1-5"},
                            {'label': "6-25", 'value': "6-25"},
                            {'label': "> 25", 'value': "> 25"},
                            {'label': "Non applicable", 'value': "Not applicable"}
                        ],
                        style={'width': '200px'},
                        id='How_many_on_a_pet'
                    )
                ], style={'font-size': '15px', 'marginLeft': '30px', 'marginRight': '30px'}),
            html.Br(),
            html.Br(),
        ]),
    html.Br(),
    html.Div([
        dcc.Link('Précédent', href='/page-4', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Suivant', href='/page-6', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
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
    dbc.Progress(value=63, style={"height": "15px"}, className="mb-3", label="63% complété"),
])
