import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv('individualDetails.csv')
total = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recover = patients[patients['current_status'] == 'Recovered'].shape[0]
death = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1(children='Corona Virus Pandemic', style={'color': 'violet', 'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total Cases', className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Active Cases', className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Recovered', className='text-light'),
                    html.H4(recover, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Deaths', className='text-light'),
                    html.H4(death, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3')
    ], className='row'),
    html.Div([
        html.Div([], className='col-md-6'),
        html.Div([], className='col-md-6')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')
], className='container')


@app.callback(Output('bar', 'figure'),
          [Input('picker', 'value')])
def update_graph(selected_graph):
    if selected_graph == 'All':
        df_state = patients['detected_state'].value_counts().reset_index()
        return {
            'data': [go.Bar(x=df_state['detected_state'], y=df_state['count'])],
            'layout': go.Layout(title='State Total Cases Count')}
    else:
        status = patients[patients['current_status'] == selected_graph]
        df_state = status['detected_state'].value_counts().reset_index()
        return {
            'data': [go.Bar(x=df_state['detected_state'], y=df_state['count'])],
            'layout': go.Layout(title='State Total Cases Count')}


if __name__ == '__main__':
    app.run(debug=True)