import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv('data.csv')
df2 = df[['tenure', 'MonthlyCharges', 'TotalCharges', 'linear_prob',
          'linear_pred']]


def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app.layout = html.Div([
    dcc.Graph(
        id='rem_churn_monthly_tenure',
        figure={
            'data': [
                dict(
                    x=df[df['Churn_Yes'] == i]['tenure'],
                    y=df[df['Churn_Yes'] == i]['MonthlyCharges'],
                    text=df[df['Churn_Yes'] == i]['TotalCharges'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.Churn_Yes.unique()
            ],
            'layout': dict(
                xaxis={'title': 'tenure'},
                yaxis={'title': 'MonthlyCharges'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    html.H4(children='Modified Table'),
    generate_table(df2)
])

if __name__ == '__main__':
    app.run_server(debug=True)
