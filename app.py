#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Mar 12 13:13:15 2020

@author: billcoleman
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

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

markdown_text = '''
### Here's Some Texty Stuff
## Two Hashes
# One Hash
#### Four hashes - this formatting seems to be similar to what you'd use in Jupyter notebooks.

This is an example of the way text will look in tandem with visual elements.
Incorporating images is fairly straightforward, you just need to host the image
somewhere. See above. /\ /\ /\.
Next I'll work out how to change size and position of stuff.
Some of that seems to be controlled from the css stylesheet.
Bill

Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

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
            html.Img(id='test_jpg',
                     src='http://www.listeningtest.eu/EXP3/images/Xperi_TUD_IRC_logo.png'),
            dcc.Markdown(children=markdown_text),
            html.H4(children='Modified Table'),
            generate_table(df2),         
])

if __name__ == '__main__':
    app.run_server(debug=True)
