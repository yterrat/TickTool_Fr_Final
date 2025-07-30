#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-3')

layout = html.Div([
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Activités extérieures', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.B("Dans le cadre de votre occupation principale (incluant le travail ou les études), \
           en moyenne combien de temps passez-vous quotidiennement dans des zones boisées ou herbeuses entre les mois d'avril et novembre ? ", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Jamais', 'value': 'Never'},
                    {'label': 'Moins d\'une heure par jour', 'value': 'Less than one hour per day'},
                    {'label': 'Entre une et cinq heures par jour', 'value': 'Between one and five hours per day'},
                    {'label': 'Plus de cinq heures par jour', 'value': 'More than five hours per day'},
                    {'label': 'Non applicable à ma situation', 'value': 'Not applicable to my situation'}
                ],
                style={'width': '400px'},
                #value='',
                id = 'time_daily_wooded_area'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    #######
    #######
    html.Hr(className='grey_blue_line'),
    html.Br(),
    html.B('À quelle fréquence pratiquez-vous les activités extérieures suivantes entre les mois d\'avril et novembre \
           (Les exemples incluent la marche ou la randonnée, le camping, la chasse, le jardinage/travaux de cour, \
            les sports récréatifs, la coupe de bois, la cueillette) ?',  style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Jamais', 'value': 'Never'},
                {'label': 'Rarement (Moins de 2 fois par année)', 'value': 'Rarely (Fewer than 2 times a year)'},
                {'label': 'Souvent (De 2 à 10 fois par année)', 'value': 'Often (From 2 to 10 times a year)'},
                {'label': 'Très souvent (Plus de 10 fois par année)', 'value': 'Very often (More than 10 times a year)'}
            ],
            style={'width': '400px'},
            #value='',
            id = 'frequency_outdoor_activities'
        )
    ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    html.Br(), 
    html.Div(
    [
        dcc.Link('Précédent', href='/page-2', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Suivant', href='/page-4', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
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
    dbc.Progress(value=33, style={"height": "15px"}, className="mb-3", label = "33% terminé"),
    html.Br(),
    #html.Div(id='display-answers3', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])
           

@callback(
      Output('record_answers', 'data',  allow_duplicate=True),
      Input('time_daily_wooded_area', 'value'),
      Input('frequency_outdoor_activities', 'value'),
      State('record_answers', 'data'),
      prevent_initial_call=True,
)

def update_dic_page3(Q1,Q2,data):
      data = data or {}
      if Q1 is not None :
          data['time_daily_wooded_area'] = Q1
      if Q2 is not None :
        data['frequency_outdoor_activities'] = Q2
      return data
  
@callback(
    Output('time_daily_wooded_area', 'value'),
    Output('frequency_outdoor_activities', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('time_daily_wooded_area', None),
        data.get('frequency_outdoor_activities', None)
    )

 
# @callback(
#     Output('display-answers3', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p3(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."