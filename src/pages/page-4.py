#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-4')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Autoprotection', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.B("Au cours de la dernière année, avez-vous visité une zone où vous saviez ou soupçonniez pouvoir \
           contracter la maladie de Lyme, ou une autre maladie transmise par les tiques ?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': "Je ne sais pas", 'value': "I don't know"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'visite_area_disease_ticks'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    html.B("Au cours de la dernière année, avez-vous recherché des informations sur les moyens de vous protéger des maladies transmises par les tiques ?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': "Je ne sais pas", 'value': "I don't know"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'search_for_informations_ticks'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    #######
    #######
    html.Div(
        id='visite_area_disease_ticks_questions',
        children=[
            html.Br(),
            html.Div(
                id='visiting_Lyme_area',
                children=[
                    html.Hr(className='grey_blue_line'),
                    html.Br(),
                    html.B("Lorsque vous étiez dans des zones de risque connues, à quelle fréquence avez-vous adopté les mesures suivantes \
                           pour vous protéger, pendant ou après avoir été dans une zone boisée ? ", style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.B("Lors de votre présence dans des zones à risque :", style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div([
                            html.Label('Porter des vêtements longs (ex : pantalons, manches longues).',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Wearing_long_layers_of_clothing'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Porter des vêtements de couleur claire.',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Wearing_light-coloured_clothing'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Rentrer ses vêtements (ex : pantalon dans les chaussettes)',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Tucking_in_clothes'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Appliquer un répulsif contenant du DEET ou de l\'icaridine (aussi connue sous le nom de picaridine) sur la peau ou les vêtements. ',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'DEET'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Marcher sur des sentiers et des chemins dégagés ',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Walking_on_cleared_paths'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                    ]),
                    html.Br(),
                    html.B("Après avoir été dans des zones à risque :", style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div([
                            html.Label('Examiner vos vêtements pour éviter d\'introduire des tiques dans votre domicile ',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Examining_your_clothes'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Mettre vos vêtements dans la sécheuse à haute température pour tuer les tiques',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'clothes_in_the_dryer'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Vous examiner pour trouver et retirer les tiques dans les 24h',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Examining_yourself'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Prendre un bain ou une douche après avoir été dans des zones à risque.',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Jamais', 'value': 'Never'},
                                    {'label': 'Rarement', 'value': 'Rarely'},
                                    {'label': 'Parfois', 'value': 'Sometimes'},
                                    {'label': "La plupart du temps", 'value': "Most of the time"},
                                    {'label': "Toujours", 'value': "Always"},
                                    {'label': "Non applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Bathing_or_showering'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                    ])
                ], style={'display':'block'}
            ),
        ]),
    ######
    ######
    html.Br(),
    html.Div(
    [
        dcc.Link('Précédent', href='/page-3', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Suivant', href='/page-5', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
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
    dbc.Progress(value=50, style={"height": "15px"}, className="mb-3", label = "50% terminé"),
    html.Br(),
    html.Br(),
    #html.Div(id='display-answers4', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])
                   
            

@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('visite_area_disease_ticks', 'value'),
    Input('search_for_informations_ticks', 'value'),
    Input('Wearing_long_layers_of_clothing', 'value'),
    Input('Wearing_light-coloured_clothing', 'value'),
    Input('Tucking_in_clothes', 'value'),
    Input('DEET', 'value'),
    Input('Walking_on_cleared_paths', 'value'),
    Input('Examining_your_clothes', 'value'),
    Input('clothes_in_the_dryer', 'value'),
    Input('Examining_yourself', 'value'),
    Input('Bathing_or_showering', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p4(Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,data):
    data = data or {}
    if Q1 is not None :
        data['visite_area_disease_ticks'] = Q1
    if Q2 is not None :
        data['search_for_informations_ticks'] = Q2 
    if Q3 is not None :   
        data['Wearing_long_layers_of_clothing'] = Q3
    if Q4 is not None :
        data['Wearing_light-coloured_clothing'] = Q4
    if Q5 is not None :
        data['Tucking_in_clothes'] = Q5
    if Q6 is not None :
        data['DEET'] = Q6
    if Q7 is not None :
        data['Walking_on_cleared_paths'] = Q7
    if Q8 is not None :
        data['Examining_your_clothes'] = Q8
    if Q9 is not None :
        data['clothes_in_the_dryer'] = Q9
    if Q10 is not None :
        data['Examining_yourself'] = Q10
    if Q11 is not None :
        data['Bathing_or_showering'] = Q11
    return data


@callback(
    Output('visite_area_disease_ticks', 'value'),
    Output('search_for_informations_ticks', 'value'),
    Output('Wearing_long_layers_of_clothing', 'value'),
    Output('Wearing_light-coloured_clothing', 'value'),
    Output('Tucking_in_clothes', 'value'),
    Output('DEET', 'value'),
    Output('Walking_on_cleared_paths', 'value'),
    Output('Examining_your_clothes', 'value'),
    Output('clothes_in_the_dryer', 'value'),
    Output('Examining_yourself', 'value'),
    Output('Bathing_or_showering', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('visite_area_disease_ticks', None),
        data.get('search_for_informations_ticks', None),
        data.get('Wearing_long_layers_of_clothing', None),
        data.get('Wearing_light-coloured_clothing', None),
        data.get('Tucking_in_clothes', None),
        data.get('DEET', None),
        data.get('Walking_on_cleared_paths', None),
        data.get('Examining_your_clothes', None),
        data.get('clothes_in_the_dryer', None),
        data.get('Examining_yourself', None),
        data.get('Bathing_or_showering', None)
    )

@callback(
    Output(component_id='visite_area_disease_ticks_questions', component_property='hidden'),
    [Input(component_id='visite_area_disease_ticks', component_property='value')])

def show_hide_element_visite_area_disease_ticks(visite_area_disease_ticks):
    if visite_area_disease_ticks == 'yes':
        return False
    else:
        return True



# @callback(
#     [Output('visite_area_disease_ticks', 'value'),
#      Output('Wearing_long_layers_of_clothing', 'value'),
#      Output('Wearing_light-coloured_clothing', 'value'),
#      Output('Tucking_in_clothes', 'value'),
#      Output('DEET', 'value'),
#      Output('Walking_on_cleared_paths', 'value'),
#      Output('Examining_your_clothes', 'value'),
#      Output('clothes_in_the_dryer', 'value'),
#      Output('Examining_yourself', 'value'),
#      Output('Bathing_or_showering', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page4(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('visite_area_disease_ticks', None),
#      data.get('Wearing_long_layers_of_clothing', None),
#      data.get('Wearing_light-coloured_clothing', None),
#      data.get('Tucking_in_clothes', None),
#      data.get('DEET', None),
#      data.get('Walking_on_cleared_paths', None),
#      data.get('Examining_your_clothes', None),
#      data.get('clothes_in_the_dryer', None),
#      data.get('Examining_yourself', None),
#      data.get('Bathing_or_showering', None),
#      ]
         
 
# @callback(
#     Output('display-answers4', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p4(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."