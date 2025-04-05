import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------
# Data Processing Section
# -----------------------
data = pd.read_csv("cpi Group data.csv")

# Convert columns to numeric if necessary
columns = ['Index', 'Inflation (%)']
for column in columns:
    if data[column].dtype == 'O':
        data[column] = pd.to_numeric(data[column], errors='coerce')

# Create Date and Month_Year columns
data['Date'] = pd.to_datetime(
    data['Year'].astype(str) + '-' + data['Month'], 
    format='%Y-%B', errors='coerce'
)
data['Month_Year'] = data['Date'].dt.strftime('%b %y')
data = data.sort_values('Date')
data = data.dropna()

# ---------------------------------------
# Create Visualizations (Figures 1-12)
# ---------------------------------------
# Visualization 1: Average Inflation Rate by Group over Year
fig1 = px.line(
    data.groupby(['Year', 'Group'])['Inflation (%)'].mean().reset_index(),
    x='Year', y='Inflation (%)', color='Group', markers=True,
    title='Average Inflation Rate by Group'
)
fig1.update_traces(line=dict(width=2), marker=dict(size=8))
fig1.update_layout(
    template='plotly_white',
    xaxis_title='Year', yaxis_title='Average Inflation (%)',
    hovermode='x unified'
)
groups = data['Group'].unique()
buttons = [dict(
    label="All",
    method="update",
    args=[{"visible": [True] * len(fig1.data)},
          {"title": "Average Inflation Rate for All Groups"}]
)]
for grp in groups:
    visible = [trace.name == grp for trace in fig1.data]
    buttons.append(dict(
        label=str(grp),
        method="update",
        args=[{"visible": visible},
              {"title": f"Average Inflation Rate for Group: {grp}"}]
    ))
fig1.update_layout(updatemenus=[dict(
    active=0, buttons=buttons, x=1.35, y=1.10,
    xanchor='right', yanchor='top'
)])

# Visualization 2: Average Inflation Rate by Years by Group
fig2 = px.line(
    data.groupby(['Year', 'Group'])['Inflation (%)'].mean().reset_index(),
    x='Group', y='Inflation (%)', color='Year', markers=True,
    title='Average Inflation Rate by Years'
)
fig2.update_traces(line=dict(width=2), marker=dict(size=8))
fig2.update_layout(template='plotly_white', hovermode='x unified')
years = data['Year'].unique()
buttons = [dict(
    label="All",
    method="update",
    args=[{"visible": [True] * len(fig2.data)},
          {"title": "Average Inflation Rate by Group for All Years"}]
)]
for yr in years:
    visible = [trace.name == str(yr) for trace in fig2.data]
    buttons.append(dict(
        label=str(yr),
        method="update",
        args=[{"visible": visible},
              {"title": f"Average Inflation Rate by Group for Year: {yr}"}]
    ))
fig2.update_layout(updatemenus=[dict(
    active=0, buttons=buttons, x=1.35, y=1.10,
    xanchor='right', yanchor='top'
)])

# Visualization 3: Average Inflation Rate by States over Month_Year
fig3 = px.line(
    data.groupby(['Month_Year', 'State'])['Inflation (%)'].mean().reset_index(),
    x='Month_Year', y='Inflation (%)', color='State', markers=True,
    title='Average Inflation Rate by States'
)
fig3.update_traces(line=dict(width=2), marker=dict(size=8))
fig3.update_layout(template='plotly_white', hovermode='x unified')
states = data['State'].unique()
buttons = [dict(
    label="All",
    method="update",
    args=[{"visible": [True] * len(fig3.data)},
          {"title": "Average Inflation Rate for all States"}]
)]
for st in states:
    visible = [trace.name == str(st) for trace in fig3.data]
    buttons.append(dict(
        label=str(st),
        method="update",
        args=[{"visible": visible},
              {"title": f"Average Inflation Rate for State: {st}"}]
    ))
fig3.update_layout(updatemenus=[dict(
    active=0, buttons=buttons, x=1.35, y=1.10,
    xanchor='right', yanchor='top'
)])

