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

df = pd.read_csv('/Users/billcoleman/NOTEBOOKS/DublinAI/data.csv')
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

markdown_text_1 = '''
### DublinAI Fellowship

DublinAI Fellowship is an intensive, eight-week professional development program for PhD grads and postdoctoral researchers that help's bridge the gap to a full-time career in data & AI related fields. Careers include Data Scientist, Machine Learning Engineer, Data Analyst or niche AI expert (NLP, Computer Vision etc).

Fellows come from a mix of data driven STEM fields: physics, math, engineering, statistics, computer science, machine & deep learning, computer vision, NLP, quantitative finance, genomics, biology, neuroscience etc.

The following is an outline group project examining a telco customer churn problem. Fellows collaborated in a sprint 'hackathon' data science challenge, implementing agile development practices as a distributed team.

### Customer Tenure by Monthly Charges

The scope of this application is to determine the which customers are more likely to churn. As a test case we considered the telcom data that can be retrieved from [this Kaggle competition](https://www.kaggle.com/blastchar/telco-customer-churn).

This plot maps customer tenure against average monthly charges. Arguably, those customers spending more per month are somewhat more likely to churn.
'''

markdown_text_ChurnCount = '''
The data collects different features for customers that either churn or did not. The data classes are not balanced in terms of customers that did and did not churn, as can be seen in the following histogram:
'''

markdown_text_tenure = '''
The models used in this analysis incorporate this information into the probability predictions for the different customers.

To have an understanding of the data we can consider the tenure record of customers that did churn and that did not churn.
'''

app.layout = html.Div([
        html.Img(id='dublinAI_logo',
                     src='http://34.245.231.73:8000/dublinAI_logo.png'),
                  dcc.Markdown(children=markdown_text_1),

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
            html.Img(id='dublinAI_logo2',
                     src='http://34.245.231.73:8000/dublinAI_logo.png'),
#            dcc.Markdown(children=markdown_text_1),
            dcc.Markdown(children=markdown_text_ChurnCount),
            html.Img(id='ChurnCount',
                     src='http://34.245.231.73:8000/ChurnCount.png'),
            dcc.Markdown(children=markdown_text_tenure),
            html.Img(id='tenure',
                     src='http://34.245.231.73:8000/tenure.png'),
            html.H4(children='Modified Table'),
            generate_table(df2),         
])

if __name__ == '__main__':
    app.run_server(debug=True)