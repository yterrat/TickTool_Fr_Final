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
        "margin": dict(t=10, b=130, l=40, r=40),  # extra space for bottom text
        "paper_bgcolor": "white",
    }

    # If invalid data, add visible warning
    if value == 0.05:
        layout_config["margin"] = dict(t=10, b=180, l=40, r=40)
        layout_config["annotations"] = [
            dict(
                text=(
                    "<b>⚠️ Score not computed</b><br>"
                    "Some answers were missing or incomplete.<br>"
                    "Please complete the questionnaire and try again."
                ),
                x=0.5,
                y=-0.15,  # was -0.35
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(size=20, color="black"),
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
    return dcc.Graph(id=gauge_id, figure=fig, style={'height': '500px', 'width': '500px'})


#######


dash.register_page(__name__, path='/page-8')

layout = html.Div([
    html.Div(id='score_summary', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '30px'}),
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Votre rapport personnalisé', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    html.P("Voici une légende qui vous aidera à comprendre la signification des couleurs :", style={'fontSize': '20px','textAlign': 'center','marginTop': '20px','marginBottom': '20px'}),
    html.Br(),
    html.Img(src='/assets/legend_p8.png', style={'width': '60%', 'height': '60%'}, className='image-gallery'),
    html.Br(),
    html.P('"Plus le score est vert, plus le risque de piqûre de tique est faible et meilleures sont vos stratégies de prévention."', style={'fontSize': '32px','textAlign': 'center','marginTop': '20px','marginBottom': '20px', 'font-weight': 'bold'}),
    html.Br(),
    html.Hr(className='orange_line'),

    # SECTION 1
    html.Br(),
    html.Div([
        html.P('Présence potentielle de tiques à pattes noires dans votre environnement', style={'fontSize': '40px','textAlign': 'center','marginTop': '20px','marginBottom': '20px','fontWeight': 'bold'}),
        html.Div([build_gauge('gauge1', 0.05, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '2px'}),
        html.Div(id='text_report1', style={'marginTop': '10px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Div(id='score_summary', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '30px'}),
        html.Br(),
        html.Hr(className='orange_line')
    ]),

    # SECTION 2
    html.Div([
        html.P('Risque d’exposition', style={'fontSize': '40px','textAlign': 'center','marginTop': '20px','marginBottom': '20px','fontWeight': 'bold'}),
        html.Div([build_gauge('gauge2', 0.05, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report2', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Br(),
        html.Hr(className='orange_line'),
    ]),

    # SECTION 3
    html.Div([
        html.P('Comportements préventifs individuels', style={'fontSize': '40px','textAlign': 'center','marginTop': '20px','marginBottom': '20px','fontWeight': 'bold'}),
        html.Div([build_gauge('gauge3', 0.05, {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]})], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report3', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Br()
    ]),

    # PET SECTION
    html.Div(id='pet_advices', children=[html.Div(id='text_pet_advices', style={'marginTop': '50px','whiteSpace': 'pre-wrap','text-align': 'justify','marginLeft': '50px','marginRight': '50px'})]),

    # Gain confidence and conclusion
    html.Div([
        html.Hr(className='orange_line'),
        html.P('Gagner en confiance face aux tiques', style={'fontSize': '40px','textAlign': 'center','marginTop': '20px','marginBottom': '20px','fontWeight': 'bold'}),
        dcc.Markdown("""
* La confiance dans la prévention des piqûres de tiques augmentera avec la mise en œuvre constante de comportements préventifs et l’expérience. Aucune méthode de prévention n’est efficace à 100 %. Malgré tous vos efforts, il se peut que vous trouviez encore des tiques sur vous, vos proches ou vos animaux. Cela ne signifie pas que vous faites mal les choses !

* Trouver les tiques n’est pas toujours facile. Les nymphes peuvent être particulièrement difficiles à repérer car elles peuvent être aussi petites qu’une graine de pavot. Encore une fois, la pratique et l’expérience vous aideront. Si vous ne pouvez pas inspecter facilement certaines parties de votre corps (par exemple à cause d’une mauvaise vue ou de mouvements limités), un miroir ou une loupe peut aider, ou demandez de l’aide à quelqu’un si possible.

* Il est compréhensible que certaines personnes ne se sentent pas à l’aise de retirer une tique fixée. Les inquiétudes courantes incluent le fait que la tête de la tique reste dans la peau ou une mauvaise manipulation. Pour savoir comment retirer correctement une tique et ce qu’il faut éviter, consultez [TickTool](https://ticktool.etick.ca/what-should-i-do-if-i-find-a-tick/).
""", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Hr(className='orange_line'),
        html.P('Conclusion', style={'fontSize': '40px','textAlign': 'center','marginTop': '20px','marginBottom': '20px','fontWeight': 'bold'}),
        dcc.Markdown("""
Nous espérons que ce rapport vous sera utile et vous permettra de vous sentir plus préparé et en confiance lors de vos activités extérieures.  
Vous avez des suggestions pour améliorer l’utilité et l’expérience de ce questionnaire ? N’hésitez pas à les envoyer à [pratique-ticktool@medvet.umontreal.ca](mailto:pratique-ticktool@medvet.umontreal.ca), nous serions ravis de vous lire.

Pour plus d’informations sur les tiques et les maladies transmises par les tiques au Canada, consultez les ressources suivantes :

[Gouvernement du Canada](https://www.canada.ca/fr/sante-publique/services/maladies/tiques-maladies-transmises-tiques.html)  
[TickTool](https://ticktool.etick.ca/)
""", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'})
    ]),

    # Export
    html.Div([
        dcc.Link('Réviser mon questionnaire', href='/page-2', className='modern-link', style={'display': 'inline-block','textAlign': 'center','backgroundColor': '#FF9636','color': 'white','padding': '10px','fontSize': '15px','borderRadius': '5px','textDecoration': 'none','whiteSpace': 'nowrap','height': '42px','lineHeight': '22px'}),
        html.Button('Exporter mon rapport en PDF', id='print-button', n_clicks=0, style={'width': '300px','textAlign': 'center','backgroundColor': '#FF9636','border': 'none','borderRadius': '5px','padding': '10px','fontSize': '15px','cursor': 'pointer','color': 'white','whiteSpace': 'nowrap','height': '42px'})
    ], style={'display': 'flex','justifyContent': 'center','alignItems': 'center','gap': '40px','marginTop': '20px'}),

    html.Br(),
    html.Hr(className='grey_blue_line'),

    # Methodology
    html.Div([
        html.P("Pour savoir comment vos niveaux de risque ont été calculés, cliquez ici :", style={'margin': '0','paddingRight': '8px','fontSize': '16px','display': 'inline'}),
        dcc.Link('Méthodologie', href='/methodology', style={'fontSize': '20px','display': 'inline','color': 'blue','textDecoration': 'underline'})
    ], style={'display': 'flex','justifyContent': 'center','alignItems': 'center','marginTop': '30px'}),

    html.Br(),
    html.Br(),
    #html.Div(id='display-answers_p8', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])
        
        
# CALLBACKS

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
                    if data['access_courtyard'] == "Yes" :
                        if(data['courtyard_herbaceous_or_forest'] == 'Yes'):
                            score1 = 2.4
                        else:
                            if data['house_deer'] == "Yes":
                                score1 = 2.4
                            else:
                                if data['house_proximity_wooded_area'] == "Yes":
                                    score1 = 2.4
                                else :
                                    score1 = 1.5
                    else:
                        if data['house_proximity_wooded_area'] == "Yes":
                            score1 = 2.4
                        else:
                            score1 = 1.5
            elif risk == 'Low':
                if ( (data['How_many_embedded_in_your_skin'] != "Not applicable") \
                    and (data['How_many_embedded_in_your_skin'] != "I don't remember") \
                        and (data['How_many_embedded_in_your_skin'] != "0")):
                    score1 = 1.5
                else:
                    if data['access_courtyard'] == "Yes" :
                        if data['house_deer'] == "Yes":
                            score1 = 1.5
                        else:
                            if data['house_proximity_wooded_area'] == "Yes":
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


# def calculat_score_and_record_answers(data):
#     ######
#     #Enregistrement des données en cas de consentement
#     ######
#     if data and data.get('consent') == 'yes':
#         now = datetime.datetime.now()
#         ip_address = request.remote_addr
#         myline = str(ip_address) + '\t' + now.strftime('%Y-%m-%d %H:%M:%S') 
#         for k in mykeys:
#             if k in data.keys():
#                 myline += '\t' + str(data[k])
#             else:
#                 myline += '\t\t'
           
#         myline += '\n'
#         unique_output = re.sub(r'[^a-zA-Z0-9]', '_', now.strftime('%Y-%m-%d %H:%M:%S'))
#         filename = 'survey_results_' +  unique_output + '.tsv'
#         with open(filename, 'a') as tsvfile:
#             tsvfile.write(myline)
#     ######
#     ######
#     # Risk Calculation based on zipcode
#     #zipcode = data['zipcode']
#     risk = risk_dict.get(data['zipcode'], 'Unknown')
#     ######
#     ######
#     # Evaluation score1 BLT in environment
#     ######
#     score1 = 0
#     if data and 'zipcode' in data:
#         if risk == 'High':
#             score1 = 2.4
#         elif risk == 'Medium':
#             if data['How_many_embedded_in_your_skin'] != "Not applicable" \
#                 and data['How_many_embedded_in_your_skin'] != "I don't remember" \
#                     and data['How_many_embedded_in_your_skin'] != "0" \
#                         and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
#                             and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
#                                 and data['How_many_freely_moving_on_your_skin'] != "0":
#                             score1 = 2.4
#             else:
#                 if data['access_courtyard'] == "Yes" :
#                     if(data['courtyard_herbaceous_or_forest'] == 'Yes'):
#                         score1 = 2.4
#                     else:
#                         if data['house_deer'] == "Yes":
#                             score1 = 2.4
#                         else:
#                             if data['house_proximity_wooded_area'] == "Yes":
#                                 score1 = 2.4
#                             else :
#                                 score1 = 1.5
#                 else:
#                     if data['house_proximity_wooded_area'] == "Yes":
#                         score1 = 2.4
#                     else:
#                         score1 = 1.5
#         elif risk == 'Low':
#             if ( (data['How_many_embedded_in_your_skin'] != "Not applicable") \
#                 and (data['How_many_embedded_in_your_skin'] != "I don't remember") \
#                     and (data['How_many_embedded_in_your_skin'] != "0")):
#                 score1 = 1.5
#             else:
#                 if data['access_courtyard'] == "Yes" :
#                     if data['house_deer'] == "Yes":
#                         score1 = 1.5
#                     else:
#                         if data['house_proximity_wooded_area'] == "Yes":
#                             score1 = 1.5
#         #elif risk not found !
#     ######
#     # Risk of exposure
#     #######       
#     score2 = 0
#     # optimiser avec x not in list
#     if data['How_many_embedded_in_your_skin'] != "Not applicable" \
#         and data['How_many_embedded_in_your_skin'] != "I don't remember" \
#             and data['How_many_embedded_in_your_skin'] != "0"\
#                 and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
#                     and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
#                         and data['How_many_freely_moving_on_your_skin'] != "0":
#                     score2 = 2.4
#     else:
#         if data['frequency_outdoor_activities'] == 'Very often (More than 10 times a year)':
#             score2 = 2.4
#         else:
#             if ( data['time_daily_wooded_area'] == 'Between one and five hours per day' ) or (  data['time_daily_wooded_area'] == 'More than five hours per day' ):
#                 score2 = 2.4
#             else:
#                 if data['frequency_outdoor_activities'] == 'Rarely':
#                     score2 = 1.5
#                 else:
#                     if data['time_daily_wooded_area'] in {'Never', 'Less than one hour per day'}:
#                         score2 =1.5
#     ######
#     # Preventive behavior
#     #######
#     score3 = 0
#     ###
#     # Constructuion d'une table de reponses considérées comme oui
#     considered_as_yes = ['Most of the time', 'Always', 'Not applicable to my situation']
#     # Calcul du score de mesures de protection
#     score_at_least_4_protective_behaviours = 0
#     if data['search_for_informations_ticks'] == 'yes' :
#         score_at_least_4_protective_behaviours += 1
#     if data['Wearing_long_layers_of_clothing'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Wearing_light-coloured_clothing'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Tucking_in_clothes'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['DEET'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Walking_on_cleared_paths'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Examining_your_clothes'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['clothes_in_the_dryer'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Bathing_or_showering'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     ######
#     ######
#     if (risk == 'High') or (risk == 'Medium') or (data['visite_area_disease_ticks'] == 'yes') : 
#         if data['Examining_yourself'] == 'Most of the time' or data['Examining_yourself'] == 'Always':
#             if (risk == 'Medium') or (risk == 'High'):
#                 if data['access_courtyard'] == 'yes':
#                     if data['courtyard_mowing'] in considered_as_yes:
#                         if data['courtyard_fallen_leaves'] in considered_as_yes:
#                             if data['courtyard_clearing_herbaceous'] in considered_as_yes:
#                                 if data['courtyard_clearing_herbaceous'] in considered_as_yes:
#                                     if data['courtyard_fences_deer'] in considered_as_yes:
#                                         if score_at_least_4_protective_behaviours >= 4 :
#                                             score3 = 2.4
#                                         else :
#                                             score3  = 1.5
#                                     else :
#                                         if score_at_least_4_protective_behaviours >= 4 :
#                                             score3 = 1.5
#                                         else:
#                                             score3 = 0.6
#                             else :
#                                 if score_at_least_4_protective_behaviours >= 4 :
#                                     score3 = 1.5
#                                 else :
#                                     score3 = 0.6
#                         else :
#                             score3 = 0.6
#                     else :
#                         score3 = 0.6
#                 else:
#                     if score_at_least_4_protective_behaviours >= 4:
#                         score3 = 2.4
#                     else :
#                         score3 = 1.5
#             else :
#                 if score_at_least_4_protective_behaviours >= 4:
#                     score3 = 2.4  
#                 else :
#                     score3 = 1.5
#         else :
#             score3 = 0.6
#     ######
#     ######
#     ######
#     ######
#     return score1, score2, score3


######
# Adaptated text report
######

# @callback(
#     Output('score_summary', 'children'),
#     Input('computed_scores', 'data')
# )
# def update_summary(scores):
#     if scores is None:
#         return "Waiting for scores..."

#     messages = []

#     if scores['score1'] >= 2:
#         messages.append("Risk 1 is high.")
#     elif scores['score1'] >= 1:
#         messages.append("Risk 1 is moderate.")
#     else:
#         messages.append("Risk 1 is low.")

#     if scores['score2'] >= 2:
#         messages.append("Risk 2 is high.")
#     elif scores['score2'] >= 1:
#         messages.append("Risk 2 is moderate.")
#     else:
#         messages.append("Risk 2 is low.")

#     if scores['score3'] >= 2:
#         messages.append("Risk 3 is high.")
#     elif scores['score3'] >= 1:
#         messages.append("Risk 3 is moderate.")
#     else:
#         messages.append("Risk 3 is low.")

#     return html.Ul([html.Li(msg) for msg in messages])
# @callback(
#     Output('text_no_calculation1', 'children'),
#     Input('computed_scores', 'data')
#     )

# def display_no_calculation(scores):
#     print(scores)
#     if scores is None:
#         return "Waiting for scores..."
#     sentence = 'PLATE !'
#     return dcc.Markdown(sentence)
   


#   return sentence

@callback(
    Output('text_report1', 'children'),
    Input('record_answers', 'data')
)
def display_personalized_text1(data):

    risque = risk_dict.get(data['zipcode'], 'Inconnu')
    valeurs_negatives = ['non', 'oui', "Je ne me souviens pas"]

    ###############################################################################
    # 1. Présence potentielle de tiques à pattes noires dans votre environnement
    ###############################################################################

    phrase = ''

    # Code postal et type de résidence
    if data['which_residence'] == 'Principale' or data['which_residence'] == 'Secondaire':
        phrase += f"""* La région de votre résidence {data['which_residence']} présente un risque de niveau **{risque}**."""
    else:
        phrase += f"""* La région de votre résidence présente un risque de niveau **{risque}**."""

    phrase += '\n\n'

    # Environnement péri-domestique
    phrase += "* Les données suggèrent que la majorité des expositions aux tiques surviennent dans l'environnement péri-domestique, plutôt qu'à distance. Bien qu'il ne soit pas possible de déterminer votre niveau exact de risque à partir de ce questionnaire, la présence de certains éléments sur ou près de votre propriété peut donner une indication du risque, selon des études scientifiques.\n\n"

    # Végétation herbacée ou zone boisée à proximité
    if data['house_proximity_wooded_area'] not in valeurs_negatives:
        phrase += "* Vous avez indiqué la **présence de zones herbacées, boisées ou de lisières sur votre terrain, ou le fait d’habiter près d’une zone boisée**. La présence de tels milieux est associée à une augmentation des maladies transmises par les tiques. Cela ne signifie pas que vous devez éviter de passer du temps à l’extérieur, mais **vous devez être vigilant et adopter des mesures de protection**. Il existe plusieurs moyens de réduire le risque d’exposition aux tiques sur votre propriété — pour en savoir plus, consultez [Que puis-je faire pour réduire les tiques dans ma cour ?](https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). Pensez à vous protéger pendant vos travaux extérieurs en **portant des vêtements longs, en appliquant un répulsif, puis en effectuant une vérification de tiques et en prenant un bain ou une douche.**\n"

    # Cour, jardin ou zone boisée
    if data['access_courtyard'] == 'oui':
        phrase += "* Vous avez indiqué **avoir une cour, un jardin ou une zone boisée**. Bien que posséder un espace extérieur n’entraîne pas automatiquement un risque de piqûre de tique, certains éléments peuvent l’augmenter, notamment : la **taille du terrain, la présence de jardins fleuris ou potagers, de zones herbacées ou boisées, de tas de bois, de murets de pierre, de litière de feuilles, ou encore des aires d’activités comme des zones de jeux pour enfants, des espaces de repas ou de détente**.\n"

    # Aire de jeux pour enfants
    if data['courtyard_children_play_area'] == 'oui':
        phrase += "* Vous avez indiqué **avoir des équipements de jeu pour enfants ou une structure d’activité sur votre propriété**. Il est conseillé de **les rapprocher de la maison et de les éloigner des zones boisées ou herbacées**. **Remplacer l’herbe par des copeaux de bois ou maintenir l’herbe très courte** est également recommandé.\n\n"

    # Présence de cerfs
    if data['house_deer'] == 'oui':
        phrase += "* Vous avez indiqué **voir ou soupçonner la présence de cerfs sur votre propriété**. Les cerfs sont des hôtes des tiques à pattes noires et jouent un rôle important dans leur cycle de vie. Des études suggèrent que **l’absence de clôture pour exclure les cerfs est associée à un risque accru de piqûres**. Bien qu’il ne soit pas toujours possible d’installer une clôture autour de toute la propriété, vous pouvez envisager d’en clôturer une partie que vous utilisez régulièrement. Cela empêchera aussi les cerfs de manger vos plantes et offrira un espace sécurisé pour vos animaux. Pour en savoir plus, consultez [Que puis-je faire pour réduire les tiques dans ma cour ?](https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). Pensez à vous protéger pendant vos travaux extérieurs en portant des vêtements longs, en appliquant un répulsif, puis en effectuant une vérification de tiques et en prenant un bain ou une douche.\n\n"

    phrase += '\n\n\n\n'

    return dcc.Markdown(phrase)
#######
#######

@callback(
    Output('text_report2', 'children'),
    Input('record_answers', 'data')
)
def display_personalized_text2(data):

    phrase = ""

    try:
        if (data['attached_to_your_skin'] != 'Jamais' and data['attached_to_your_skin'] != 'Non applicable') or (data['Freely_moving'] != 'Jamais' and data['Freely_moving'] != 'Non applicable'):
            phrase += "* Vous avez indiqué avoir trouvé une tique sur vous au cours des 12 derniers mois. Pour cette raison, un niveau de risque **élevé** d'exposition aux tiques vous a été attribué.\n\n"
    except:
        pass

    try:
        if data['On_a_pet'] != 'Jamais' and data['On_a_pet'] != 'Non applicable':
            phrase += "* Vous avez indiqué avoir trouvé une tique sur votre animal au cours des 12 derniers mois. Pour cette raison, un niveau de risque **élevé** d'exposition aux tiques vous a été attribué, car l’exposition de votre animal suggère souvent une exposition similaire pour vous.\n\n"
    except:
        pass

    try:
        if data['Freely_moving_outside'] != 'Jamais' and data['Freely_moving_outside'] != 'Non applicable':
            phrase += "* Vous avez indiqué avoir trouvé une tique dans votre environnement au cours des 12 derniers mois. Cela suggère que vous fréquentez des habitats à tiques. Un niveau de risque **élevé** d’exposition vous a été attribué.\n\n"
    except:
        pass

    try:
        if data['time_daily_wooded_area'] == 'Plus de cinq heures par jour':
            phrase += "* Vous avez indiqué pratiquer des activités extérieures dans des habitats propices aux tiques, au moins une ou deux fois par saison. Les loisirs en plein air sont associés à un risque accru de piqûres et de maladies transmises par les tiques. Des études antérieures ont établi un lien entre des activités telles que la randonnée, la chasse ou le jardinage, et un risque accru. Vous n'avez pas besoin d'éviter ces activités, mais il est important de vous **protéger, vous et vos proches**, et de faire des vérifications de tiques !\n\n"
        elif data['time_daily_wooded_area'] == 'Entre une et cinq heures par jour':
            phrase += "* Une exposition professionnelle ou récréative fréquente en milieu naturel est aussi liée à un risque accru. Il est donc essentiel d’adopter des mesures de prévention régulières : réappliquer le répulsif si nécessaire, effectuer des vérifications de tiques en cours de journée, etc.\n\n"
    except:
        pass

    try:
        if data['time_daily_wooded_area'] in ['Plus de cinq heures par jour', 'Entre une et cinq heures par jour']:
            phrase += "* Si vous passez souvent du temps dans des habitats propices aux tiques, envisagez des vêtements traités à la perméthrine comme protection supplémentaire. Pour plus d’informations, consultez [Tout ce que vous devez savoir sur la prévention](https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n\n"
    except:
        pass

    valeurs_negatives = ['Jamais', 'Non applicable']

    try:
        if (data['time_daily_wooded_area'] in ['Jamais', 'Moins d\'une heure par jour']) \
            and (data['attached_to_your_skin'] in valeurs_negatives) \
            and (data['Freely_moving'] in valeurs_negatives) \
            and (data['On_a_pet'] in valeurs_negatives) \
            and (data['Freely_moving_outside'] in valeurs_negatives):
                phrase += "* Vous avez indiqué passer peu de temps à l’extérieur, ce qui diminue les risques d'exposition. Toutefois, il existe un faible risque de rencontrer une tique n’importe où au Canada (hors cercle arctique), notamment en raison de leur dispersion par les oiseaux.\n\n"

        if (data['time_daily_wooded_area'] in ['Jamais', 'Moins d\'une heure par jour']) \
            and ((data['attached_to_your_skin'] not in valeurs_negatives) \
                or (data['Freely_moving'] not in valeurs_negatives) \
                or (data['On_a_pet'] not in valeurs_negatives) \
                or (data['Freely_moving_outside'] not in valeurs_negatives)):
                phrase += "* Vous avez déjà trouvé une tique, malgré un temps limité passé en extérieur. Cela pourrait être dû à la proximité avec un habitat à tiques, ou à une rencontre hors habitat typique. Quoi qu’il en soit, **restez vigilant et effectuez régulièrement des vérifications de tiques**.\n\n"
    except:
        pass

    return dcc.Markdown(phrase)


#######
#######

@callback(
    Output('text_report3', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text3(data):
    
    sentence = ""
    
    # try :
    #     risk = risk_dict.get(data['zipcode'], 'Unknown')
    #     if risk == 'Low':
    #         sentence += "*Ce niveau de risque vous serait attribué si vous viviez ou visitiez une zone à risque de maladie de Lyme, ou si la maladie de Lyme apparaissait dans votre région actuelle.*\n\n"
    # except:
    #     sentence += "*Ce niveau de risque vous serait attribué si vous viviez ou visitiez une zone à risque de maladie de Lyme, ou si la maladie de Lyme apparaissait dans votre région actuelle.*\n\n"
        
    sentence += ("Des recherches ont démontré l'association entre un risque accru de maladies transmises par les tiques et le fait de ne pas adopter de mesures de protection, "
                 "notamment ne pas effectuer de contrôle corporel, ne pas utiliser de répulsif, ne pas porter de vêtements appropriés, et ne pas prendre de douche après avoir passé du temps à l'extérieur. "
                 "Chaque comportement offre une couche de protection supplémentaire, et aucun comportement seul ne garantit de prévenir les piqûres de tiques ou les maladies. "
                 "Il est donc recommandé d'adopter autant de comportements préventifs que possible et réalisables pour vous et votre famille : [Lien TickTool](https://ticktool.etick.ca/incorporate-prevention) \n\n")
    
    no_body_check = ['Never','Rarely', 'Sometimes']
    try :
        if data['Examining_yourself'] in no_body_check:
            sentence += "* Vous avez indiqué que vous ne faites jamais, rarement ou parfois un contrôle corporel des tiques après avoir été dans une zone boisée où la maladie de Lyme est endémique, ce qui explique pourquoi vous avez reçu un score « Faible » pour vos comportements préventifs.\n\n"
    
        if data['Examining_yourself'] in no_body_check or data['Examining_yourself'] == 'Not applicable':
            sentence += ("* Bien qu'aucun comportement unique n'ait démontré de manière constante être le plus efficace, effectuer un contrôle corporel minutieux des tiques est la méthode de protection la plus recommandée. "
                         "Cela ne nécessite pas d’équipement spécial – bien qu’un miroir pleine longueur et un miroir à main puissent aider – cela prend simplement du temps. "
                         "En planifiant et en réservant 10 minutes pour un contrôle après une sortie en plein air, vous augmentez vos chances de le faire et réduisez ainsi votre risque de piqûre ou de maladie transmise par les tiques. "
                         "N’oubliez pas de vérifier aussi les autres membres du foyer et les animaux ! Si vous trouvez une tique, félicitez-vous, retirez-la et poursuivez votre contrôle au cas où il y en aurait d’autres.\n\n")
        else :
            sentence += ("* Vous avez indiqué que vous faites un contrôle corporel des tiques la plupart du temps après avoir été dans une zone boisée où la maladie de Lyme est endémique – bravo ! "
                         "Bien qu'aucun comportement unique n'ait démontré de manière constante être le plus efficace, effectuer un contrôle des tiques est la méthode de protection la plus recommandée. "
                         "Cela ne nécessite pas d’équipement spécial – bien qu’un miroir pleine longueur et un miroir à main puissent aider – cela prend simplement du temps. "
                         "En planifiant et en réservant du temps pour un contrôle après une sortie en plein air, vous augmentez vos chances de le faire et réduisez ainsi votre risque de piqûre ou de maladie transmise par les tiques. "
                         "N’oubliez pas de vérifier aussi les autres membres du foyer et les animaux ! Si vous trouvez une tique, félicitez-vous, retirez-la et poursuivez votre contrôle au cas où il y en aurait d’autres.\n\n")
    except :
        pass   
    
    #Q13 ????????
    
    # Feedback sur vivre seul ou avec quelqu’un
    try:
        if data['live_alone'] == 'yes' :
            sentence += ("* Effectuer un contrôle des tiques peut être difficile pour tout le monde, car les tiques aiment se cacher dans des endroits difficiles d'accès. "
                         "Comme vous **vivez seul**, il peut être très utile d'avoir à la fois un **miroir pleine longueur** et un **miroir à main** pour faciliter ce processus. "
                         "Certaines personnes trouvent qu'avoir un **rouleau anti-peluches** peut aider à atteindre les tiques non attachées, et de même, un **gant de toilette sous la douche** peut aider à déloger les tiques dans des endroits inaccessibles. "
                         "N'oubliez pas de porter une attention particulière à votre **cuir chevelu, ligne des cheveux, oreilles, bras, poitrine, dos, taille, nombril, aine, jambes, derrière les genoux et entre les orteils**.\n\n"
                         "En 2021, 45 % des cas de maladie de Lyme au Canada ont été diagnostiqués chez des adultes âgés de 55 à 79 ans. "
                         "Cela ne signifie pas que les personnes de ce groupe d’âge ne peuvent pas passer du temps en plein air, mais suggère plutôt que ce groupe devrait **adopter des comportements constants** pour se protéger des tiques.\n\n"
                         "Pour plus d'informations sur la protection, consultez [Tout ce que vous devez savoir sur la prévention](https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n")
        elif data['live_with_someone_over_18'] == 'yes' :
            sentence += ("* Comme vous **vivez avec un autre adulte**, vous pouvez **vous rappeler mutuellement d’adopter des comportements préventifs** contre les piqûres de tiques et **vous aider à effectuer un contrôle des tiques** – notamment dans les zones difficiles à atteindre comme le **cuir chevelu et le dos**. "
                         "En vous aidant et en vous rappelant mutuellement de penser aux tiques, il sera **plus facile d’intégrer ces pratiques dans votre routine**. **Si vous faites un contrôle seul**, il peut être très utile d'avoir à la fois un **miroir pleine longueur** et un **miroir à main**. "
                         "Certaines personnes trouvent qu'avoir un **rouleau anti-peluches** peut aussi aider à atteindre les tiques non attachées, et de même, un **gant de toilette sous la douche** peut aider à déloger les tiques dans des endroits inaccessibles.\n\n"
                         "En 2021, 45 % des cas de maladie de Lyme au Canada ont été diagnostiqués chez des adultes âgés de 55 à 79 ans. "
                         "Cela ne signifie pas que les personnes de ce groupe d’âge ne peuvent pas passer du temps en plein air, mais suggère plutôt que ce groupe devrait essayer d’adopter des comportements constants pour se protéger des tiques.\n\n"
                         "Pour plus d'informations sur la protection, consultez [Tout ce que vous devez savoir sur la prévention](https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n")
        elif data['live_with_child_0_4'] == 'yes' or data['live_with_child_5_14'] == 'yes' or data['live_with_child_15_18'] == 'yes':
            sentence += ("* Environ **11 % des cas de maladie de Lyme signalés au Canada en 2021 concernaient des enfants âgés de 5 à 14 ans**, mais d'autres données suggèrent que le risque de piqûres de tiques est **plus élevé chez les enfants de 5 ans ou moins**. "
                         "Cela s’explique par le fait que les enfants de cet âge **jouent souvent près du sol et quittent les sentiers balisés**. "
                         "Ils sont aussi **moins susceptibles de se contrôler** pour détecter les tiques. "
                         "Cela ne signifie **pas** que les enfants plus âgés ne peuvent pas développer une maladie transmise par les tiques, et il est important que tous les membres de la famille apprennent à se protéger des tiques. "
                         "Comme pour les adultes, le risque peut être réduit en effectuant un **contrôle des tiques, en portant des vêtements longs, en rentrant les vêtements dans les chaussures, en utilisant un répulsif si l’enfant a plus de 6 mois, et en prenant une douche après avoir passé du temps à l’extérieur**.\n"
                         "Pour plus d’informations sur la protection des enfants contre les piqûres de tiques, consultez [Comment puis-je protéger mes enfants ?](https://ticktool.etick.ca/how-can-i-protect-my-children/).\n")
    except :
        pass
    
    try :
        yes_property_management = ['Most of the time', 'Always']
        
        #Tonte
        if data['courtyard_mowing'] in yes_property_management:
            sentence += ("* Bravo pour entretenir régulièrement votre pelouse ! Garder l'herbe courte est très important pour réduire le risque d'exposition aux tiques. "
                         "Les tiques grimpent sur l'herbe haute pour s'attacher aux personnes et aux animaux qui passent. "
                         "En gardant l'herbe courte régulièrement et de façon constante – surtout dans les zones fréquentées par vous ou vos animaux – vous rendez votre propriété moins accueillante pour les tiques.\n\n")
        else:
            sentence += ("* L'entretien de la pelouse est très important pour réduire le risque d'exposition aux tiques. "
                         "Les tiques grimpent sur l'herbe haute pour s'attacher aux personnes et aux animaux qui passent. "
                         "En gardant l'herbe courte régulièrement et de façon constante – surtout dans les zones fréquentées par vous ou vos animaux – vous pouvez rendre votre propriété moins accueillante pour les tiques.\n\n")
        
        #Enlèvement des feuilles mortes
        if data['courtyard_fallen_leaves'] in yes_property_management:
            sentence += ("* Bravo pour enlever régulièrement les feuilles mortes de votre propriété ! "
                         "Les feuilles mortes offrent un environnement sûr pour les tiques, les protégeant du froid en hiver et du dessèchement en été. "
                         "En enlevant ces feuilles, vous réduisez un des habitats les plus importants pour les tiques sur votre propriété. "
                         "Selon la taille de votre terrain, vous pouvez vous concentrer sur les zones où vous ou vos animaux passez le plus de temps.\n\n")
        else:
            sentence += ("* Les feuilles mortes offrent un environnement sûr pour les tiques, les protégeant du froid en hiver et du dessèchement en été. "
                         "En enlevant ces feuilles, vous pouvez réduire un des habitats les plus importants pour les tiques sur votre propriété. "
                         "Selon la taille de votre terrain, vous pouvez vous concentrer sur les zones où vous ou vos animaux passez le plus de temps.\n\n")
        
        #Débroussaillage et élagage
        if data['courtyard_clearing_herbaceous'] in yes_property_management:
            sentence += ("* Bravo pour le débroussaillage régulier et l’élagage des branches ! Ces habitats sont propices aux petits rongeurs, qui non seulement portent des tiques, mais jouent un rôle clé dans le cycle de vie des bactéries responsables de la maladie de Lyme et d'autres maladies transmises par les tiques. "
                         "En supprimant les zones herbacées dans les endroits où vous ou vos animaux passez beaucoup de temps, vous rendez ces lieux moins accueillants pour les souris et les tiques, réduisant ainsi la probabilité qu'ils s'approchent de votre maison.\n\n")
        else :
            sentence += ("* Les broussailles herbacées et les branches longues offrent un habitat favorable aux petits rongeurs, qui non seulement portent des tiques, mais jouent un rôle clé dans le cycle de vie des bactéries responsables de la maladie de Lyme et d'autres maladies transmises par les tiques. "
                         "En supprimant les zones herbacées dans les endroits où vous ou vos animaux passez beaucoup de temps, vous pouvez rendre ces lieux moins accueillants pour les souris et les tiques, réduisant ainsi la probabilité qu'ils s'approchent de votre maison.\n\n")
        
        sentence += ("Gardez à l'esprit que le jardinage, le temps passé dans la végétation et les activités extérieures générales peuvent augmenter votre risque d'exposition aux maladies transmises par les tiques. "
                     "Pensez donc à vous protéger pendant vos travaux en portant des vêtements longs et en appliquant un répulsif, ainsi qu’à effectuer un contrôle des tiques et à prendre une douche ensuite. "
                     "Beaucoup craignent que les mesures extérieures pour réduire les tiques puissent avoir des conséquences environnementales négatives. "
                     "Pour en savoir plus sur ce sujet et d'autres questions fréquentes, consultez [Que puis-je faire pour réduire les tiques dans mon jardin ?](https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/).\n\n")
     
    except :
        pass
     
    return dcc.Markdown(sentence)
#######
#######

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
    
        # Traitement anti-tiques pour les chiens
        if data['dog'] == 'yes' or data['cat'] == 'yes' or data['horse'] == 'yes':
            sentence += ("* Les animaux de compagnie **ne peuvent pas transmettre la maladie de Lyme ni d'autres maladies transmises par les tiques aux humains. "
                         "Cependant, avoir un animal est associé à un risque accru de piqûres de tiques ou de propagation de maladies transmises par les tiques. "
                         "Cela s'explique généralement par le fait que la présence d'un animal signifie que vous passez plus de temps à l'extérieur, donc plus près des tiques**. "
                         "Cela ne signifie pas que vous devez éviter d'avoir des animaux ! Si vous voyez des tiques sur votre animal, cela suggère que vous avez peut-être aussi été dans un habitat à tiques, "
                         "et que vous devriez prendre des mesures pour protéger à la fois vous-même, votre(s) animal(aux) et votre famille.\n\n")
        
        if data['anti_tick_treatment_dog'] in no_anti_ticks :
            sentence += ("* Vous avez indiqué **prendre soin d'au moins un chien**. Les chiens sont exposés aux piqûres de tiques, et **tout comme les humains, ils peuvent souffrir de la maladie de Lyme** "
                         "et d'autres maladies transmises par les tiques. Heureusement, plusieurs produits spécifiques aux espèces existent pour protéger les animaux contre les tiques et la maladie de Lyme, "
                         "y compris **comprimés, traitements spot-on et vaccins**. Certains de ces produits peuvent aussi protéger votre animal contre d'autres parasites comme les **puces et les vers**. "
                         "Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient, quand l’utiliser, "
                         "en fonction de vos activités, du risque, du climat local, de l'efficacité des traitements disponibles et de vos préférences. "
                         "Il n'existe aucune preuve suggérant que posséder un chien augmente votre risque de contracter une maladie transmise par les tiques. "
                         "Cependant, **les personnes qui ont des chiens passent souvent plus de temps à l'extérieur** dans des habitats à tiques, il est donc important que vous vous protégiez.\n\n")
        elif data['anti_tick_treatment_dog'] == 'yes':
            sentence += ("* Vous avez indiqué **prendre soin d'au moins un chien et lui fournir des produits anti-tiques** – bravo ! Les chiens sont exposés aux piqûres de tiques, et **tout comme les humains, ils peuvent souffrir de la maladie de Lyme** "
                         "et d'autres maladies transmises par les tiques. En administrant un produit préventif contre les tiques, vous aidez à les garder en sécurité. "
                         "Plusieurs produits spécifiques aux espèces existent pour protéger les animaux contre les tiques et la maladie de Lyme, y compris **comprimés, traitements spot-on et vaccins**. "
                         "Certains de ces produits peuvent aussi protéger votre animal contre d'autres parasites comme les **puces et les vers**. "
                         "Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient, quand l’utiliser, "
                         "en fonction de vos activités, du risque, du climat local, de l'efficacité des traitements disponibles et de vos préférences. "
                         "Il n'existe aucune preuve suggérant que posséder un chien augmente votre risque de contracter une maladie transmise par les tiques. "
                         "Cependant, **les personnes qui ont des chiens passent souvent plus de temps à l'extérieur** dans des habitats à tiques, il est donc important que vous vous protégiez.\n\n")
        
        # Traitement anti-tiques pour les chats
        if data['anti_tick_treatment_cat'] in no_anti_ticks :
            sentence += ("* Vous avez indiqué prendre soin d'au moins un chat. Les chats sont exposés aux piqûres de tiques, il est donc important de les protéger avec des produits anti-tiques spécifiques à leur espèce. "
                         "En administrant un produit préventif, vous contribuez à les garder en sécurité. Plusieurs **produits spécifiques aux espèces** existent pour protéger les animaux contre les tiques, "
                         "y compris les comprimés et traitements spot-on. Certains de ces produits peuvent aussi protéger votre animal contre d'autres parasites comme les puces et les vers. "
                         "Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient, quand l’utiliser, "
                         "en fonction de vos activités, du risque, du climat local, de l'efficacité des traitements disponibles et de vos préférences. "
                         "Il est intéressant de noter que posséder un chat a été associé à un risque accru de maladies transmises par les tiques, contrairement à la possession d’un chien. "
                         "Cela peut être dû à des différences dans les comportements préventifs entre propriétaires de chats et de chiens, dans l'administration des produits anti-tiques, "
                         "à des contrôles de tiques moins fréquents chez les chats, à un toilettage plus intense chez les chats, ou parce que les chats ont tendance à errer dans l'herbe haute. "
                         "Quelle que soit la raison de cette association, il est toujours conseillé d'effectuer des contrôles de tiques sur votre chat, si possible, "
                         "et de parler à votre vétérinaire des mesures de prévention.\n\n")
        elif  data['anti_tick_treatment_cat'] == 'yes':
            sentence += ("* Vous avez indiqué prendre soin d'au moins un chat et lui fournir des produits anti-tiques – bravo ! Les chats sont exposés aux piqûres de tiques, il est donc important de les protéger avec des produits anti-tiques spécifiques à leur espèce. "
                         "Plusieurs **produits spécifiques aux espèces** existent pour protéger les animaux contre les tiques, y compris les comprimés et traitements spot-on. Certains de ces produits peuvent aussi protéger votre animal contre d'autres parasites comme les puces et les vers. "
                         "Votre vétérinaire est la meilleure personne pour vous conseiller sur ces options afin que vous puissiez choisir ce qui vous convient, quand l’utiliser, "
                         "en fonction de vos activités, du risque, du climat local, de l'efficacité des traitements disponibles et de vos préférences. "
                         "Il est intéressant de noter que posséder un chat a été associé à un risque accru de maladies transmises par les tiques, contrairement à la possession d’un chien. "
                         "Cela peut être dû à des différences dans les comportements préventifs entre propriétaires de chats et de chiens, dans l'administration des produits anti-tiques, "
                         "à des contrôles de tiques moins fréquents chez les chats, à un toilettage plus intense chez les chats, ou parce que les chats ont tendance à errer dans l'herbe haute. "
                         "Quelle que soit la raison de cette association, il est toujours conseillé d'effectuer des contrôles de tiques sur votre chat, si possible, "
                         "et de parler à votre vétérinaire des mesures de prévention.\n\n")   
        
        # Chevaux
        if data['horse'] == 'yes':
            sentence += ("* Les chevaux peuvent aussi souffrir de la maladie de Lyme, et comme aucun vaccin n’est homologué pour les chevaux, la prévention des tiques est importante. "
                         "Un toilettage et un contrôle quotidiens des tiques, une gestion appropriée des pâturages et l’utilisation de répulsifs spécifiques aux chevaux peuvent aider à réduire le risque de piqûres. "
                         "Pour plus d’informations sur les maladies transmises par les tiques et la prévention, parlez à votre vétérinaire. "
                         "Certaines études ont trouvé que posséder ou monter à cheval est associé à un risque accru de piqûres de tiques et de maladies transmises par les tiques. "
                         "Cela s’explique probablement par le fait que les cavaliers et leurs chevaux partagent le même environnement et donc un risque similaire d’exposition aux tiques.\n\n")
        
        sentence += ("* Pour plus d’informations sur les animaux de compagnie et les tiques, consultez [Comment puis-je protéger mes animaux ?](https://ticktool.etick.ca/how-can-i-protect-my-pets/)    [Tick Talk Canada](https://ticktalkcanada.com/)\n\n")
    
    except:
        pass
    
    return html.Div([
        html.Hr(className='orange_line'),
        html.P(
            'Un mot sur les animaux de compagnie',
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




#### Print the dictionnary

# @callback(
#     Output('hidden-div', 'children'),
#     Input('print-button', 'n_clicks')
# )
# def trigger_print(n_clicks):
#     if n_clicks > 0:
#         return dcc.Location(id='print-location', href='javascript:window.print();')
#     return ''

# ######
# ######

# #Display data dictionnary for dev
   
# @callback(
#     Output('display-answers_p8', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p8(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."
