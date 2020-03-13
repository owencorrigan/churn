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

# df = pd.read_csv('/Users/billcoleman/NOTEBOOKS/DublinAI/data.csv')
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

markdown_text_1 = '''
### DublinAI Fellowship 

DublinAI Fellowship is an intensive, eight-week professional development program for PhD grads and postdoctoral researchers that help's bridge the gap to a full-time career in data & AI related fields. Careers include Data Scientist, Machine Learning Engineer, Data Analyst or niche AI expert (NLP, Computer Vision etc).

Fellows come from a mix of data driven STEM fields: physics, math, engineering, statistics, computer science, machine & deep learning, computer vision, NLP, quantitative finance, genomics, biology, neuroscience etc.

The following is an outline group project examining a telco customer churn problem. Fellows collaborated in a sprint 'hackathon' data science challenge, implementing agile development practices as a distributed team.

## Telco Customer Churn
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

markdown_text_Contract = '''
As can be seen from the histogram the majority of the customers that churn will do it after one  month (mean=17.97, mode=1, median=10). The tenure record of customers that did not churn is instead rather uniform. This seems to suggest that once a customer subscribe a contract that is long enough it will be unlikely that he will eventually churn. This intuition is supported by considering the type of contract stipulated by customers
'''

markdown_text_InternetService = '''
In the figure, on the Churn axis, 1 stands for churning and 0 for not churning. It can be seen that it is way more likely for customers with month to month contracts to churn rather than for customers that have longer types of contracts.

Other features that seem to be relevant to determine if a customer will churn or not are the type of payment used and, surprisingly, the type of internet line used.
'''

markdown_text_Customer1_probability = '''
The following analysis will indeed show that our intuition is correct
Based on the exploratory analysis, we now have a better understanding of our customer demographics and the factors that affect churn. But there is value in being able to predict if (and when) a customer is going to churn. For one, it can cost between 5 to 25 times as much to attract a new customer than to retain an existing one. What is the best way to predict churn? There is a lack of industry consensus, but survival analysis (Cox Proportional Hazards regression) and logistic regression are two techniques that have been found to produce good predictions. 
Cox PH regression (also known as survival analysis) is generally used to model the time until a certain event takes place – in this case, churn. It not only gives us a list of possible churners for the period, but for each customer, it also enables us to examine the probability of them churning as a function of time. With this knowledge, a customer can be targeted for special promotions or mobile & web push notifications when they’re deemed to be at risk for churn. 

We fitted a Cox PH model to our dataset, tuning hyperparameters using a grid search. We then excluded customers who had already churned, and conditioned our predictions on the basis that we knew the customers were still with us when the data was collected. The probability of churn for an example customer is shown in the following figure.
'''

markdown_text_Cox_FeatureRelevance = '''
This information also lets us distinguish various levels of loyalty profiles – e.g. near-future and far-future churners - and the factors that most influence this behaviour. The figure below shows the weights of the model. For our data set, the largest factor influencing churn was the type of internet service (consistent with our initial exploratory analysis). On the other hand, customers were unlikely to churn if they were tied down to a two year contract.
'''

markdown_text_Cox_InternetService = '''
The technique also enables us to look at how particular factors influence the model over time. In the figure below, we can compare the ‘survival’ (retention, in this case) curves for customers who subscribe to a fiber optic internet service to those who do not. We can not only see that customers who do subscribe are at a greater risk of churn (their curve drops off more quickly), but also gauge when they are likely to churn.
'''

markdown_text_Cox_ContractTwoYear = '''
The impact of getting customers to commit to a two year contract is clear from the following survival curves.
'''

markdown_text_shapLogistic = '''
Another approach that we used to analyse the problem consist in a simple logistic regression. This rather simplistic form of modelling only allow to get information about the probability that a customer will churn in the future. Anyhow, being so simple, it can be used as a first estimate as to determine which customers are more likely to churn. Similarly to what we did for the Cox model we can get an idea on which are the features that are considered diriment in determining if a customer will churn or not.
'''

markdown_text_conclusions = '''
As can be seen from the graphics this model attributes more importance to the tenure track of the customer, making it less likely for customer to churn whenever they have been customers for a long number of months. Note that in the Cox model this information is not consider as a feature and it only affect the baseline probability of the model.
'''

app.layout = html.Div([
        html.Img(id='dublinAI_logo',
                     src='https://demo.churnbucket.ie/static/dublinAI_logo.png'),

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
# =============================================================================
#             html.Img(id='dublinAI_logo2',
#                      src='https://churnbucket.ie/static/dublinAI_logo.png'),
# =============================================================================
#            dcc.Markdown(children=markdown_text_1),
            dcc.Markdown(children=markdown_text_ChurnCount),
            html.Img(id='ChurnCount',
                     src='https://demo.churnbucket.ie/static/ChurnCount.png'),
            dcc.Markdown(children=markdown_text_tenure),
            html.Img(id='tenure',
                     src='https://demo.churnbucket.ie/static/tenure.png'),
            dcc.Markdown(children=markdown_text_Contract),
            html.Img(id='Contract',
                     src='https://demo.churnbucket.ie/static/Contract.png'),
            dcc.Markdown(children=markdown_text_InternetService),
            html.Img(id='PaymentMethod',
                     src='https://demo.churnbucket.ie/static/PaymentMethod.png'),
            html.Img(id='InternetService',
                     src='https://demo.churnbucket.ie/static/InternetService.png'),
            dcc.Markdown(children=markdown_text_Customer1_probability),
            html.Img(id='Cust_1_prob',
                     src='https://demo.churnbucket.ie/static/Customer1_Probability.png'),
            dcc.Markdown(children=markdown_text_Cox_FeatureRelevance),
            html.Img(id='featureRelevance',
                     src='https://demo.churnbucket.ie/static/Cox_FeatureRelevance.png'),
            dcc.Markdown(children=markdown_text_Cox_InternetService),
            html.Img(id='internetService',
                     src='https://demo.churnbucket.ie/static/Cox_InternetService.png'),
            dcc.Markdown(children=markdown_text_Cox_ContractTwoYear),
            html.Img(id='Contract2Year',
                     src='https://demo.churnbucket.ie/static/Cox_ContractTwoYear.png'),
            dcc.Markdown(children=markdown_text_shapLogistic),
            html.Img(id='shapLogistic',
                     src='https://demo.churnbucket.ie/static/shapLogistic.png'),
            dcc.Markdown(children=markdown_text_conclusions),
#            html.H4(children='Modified Table'),
#            generate_table(df2),         
],
style={'backgroundColor': 'white',
       'color': 'black',
       'text-align': 'center'},
)

if __name__ == '__main__':
    app.run_server(debug=True)