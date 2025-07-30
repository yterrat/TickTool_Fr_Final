#!/usr/bin/env python3

# Import des modules
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-7')

layout = html.Div([
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.P("Avec votre consentement, les informations fournies dans ce questionnaire pourront être utilisées dans le cadre de projets de recherche. \
           Ces projets seront supervisés par un chercheur principal de l’Université de Montréal et seront approuvés par un comité d’éthique de la recherche. \
           Il ne vous sera pas demandé de fournir votre nom ou vos coordonnées. \
           Le chercheur s’engage à maintenir et protéger la confidentialité des données vous concernant, \
           selon les conditions décrites dans ce formulaire. Vous pouvez néanmoins compléter le questionnaire et obtenir un rapport personnalisé, même si vous ne consentez pas à ce que vos réponses soient utilisées à des fins de recherche.",
            style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px', 'textAlign': 'justify'}),
    html.Br(),
    html.P("Consentement à l’utilisation secondaire des données :",
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px','text-decoration': 'underline'}),
    html.P("Je consens à ce que le chercheur, ou les étudiants sous sa supervision, utilisent des données anonymisées pour de futurs projets de recherche, \
           sous réserve de leur approbation éthique et conformément aux mêmes principes de confidentialité et de protection des informations.",
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px'}),
    html.Br(),
    html.B("Consentez-vous à partager vos réponses avec l’Université de Montréal ?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Oui', 'value': 'yes'},
                {'label': 'Non', 'value': 'no'}
            ],
            style={'width': '100px'},
            value='',
            id='consent'
        )
    ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    html.Br(),

    html.Div(
        id='personal_questions',
        children=[
            html.Hr(className='grey_blue_line'),
            html.Br(),
            dcc.Markdown('*Merci d’avoir accepté de partager vos réponses à des fins de recherche. Nous vous serions reconnaissants de bien vouloir remplir les questions socio-démographiques suivantes. \
            Ces informations nous aident à orienter le matériel éducatif sur la maladie de Lyme là où il est le plus pertinent. \
            Vous pouvez choisir l’option « Je préfère ne pas répondre » pour chaque question si vous souhaitez ne pas divulguer certaines informations.*',
                style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px'}),
            html.Br(),
            html.Div([
                html.B('Questions socio-démographiques', style={'font-size': '60px'})
            ], style={'text-align': 'center'}),

            html.P("Quel est votre genre ?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'De genre fluide', 'value': 'Gender-fluid'},
                            {'label': "Homme", 'value': "Man"},
                            {'label': "Non-binaire", 'value': "NonBinary"},
                            {'label': "Homme trans", 'value': "Trans Man"},
                            {'label': "Femme trans", 'value': "Trans Women"},
                            {'label': "Bispirituel(le)", 'value': "Two-spirit"},
                            {'label': "Femme", 'value': "Women"},
                            {'label': "Je ne m’identifie à aucune des options proposées", 'value': "I don’t identify with any option provided "},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"}
                        ],
                        id='Gender',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Br(),

            html.P("Quel âge avez-vous ?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': "Moins de 18 ans", 'value': "Under 18"},
                            {'label': "Entre 18 et 24 ans", 'value': "18-24"},
                            {'label': "Entre 25 et 34 ans", 'value': "25-34"},
                            {'label': "Entre 35 et 44 ans", 'value': "35-44"},
                            {'label': "Entre 45 et 54 ans", 'value': "45-54"},
                            {'label': "Entre 55 et 64 ans", 'value': "55-64"},
                            {'label': "Entre 65 et 74 ans", 'value': "65-74"},
                            {'label': "75 ans ou plus", 'value': "75 or older"},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"}
                        ],
                        id='Age',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Br(),

            html.P("Quel est le niveau d’études que vous avez complété à ce jour ?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'École primaire ou moins', 'value': 'Elementary school or less'},
                            {'label': "Quelques études postsecondaires", 'value': "Some post-secondary school"},
                            {'label': "Collège, école professionnelle ou technique", 'value': "College, vocational or trade school"},
                            {'label': "Programme universitaire de premier cycle", 'value': "Undergraduate university program"},
                            {'label': "Programme universitaire de deuxième ou troisième cycle", 'value': "Graduate or professional university program"},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"}
                        ],
                        id='Education',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Br(),

            html.P("Laquelle des catégories suivantes décrit le mieux votre situation professionnelle actuelle ?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Temps plein (35 heures ou plus/semaine)', 'value': 'Working full-time (35 or more hours per week)'},
                            {'label': 'Temps partiel (moins de 35 heures/semaine)', 'value': 'Working part-time (less than 35 hours per week)'},
                            {'label': "Travailleur autonome", 'value': "Self-employed"},
                            {'label': "Étudiant à temps plein (sans emploi)", 'value': "Student attending full time school (not working)"},
                            {'label': "Sans emploi, à la recherche d’un emploi", 'value': "Unemployed, but looking for work"},
                            {'label': "Inactif (ex. sans emploi et ne cherche pas, parent ou personne au foyer à plein temps)", 'value': "Not in the workforce (e.g. unemployed, but not looking for work, a full-time homemaker or parent), but looking for work"},
                            {'label': "Retraité(e)", 'value': "Retired"},
                            {'label': "Autre", 'value': "Other"},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"}
                        ],
                        id='Employment_status',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Br(),

            html.P("Quelle est la catégorie qui décrit le mieux le revenu total de votre ménage (avant impôts) ?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Moins de 20 000 $', 'value': 'Under $20,000'},
                            {'label': "De 20 000 $ à moins de 40 000 $", 'value': "$20,000 to just under $40,000"},
                            {'label': "De 40 000 $ à moins de 60 000 $", 'value': "$40,000 to just under $60,000"},
                            {'label': "De 60 000 $ à moins de 80 000 $", 'value': "$60,000 to just under $80,000"},
                            {'label': "De 80 000 $ à moins de 100 000 $", 'value': "$80,000 to just under $100,000"},
                            {'label': "De 100 000 $ à moins de 120 000 $", 'value': "$100,000 to just under $120,000"},
                            {'label': "De 120 000 $ à moins de 150 000 $", 'value': "$120,000 to just under $150,000"},
                            {'label': "150 000 $ et plus", 'value': "$150,000 and above"},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"}
                        ],
                        id='Income',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Br(),

            html.P("Quelle est la principale langue parlée dans votre foyer ?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Anglais', 'value': 'English'},
                            {'label': "Français", 'value': "French"},
                            {'label': "Autre (veuillez préciser)", 'value': "Other (please specify)"},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"},
                        ],
                        id='primary_language',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Br(),

            html.P("Veuillez sélectionner le(s) groupe(s) de population auquel(s) vous vous identifiez.", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Arabe', 'value': 'Arab'},
                            {'label': "Noir", 'value': "Black"},
                            {'label': "Chinois", 'value': "Chinese"},
                            {'label': "Philippin", 'value': "Filipino"},
                            {'label': "Autochtone (Première Nation, Métis ou Inuk)", 'value': "Indigenous (that is, First Nation, Métis, or Inuk)"},
                            {'label': "Japonais", 'value': "Japanese"},
                            {'label': "Coréen", 'value': "Korean"},
                            {'label': "Latino-Américain", 'value': "Latin American"},
                            {'label': "Sud-Asiatique (ex. Indien, Pakistanais, Sri Lankais, etc.)", 'value': "South Asian (e.g., East Indian, Pakistani, Sri Lankan, etc.)"},
                            {'label': "Sud-Est asiatique (ex. Vietnamien, Cambodgien, Laotien, Thaïlandais, etc.)", 'value': "Southeast Asian (including Vietnamese, Cambodian, Laotian, Thai, etc.)"},
                            {'label': "Ouest asiatique (ex. Iranien, Afghan, etc.)", 'value': "West Asian (e.g., Iranian, Afghan, etc.)"},
                            {'label': "Blanc", 'value': "White"},
                            {'label': "Groupe de population non listé ci-dessus", 'value': "Population group not listed above"},
                            {'label': "Je préfère ne pas répondre", 'value': "I prefer not to answer"}
                        ],
                        id='population_group',
                        value='I prefer not to answer'
                    )],
                style={'font-size': '15px'}
            ),
            html.Div(
                id='population_group_addition',
                children=[
                    html.Br(),
                    html.P('Veuillez préciser le groupe de population :', className='question_style2'),
                    dcc.Textarea(
                        id='population_group_text',
                        value='',
                        style={'width': '30%', 'height': 40}
                    )
                ]),
            html.Br(),

            html.P("Vous avez maintenant terminé le questionnaire ! Merci pour votre intérêt. Si vous souhaitez commenter votre expérience ou le contenu du questionnaire, vous pouvez le faire ici :", className='question_style2'),
            dcc.Textarea(
                id='commentaries',
                value='',
                style={'width': '100%', 'height': 300}
        ),
    ]),
    html.Br(),
    html.Br(),

    html.Div([
        dcc.Link('Précédent', href='/page-6', className='modern-link', style={'textAlign': 'center', 'whiteSpace': 'nowrap'}),
        dcc.Link('Accéder à votre rapport personnalisé', href='/page-8', className='modern-link', style={'textAlign': 'center', 'whiteSpace': 'nowrap'}),
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '40px'
    }),
    html.Br(),
    html.Br(),
    dbc.Progress(value=100, style={"height": "15px"}, className="mb-3", label="100 % complété"),
])
    
    
@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('consent', 'value'),
    Input('Gender', 'value'),
    Input('Age', 'value'),
    Input('Education', 'value'),
    Input('Employment_status', 'value'),
    Input('Income', 'value'),
    Input('primary_language', 'value'),
    Input('population_group', 'value'),
    Input('population_group_text', 'value'),
    Input('commentaries', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p7(Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,data):
    data = data or {}
    if Q1 is not None :
        data['consent'] = Q1
    if Q2 is not None :
        data['Gender'] = Q2
    if Q3 is not None :
        data['Age'] = Q3
    if Q4 is not None :
        data['Education'] = Q4
    if Q5 is not None :
        data['Employment_status'] = Q5
    if Q6 is not None :
        data['Income'] = Q6
    if Q7 is not None :
        data['primary_language'] = Q7
    if Q8 is not None :
        data['population_group'] = Q8
    if Q9 is not None:
        data['population_group_text'] = Q9
    if Q10 is not None :
        data['commentaries'] = Q10
    return data


# Afficher les valeurs du data quand la page esr reparcourue 

@callback(
    Output('consent', 'value'),
    Output('Gender', 'value'),
    Output('Age', 'value'),
    Output('Education', 'value'),
    Output('Employment_status', 'value'),
    Output('Income', 'value'),
    Output('primary_language', 'value'),
    Output('population_group', 'value'),
    Output('population_group_text', 'value'),
    Output('commentaries', 'value'),
    Input('record_answers', 'data')
)

def set_dropdown_value(data):
    return (
        data.get('consent', None),
        data.get('Gender', None),
        data.get('Age', None),
        data.get('Education', None),
        data.get('Employment_status', None),
        data.get('Income', None),
        data.get('primary_language', None),
        data.get('population_group', None),
        data.get('population_group_text', None),
        data.get('commentaries', None)
    )


@callback(
    Output(component_id='personal_questions', component_property='hidden'),
    [Input(component_id='consent', component_property='value')]
)
def show_hide_element_consent(consent):
    if consent == 'yes':
        return False
    else:
        return True

    
#######
#######
    
@callback(
    Output(component_id='population_group_addition', component_property='hidden'),
    [Input(component_id='population_group', component_property='value')])

def show_hide_element_population_group_addition(answ):
    if answ == 'Population group not listed above':
        return False
    else:
        return True

# @callback(
#     [Output('Age', 'value'),
#      Output('Education', 'value'),
#      Output('Employment_status', 'value'),
#      Output('Income', 'value'),
#      Output('primary_language', 'value'),
#      Output('population_group', 'value'),
#      Output('commentaries', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page7(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('Age', None),
#      data.get('Education', None),
#      data.get('Employment_status', None),
#      data.get('Income', None),
#      data.get('primary_language', None),
#      data.get('population_group', None),
#      data.get('commentaries', None)
#      ]
