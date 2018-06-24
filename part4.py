# Imports -- you may add others but do not need to
import csv

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='liyuyingcathy', api_key='e6Otvjw0o8OiZ3ZrQWit')

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets
x = []
y = []
with open('noun_data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', lineterminator='\r\n')
    for item in reader:
        if len(item) != 0 and item[0] != 'Noun':
            x.append(item[0])
            y.append(item[1])
    csv_file.close()

data = [go.Bar(x=x, y=y)]
layout = go.Layout(title='The Most Common Nouns')
fig = go.Figure(data=data, layout=layout)
py.image.save_as(fig, filename='part4_viz_image.png')
