#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, path='/page-2')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
    html.B('Profil d\'exposition', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    #######
    #######
    html.B("Caractéristiques démographiques de votre ménage", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.P("Veuillez indiquer votre code postal.", style={'font-size': '20px','margin-bottom': '1px'}), 
            html.P("Si vous avez ou visitez plusieurs résidences, \
                   nous vous suggérons de commencer par saisir le code postal de votre résidence principale, \
                       puis de répéter ce questionnaire pour les autres résidences.", style={'font-size': '20px', 'margin-bottom': '1px'}),
            html.P("Si vous ne souhaitez pas répondre, vous pouvez laisser ce champ vide. Veuillez noter que sans code postal, nous ne pouvons pas fournir \
                   d'informations sur votre risque environnemental lié aux tiques à pattes noires. \
                       Si vous souhaitez continuer sans fournir votre code postal, vous pouvez toujours recevoir d'autres \
                           informations sur votre profil de risque.", style={'font-size': '20px'}),
            dcc.Input(
                type='text',
                placeholder='Saisissez le code postal à 6 caractères',
                maxLength=6,
                id='zipcode',
                style={'marginBottom': '10px', 'width': '200px'}
                )
            ]),
            html.Br(),
            html.P("Veuillez indiquer pour quelle résidence vous complétez ce questionnaire", style={'font-size': '20px'}),
            dcc.Dropdown(
                options=[
                    {'label': 'Principale' , 'value': 'Primary'},
                    {'label': 'Secondaire', 'value': 'Secondary'},
                    {'label': 'Autre', 'value': 'Other'},
                    {'label': 'Je préfère ne pas répondre', 'value': 'I prefer not to answer'},
                ],
                style={'width': '200px'},
                #value='',
                id = 'which_residence'
            ),
            html.Br(),
            html.P("Avez-vous déjà complété ce questionnaire auparavant, pour cette résidence ?", style={'font-size': '20px'}),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                ],
                style={'width': '200px'},
                #value='',
                id = 'previous_completion'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    #######
    #######
    html.Hr(className='grey_blue_line'),
    html.B('Veuillez indiquer si les énoncés suivants sont vrais pour votre ménage, la plupart du temps.', style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label('Je vis seul(e)', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                ],
                style={'width': '200px'},
                #value='',
                id = 'live_alone'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    ]),
    #######
    #######
    
    html.Div(
        id='live_not_alone_questions',
        children=[
            html.Br(),
            html.Div([
                html.Label('Je vis avec au moins un enfant âgé de 0 à 4 ans', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                    ],
                    #value='',
                    style={'width': '200px'},
                    id = 'live_with_child_0_4'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            html.Br(),
            html.Div([
                html.Label('Je vis avec au moins un enfant âgé de 5 à 14 ans', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                    ],
                    #value='',
                    style={'width': '200px'},
                    id = 'live_with_child_5_14'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            html.Br(),
            html.Div([
                html.Label('Je vis avec au moins un enfant âgé de 15 à 18 ans', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                    ],
                    #value='',
                    style={'width': '200px'},
                    id = 'live_with_child_15_18'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            html.Br(),
            html.Div([
                html.Label('Je vis avec au moins une personne de plus de 18 ans', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                    ],
                    style={'width': '200px'},
                    #value='',
                    id = 'live_with_someone_over_18'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
        ], style={'display' : 'block'}
    ),
    #######
    #######
    html.Hr(className='grey_blue_line'),
    html.B('Veuillez indiquer lesquels des énoncés suivants s\'appliquent à votre situation :', style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label('Il y a au moins un chien dans mon ménage', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                ],
                style={'width': '200px'},
                #value='',
                id = 'dog'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
        html.Br(),
        html.Div([
            html.Label('Il y a au moins un chat dans mon ménage qui sort à l\'extérieur', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                ],
                style={'width': '200px'},
                #value='',
                id = 'cat'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
        html.Br(),
        html.Div([
            html.Label('Je suis responsable de prendre soin d\'au moins un cheval', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': 'Je préfère ne pas répondre', 'value': 'prefer_not_to_say'}
                ],
                #value='',
                style={'width': '200px'},
                id = 'horse'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'})
    ]),
    #######
    #######
    html.Div(
        id='dog_questions',
        children=[
            html.Hr(className='grey_blue_line'),
            html.B("Si vous avez plus d'un chien, veuillez répondre 'Oui' aux questions suivantes \
                   si la question s'applique à au moins un de vos chiens." , style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Label('Au cours des 12 derniers mois, avez-vous utilisé des produits anti-tiques (ex : Bravecto®, K9 Advantix®II, NexGard®) pour votre chien ?', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Oui', 'value': 'yes'},
                            {'label': 'Non', 'value': 'no'},
                            {'label': "Je ne me souviens pas", 'value': "I don't remember"}
                        ],
                        style={'width': '200px'},
                        #value='',
                        id = 'anti_tick_treatment_dog'
                    ),
                ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                html.Br(),
                html.Div([
                    html.Label('Avez-vous fait vacciner votre chien contre la maladie de Lyme ?', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Oui', 'value': 'yes'},
                            {'label': 'Non', 'value': 'no'},
                            {'label': "Je ne me souviens pas", 'value': "I don't remember"}
                        ],
                        #value='',
                        style={'width': '200px'},
                        id = 'vaccination_treatment_dog'
                    ),
                ], 
                style={'font-size': '15px', 'marginLeft' : '30px'})
            ]),
        ], style={'display' : 'block'}
    ),
    ######
    ######
    html.Div(
        id='cat_questions',
        children=[
            html.Hr(className='grey_blue_line'),
            html.B("Si vous avez plus d'un chat, veuillez répondre 'Oui' à la question suivante \
                   si la question s'applique à au moins un de vos chats. " , style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Label('Au cours des 12 derniers mois, avez-vous protégé votre chat en utilisant des produits anti-tiques (ex : Bravecto®) ?', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Oui', 'value': 'yes'},
                            {'label': 'Non', 'value': 'no'},
                            {'label': "Je ne me souviens pas", 'value': "I don't remember"}
                        ],
                        style={'width': '200px'},
                        #value='',
                        id = 'anti_tick_treatment_cat'
                    ),
                ], style={'font-size': '15px', 'marginLeft' : '30px'})
            ]),
        ], style={'display' : 'block'}
    ),
    #######
    #######
    html.Hr(className='grey_blue_line'),
    html.B("Les questions suivantes concernent votre domicile :", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label('Vivez-vous à proximité (à moins de 500 pieds ou 150 mètres) d\'une zone boisée ?', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': "Je ne sais pas", 'value': "I don't know"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'house_proximity_wooded_area'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
        html.Br(),
        html.Div([
            html.Label('Avez-vous accès à une cour, un jardin ou une zone boisée ?', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': "Je ne sais pas", 'value': "I don't know"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'access_courtyard'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
        html.Br(),
        html.Div([
            html.Label('Êtes-vous au courant de la présence de cerfs sur votre propriété, ou la soupçonnez-vous ?', style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Oui', 'value': 'yes'},
                    {'label': 'Non', 'value': 'no'},
                    {'label': "Je ne sais pas", 'value': "I don't know"}
                ],
                #value='',
                style={'width': '200px'},
                id = 'house_deer'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    ]),
    html.Hr(className='grey_blue_line'),
    ######
    ######
    html.Div(
        id='courtyard_questions',
        children=[
            html.B("Puisque vous avez accès à une cour, un jardin ou une zone boisée, y a-t-il les éléments suivants sur votre propriété ?", style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            html.Div([
                html.Label('Zones herbacées ou forestières/lisières', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': "Je ne sais pas", 'value': "I don't know"}
                    ],
                    style={'width': '200px'},
                    #value='',
                    id = 'courtyard_herbaceous_or_forest'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            html.Br(),
            html.Div([
                html.Label('Aire de jeux pour enfants', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': "Je ne sais pas", 'value': "I don't know"}
                    ],
                    style={'width': '200px'},
                    #value='',
                    id = 'courtyard_children_play_area'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            html.Br(),
            html.Div([
                html.Label('Clôtures pour exclure les cerfs de votre propriété', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': "Je ne sais pas", 'value': "I don't know"}
                    ],
                    #value='',
                    style={'width': '200px'},
                    id = 'courtyard_fences_deer'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            html.Br(),
            html.Div([
                html.Label('Un corridor ou une bordure de copeaux de bois ou de gravier entre la cour et les bois et broussailles environnants', style={'font-size': '20px'}),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {'label': 'Oui', 'value': 'yes'},
                        {'label': 'Non', 'value': 'no'},
                        {'label': "Je ne sais pas", 'value': "I don't know"}
                    ],
                    #value='',
                    style={'width': '200px'},
                    id = 'courtyard_corridor'
                ),
            ], style={'font-size': '15px', 'marginLeft' : '30px'}),  
            ######
            ######
            html.Hr(className='grey_blue_line'),
            #######
            html.B("À quelle fréquence mettez-vous en pratique les activités suivantes sur votre propriété ?", style={'font-size': '20px'}),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Label('Tonte régulière durant le printemps, l\'été et l\'automne', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Jamais', 'value': 'Never'},
                            {'label': 'Rarement', 'value': 'Rarely'},
                            {'label': "Parfois", 'value': "Sometimes"},
                            {'label': 'La plupart du temps', 'value': 'Most of the time'},
                            {'label': "Toujours", 'value': "Always"}
                        ],
                        #value='',
                        style={'width': '200px'},
                        id = 'courtyard_mowing'
                    ),
                    html.Br()
                ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                html.Div([
                    html.Label('Enlèvement des feuilles mortes', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Jamais', 'value': 'Never'},
                            {'label': 'Rarement', 'value': 'Rarely'},
                            {'label': "Parfois", 'value': "Sometimes"},
                            {'label': 'La plupart du temps', 'value': 'Most of the time'},
                            {'label': "Toujours", 'value': "Always"}
                        ],
                        #value='',
                        style={'width': '200px'},
                        id = 'courtyard_fallen_leaves'
                    ),
                    html.Br()
                ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                html.Div([
                    html.Label('Défrichage des broussailles herbacées et élagage des branches durant le printemps, l\'été et l\'automne', style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Jamais', 'value': 'Never'},
                            {'label': 'Rarement', 'value': 'Rarely'},
                            {'label': "Parfois", 'value': "Sometimes"},
                            {'label': 'La plupart du temps', 'value': 'Most of the time'},
                            {'label': "Toujours", 'value': "Always"}
                        ],
                        #value='',
                        style={'width': '200px'},
                        id = 'courtyard_clearing_herbaceous'
                    ),
                    html.Br()
                ], style={'font-size': '15px', 'marginLeft' : '30px'}),
            ]),
        ], style={'display':'block'}
    ),
    #######
    #######
    html.Br(),
    html.Br(), 
    html.Div(
    [
        dcc.Link('Précédent', href='/', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Suivant', href='/page-3', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
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
    dbc.Progress(value=17, style={"height": "15px"}, className="mb-3", label = "17% terminé"),
    html.Br(),
    html.Br(),
    #html.Div(id='display-answers_p2', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])
                   

# Callbacks     
######
######

@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('zipcode', 'value'),
    Input('which_residence', 'value'),
    Input('previous_completion', 'value'),
    Input('live_alone', 'value'),
    Input('live_with_child_0_4', 'value'),
    Input('live_with_child_5_14', 'value'),
    Input('live_with_child_15_18', 'value'),
    Input('live_with_someone_over_18', 'value'),
    Input('dog', 'value'),
    Input('cat', 'value'),
    Input('horse', 'value'),
    Input('anti_tick_treatment_dog', 'value'),
    Input('vaccination_treatment_dog', 'value'),
    Input('anti_tick_treatment_cat', 'value'),
    Input('house_proximity_wooded_area', 'value'),
    Input('access_courtyard', 'value'),
    Input('house_deer', 'value'),
    Input('courtyard_herbaceous_or_forest', 'value'),
    Input('courtyard_children_play_area', 'value'),
    Input('courtyard_fences_deer', 'value'),
    Input('courtyard_corridor', 'value'),
    Input('courtyard_mowing', 'value'),
    Input('courtyard_fallen_leaves', 'value'),
    Input('courtyard_clearing_herbaceous', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_page2(Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16,Q17,Q18,Q19,Q20,Q21,Q22,Q23,Q24,data):
      data = data or {}
      if Q1 is not None :
          data['zipcode'] = Q1
      if Q2 is not None :
          data['which_residence'] = Q2
      if Q3 is not None :
          data['previous_completion'] = Q3
      if Q4 is not None :
          data['live_alone'] = Q4
      if Q5 is not None :
          data['live_with_child_0_4'] = Q5
      if Q6 is not None :
          data['live_with_child_5_14'] = Q6
      if Q7 is not None :
          data['live_with_child_15_18'] = Q7
      if Q8 is not None :
          data['live_with_someone_over_18'] = Q8
      if Q9 is not None :  
          data['dog'] = Q9
      if Q10 is not None :  
          data['cat'] = Q10
      if Q11 is not None :
          data['horse'] = Q11
      if Q12 is not None :
        data['anti_tick_treatment_dog'] = Q12
      if Q13 is not None :
        data['vaccination_treatment_dog'] = Q13
      if Q14 is not None :
        data['anti_tick_treatment_cat'] = Q14
      if Q15 is not None :
        data['house_proximity_wooded_area'] = Q15
      if Q16 is not None :
        data['access_courtyard'] = Q16
      if Q17 is not None :
        data['house_deer'] = Q17
      if Q18 is not None :
        data['courtyard_herbaceous_or_forest'] = Q18    
      if Q19 is not None :
        data['courtyard_children_play_area'] = Q19
      if Q20 is not None :
        data['courtyard_fences_deer'] = Q20
      if Q21 is not None :
        data['courtyard_corridor'] = Q21
      if Q22 is not None :
        data['courtyard_mowing'] = Q22
      if Q23 is not None :
        data['courtyard_fallen_leaves'] = Q23
      if Q24 is not None :
        data['courtyard_clearing_herbaceous'] = Q24
      return data


# Afficher les réponses quand le bouton precedent est activé
@callback(
    Output('zipcode', 'value'),
    Output('which_residence', 'value'),
    Output('previous_completion', 'value'),
    Output('live_alone', 'value'),
    Output('live_with_child_0_4', 'value'),
    Output('live_with_child_5_14', 'value'),
    Output('live_with_child_15_18', 'value'),
    Output('live_with_someone_over_18', 'value'),
    Output('dog', 'value'),
    Output('cat', 'value'),
    Output('horse', 'value'),
    Output('anti_tick_treatment_dog', 'value'),
    Output('vaccination_treatment_dog', 'value'),
    Output('anti_tick_treatment_cat', 'value'),
    Output('house_proximity_wooded_area', 'value'),
    Output('access_courtyard', 'value'),
    Output('house_deer', 'value'),
    Output('courtyard_herbaceous_or_forest', 'value'),
    Output('courtyard_children_play_area', 'value'),
    Output('courtyard_fences_deer', 'value'),
    Output('courtyard_corridor', 'value'),
    Output('courtyard_mowing', 'value'),
    Output('courtyard_fallen_leaves', 'value'),
    Output('courtyard_clearing_herbaceous', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('zipcode', None),
        data.get('which_residence', None),
        data.get('previous_completion', None),
        data.get('live_alone', None),
        data.get('live_with_child_0_4', None),
        data.get('live_with_child_5_14', None),
        data.get('live_with_child_15_18', None),
        data.get('live_with_someone_over_18', None),
        data.get('dog', None),
        data.get('cat', None),
        data.get('horse', None),
        data.get('anti_tick_treatment_dog', None),
        data.get('vaccination_treatment_dog', None),
        data.get('anti_tick_treatment_cat', None),
        data.get('house_proximity_wooded_area', None),
        data.get('access_courtyard', None),
        data.get('house_deer', None),
        data.get('courtyard_herbaceous_or_forest', None),
        data.get('courtyard_children_play_area', None),
        data.get('courtyard_fences_deer', None),
        data.get('courtyard_corridor', None),
        data.get('courtyard_mowing', None),
        data.get('courtyard_fallen_leaves', None),
        data.get('courtyard_clearing_herbaceous', None)
    )


# Dynamic display of questions (cats, dogs, courtyard)
# This section was working properly with a dcc.store set to 'session'

@callback(
    Output(component_id='live_not_alone_questions', component_property='hidden'),
    [Input(component_id='live_alone', component_property='value')])

def show_hide_element_live_not_alone(live_alone):
    if live_alone == 'no':
        return False
    else:
        return True

@callback(
    Output(component_id='dog_questions', component_property='hidden'),
    [Input(component_id='dog', component_property='value')])

def show_hide_element_dog(dog):
    if dog == 'yes':
        return False
    else:
        return True
    
@callback(
    Output(component_id='cat_questions', component_property='hidden'),
    [Input(component_id='cat', component_property='value')])

def show_hide_element_cat(cat):
    if cat == 'yes':
        return False
    else:
        return True

@callback(
    Output(component_id='courtyard_questions', component_property='hidden'),
    [Input(component_id='access_courtyard', component_property='value')])

def show_hide_element_courtyard(courtyard):
    if courtyard == 'yes':
        return False
    else:
        return True




######
######

## Affichage du data
# @callback(
#     Output('display-answers_p2', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p2(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."