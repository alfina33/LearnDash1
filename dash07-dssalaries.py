# -*- coding: utf-8 -*-
"""
Created on Mon May  1 21:22:58 2023

@author: HP
"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# load data
df = pd.read_csv('https://raw.githubusercontent.com/alfina33/LearnDash1/main/ds_salaries.csv') 

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Data Science Salaries 2020-2023', style={
            'textAlign': 'center', 'color': '#CD5C5C'}),
    html.Div(children='''Data Source: https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023''',
             style={'textAlign': 'center'}),
    dcc.Dropdown(df.job_title.unique(), 'Data Scientist',
                 id='dropdown-job_title', placeholder='Select a job title'),
    dcc.Dropdown(df.company_location.unique(), 'US',
                 id='dropdown-company_location', placeholder='Select a company location'),
    dcc.Graph(id='histogram'),
    dcc.Graph(id='heatmap'),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
])

@callback(
    [Output('histogram', 'figure'),
     Output('heatmap', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('dropdown-job_title', 'value'),
     Input('dropdown-company_location', 'value')]
)

def update_graph(job_title_value, company_location_value):
    dff1 = df[(df['job_title'] == job_title_value)]
    dff2 = df[(df['job_title'] == job_title_value) & (df['company_location'] == company_location_value)]
    histogram = px.histogram(dff2, x='salary_in_usd', color='job_title', nbins=30, title='Salary Distribution Job Title')
    grup1 = dff1.groupby(['work_year', 'job_title', 'experience_level'])['salary_in_usd'].mean().reset_index()
    heatmap = px.imshow(grup1.pivot_table(index='experience_level', columns='job_title', values='salary_in_usd'),
                        title='Salary by Job Title and Experience Level')
    grup2 = dff1.groupby(['work_year', 'job_title', 'employment_type'])['salary_in_usd'].mean().reset_index()
    bar_chart = px.bar(grup2, x='employment_type', y='salary_in_usd', color='work_year',
                       title='Salary by employment type')
    pie_chart = px.pie(dff1, values='salary_in_usd', names='remote_ratio')
    
    return histogram, heatmap, bar_chart, pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)