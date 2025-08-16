#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback
import dash_daq as daq
import datetime
from flask import request
import re
import pandas as pd
import json
import plotly.graph_objs as go


#Zipcode section
df_zipcodes = pd.read_csv('Zipcodes_dereplicate.csv')
risk_dict = dict(zip(df_zipcodes['POSTALCODE'], df_zipcodes['RISK']))

#Keys tab
mykeys = [
  "consent",
  "zipcode",
  "which_residence",
  "previous_completion",
  "live_alone",
  "live_with_child_0_4",
  "live_with_child_5_14",
  "live_with_child_15_18",
  "live_with_someone_over_18",
  "dog",
  "cat",
  "horse",
  "anti_tick_treatment_dog",
  "vaccination_treatment_dog",
  "anti_tick_treatment_cat",
  "house_proximity_wooded_area",
  "access_courtyard",
  "house_deer",
  "courtyard_herbaceous_or_forest",
  "courtyard_children_play_area",
  "courtyard_fences_deer",
  "courtyard_corridor",
  "courtyard_mowing",
  "courtyard_fallen_leaves",
  "courtyard_clearing_herbaceous",
  "time_daily_wooded_area",
  "frequency_outdoor_activities",
  "visite_area_disease_ticks",
  "search_for_informations_ticks",
  "Wearing_long_layers_of_clothing",
  "Wearing_light-coloured_clothing",
  "Tucking_in_clothes",
  "DEET",
  "Walking_on_cleared_paths",
  "Examining_your_clothes",
  "clothes_in_the_dryer",
  "Examining_yourself",
  "Bathing_or_showering",
  "attached_to_your_skin",
  "Freely_moving",
  "On_a_pet",
  "Freely_moving_outside",
  "How_many_embedded_in_your_skin",
  "How_many_freely_moving_on_your_skin",
  "How_many_on_a_pet",
  "confidence_prevent_tick_bite",
  "confidence_young_tick",
  "confidence_adult_tick",
  "safely_remove_a_tick",
  "Age",
  "Education",
  "Employment_status",
  "Income",
  "primary_language",
  "primary_language_text",
  "population_group",
  "population_group_text",
  "commentaries"
]






def build_gauge_figure(value, color_ranges):
    import plotly.graph_objects as go
    active_key = None
    for clr, rng in color_ranges.items():
        if rng[0] <= value < rng[1]:
            active_key = clr
            break
    if value >= 3:
        active_key = list(color_ranges.keys())[-1]
    # Color maps
    steps = []
    color_map = {
        'grey': 'rgba(128,128,128,0.8)',
        'limegreen': 'rgba(50,205,50,0.8)',
        'orange': 'rgba(255,165,0,0.8)',
        'red': 'rgba(255,0,0,0.8)',
    }
    full_opacity_map = {
        'grey': 'rgba(128,128,128,1)',
        'limegreen': 'rgba(50,205,50,1)',
        'orange': 'rgba(255,165,0,1)',
        'red': 'rgba(255,0,0,1)',
    }
    for clr, rng in color_ranges.items():
        steps.append({
            'range': rng,
            'color': full_opacity_map[clr] if clr == active_key else color_map[clr]
        })
    # Label formatting
    labels = ['Faible', 'Modéré', 'Élevé']
    bold = lambda text: f'<b>{text}</b>'
    faded = lambda text: f'<span style="color:lightgray">{text}</span>'
    if 0.1 <= value < 1:
        ticktext = [bold('Faible'), faded('Modéré'), faded('Élevé')]
    elif 1 <= value < 2:
        ticktext = [faded('Faible'), bold('Modéré'), faded('Élevé')]
    elif 2 <= value <= 3:
        ticktext = [faded('Faible'), faded('Modéré'), bold('Élevé')]
    else:
        ticktext = labels
    # Gauge creation
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=value,
        gauge={
            'axis': {
                'range': [0, 3],
                'tickvals': [0.6, 1.5, 2.4],
                'ticktext': ticktext,
                'tickangle': 0,
                'tickfont': {'size': 18},
            },
            'bar': {'color': 'black', 'thickness': 0.2},
            'steps': steps,
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'valueformat': '.2f', 'font': {'color': 'rgba(0,0,0,0)'}}
    ))
    layout_config = {
        #"margin": dict(t=10, b=130, l=40, r=40),  # extra space for bottom text
        "margin": dict(t=0, b=0, l=0, r=0),
        "paper_bgcolor": "white",
    }
    # If invalid data, add visible warning
    if value == 0.05:
        layout_config["margin"] = dict(t=40, b=140, l=40, r=40)
        layout_config["annotations"] = [
            dict(
                text=(
                    "<b>⚠️ Score non calculé</b><br>"
                    "Certaines réponses étaient manquantes ou incomplètes.<br>"
                    "Veuillez compléter le questionnaire et réessayer."
                ),
                x=0.5,
                y=-0.15,  # was -0.35
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(size=14, color="black"),
                align='center',
                xanchor='center',
                yanchor='top',
                borderpad=10,
                bgcolor='rgba(255,255,255,0.9)',
            )
        ]
    fig.update_layout(**layout_config)
    return fig



# Function to build the full Dash component
def build_gauge(gauge_id, value, color_ranges):
    fig = build_gauge_figure(value, color_ranges)
    return dcc.Graph(id=gauge_id, figure=fig, style={'height': '400px', 'width': '400x'})
#######

dash.register_page(__name__, path='/page-8')

