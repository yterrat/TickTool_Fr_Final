#!/usr/bin/env python3

import dash
from dash import dcc, html, Input, Output, callback
import dash_daq as daq
import datetime
from flask import request
import re
import pandas as pd

dash.register_page(__name__, path='/methodology')

layout = html.Div([
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.P('Méthodologie', style={'font-size' : '80px', "font-weight": "bold", 'text-align': 'center'}),
    html.Br(),
    html.Br(),

    html.P("Potentiel de présence de la tique à pattes noires dans l'environnement", style={'font-size' : '35px', "font-weight": "bold", 'text-align': 'center'}),
    dcc.Markdown("""À l'aide du code postal à 6 chiffres, un niveau de risque initial est déterminé à une résolution de 1 km² en utilisant des données sur la convenance de l'habitat pour *Ixodes scapularis* (la tique à pattes noires de l'Est), puis ce niveau est ajusté selon la présence ou l'absence de caractéristiques spécifiques sur la propriété, comme illustré ci-dessous. Veuillez noter que ces niveaux de risque indiquent uniquement le risque de rencontrer *Ixodes scapularis*. Ils ne reflètent pas le risque de contracter la maladie de Lyme ou d'autres maladies transmises par les tiques.

Le risque lié à *Ixodes scapularis* a été calculé en intégrant des données sur la température (nombre annuel de degrés-jours de surface au-dessus de 0°C) et la présence d’un habitat propice, recueillies entre 2018 et 2023, afin d’obtenir un indice de risque quantitatif. Des informations supplémentaires sur la méthodologie utilisée pour calculer ce risque sont disponibles dans Kotchi et al (2021) [Publication scientifique] (https://doi.org/10.3390/rs13030524). En utilisant la méthode d’optimisation de Jenks et les coupures naturelles de Jenks, l’indice de risque a été catégorisé à une résolution de 1 km² en trois niveaux : faible, moyen et élevé. Ces niveaux de risque ont été établis pour tous les codes postaux du Manitoba, du centre et de l’est du Canada pour évaluer le risque de *Ixodes scapularis*. Ils ne sont pas applicables pour évaluer le risque de *Ixodes pacificus* (la tique à pattes noires de l’Ouest). Les personnes résidant à l’ouest du Manitoba sont invitées à consulter les ressources provinciales ainsi que eTick pour en apprendre davantage sur le risque potentiel dans leur région.""", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
    
    html.Img(src='/assets/BLT_in_environment_V2.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),

    html.Hr(className='orange_line'),
    html.Br(),
    html.P("Risque d'exposition", style={'font-size' : '35px', "font-weight": "bold", 'text-align': 'center'}),
    dcc.Markdown("""Le risque associé aux activités en plein air est formulé à partir d’expositions antérieures aux tiques et du nombre d’heures passées à l’extérieur chaque jour, soit pour des activités récréatives, soit dans des zones boisées dans le cadre professionnel, comme illustré ci-dessous.""", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),

    html.Img(src='/assets/Risk_of_exposure_V2.png', style={'width': '15%', 'height': '15%'}, className='image-gallery'),

    html.Hr(className='orange_line'),
    html.Br(),
    html.P("Comportements préventifs", style={'font-size' : '35px', "font-weight": "bold", 'text-align': 'center'}),
    dcc.Markdown("""Le risque associé à l’adoption de comportements préventifs est évalué à partir des réponses de l’utilisateur concernant différents comportements de prévention, ainsi que le fait qu’il sache ou soupçonne avoir visité ou vécu dans une région où il pourrait contracter une maladie transmise par les tiques (voir ci-dessous). Ce niveau de risque ne tient pas compte du risque environnemental réel (selon le code postal), car celui-ci est déjà fourni séparément. L’objectif de ce niveau de risque est d’encourager les utilisateurs à réfléchir aux comportements préventifs qu’ils mettent actuellement en œuvre et à ceux qu’ils souhaiteraient adopter à l’avenir, en fonction de leur risque environnemental et de leur exposition extérieure.""", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),

    html.Img(src='/assets/Preventive_behaviours_V2.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),

    html.Br(),
    html.Br(),
])