# Visualization 4: Average Inflation Rate for Months and Years by State
fig4 = px.line(
    data.groupby(['Month_Year', 'State'])['Inflation (%)'].mean().reset_index(),
    x='State', y='Inflation (%)', color='Month_Year', markers=True,
    title='Average Inflation Rate for Months and Year'
)
fig4.update_traces(line=dict(width=2), marker=dict(size=8))
fig4.update_layout(template='plotly_white', hovermode='x unified')
month_year = data['Month_Year'].unique()
buttons = [dict(
    label="All",
    method="update",
    args=[{"visible": [True] * len(fig4.data)},
          {"title": "Average Inflation Rate for all months and Years"}]
)]
for mn_yr in month_year:
    visible = [trace.name == str(mn_yr) for trace in fig4.data]
    buttons.append(dict(
        label=str(mn_yr),
        method="update",
        args=[{"visible": visible},
              {"title": f"Average Inflation Rate for month and Year: {mn_yr}"}]
    ))
fig4.update_layout(updatemenus=[dict(
    active=0, buttons=buttons, x=1.35, y=1.10,
    xanchor='right', yanchor='top'
)])

# Visualization 5: Bar chart for monthly median inflation across years
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
traces = []
for month in months:
    month_data = data[data['Month'] == month]
    if not month_data.empty:
        month_grouped = month_data.groupby('Year')['Inflation (%)'].median().reset_index()
        trace = go.Bar(
            x=month_grouped['Year'], y=month_grouped['Inflation (%)'],
            name=month,
            marker=dict(color='rgb(150, 95, 100)', line=dict(width=1, color='black')),
            visible=False
        )
    else:
        trace = go.Bar(x=[], y=[], name=month, visible=False)
    traces.append(trace)
if traces:
    traces[0]['visible'] = True
buttons = []
for i, month in enumerate(months):
    visibility = [False] * len(months)
    visibility[i] = True
    buttons.append(dict(
        label=month,
        method="update",
        args=[{"visible": visibility},
              {"title": f"Average Inflation in {month} Across Years"}],
    ))
layout5 = go.Layout(
    template='plotly_white',
    updatemenus=[dict(
        active=0, buttons=buttons, x=0.05, y=1.15,
        xanchor='left', yanchor='top'
    )],
    title=f"Average Inflation in {months[0]} Across Years",
    xaxis=dict(title="Year", tickmode='linear', dtick=1),
    yaxis=dict(title="Average Inflation (%)"),
    hovermode='x unified'
)
fig5 = go.Figure(data=traces, layout=layout5)

# Visualization 6: Contribution Analysis with Pie and Stacked Bar Chart
unique_months = sorted(
    data['Month_Year'].unique(), 
    key=lambda x: pd.to_datetime(x, format='%b %y')
)
fig6 = make_subplots(
    rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'xy'}]],
    subplot_titles=("Contribution Pie Chart", "Contribution Stacked Bar Chart"),
    horizontal_spacing=0.30
)
trace_indices = []
all_traces = []
for month in unique_months:
    snapshot = data[data['Month_Year'] == month]
    group_contrib = snapshot.groupby('Group')['Inflation (%)'].median().reset_index()
    pie_trace = go.Pie(
        labels=group_contrib['Group'],
        values=group_contrib['Inflation (%)'],
        textinfo='percent+label',
        name=month
    )
    current_indices = []
    fig6.add_trace(pie_trace, row=1, col=1)
    current_indices.append(len(all_traces))
    all_traces.append(pie_trace)
    group_contrib['dummy'] = 'Inflation Contribution'
    temp_fig = px.bar(
        group_contrib, x='dummy', y='Inflation (%)',
        color='Group', color_discrete_sequence=px.colors.qualitative.Set3
    )
    bar_traces = list(temp_fig.data)
    for trace in bar_traces:
        fig6.add_trace(trace, row=1, col=2)
        current_indices.append(len(all_traces))
        all_traces.append(trace)
    trace_indices.append(current_indices)
fig6.update_layout(barmode='stack')
total_traces = len(all_traces)
buttons = []
for i, month in enumerate(unique_months):
    vis = [False] * total_traces
    for idx in trace_indices[i]:
        vis[idx] = True
    buttons.append(dict(
        label=month,
        method="update",
        args=[{"visible": vis},
              {"title": f"Contribution Analysis for {month}"}]
    ))
