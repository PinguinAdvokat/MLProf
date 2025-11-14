import pandas as pd
import sqlite3 as sq
import folium
import selenium
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

def filter(df, country, part_day):
    if country:
        df = df[df.country == country]
    if part_day:
        df = df[df.part_day == part_day]
    return df

def get_day_part(df):
    if pd.isna(df):
        return None
    hour = pd.to_datetime(df).hour
    if 0 <= hour < 6:
        return 'Ночь'
    elif 6 <= hour < 12:
        return 'Утро'
    elif 12 <= hour < 18:
        return 'День'
    else:
        return 'Вечер'

try:
    conn = sq.connect("../data.db")
    df = pd.read_sql('SELECT * FROM data', conn)
    conn.close()
except Exception as e:
    print(e)

df['part_day'] = df['time'].apply(get_day_part)
print(df.part_day.unique())

app = Dash()

m = folium.Map(zoom_start=12)
for track in df.groupby('track_id'):
    track = track[1]
    folium.PolyLine(track[['latitude', 'longitude']].values).add_to(m)

map_html = m.get_root().render()

day_parts = df.part_day.unique()
countrys = df.country.unique()
app.layout = [
    html.H1(children='I have no idea how it works', style={'textAlign':'center'}),
    dcc.Dropdown(day_parts[day_parts != None], '', id='part_day'),
    dcc.Dropdown(countrys[countrys != None], '', id='country'),

    dcc.Graph(id='season-step_freq'),
    #dcc.Graph(figure=px.histogram(df, x='season', y='step_frequency', histfunc='avg')),

    dcc.Graph(id='temp_to_hour'),
    #dcc.Graph(figure=px.histogram(df, x='hour', y='tempurture', histfunc='avg')),

    dcc.Graph(id='count_type'),
    #dcc.Graph(figure=px.histogram(df, x='type', histfunc='count')),

    dcc.Graph(id='step_freq_to_ele'),
    #dcc.Graph(figure=px.histogram(df, x='elevation', y='step_frequency', histfunc='avg')),

    dcc.Graph(id='count_season'),

    dcc.Graph(id='step_freq_to_temp'),
    #dcc.Graph(figure=px.histogram(df, x='tempurture', y='step_frequency', histfunc='avg')),

    dcc.Graph(id='count_country'),

    html.Iframe(
        srcDoc=map_html,
        width="100%",
        height="600"
    )
]

@callback(
    Output('season-step_freq', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def season_step_freq(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='season', y='step_frequency', histfunc='avg')

@callback(
    Output('temp_to_hour', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def temp_to_hour(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='hour', y='tempurture', histfunc='avg')

@callback(
    Output('count_type', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def count_type(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='type', histfunc='count')

@callback(
    Output('step_freq_to_ele', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def step_freq_to_ele(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='elevation', y='step_frequency', histfunc='avg')

@callback(
    Output('step_freq_to_temp', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def step_freq_to_temp(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='tempurture', y='step_frequency', histfunc='avg')

@callback(
    Output('count_season', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def count_season(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='season', histfunc='count')

@callback(
    Output('count_country', 'figure'),
    Input('part_day', 'value'),
    Input('country', 'value')
)
def count_country(part_day, country):
    dff = filter(df, country, part_day)
    return px.histogram(dff, x='country', histfunc='count')




if __name__ == '__main__':
    app.run(debug=True)