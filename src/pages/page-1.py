import dash
from dash import dcc, html, Input, Output, callback, State
import random
import plotly.graph_objs as go

# Enregistrement de la page principale

dash.register_page(__name__, path='/')

# Configuration
allowed_values = [0.1, 0.6, 1.5, 2.4]
step_size = 0.05
pause_ticks = 20

initial_state = {
    "gauge_in1": {"current": 0.0, "target": 0.6, "wait": 0, "has_left_zero": False},
    "gauge_in2": {"current": 0.0, "target": 1.5, "wait": 0, "has_left_zero": False},
    "gauge_in3": {"current": 0.0, "target": 2.4, "wait": 0, "has_left_zero": False},
}


def build_gauge(gauge_id, value, color_ranges, tickvals, ticktext):
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=value,
        gauge={
            'axis': {
                'range': [0, 3],
                'tickvals': tickvals,
                'ticktext': ticktext,
                'tickangle': 0,
                'tickfont': {'size': 18},
            },
            'bar': {'color': 'black', 'thickness': 0.2},
            'steps': [{'range': rng, 'color': clr} for clr, rng in color_ranges.items()],
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'valueformat': '.2f', 'font': {'color': 'rgba(0,0,0,0)'}}
    ))
    fig.update_traces(delta={'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                      value=value)
    return dcc.Graph(id=gauge_id, figure=fig, style={'height': '500px', 'width': '500px'})


layout = html.Div([
    html.Img(src='/assets/PraTIQUE_couleur.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Évaluez votre stratégie de prévention', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    html.P([
        "Le risque de piqûres de tiques – et la manière de les prévenir – peut parfois sembler compliqué.",
        html.Br(),
        "Souhaitez-vous mieux comprendre votre risque de piqûre et apprendre comment améliorer votre stratégie de prévention pour vous-même et votre famille ?",
        html.Br(), html.Br(),
        "Remplissez le questionnaire et recevez un rapport personnalisé pour vous aider à prendre des décisions éclairées et agir de manière adaptée pour vous protéger, vous et vos proches.",
        html.Br(),
        "Le questionnaire prend environ 15 minutes à remplir."
    ], style={'textAlign': 'center', 'marginLeft': '20px','marginRight': '20px','fontSize': '20px'}),

    html.Br(),
    # html.Div([
    #     html.P('Risque de présence de tiques à pattes noires dans votre environnement', style={'font-size': '25px', "font-weight": "bold"}),
    #     html.P('Risque d’exposition', style={'font-size': '25px', "font-weight": "bold"}),
    #     html.P('Niveau de prévention', style={'font-size': '25px', "font-weight": "bold"})
    # ], style={
    #     'display': 'flex',
    #     'justify-content': 'space-evenly',
    #     'align-items': 'center',
    #     'margin-top': '20px'
    # }),

    # html.Div([
    #     build_gauge('gauge_in1', 0.0, {
    #         'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
    #     }, [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé']),

    #     build_gauge('gauge_in2', 0.0, {
    #         'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
    #     }, [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé']),

    #     build_gauge('gauge_in3', 0.0, {
    #         'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]
    #     }, [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé'])
    # ], style={
    #     'display': 'flex',
    #     'justify-content': 'space-evenly',
    #     'align-items': 'center',
    #     'margin-top': '40px',
    # }),
    html.Div([

        html.Div([  # Une colonne = titre + gauge
            html.P('Risque de présence de tiques à pattes noires dans votre environnement',
                   style={'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
            build_gauge('gauge_in1', 0.0, {
                'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
            }, [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé'])
        ], style={'flex': 1, 'margin': '0 10px'}),
    
        html.Div([
            html.P('Risque d’exposition',
                   style={'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
            build_gauge('gauge_in2', 0.0, {
                'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
            }, [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé'])
        ], style={'flex': 1, 'margin': '0 10px'}),
    
        html.Div([
            html.P('Niveau de prévention',
                   style={'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
            build_gauge('gauge_in3', 0.0, {
                'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]
            }, [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé'])
        ], style={'flex': 1, 'margin': '0 10px'})

    ], style={
        'display': 'flex',
        'justify-content': 'space-evenly',
        'align-items': 'flex-start',  # pour l'alignement vertical
        'margin-top': '30px'
    }),


    html.Br(),
    html.Div(dcc.Link("Commencer le questionnaire et obtenir vos scores et un rapport personnalisé", href='/page-2', style={
        'font-size': '20px',
        'text-decoration': 'none',
        'color': 'white',
        'background-color': '#FF9636',
        'padding': '10px 20px',
        'border-radius': '8px',
        'font-weight': '500',
        'display': 'inline-block'
    }), style={'text-align': 'center', 'margin-top': '30px'}),

    html.Br(), html.Br(),
    html.Img(src='/assets/UdeM.png', style={'width': '20%', 'height': '20%'}, className='image-gallery'),
    html.Br(), html.Br(),
    dcc.Store(id='gauge-state', data=initial_state),
    dcc.Interval(id='interval', interval=100, n_intervals=0)
])


@callback(
    Output('gauge_in1', 'figure'),
    Output('gauge_in2', 'figure'),
    Output('gauge_in3', 'figure'),
    Output('gauge-state', 'data'),
    Input('interval', 'n_intervals'),
    State('gauge-state', 'data'),
    prevent_initial_call=True
)
def animate_gauges(n, state):
    updated_state = {}

    def update_value(gauge_data):
        current = gauge_data["current"]
        target = gauge_data["target"]
        wait = gauge_data.get("wait", 0)
        has_left_zero = gauge_data.get("has_left_zero", False)

        if wait > 0:
            return {"current": current, "target": target, "wait": wait - 2, "has_left_zero": has_left_zero}

        if abs(current - target) < step_size:
            if not has_left_zero and target > 0:
                has_left_zero = True
            possible_values = [v for v in allowed_values if v != target and (has_left_zero or v > 0)]
            new_target = random.choice(possible_values)
            return {"current": round(target, 2), "target": new_target, "wait": pause_ticks, "has_left_zero": has_left_zero}
        else:
            direction = 1 if target > current else -1
            new_current = round(current + direction * step_size, 2)
            return {"current": new_current, "target": target, "wait": 0, "has_left_zero": has_left_zero}

    updated_state["gauge_in1"] = update_value(state["gauge_in1"])
    updated_state["gauge_in2"] = update_value(state["gauge_in2"])
    updated_state["gauge_in3"] = update_value(state["gauge_in3"])

    fig1 = build_gauge('gauge_in1', updated_state["gauge_in1"]["current"],
                       {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
                       [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé']).figure

    fig2 = build_gauge('gauge_in2', updated_state["gauge_in2"]["current"],
                       {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
                       [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé']).figure

    fig3 = build_gauge('gauge_in3', updated_state["gauge_in3"]["current"],
                       {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]},
                       [0.6, 1.5, 2.4], ['Faible', 'Modéré', 'Élevé']).figure

    return fig1, fig2, fig3, updated_state
