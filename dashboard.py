import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Dash, dash_table, Input, Output

import plotly.graph_objects as go
import geopandas as gpd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
# Load the dataset
df = pd.read_csv('https://drive.google.com/uc?id=1jgsrxU7XCaG2IhNeJLKSQW_Tu0aey_-_')
load_figure_template("all")
# Initialize the Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
m = df['month'].value_counts().sort_index(ascending=False)
monthly_growth = pd.DataFrame({'month': m.index, 'number of flats added': m.values})
# Neighborhood Performance
avg_price_neighborhood = round(df.groupby('neighborhood')['monthly_rent'].mean(), 2).reset_index()
avg_price_neighborhood.rename(columns={"monthly_rent": "avg_monthly_rent"}, inplace=True)
fig_neighborhood = px.bar(avg_price_neighborhood, x='avg_monthly_rent', y='neighborhood', title='Neighborhood Performance, Average selling price per neighborhood', template='cyborg_dark')


avg_price_per_sqm_neighborhood = round(df.groupby('neighborhood')['price_per_square_meter'].mean(), 2).reset_index()
fig_price_per_sqm = px.bar(avg_price_per_sqm_neighborhood, x='neighborhood', y='price_per_square_meter', title='Price per Square Meter Per Neighborhood',template='cyborg_dark', text='neighborhood')
selected_columns = ['monthly_rent', 'sq_meters', 'bedrooms', 'bathrooms', 'floor']

# Create a correlation matrix
correlation_matrix = df[selected_columns].corr()
configurations_count = df.groupby(['neighborhood', 'bathrooms', 'bedrooms']).size().reset_index(name='count')


# Create a bubble chart
configuration = px.scatter(
    configurations_count,
    x='bathrooms',
    y='bedrooms',
    size='count',
    color= 'count',
    color_continuous_scale= 'purples',
    template='sketchy_dark',
    hover_data=['bathrooms', 'bedrooms', 'count'],
    title='Most Common Bathroom and Bedroom Configurations',
    labels={'bathrooms': 'Bathrooms', 'bedrooms': 'Bedrooms', 'count': 'Frequency'},
    size_max=100,  # Adjust the maximum size of bubbles
)

# Create an interactive heatmap with Plotly Express
correlation = px.imshow(
    correlation_matrix,
    labels=dict(color="Correlation"),
    x=selected_columns,
    y=selected_columns,
    color_continuous_scale='aggrnyl', 
    # Optional: Choose a color scale
    title='Correlation Heatmap'
)
fig_price_per_sqm.update_layout(
    autosize=False,
    width=600,
    height=400,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    ))

fig_neighborhood.update_layout(
    autosize=False,
    width=600,
    height=400,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    ))
   


monthly_growth_fig = px.line(
    monthly_growth,
    x='month', y='number of flats added',
    markers=True,
    template='cyborg_dark',
    title= 'Monthly growth of numbers of apartments added'
)

monthly_growth_fig.update_layout(
    autosize=False,
    width=600,
    height=300,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    ))
monthly_growth_fig.add_trace(go.Scatter(x=monthly_growth['month'], y=monthly_growth['number of flats added'],
                         line = dict(color='royalblue', width=2), marker_color='red'))
correlation.update_layout(
    autosize=False,
    width=600,
    height=400,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    ))
configuration.update_layout(
    autosize=False,
    width=700,
    height=400,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    ))
correlation.update_layout(template='sketchy_dark')

PAGE_SIZE = 5

# Define app layout
app.layout = html.Div([
    
    html.Br(),
    html.Div([
        html.H1("BERLIN APARTMENT PERFORMANCE ANALYSIS", style={'textAlign': 'center', 'color': 'white'})
    ]),


    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='neighborhood-dropdown',
                options=[{'label': neighborhood, 'value': neighborhood} for neighborhood in df['neighborhood'].unique()],
                multi=True,
                placeholder='Select Neighborhood(s)',
                style={'background-color': 'rgb(35, 38, 40)', 'color':'grey', 'margin-left':'30px'}
            )], width=5)
            
        ], align='right'),
    
    html.Br(),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table-sorting-filtering',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                style_header={
                    'backgroundColor': 'darkpurple',
                    'fontWeight': 'bold',
                    'color': 'black'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
                
                page_current=0,
                page_size=20,
                page_action='custom',
                filter_action='custom',
                filter_query='',
                sort_action='custom',
                sort_mode='multi',
                sort_by=[]
            )
        ], 
        style={'height': 300, 'width': 700, 'overflowY': 'scroll', 'text-align': 'center', 'margin-left':'50px'},
                className='six columns',
                width=5),
        dbc.Col([
            dcc.Graph(id='monthly-growth', figure=monthly_growth_fig, style={'margin-left':'20px'})
        ], width=5),
        
    ], align='center'),
    html.Br(),
    dbc.Row([
         dbc.Col([
            dcc.Graph(id='neighborhood-performance', figure=fig_neighborhood,  style={'margin-left':'50px'})
        ], width=5),
         dbc.Col([
            dcc.Graph(id='price-per-sqm', figure=fig_price_per_sqm, style={'margin-left':'80px'})
        ], width=6)
    ],  align='center'),
    html.Br(),
    dbc.Row([
        
        dbc.Col([
            dcc.Graph(id='correlation-price', figure=correlation, style={'margin-left':'50px'})
        ], width=5),
        dbc.Col([
            dcc.Graph(id='configuration', figure=configuration, style={'margin-left':'50px'})
        ], width=6)
    ],  align='center')

])







operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']] 





def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-sorting-filtering', 'data'),
    Input('table-sorting-filtering', "page_current"),
    Input('table-sorting-filtering', "page_size"),
    Input('table-sorting-filtering', 'sort_by'),
    Input('table-sorting-filtering', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')



@app.callback(
    Output('neighborhood-performance', 'figure'),
    Output('price-per-sqm', 'figure'),
    Input('neighborhood-dropdown', 'value')
)
def update_figures(selected_neighborhoods):

    # Update Neighborhood Performance
    filtered_avg_price_neighborhood = avg_price_neighborhood[avg_price_neighborhood['neighborhood'].isin(selected_neighborhoods)] if selected_neighborhoods else avg_price_neighborhood
    

    neighborhood_fig = px.bar(filtered_avg_price_neighborhood, x='avg_monthly_rent', y='neighborhood', title='Neighborhood Performance, Average selling price per neighborhood', template='cyborg_dark')
    # Update chart figure
    
    
    
    # Update Price per Square Meter
    filtered_avg_price_per_sqm_neighborhood = avg_price_per_sqm_neighborhood[avg_price_per_sqm_neighborhood['neighborhood'].isin(selected_neighborhoods)] if selected_neighborhoods else avg_price_per_sqm_neighborhood
    price_per_sqm_fig = px.bar(filtered_avg_price_per_sqm_neighborhood, x='neighborhood', y='price_per_square_meter', title='Price per Square Meter', template='cyborg_dark')

    price_per_sqm_fig.update_layout(
    autosize=False,
    width=700,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    ))

    neighborhood_fig.update_layout(
        autosize=False,
        width=600,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=4
        ))
   
    
    # Group by neighborhood and calculate average rent for each month
    
    
    return neighborhood_fig, price_per_sqm_fig



# Run the app
if __name__ == '__main__':
    app.run_server(port='8052', debug=True)