fig6.update_layout(
    updatemenus=[dict(
        active=0, buttons=buttons, x=0.5, y=1.2,
        xanchor='center', yanchor='top'
    )],
    title=f"Contribution Analysis for {unique_months[0]}",
    template='plotly_white'
)

# Visualization 7: Histogram and Boxplot (combined in one tab)
fig7_hist = px.histogram(
    data, x='Index', color='Group',
    facet_col='Group', facet_col_wrap=3, template='plotly_white',
    title='Distribution of Index Values by Group',
    labels={'Index': 'Index Value'},
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig7_hist.update_layout(bargap=0.1)
fig7_box = px.box(
    data, x='Group', y='Index',
    title='Box Plot of Index Values by Group',
    template='plotly_white',
    labels={'Index': 'Index Value', 'Group': 'Group'},
    color='Group', color_discrete_sequence=px.colors.qualitative.Plotly
)

# Visualization 8: Dynamic Time Window Analysis of Inflation
fig8 = px.line(
    data, x='Date', y='Inflation (%)',
    title='Dynamic Time Window Analysis of Inflation'
)
fig8.update_traces(line=dict(width=2), marker=dict(size=8))
fig8.update_layout(
    template='plotly_white',
    xaxis_title='Date', yaxis_title='Inflation (%)',
    xaxis=dict(
        showgrid=False,
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    hovermode='x unified'
)

# Visualization 9: Inflation by Sector with Timeline and Sector Dropdowns
agg_year = data.groupby(['Year','Sector'])['Inflation (%)'].mean().reset_index()
agg_month_year = data.groupby(['Month_Year','Sector'])['Inflation (%)'].mean().reset_index()
sectors = data['Sector'].unique()
fig9 = go.Figure()
for sec in sectors:
    df_sec = agg_year[agg_year['Sector'] == sec]
    fig9.add_trace(go.Scatter(
        x=df_sec['Year'], y=df_sec['Inflation (%)'],
        mode='lines+markers', name=sec,
        line=dict(width=2), marker=dict(size=8)
    ))
timeline_buttons = [
    dict(
        label="Year",
        method="update",
        args=[{"x": [agg_year[agg_year['Sector'] == sec]['Year'] for sec in sectors],
               "y": [agg_year[agg_year['Sector'] == sec]['Inflation (%)'] for sec in sectors]},
              {"title": "Average Inflation Rate by Year for Sectors"}]
    ),
    dict(
        label="Month_Year",
        method="update",
        args=[{"x": [agg_month_year[agg_month_year['Sector'] == sec]['Month_Year'] for sec in sectors],
               "y": [agg_month_year[agg_month_year['Sector'] == sec]['Inflation (%)'] for sec in sectors]},
              {"title": "Average Inflation Rate by Month_Year for Sectors"}]
    )
]
sector_buttons = [dict(
    label="All",
    method="update",
    args=[{"visible": [True] * len(sectors)},
          {"title": "Average Inflation Rate for All Sectors"}]
)]
for i, sec in enumerate(sectors):
    vis = [False] * len(sectors)
    vis[i] = True
    sector_buttons.append(dict(
        label=sec,
        method="update",
        args=[{"visible": vis},
              {"title": f"Average Inflation Rate for Sector: {sec}"}]
    ))
fig9.update_layout(
    template="plotly_white",
    updatemenus=[
        dict(
            buttons=timeline_buttons, direction="down",
            pad={"r": 10, "t": 10}, showactive=True,
            x=0.1, y=1.15, xanchor="left", yanchor="top", active=0
        ),
        dict(
            buttons=sector_buttons, direction="down",
            pad={"r": 10, "t": 10}, showactive=True,
            x=0.35, y=1.15, xanchor="left", yanchor="top", active=0
        )
    ]
)

# Visualization 10: Aggregated Inflation by Group and Sector
fig10 = px.bar(
    data.groupby(['Group', 'Sector'])['Inflation (%)'].mean().reset_index(),
    x='Group', y='Inflation (%)', color='Sector', barmode='group',
    title='Aggregated Inflation by Group and Sector'
)
fig10.update_traces(marker_line=dict(width=1, color='black'))
fig10.update_layout(template='plotly_white', hovermode='x unified')

# Visualization 11: Moving Standard Deviation of Inflation Rate by Sector
df_avg = data.groupby(['Month_Year', 'Sector'])['Inflation (%)'].mean().reset_index()
window = 5
df_avg['moving_std'] = df_avg.groupby('Sector')['Inflation (%)'].transform(lambda x: x.rolling(window, min_periods=1).std())
fig11 = px.line(
    df_avg, x='Month_Year', y='moving_std', color='Sector',
    markers=True, title='Moving Standard Deviation of Inflation Rate by Sector'
)
fig11.update_traces(line=dict(width=2), marker=dict(size=8))
sectors_list = df_avg['Sector'].unique()
buttons = [dict(
    label="All",
    method="update",
    args=[{"visible": [True] * len(fig11.data)},
          {"title": "Moving Standard Deviation of Inflation Rate by Sector: All"}]
)]
for sec in sectors_list:
    visibility = [trace.name == sec for trace in fig11.data]
    buttons.append(dict(
        label=str(sec),
        method="update",
        args=[{"visible": visibility},
              {"title": f"Moving Standard Deviation of Inflation Rate for Sector: {sec}"}]
    ))
fig11.update_layout(
    template='plotly_white',
    updatemenus=[dict(
        active=0, buttons=buttons, x=1.15, y=1.15,
        xanchor="right", yanchor="top"
    )]
)

# Visualization 12: Overall Inflation Volatility by Group
data_avg = data.groupby(['Month_Year', 'Group'])['Inflation (%)'].mean().reset_index()
volatility_data = data_avg.groupby('Group')['Inflation (%)'].std().reset_index()
volatility_data.rename(columns={'Inflation (%)': 'Overall Volatility'}, inplace=True)
fig12 = px.bar(
    volatility_data, x='Group', y='Overall Volatility', color='Group',
    title='Overall Inflation Volatility by Group',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig12.update_traces(marker_line=dict(width=1, color='black'))
fig12.update_layout(template='plotly_white', hovermode='x unified')

# -------------------------------
# Build the Dash App Layout
# -------------------------------
external_stylesheets = [dbc.themes.CERULEAN]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Create a stylish Navbar
navbar = dbc.NavbarSimple(
    brand="Inflation Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
    style={"fontFamily": "Arial, sans-serif"}
)

# Define tab items with dbc.Tabs for a cleaner look
tabs = dbc.Tabs([
    dbc.Tab(dcc.Graph(figure=fig1), label="Vis 1: Inflation by Group", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig2), label="Vis 2: Inflation by Year", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig3), label="Vis 3: Inflation by States", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig4), label="Vis 4: Inflation by Month & State", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig5), label="Vis 5: Median Inflation", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig6), label="Vis 6: Contribution Analysis", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(html.Div([
        html.H4("Histogram", style={"textAlign": "center", "marginTop": "15px", "fontFamily": "Arial, sans-serif"}),
        dcc.Graph(figure=fig7_hist),
        html.H4("Boxplot", style={"textAlign": "center", "marginTop": "15px", "fontFamily": "Arial, sans-serif"}),
        dcc.Graph(figure=fig7_box)
    ]), label="Vis 7: Distribution", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig8), label="Vis 8: Dynamic Time Analysis", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig9), label="Vis 9: Sector Analysis", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig10), label="Vis 10: Group & Sector", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig11), label="Vis 11: Moving Std Dev", tab_style={"fontFamily": "Arial, sans-serif"}),
    dbc.Tab(dcc.Graph(figure=fig12), label="Vis 12: Volatility", tab_style={"fontFamily": "Arial, sans-serif"})
], style={"marginTop": "20px"})

# Build the layout with a container
app.layout = dbc.Container([
    navbar,
    dbc.Container(tabs, fluid=True, style={"marginTop": "30px"})
], fluid=True, style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f8f9fa", "padding": "20px"})

if __name__ == '__main__':
    app.run(debug=True)