layout = html.Div([
    html.Div(id='score_summary', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '30px'}),
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    ######
    ######
    html.Div([
        html.B('Votre rapport personnalisé', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    html.P("Voici une légende qui vous aidera à comprendre la signification des couleurs :", style={'fontSize': '20px','textAlign': 'center','marginTop': '20px','marginBottom': '20px'  }),
    html.Br(),
    html.Div([
        # GREEN
        html.Div(
            [
                html.Div(
                    style={
                        "width": "150px",
                        "height": "75px",
                        "backgroundColor": "limegreen",
                        "border": "4px solid black",
                        "borderRadius": "20px",
                        "flexShrink": 0,  # prevent resizing
                    }
                ),
                html.Span("Niveau de risque faible", style={"fontSize": '28px'}),
            ],
            style={"display": "flex", "alignItems": "center", "gap": "12px"},
        ),
    
        html.Br(),
    
        # ORANGE
        html.Div(
            [
                html.Div(
                    style={
                        "width": "150px",
                        "height": "75px",
                        "backgroundColor": "orange",
                        "border": "4px solid black",
                        "borderRadius": "20px",
                        "flexShrink": 0,
                    }
                ),
                html.Span("Niveau de risque moyen", style={"fontSize": '28px'}),
            ],
            style={"display": "flex", "alignItems": "center", "gap": "12px"},
        ),
    
        html.Br(),
    
        # RED
        html.Div(
            [
                html.Div(
                    style={
                        "width": "150px",
                        "height": "75px",
                        "backgroundColor": "red",
                        "border": "4px solid black",
                        "borderRadius": "20px",
                        "flexShrink": 0,
                    }
                ),
                html.Span("Niveau de risque élevé", style={"fontSize": '28px'}),
            ],
            style={"display": "flex", "alignItems": "center", "gap": "12px"},
        ),
    
        html.Br(),
    
        # GREY 
        html.Div(
            [
                html.Div(
                    style={
                        "width": "150px",
                        "height": "75px",
                        "backgroundColor": "grey",
                        "border": "4px solid black",
                        "borderRadius": "20px",
                        "flexShrink": 0,
                    }
                ),
                html.Span(
                    [
                        "Nous n'avons pas pu évaluer votre niveau de risque, soit en raison de réponses incomplètes, soit parce que les données pour votre code postal ne sont pas disponibles. Cela ne signifie pas que le risque est faible — juste que nous n'avons pas suffisamment d'informations. Vous pouvez consulter ",
                        html.A(
                            "etick.ca",
                            href="https://www.etick.ca",
                            target="_blank",
                            style={"color": "blue", "textDecoration": "underline"}
                        ),
                        " pour savoir si des tiques Ixodes scapularis (ou autres) sont présentes dans votre région."
                    ],
                    style={
                        "fontSize": "18px",
                        "textAlign": "justify",  
                        "maxWidth": "1100px",    
                    }
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "flex-start",
                "gap": "12px",
            },
        )
        ],style={"marginLeft": "200px", "marginRight": "200px"}
    ),
    ######
    ######
    html.Br(),
    html.Br(),
    html.P('« Plus le score est vert, plus votre risque d\'être mordu par une tique est faible et meilleures sont vos stratégies de prévention. »', style={'fontSize': '32px', 'textDecoration': 'underline','textAlign': 'center','marginTop': '20px','marginBottom': '20px', 'font-weight': 'bold' }),
    html.Br(),
    #html.Hr(className='orange_line'),
    #############
    # SECTION 1 #
    #############
    
    html.Br(),
    html.Div([
        html.Div([
            html.P(
                'Présence potentielle de tiques à pattes noires dans votre environnement',
                style={
                    'fontSize': '40px',
                    'textAlign': 'center',
                    'marginTop': '20px',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }
            )
        ], style={
            'border': '1px solid #FF9636',       
            'borderRadius': '15px',              
            'padding': '10px',                   
            'backgroundColor': '#FFF3E0',        
            'marginLeft': '40px',
            'marginRight': '40px',
            'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'  # Optional: subtle shadow
        }),
        html.Br(),
        html.Div([
            build_gauge('gauge1', 0.05, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
            ], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report1', style={'marginTop': '10px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        ###
        # Void message (blank if not)
        ###
        html.Div(id='score_summary', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '30px'}),
        html.Br(),
        #html.Hr(className='orange_line')
    ]),
    #############
    # SECTION 2 #
    #############
    html.Div([
        html.Div([
            html.P(
                'Risque d\'exposition',
                style={
                    'fontSize': '40px',
                    'textAlign': 'center',
                    'marginTop': '20px',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }
            )
        ], style={
            'border': '1px solid #FF9636',       # Border color and thickness
            'borderRadius': '15px',              # Rounded corners
            'padding': '10px',                   # Space inside the box
            'backgroundColor': '#FFF3E0',        # Optional: light background
            'marginLeft': '40px',
            'marginRight': '40px',
            'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'  # Optional: subtle shadow
        }),
            html.Br(),
        html.Div([
            build_gauge('gauge2', 0.05, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
            ], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report2', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Br(),
        #html.Hr(className='orange_line'),
    ]),
    #############
    # SECTION 3 #
    #############
    html.Div([
        html.Div([
            html.P(
                'Comportements préventifs individuels',
                style={
                    'fontSize': '40px',
                    'textAlign': 'center',
                    'marginTop': '20px',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }
            )
        ], style={
            'border': '1px solid #FF9636',       # Border color and thickness
            'borderRadius': '15px',              # Rounded corners
            'padding': '10px',                   # Space inside the box
            'backgroundColor': '#FFF3E0',        # Optional: light background
            'marginLeft': '40px',
            'marginRight': '40px',
            'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'  # Optional: subtle shadow
        }),
        html.Div([
            build_gauge('gauge3', 0.05, {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]})
            ], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report3', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Br()
        #html.Hr(className='orange_line'),
    ]),
    ###############
    # PET SECTION #
    ###############
    html.Div(
        id='pet_advices',
        children=[
            html.Div(
                id='text_pet_advices',
                style={
                    'marginTop': '50px',
                    'whiteSpace': 'pre-wrap',
                    'text-align': 'justify',
                    'marginLeft': '50px',
                    'marginRight': '50px'
                }
            )       
        ]
    ),        
    ##################################
    # Gain confidence and conclusion #
    ##################################
    html.Div([
        html.Hr(className='orange_line'),
        html.P(
             'Gagner en confiance avec les tiques',
             style={
                 'fontSize': '40px',
                 'textAlign': 'center',
                 'marginTop': '20px',
                 'marginBottom': '20px',
                 'fontWeight': 'bold'
             }
        ),
        dcc.Markdown("* La confiance dans la prévention des morsures de tiques augmentera avec la mise en œuvre cohérente de comportements préventifs contre les tiques et l'expérience. Aucune méthode de prévention des morsures de tiques n'est efficace à 100%, et malgré vos meilleurs efforts, vous pourriez encore trouver des tiques sur vous, les membres de votre famille et vos animaux de compagnie. Cela ne signifie pas que vous faites quelque chose de mal !\n\n* Trouver des tiques n'est pas toujours facile. Les nymphes peuvent être particulièrement difficiles à détecter car elles peuvent être de la taille d'une graine de pavot. Encore une fois, la pratique et l'expérience aideront. Si vous n'êtes pas physiquement capable de détecter une tique (par exemple, en raison d'une mauvaise vue ou de mouvements restreints), des miroirs et une loupe peuvent faciliter les choses, ou si possible, demander à quelqu'un de vous aider.\n\n* Il est compréhensible que certaines personnes ne se sentent pas confiantes pour retirer une tique attachée. Les préoccupations courantes incluent le fait que les pièces buccales de la tique restent dans la peau ou une mauvaise manipulation de la tique. Pour des informations sur comment retirer une tique et ce qu'il ne faut pas faire, consultez [TickTool] (https://ticktool.etick.ca/what-should-i-do-if-i-find-a-tick/).\n\n", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),      
        html.Hr(className='orange_line'),
        html.P(
             'Conclusion',
             style={
                 'fontSize': '40px',
                 'textAlign': 'center',
                 'marginTop': '20px',
                 'marginBottom': '20px',
                 'fontWeight': 'bold'
             }
        ),
        dcc.Markdown("Nous espérons que ce rapport vous sera utile et vous permettra de vous sentir plus préparé et confiant lorsque vous passez du temps à l'extérieur. Avez-vous des suggestions sur la façon d'améliorer l'utilité globale et l'expérience utilisateur de ce questionnaire ? Si c'est le cas, veuillez envoyer vos idées à [pratique-ticktool@medvet.umontreal.ca](mailto:pratique-ticktool@medvet.umontreal.ca), nous aimerions les entendre. Pour plus d'informations sur les tiques et les maladies transmises par les tiques au Canada, vous pouvez consulter les ressources suivantes : \n\n [Gouvernement du Canada] (https://www.canada.ca/en/public-health/services/diseases/ticks-tick-borne-diseases.html)\n\n [TickTool] (https://ticktool.etick.ca/)\n\n", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'})
    ]),
    html.Div([
        dcc.Link(
            'Réviser mon questionnaire',
            href='/page-2',
            className='modern-link',
            style={
                'display': 'inline-block',
                'textAlign': 'center',
                'backgroundColor': '#FF9636',
                'color': 'white',
                'padding': '10px',
                'fontSize': '15px',
                'borderRadius': '5px',
                'textDecoration': 'none',
                'whiteSpace': 'nowrap',
                'height': '42px',
                'lineHeight': '22px',
                'width': '300px'  # Match button width
            }
        ),
        html.Button(
            'Exporter mon rapport en document PDF',
            id='print-button',
            n_clicks=0,
            style={
                'width': '300px',
                'textAlign': 'center',
                'backgroundColor': '#FF9636',
                'border': 'none',
                'borderRadius': '5px',
                'padding': '10px',
                'fontSize': '15px',
                'cursor': 'pointer',
                'color': 'white',
                'height': '42px',
                'lineHeight': '22px'
            }
        )
    ],
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'gap': '20px',
            'marginTop': '40px'
        }
    ),
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ####################
    # Risk Calculation #
    ####################
    html.Div(
    [
        html.P("Pour apprendre comment vos niveaux de risque ont été calculés, veuillez cliquer ici :", style={
            'margin': '0',
            'paddingRight': '8px',
            'fontSize': '16px',
            'display': 'inline'
        }),
        dcc.Link('Méthodologie', href='/methodology', style={
            'fontSize': '20px',
            'display': 'inline',
            'color': 'blue',
            'textDecoration': 'underline'
        })
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'marginTop': '30px'
    }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='display-answers_p8', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
    
])

######
######
            
@callback(
    Output('gauge1', 'figure'),
    Output('gauge2', 'figure'),
    Output('gauge3', 'figure'),
    Input('record_answers', 'data')
)



def calculat_score_and_record_answers(data):
    ######
    #Enregistrement des données en cas de consentement
    ######
    try : 
        if data and data.get('consent') == 'yes':
            now = datetime.datetime.now()
            ip_address = request.remote_addr
            myline = str(ip_address) + '\t' + now.strftime('%Y-%m-%d %H:%M:%S') 
            for k in mykeys:
                if k in data.keys():
                    myline += '\t' + str(data[k])
                else:
                    myline += '\t\t'
               
            myline += '\n'
            unique_output = re.sub(r'[^a-zA-Z0-9]', '_', now.strftime('%Y-%m-%d %H:%M:%S'))
            filename = 'survey_results_' +  unique_output + '.tsv'
            with open(filename, 'a') as tsvfile:
                tsvfile.write(myline)
    except:
        pass
    ######
    ######
    # Evaluation score1 BLT in environment
    ######
    score1 = 0.05
    try :
        if data and 'zipcode' in data:
            risk = risk_dict.get(data['zipcode'], 'Unknown')
            if risk == 'High':
                score1 = 2.4
            elif risk == 'Medium':
                if data['How_many_embedded_in_your_skin'] != "Not applicable" \
                    and data['How_many_embedded_in_your_skin'] != "I don't remember" \
                        and data['How_many_embedded_in_your_skin'] != "0" \
                            and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
                                and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
                                    and data['How_many_freely_moving_on_your_skin'] != "0":
                                score1 = 2.4
                else:
                    if data['access_courtyard'] == "yes" :
                        if(data['courtyard_herbaceous_or_forest'] == 'yes'):
                            score1 = 2.4
                        else:
                            if data['house_deer'] == "yes":
                                score1 = 2.4
                            else:
                                if data['house_proximity_wooded_area'] == "yes":
                                    score1 = 2.4
                                else :
                                    score1 = 1.5
                    else:
                        if data['house_proximity_wooded_area'] == "yes":
                            score1 = 2.4
                        else:
                            score1 = 1.5
            elif risk == 'Low':
                if ( (data['How_many_embedded_in_your_skin'] != "Not applicable") \
                    and (data['How_many_embedded_in_your_skin'] != "I don't remember") \
                        and (data['How_many_embedded_in_your_skin'] != "0")):
                    score1 = 1.5
                else:
                    if data['access_courtyard'] == "yes" :
                        if data['house_deer'] == "yes":
                            score1 = 1.5
                        else:
                            if data['house_proximity_wooded_area'] == "yes":
                                score1 = 1.5
    except :
        pass
    ######
    # Risk of exposure
    #######       
    score2 = 0.05
    # optimiser avec x not in list
    try :
        if data['How_many_embedded_in_your_skin'] != "Not applicable" \
            and data['How_many_embedded_in_your_skin'] != "I don't remember" \
                and data['How_many_embedded_in_your_skin'] != "0"\
                    and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
                        and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
                            and data['How_many_freely_moving_on_your_skin'] != "0":
                        score2 = 2.4
        else:
            if data['frequency_outdoor_activities'] == 'Very often (More than 10 times a year)':
                score2 = 2.4
            else:
                if ( data['time_daily_wooded_area'] == 'Between one and five hours per day' ) or (  data['time_daily_wooded_area'] == 'More than five hours per day' ):
                    score2 = 2.4
                else:
                    if data['frequency_outdoor_activities'] == 'Rarely':
                        score2 = 1.5
                    else:
                        if data['time_daily_wooded_area'] in {'Never', 'Less than one hour per day'}:
                            score2 =1.5
    except :
        pass
    ######
    # Preventive behavior
    #######
    score3 = 0.05
    ###
    try :
        # Constructuion d'une table de reponses considérées comme oui
        considered_as_yes = ['Most of the time', 'Always', 'Not applicable to my situation']
        # Calcul du score de mesures de protection
        score_at_least_4_protective_behaviours = 0
        if data['search_for_informations_ticks'] == 'yes' :
            score_at_least_4_protective_behaviours += 1
        if data['Wearing_long_layers_of_clothing'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Wearing_light-coloured_clothing'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Tucking_in_clothes'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['DEET'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Walking_on_cleared_paths'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Examining_your_clothes'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['clothes_in_the_dryer'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Bathing_or_showering'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        ######
        ######
        risk = risk_dict.get(data['zipcode'], 'Unknown')
        if (risk == 'High') or (risk == 'Medium') or (data['visite_area_disease_ticks'] == 'yes') : 
            if data['Examining_yourself'] == 'Most of the time' or data['Examining_yourself'] == 'Always':
                if (risk == 'Medium') or (risk == 'High'):
                    if data['access_courtyard'] == 'yes':
                        if data['courtyard_mowing'] in considered_as_yes:
                            if data['courtyard_fallen_leaves'] in considered_as_yes:
                                if data['courtyard_clearing_herbaceous'] in considered_as_yes:
                                    if data['courtyard_clearing_herbaceous'] in considered_as_yes:
                                        if data['courtyard_fences_deer'] in considered_as_yes:
                                            if score_at_least_4_protective_behaviours >= 4 :
                                                score3 = 2.4
                                            else :
                                                score3  = 1.5
                                        else :
                                            if score_at_least_4_protective_behaviours >= 4 :
                                                score3 = 1.5
                                            else:
                                                score3 = 0.6
                                else :
                                    if score_at_least_4_protective_behaviours >= 4 :
                                        score3 = 1.5
                                    else :
                                        score3 = 0.6
                            else :
                                score3 = 0.6
                        else :
                            score3 = 0.6
                    else:
                        if score_at_least_4_protective_behaviours >= 4:
                            score3 = 2.4
                        else :
                            score3 = 1.5
                else :
                    if score_at_least_4_protective_behaviours >= 4:
                        score3 = 2.4  
                    else :
                        score3 = 1.5
            else :
                score3 = 0.6
    except :
        pass
    ######
    ######
    ######
    ######
    fig1 = build_gauge_figure(score1, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
    fig2 = build_gauge_figure(score2, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
    fig3 = build_gauge_figure(score3, {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]})
    

    return fig1, fig2, fig3

            


@callback(
    Output('text_report1', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text1(data):
    sentence = ''
    
    
    try :
        risk = risk_dict.get(data['zipcode'], 'Unknown')
        no_anti_ticks = ['no', 'yes', "I don't remember"]
        
        if risk == 'Unknown':
            sentence += '* À l\'heure actuelle, nous n\'avons pas de données pour indiquer l\'adéquation de l\'habitat pour Ixodes scapularis dans votre région de code postal. Pour mieux comprendre où les tiques Ixodes scapularis (et autres tiques) sont présentes au Canada, vous pouvez consulter [eTick] (https://www.etick.ca/) . Pour savoir si vous êtes dans une zone à risque de maladie de Lyme, vous pouvez utiliser [cet outil] (https://www.canada.ca/fr/sante-publique/services/maladies/maladie-lyme/surveillance-maladie-lyme.html#a4) fourni par l\'Agence de la santé publique du Canada. De plus, vous pouvez consulter les pages web de votre gouvernement provincial pour des ressources sur les tiques et la maladie de Lyme afin d\'en apprendre davantage sur le risque dans votre région.\n\n'
        ###############################################################################
        # 1 The potential presence of blacklegged ticks in your environment
        ###############################################################################
        
        #Postal Code & residency feedback
        if data['which_residence'] == 'Primary' or data['which_residence'] == 'Secondary':
            sentence += f"""* La région de votre résidence {data['which_residence']} présente un niveau de risque **{risk}**"""
        else :
            sentence += f"""* La région de votre résidence présente un niveau de risque **{risk}**"""
        
        sentence += '\n\n'
    except :
        pass
    
    #Blacklegged ticks on your property and property management
    sentence += "* Les preuves suggèrent que la plupart des expositions aux tiques se produisent dans l'environnement péri-domestique, plutôt qu'ailleurs. Bien qu'il ne soit pas possible de déterminer votre niveau exact de risque pour les tiques à pattes noires basé sur un questionnaire, la présence de certaines caractéristiques sur ou près de votre propriété peut fournir une indication du risque, basée sur les preuves rapportées dans la littérature scientifique.\n\n"
    
    try:
    #Herbaceous or wooded area in proximity
        if data['house_proximity_wooded_area'] not in no_anti_ticks:
            sentence += "* Vous avez signalé avoir **des zones herbacées ou boisées ou des bordures sur votre propriété, et/ou vivre près d'une zone boisée**. La présence de zones herbacées, boisées, et l'intersection de ces deux habitats ont été démontrées comme étant associées à une augmentation des maladies transmises par les tiques. Cela ne signifie pas que vous ne pouvez pas passer du temps à l'extérieur, mais plutôt que **vous devriez être vigilant et prendre des mesures pour vous protéger**. Il existe plusieurs façons de réduire le risque d'exposition aux tiques sur votre propriété - pour plus d'informations, consultez [Que puis-je faire pour réduire les tiques dans ma cour ?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). N'oubliez pas de vous protéger lors de modifications à votre propriété en **portant des vêtements longs et en appliquant un répulsif à insectes, et d'effectuer une vérification des tiques et de prendre un bain ou une douche par la suite**.\n"
    except:
         pass
    try:
        # Courtyard feedback
        if data['access_courtyard']== 'yes':
            sentence += "* Vous avez signalé **avoir une cour, un jardin ou une zone boisée**. Bien qu'avoir un espace extérieur ne signifie pas automatiquement que vous êtes à risque d'exposition aux tiques, il y a certains éléments qui sont connus pour augmenter votre risque de morsure de tique et/ou de maladies transmises par les tiques. Ceux-ci incluent : La **taille de votre cour, Certains types de couverture, comme les jardins de fleurs ou de légumes et les zones herbacées et boisées**. La **présence d'un tas de bois, la présence d'un mur de pierre, la présence de litière de feuilles, les zones d'activité comme les aires de jeux pour enfants, les zones de restauration et les zones d'assise**.\n"
    except:
          pass
    try:
        #children's play equipment
        if data['courtyard_children_play_area'] == 'yes':
            sentence += "* Vous avez signalé **avoir des équipements de jeu pour enfants ou une structure d'activité sur votre propriété**. C'est une bonne idée de **rapprocher ce type d'équipement de la maison, et de l'éloigner des herbes hautes ou des zones herbacées/boisées**. Il est **préférable d'avoir des copeaux de bois plutôt que de l'herbe dans cette zone, ou de garder l'herbe très courte**.\n\n"
    except:
         pass
    
    try:
    #deer on your property
        if data['house_deer'] == 'yes':
            sentence += "* Vous avez signalé **voir ou soupçonner des cerfs sur votre propriété**. Les cerfs sont une espèce hôte pour la tique à pattes noires, ce qui signifie qu'ils jouent un rôle important dans le cycle de vie de la tique. La recherche suggère que ne pas avoir de clôture pour exclure les cerfs est associé à un risque accru de morsures de tiques, et que la présence de cerfs est associée à un risque accru pour les gens de contracter une maladie transmise par les tiques. Bien qu'il ne soit peut-être pas faisable d'installer une clôture autour de l'entièreté de votre propriété, vous pourriez considérer clôturer une zone de la propriété que vous utilisez régulièrement. Faire cela empêchera également les cerfs de manger vos plantes et fournit un espace sûr pour que les animaux de compagnie puissent courir. Il existe plusieurs façons de réduire le risque d'exposition aux tiques sur votre propriété, comme installer des clôtures et créer une bordure de paillis ou de gravier autour de votre cour. Pour plus d'informations, consultez [Que puis-je faire pour réduire les tiques dans ma cour ?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). N'oubliez pas de vous protéger lors du travail sur votre propriété en portant des vêtements longs et en appliquant un répulsif à insectes, et d'effectuer une vérification des tiques et de prendre un bain ou une douche par la suite.\n\n"
    except:
          pass
      
    sentence += '\n\n\n\n'
    
    return dcc.Markdown(sentence)

######
######

@callback(
    Output('text_report2', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text2(data):
    
    
    sentence = ""
    #Your tick exposure in the last 12 months
    #sentence += "### Your tick exposure in the last 12 months\n\n"
    
    try :
    
        if (data['attached_to_your_skin'] != 'Never' and  data['attached_to_your_skin'] != 'Not applicable') or (data['Freely_moving'] != 'Never' and  data['Freely_moving'] != 'Not applicable'):
            sentence += "* Vous avez signalé avoir trouvé une tique sur vous au cours des 12 derniers mois. Pour cette raison, vous avez reçu un niveau de risque « élevé » pour l'exposition aux tiques.\n\n"
    except :
        pass
    
    try :
        if data['On_a_pet'] != 'Never' and  data['On_a_pet'] != 'Not applicable':
            sentence += "* Vous avez signalé avoir trouvé une tique sur votre animal de compagnie au cours des 12 derniers mois. Pour cette raison, vous avez reçu un niveau de risque « élevé » pour l'exposition aux tiques, car l'exposition des animaux de compagnie aux tiques suggère généralement que leurs propriétaires ont également été dans un habitat à risque.\n\n"
    except :
        pass
    
    try :
        if data['Freely_moving_outside'] != 'Never' and  data['Freely_moving_outside'] != 'Not applicable':
            sentence += "* Vous avez signalé avoir trouvé une tique dans votre environnement au cours des 12 derniers mois. Pour cette raison, vous avez reçu un niveau de risque « élevé » pour l'exposition aux tiques car cela suggère que vous passez du temps dans ou près d'habitats de tiques.\n\n"
    except :
        pass
    
    
    #outdoor activity
    try :
        
        if data['frequency_outdoor_activities'] != 'Never':
            sentence += "* Vous avez signalé participer à au moins une activité de plein air qui se déroule dans des habitats potentiels de tiques, au moins une ou deux fois par saison. Les loisirs de plein air en général peuvent être associés à une augmentation des morsures de tiques et du risque de maladie transmise par les tiques, et un temps accru passé dans la végétation peut également augmenter le risque de maladies transmises par les tiques. Des études de recherche antérieures ont trouvé des associations entre des activités spécifiques comme la randonnée, la chasse et le travail de jardinage et un risque accru de contracter une maladie transmise par les tiques. Cependant, il est prudent de supposer qu'il peut y avoir un risque d'exposition aux tiques lors de la participation à toute activité de plein air se déroulant dans des zones herbeuses, boisées ou herbacées. Bien qu'il ne soit pas nécessaire d'arrêter de faire ces activités – il est important de vous protéger, votre famille et vos animaux de compagnie des morsures de tiques, et de toujours effectuer des vérifications de tiques !\n\n"
        elif data['time_daily_wooded_area'] == 'Between one and five hours per day':
            sentence += "* Comme pour la participation à des activités de plein air, l'exposition professionnelle aux tiques a été associée à un risque accru de maladies transmises par les tiques, il est donc important pour vous d'adopter des mesures de prévention cohérentes et régulières. Selon le répulsif à insectes que vous choisissez d'utiliser et combien de temps vous êtes à l'extérieur en une journée, vous pourriez avoir besoin de réappliquer le répulsif pendant que vous êtes dehors, alors emportez-le avec vous et/ou laissez-en un dans la voiture. C'est aussi une bonne idée de s'arrêter et d'effectuer des vérifications de tiques tout au long de la journée, plutôt que d'attendre jusqu'à la fin de la journée.\n\n"
    except :
        pass
    
    sentence += "* Si vous travaillez fréquemment ou passez du temps dans des habitats potentiels de tiques, vous pourriez souhaiter investir dans des vêtements qui ont été traités avec de la perméthrine comme couche de protection supplémentaire. Pour plus d'informations sur comment vous protéger des tiques à l'extérieur, consultez .\n\n"

    
        
    # try :
    #     if data['time_daily_wooded_area'] == 'More than five hours per day' or data['time_daily_wooded_area'] == 'Between one and five hours per day':
    #         sentence += "* If you frequently work or spend time in potential tick habitats, you may wish to invest in clothing which has been treated with permethrin as an additional layer of protection. For more information on how to protect yourself from ticks when outdoors, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n\n"
    # except :
    #     pass    
    
    
    no_in_prior_tick_exposure = ['Never','Not applicable']
    
    try :
        if (data['frequency_outdoor_activities'] == 'Never' or data['time_daily_wooded_area'] == 'Less than one hour per day') \
            and (data['attached_to_your_skin'] in no_in_prior_tick_exposure ) \
                and (data['Freely_moving'] in no_in_prior_tick_exposure ) \
                    and (data['On_a_pet'] in no_in_prior_tick_exposure) \
                        and (data['Freely_moving_outside'] in no_in_prior_tick_exposure) :
                            sentence += "* Vous avez signalé passer peu de temps soit à vous divertir soit à travailler à l'extérieur, ce qui signifie que vous êtes moins susceptible d'entrer dans des habitats de tiques. Cependant, notez qu'il y a un faible risque de rencontrer une tique n'importe où au Canada au sud du cercle arctique en raison de la possibilité que les tiques soient dispersées par les oiseaux en dehors de leurs habitats habituels.\n\n"
        
        if (data['frequency_outdoor_activities'] == 'Never' or data['time_daily_wooded_area'] == 'Less than one hour per day') \
            and ( (data['attached_to_your_skin'] not in no_in_prior_tick_exposure ) \
                or (data['Freely_moving'] not in no_in_prior_tick_exposure ) \
                    or (data['On_a_pet'] not in no_in_prior_tick_exposure) \
                        or (data['Freely_moving_outside'] not in no_in_prior_tick_exposure) ):
                            sentence += "* Vous avez signalé avoir trouvé une tique auparavant, malgré le fait de passer peu de temps à vous divertir ou à travailler à l'extérieur. Cela peut être parce que vos activités vous amènent à proximité d'habitats de tiques ou que vous avez rencontré une tique en dehors de son habitat habituel. Peu importe pourquoi, il sera important de rester vigilant et d'effectuer des vérifications de tiques.\n\n"
    except :
        pass   
    return dcc.Markdown(sentence)


######
######

@callback(
    Output('text_report3', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text3(data):
    
    sentence = ""
    
    # try :
    #     risk = risk_dict.get(data['zipcode'], 'Unknown')
    #     if risk == 'Low':
    #         sentence += "*This is the risk level you would be given if you lived in or visited a Lyme disease risk area, or if Lyme disease emerges in your current region.*\n\n"
    # except:
    #     sentence += "*This is the risk level you would be given if you lived in or visited a Lyme disease risk area, or if Lyme disease emerges in your current region.*\n\n"
        
    sentence += "La recherche a démontré l'association entre un risque accru de maladies transmises par les tiques et le manque d'adoption de mesures de protection, incluant ne pas effectuer de vérification de tiques, ne pas utiliser de répulsif à insectes, ne pas porter de vêtements appropriés, et ne pas se baigner après avoir passé du temps à l'extérieur. Chaque comportement fournit une couche de protection supplémentaire, et il n'y a aucun comportement unique qui garantit de prévenir les morsures de tiques ou les maladies. Par conséquent, il est recommandé que vous adoptiez autant de comportements préventifs que possible et faisable pour vous et votre famille : [Comment puis-je me protéger ?](https://ticktool.etick.ca/incorporate-prevention) \n\n"
    try:
        if data['visite_area_disease_ticks'] != 'yes':
            sentence += "* Vous avez signalé ne pas vivre dans ou visiter une région où vous saviez ou soupçonniez pouvoir contracter la maladie de Lyme ou une autre maladie transmise par les tiques. Basé sur votre adoption actuelle de comportements préventifs, votre niveau de risque et commentaires reflètent deux situations potentielles : 1) si les tiques et pathogènes associés émergeaient dans votre région et/ou 2) si vous déménagiez vers ou visitiez (consciemment ou inconsciemment) une zone avec un habitat approprié pour les tiques Ixodes scapularis. \n\n"
    except:
        pass
    
    no_body_check = ['Never','Rarely', 'Sometimes']
    try :
        if data['Examining_yourself'] in no_body_check:
            sentence += "* Vous avez signalé que vous n'effectuez jamais, rarement, ou parfois une vérification corporelle pour les tiques après avoir été dans une zone boisée dans une région endémique de maladie de Lyme, c'est pourquoi vous avez reçu un score « Faible » pour vos comportements préventifs.\n\n"
    
        if data['Examining_yourself'] in no_body_check or data['Examining_yourself'] == 'Not applicable':
            sentence += "* Bien qu'aucun comportement unique n'ait été démontré de manière cohérente comme étant le plus efficace, effectuer une vérification approfondie des tiques est la méthode de protection la plus largement recommandée. Elle ne nécessite pas d'équipement spécial – bien qu'un miroir pleine longueur et à main puisse aider – elle prend juste du temps. En planifiant à l'avance et en programmant 10 minutes pour une vérification de tiques après avoir passé du temps à l'extérieur, vous pouvez rendre plus probable que vous le fassiez, et ainsi réduire votre chance d'une morsure de tique ou de contracter une maladie transmise par les tiques. Et n'oubliez pas de vérifier aussi les autres membres du foyer et les animaux de compagnie ! Si vous trouvez une tique, félicitez-vous de l'avoir fait, retirez-la et continuez votre vérification de tiques au cas où il y en aurait d'autres\n\n"
        else :
            sentence += "* Vous avez signalé effectuer une vérification corporelle pour les tiques la plupart du temps après avoir été dans une zone boisée dans une région endémique de maladie de Lyme – bien fait ! Bien qu'aucun comportement unique n'ait été démontré de manière cohérente comme étant le plus efficace, effectuer une vérification de tiques est la méthode de protection la plus largement recommandée que vous puissiez adopter. Elle ne nécessite pas d'équipement spécial – bien qu'un miroir pleine longueur et à main puisse aider – elle prend juste du temps. En planifiant à l'avance et en programmant du temps pour une vérification de tiques après avoir passé du temps à l'extérieur, vous pouvez rendre plus probable que vous le fassiez, et ainsi réduire votre chance d'une morsure de tique ou de contracter une maladie transmise par les tiques. Et n'oubliez pas de vérifier aussi les autres membres du foyer et les animaux de compagnie ! Si vous trouvez une tique, félicitez-vous de l'avoir fait, retirez-la et continuez votre vérification de tiques au cas où il y en aurait d'autres.\n\n"
    except :
        pass   
    
    #Q13 ????????
    
    # Living alone or live with someone feedback
    try:
        if data['live_alone'] == 'yes' :
            sentence += """* Effectuer des vérifications de tiques peut être difficile pour tout le monde, car les tiques aiment se cacher dans des endroits où elles ne peuvent pas être trouvées. Comme vous **vivez seul(e)**, il peut être très utile d'avoir à la fois un **miroir pleine longueur** ainsi qu'un **miroir à main** pour rendre ce processus plus facile. Certaines personnes trouvent qu'avoir un **rouleau adhésif** disponible peut aider à atteindre les tiques qui ne se sont pas attachées, et de même, un **gant de crin dans la douche** peut aider à déloger les tiques des endroits que vous ne pouvez pas atteindre. N'oubliez pas de porter une attention particulière à votre **cuir chevelu, ligne de cheveux, oreilles, bras, poitrine, dos, taille, nombril, aine, jambes et derrière les genoux, et entre les orteils**.\n\n  En 2021, 45% des cas de maladie de Lyme au Canada ont été diagnostiqués chez des adultes âgés de 55-79 ans. Cela ne signifie pas que les personnes de ce groupe d'âge ne peuvent pas passer du temps à l'extérieur, mais suggère plutôt que ce groupe d'âge devrait **adopter des comportements cohérents** pour se protéger des tiques.\n\n  Pour plus d'informations sur comment vous protéger, consultez [Tout ce que vous devez savoir sur la prévention] (https://ticktool.etick.ca/incorporate-prevention)\n"""
        elif data['live_with_someone_over_18'] == 'yes' :
            sentence += """* Comme vous **vivez avec un autre adulte**, vous pouvez **vous rappeler mutuellement d'adopter des comportements préventifs** contre les morsures de tiques et **vous entraider pour effectuer une vérification de tiques** – particulièrement les endroits difficiles à atteindre comme le **cuir chevelu et le dos**. En vous aidant et vous rappelant mutuellement de penser aux tiques, il sera **plus facile d'incorporer ces pratiques dans votre routine**. **Si vous effectuez une vérification de tiques seul(e)**, il peut être très utile d'avoir à la fois un **miroir pleine longueur** ainsi qu'un **miroir à main** pour rendre ce processus plus facile. Certaines personnes trouvent qu'avoir un **rouleau adhésif** disponible peut aussi être utile pour atteindre les tiques qui ne se sont pas attachées, et de même, un **gant de crin dans la douche** peut aider à déloger les tiques des endroits que vous ne pouvez pas atteindre.\n\nEn 2021, 45% des cas de maladie de Lyme au Canada ont été diagnostiqués chez des adultes âgés de 55-79 ans. Cela ne signifie pas que les personnes de ce groupe d'âge ne peuvent pas passer du temps à l'extérieur, mais suggère plutôt que ce groupe d'âge devrait essayer d'adopter des comportements cohérents pour se protéger des tiques.\n\n  Pour plus d'informations sur comment vous protéger, consultez [Tout ce que vous devez savoir sur la prévention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n"""
        elif data['live_with_child_0_4'] == 'yes' or data['live_with_child_5_14'] == 'yes' or data['live_with_child_15_18'] == 'yes':
            sentence += """* Approximativement **11% des cas de maladie de Lyme rapportés au Canada en 2021 étaient chez des enfants âgés de 5-14 ans**, cependant d'autres preuves suggèrent que le risque de morsures de tiques est **plus élevé chez les enfants âgés de 5 ans ou moins**. Cela peut être attribué au fait que les enfants de cet âge **jouent souvent près du sol et quittent les sentiers désignés**. Ils sont aussi **moins susceptibles de se vérifier eux-mêmes** pour les tiques. Cela ne signifie **pas** que les enfants plus âgés ne peuvent pas développer une maladie transmise par les tiques, et il est important que tous les membres de la famille apprennent comment se protéger des tiques. Comme avec les adultes, le risque peut être réduit en effectuant une **vérification de tiques, en portant des vêtements longs, en rentrant les vêtements, en portant un répulsif à insectes si âgé de plus de 6 mois, et en se baignant ou prenant une douche après avoir passé du temps à l'extérieur**.\n  Pour plus d'informations sur comment protéger les enfants des morsures de tiques, consultez [Comment puis-je protéger mes enfants ?] (https://ticktool.etick.ca/how-can-i-protect-my-children/)'.\n"""
    except :
        pass
    
    try :
    #Lawn management practice
        #sentence += "\n\nThere are several ways to reduce the risk of tick exposure of your property. Here, we will describe three key methods:\n\n"
        
        yes_property_management = ['Most of the time', 'Always']
        
        #Mowing
        if data['courtyard_mowing'] in yes_property_management:
            sentence += "* Bien fait pour l'entretien régulier de la pelouse ! Garder l'herbe courte est très important pour réduire le risque d'exposition aux tiques. Les tiques grimpent sur l'herbe longue pour pouvoir s'attacher aux personnes et animaux qui passent. En gardant régulièrement et de manière cohérente l'herbe courte – spécialement dans les zones que vous ou vos animaux de compagnie fréquentez – vous rendez votre propriété moins hospitalière pour les tiques.\n\n"
        else:
            sentence += "* L'entretien de la pelouse est très important pour réduire le risque d'exposition aux tiques. Les tiques grimpent sur l'herbe longue pour pouvoir s'attacher aux personnes et animaux qui passent. En gardant régulièrement et de manière cohérente l'herbe courte – spécialement dans les zones que vous ou vos animaux de compagnie fréquentez – vous pouvez rendre votre propriété moins hospitalière pour les tiques.\n\n"
        
        #Removing leaves
        if data['courtyard_fallen_leaves'] in yes_property_management:
            sentence += "* Bien fait pour l'enlèvement régulier des feuilles sur votre propriété ! La litière de feuilles fournit un environnement sûr pour les tiques, les gardant au chaud en hiver et les empêchant de se dessécher en été. En enlevant la litière de feuilles, vous réduisez l'un des habitats les plus importants pour les tiques sur votre propriété. Selon la taille de votre propriété, vous pourriez souhaiter vous concentrer sur les zones où vous ou vos animaux de compagnie aimez passer du temps.\n\n"
        else:
            sentence += "* La litière de feuilles fournit un environnement sûr pour les tiques, les gardant au chaud en hiver et les empêchant de se dessécher en été. En enlevant la litière de feuilles, vous pouvez réduire l'un des habitats les plus importants pour les tiques sur votre propriété. Selon la taille de votre propriété, vous pourriez souhaiter vous concentrer sur les zones où vous ou vos animaux de compagnie aimez passer du temps.\n\n"
        
        #Brush and branches
        if data['courtyard_clearing_herbaceous'] in yes_property_management:
            sentence += "* Bien fait pour le dégagement régulier des broussailles herbacées et la taille des branches ! Ces habitats fournissent un environnement approprié pour les petits rongeurs, qui non seulement portent des tiques mais sont vitaux dans le cycle de vie des bactéries qui causent la maladie de Lyme et autres maladies transmises par les tiques. En enlevant les zones herbacées dans les zones où vous ou vos animaux de compagnie passez beaucoup de temps, vous rendez ces zones moins hospitalières pour les souris et les tiques, réduisant la chance qu'elles s'aventurent près de votre maison.\n\n"
        else :
            sentence += "* Les broussailles herbacées et les longues branches fournissent un environnement approprié pour les petits rongeurs, qui non seulement portent des tiques mais sont vitaux dans le cycle de vie des bactéries qui causent la maladie de Lyme et autres maladies transmises par les tiques. En enlevant les zones herbacées dans les zones où vous ou vos animaux de compagnie passez beaucoup de temps, vous pouvez rendre ces zones moins hospitalières pour les souris et les tiques, réduisant la chance qu'elles s'aventurent près de votre maison.\n\n"
        
        sentence += "Gardez à l'esprit que le travail de jardinage, le temps passé dans la végétation et l'activité générale de plein air peuvent augmenter votre risque de contracter une maladie transmise par les tiques, alors n'oubliez pas de vous protéger pendant que vous travaillez sur votre propriété en portant des vêtements longs et en appliquant un répulsif à insectes, et d'effectuer une vérification de tiques et de prendre un bain ou une douche par la suite. Beaucoup de gens s'inquiètent que les mesures extérieures pour réduire le risque d'exposition aux tiques puissent avoir des conséquences environnementales négatives. Pour en apprendre davantage à ce sujet et d'autres FAQ, consultez '[Que puis-je faire pour réduire les tiques dans ma cour ?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/)."
     
    except :
        pass
     
    return dcc.Markdown(sentence)

######
######

@callback(
    Output(component_id='pet_advices', component_property='hidden'),
    Input('record_answers', 'data')
    )

def display_pet_advices(data):
    try :
        if data['dog'] == 'yes' or data['cat'] == 'yes' or data['horse'] == 'yes':
            return False
        else:
            return True
    except:
        return True


@callback(
    Output('text_pet_advices', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_pet_advices_text(data):
    
    sentence = ''
    
    no_anti_ticks = ['no', "I don't remember"]
    
    try :
    
        #Dog anti-tick treatnment
        if data['dog'] == 'yes' or data['cat'] == 'yes' or data['horse'] == 'yes':
            sentence += "* Les animaux de compagnie ne sont **pas capables de transmettre la maladie de Lyme ou d'autres maladies transmises par les tiques aux humains. Avoir un animal de compagnie a été associé à un risque accru de morsures de tiques ou de maladie transmise par les tiques. C'est généralement parce qu'avoir un animal de compagnie signifie que vous passez plus de temps à l'extérieur et donc plus près des tiques**. Cela ne signifie pas que vous devriez éviter d'avoir des animaux de compagnie ! Si vous voyez des tiques sur votre animal de compagnie, cela suggère que vous avez peut-être aussi été dans un habitat de tiques et que vous devriez prendre des mesures pour protéger à la fois vous, vos animaux de compagnie et votre famille.\n\n"
        
        if data['anti_tick_treatment_dog'] in no_anti_ticks :
            sentence += "* Vous avez signalé **prendre soin d'au moins un chien**. Les chiens sont à risque de morsures de tiques, et **tout comme les gens, peuvent souffrir de la maladie de Lyme** et d'autres maladies transmises par les tiques. Heureusement, il existe plusieurs produits spécifiques aux espèces disponibles pour les animaux de compagnie pour les protéger des tiques et de la maladie de Lyme, incluant **des comprimés, des traitements spot-on et des vaccins**. Certains de ces produits peuvent aussi protéger votre animal de compagnie d'autres parasites comme **les puces et les vers**. Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient d'utiliser, et quand, basé sur vos activités et risque, le climat local, l'efficacité des médicaments préventifs disponibles, et vos propres préférences. Il n'y a aucune preuve suggérant qu'avoir un chien augmente votre risque de contracter une maladie transmise par les tiques. Cependant, **les gens qui ont des chiens peuvent passer plus de temps à l'extérieur** dans des habitats de tiques, il est donc important pour vous de vous protéger des tiques.\n\n"
        elif data['anti_tick_treatment_dog'] == 'yes':
            sentence += "* Vous avez signalé **prendre soin d'au moins un chien et lui fournir des produits anti-tiques** – bien fait ! Les chiens sont à risque de morsures de tiques, et **tout comme les gens, peuvent souffrir de la maladie de Lyme** et d'autres maladies transmises par les tiques. En administrant un produit préventif contre les tiques, vous aidez à les garder en sécurité. Il existe plusieurs produits spécifiques aux espèces disponibles pour les animaux de compagnie pour les protéger des tiques et de la maladie de Lyme, incluant **des comprimés, des traitements spot-on et des vaccins**. Certains de ces produits peuvent aussi protéger votre animal de compagnie d'autres parasites comme **les puces et les vers**. Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient d'utiliser, et quand, basé sur vos activités et risque, le climat local, l'efficacité des médicaments préventifs disponibles, et vos propres préférences. Il n'y a aucune preuve suggérant qu'avoir un chien augmente votre risque de contracter une maladie transmise par les tiques. Cependant, **les gens qui ont des chiens peuvent passer plus de temps à l'extérieur** dans des habitats de tiques, il est donc important pour vous de vous protéger des tiques.\n\n"
        
        #Cats anti-tick treatments 
        if data['anti_tick_treatment_cat'] in no_anti_ticks :
            sentence += "* Vous avez signalé prendre soin d'au moins un chat. Les chats sont à risque de morsures de tiques, il est donc important de les protéger avec des produits préventifs contre les tiques spécifiques aux espèces. En administrant un produit préventif contre les tiques, vous aidez à les garder en sécurité. Il existe plusieurs **produits spécifiques aux espèces** disponibles pour les animaux de compagnie pour les protéger des tiques, incluant des comprimés et des traitements spot-on. Certains de ces produits peuvent aussi protéger votre animal de compagnie d'autres parasites comme les puces et les vers. Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient d'utiliser, et quand, basé sur vos activités et risque, le climat local, l'efficacité des médicaments préventifs disponibles, et vos propres préférences. Il est intéressant de noter que la possession de chats a été associée à un risque accru de maladies transmises par les tiques, alors que cela n'a pas été trouvé avec la possession de chiens. Cela peut être dû à des différences dans les comportements préventifs entre les propriétaires de chats et de chiens, des différences dans l'administration de produits préventifs contre les tiques, des vérifications de tiques réduites chez les chats, un comportement de toilettage accru chez les chats ou parce que les chats sont plus susceptibles de rôder dans les herbes hautes. Peu importe pourquoi cette association a été trouvée, il est toujours conseillé d'effectuer des vérifications de tiques sur votre chat, si possible, et de parler à votre vétérinaire des mesures de prévention contre les tiques.\n\n"
        elif  data['anti_tick_treatment_cat'] == 'yes':
            sentence += "* Vous avez signalé prendre soin d'au moins un chat et lui fournir des produits anti-tiques – bien fait ! Les chats sont à risque de morsures de tiques, il est donc important de les protéger avec des produits préventifs contre les tiques spécifiques aux espèces. Il existe plusieurs **produits spécifiques aux espèces** disponibles pour les animaux de compagnie pour les protéger des tiques, incluant des comprimés et des traitements spot-on. Certains de ces produits peuvent aussi protéger votre animal de compagnie d'autres parasites comme les puces et les vers. Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient d'utiliser, et quand, basé sur vos activités et risque, le climat local, l'efficacité des médicaments préventifs disponibles, et vos propres préférences. Il est intéressant de noter que la possession de chats a été associée à un risque accru de maladies transmises par les tiques, alors que cela n'a pas été trouvé avec la possession de chiens. Cela peut être dû à des différences dans les comportements préventifs entre les propriétaires de chats et de chiens, des différences dans l'administration de produits préventifs contre les tiques, des vérifications de tiques réduites chez les chats, un comportement de toilettage accru chez les chats ou parce que les chats sont plus susceptibles de rôder dans les herbes hautes. Peu importe pourquoi cette association a été trouvée, il est toujours conseillé d'effectuer des vérifications de tiques sur votre chat, si possible, et de parler à votre vétérinaire des mesures de prévention contre les tiques.\n\n"   
        #Horse
        if data['horse'] == 'yes':
            sentence += "* Les chevaux peuvent aussi souffrir de la maladie de Lyme, et comme il n'y a pas de vaccin licencié pour les chevaux, la prévention contre les tiques est importante. Le toilettage et la vérification quotidienne des tiques, la gestion appropriée des pâturages, et l'utilisation de répulsifs à insectes spécifiques aux espèces peuvent tous aider à réduire le risque de morsures de tiques. Pour plus d'informations sur les maladies transmises par les tiques et la prévention des morsures de tiques, parlez à votre vétérinaire. Certaines études ont trouvé que posséder ou monter des chevaux a été associé à un risque accru de morsures de tiques et de maladie transmise par les tiques. Cela est très probablement dû au fait que les cavaliers et les chevaux sont dans le même environnement et ont un risque similaire d'exposition aux tiques.\n"
        
        sentence += "* Pour plus d'informations sur les animaux de compagnie et les tiques, visitez [Comment puis-je protéger mes animaux de compagnie ?](https://ticktool.etick.ca/how-can-i-protect-my-pets/) et [Tick Talk Canada]( https://ticktalkcanada.com/)"
    except:
        pass
    
    # return [html.Hr(className='orange_line'),
    #     html.P(
    #         'A note about pets',
    #         style={
    #             'fontSize': '40px',
    #             'textAlign': 'center',
    #             'marginTop': '20px',
    #             'marginBottom': '20px',
    #             'fontWeight': 'bold'
    #         }
    #     ),
    #     dcc.Mardown(sentence)]
    return html.Div([
        html.Hr(className='orange_line'),
        html.P(
            'Note sur les animaux de compagnie',
            style={
                'fontSize': '40px',
                'textAlign': 'center',
                'marginTop': '20px',
                'marginBottom': '20px',
                'fontWeight': 'bold'
            }
        ),
        dcc.Markdown(sentence)
    ])

@callback(
    Output('hidden-div', 'children'),
    Input('print-button', 'n_clicks')
)
def trigger_print(n_clicks):
    if n_clicks > 0:
        return dcc.Location(id='print-location', href='javascript:window.print();')
    return ''


