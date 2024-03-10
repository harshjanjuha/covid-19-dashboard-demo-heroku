import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output

# external CSS style sheets
external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65',
        'crossorigin': 'anonymous'
    }
]
patients = pd.read_csv('IndividualDetails.csv')
total_cases = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]
recovered_df = patients[patients['current_status'] == 'Recovered']
recovered_df = recovered_df['gender'].value_counts().reset_index()

line_df = patients.copy()
line_df['diagnosed_date'] = pd.to_datetime(patients['diagnosed_date'], dayfirst=True)
line_df['week'] = line_df['diagnosed_date'].dt.isocalendar().week
line_df = line_df[['week', 'current_status']]
line_df = line_df.groupby('week').value_counts().reset_index()
recover_df = line_df[line_df['current_status'] == 'Recovered']  # .plot(kind='line',x='week',y='count')
deaths_df = line_df[line_df['current_status'] == 'Deceased']
hospital_df = line_df[line_df['current_status'] == 'Hospitalized']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# app.layout = html.H1('COVID-19 Dashboard', style={'text-align': 'center'})
app.layout = html.Div([
    html.H1("COVID-19 Dashboard - India's Perspective", style={'textAlign': 'center', 'color': 'white'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className="text-light"),
                    html.H4(total_cases, className="text-light")
                ], className="card-body")
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className="text-light"),
                    html.H4(active, className="text-light")
                ], className="card-body")
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered", className="text-light"),
                    html.H4(recovered, className="text-light")
                ], className="card-body")
            ], className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className="text-light"),
                    html.H4(deaths, className="text-light")
                ], className="card-body")
            ], className='card bg-success')
        ], className='col-md-3'),
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='line', figure={
                            'data': [go.Scatter(x=hospital_df['week'], y=hospital_df['count'], name='Hospitalized'),
                                     go.Scatter(x=recover_df['week'], y=recover_df['count'], name='Recovered'),
                                     go.Scatter(x=deaths_df['week'], y=deaths_df['count'], name='deaths')],
                            'layout': go.Layout(title='Weekly plot',yaxis={'type': 'log'},
                                                xaxis={'title': 'Week'},
                                                legend={'title': 'Data Types'})
                        }
                    )
                ], className="card-body")
            ], className="card")
        ], className="col-md-6"),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='pie_chart', figure={
                        'data': [go.Pie(values=recovered_df['count'], labels=recovered_df['gender'])],
                        'layout': go.Layout(title='Deaths based on gender')
                    })
                ], className="card-body")
            ], className="card")
        ], className="col-md-6"),
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='select', options=options, value='All'),
                    # value param contains the default select option from options list of dict's value key
                    dcc.Graph(id='bar')
                ], className="card-body")
            ], className="card")
        ], className='col-md-12'),
    ], className="row"),
], className="container")


# @app.callback(Output('bar', 'figure'), [Input('select', 'value')]) in this we meant , bar is id and parameter is figure and in input select is id and value is from where we are getting the value
@app.callback(Output('bar', 'figure'), [Input('select', 'value')])
def get_graph(selected_type):
    # plots graph
    if selected_type == 'All':
        bar_df = patients['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x=bar_df['detected_state'], y=bar_df['count'])],
                'layout': go.Layout(title='Total Counts')}
    else:
        selected_df = patients[patients['current_status'] == selected_type]
        bar_df = selected_df['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x=bar_df['detected_state'], y=bar_df['count'])],
                'layout': go.Layout(title=f'{selected_type} Counts')}


if __name__ == '__main__':
    app.run_server(debug=True)
