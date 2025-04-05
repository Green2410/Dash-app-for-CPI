import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------
# Set page configuration
# -----------------------------------------------------------
st.set_page_config(
    page_title="Inflation Dashboard",
    layout="wide"
)

# -----------------------------------------------------------
# Caching: Load Data Only Once
# -----------------------------------------------------------
@st.cache_data
def load_data(csv_path):
    data = pd.read_csv(csv_path)
    
    # Convert necessary columns to numeric
    columns = ['Index', 'Inflation (%)']
    for column in columns:
        if data[column].dtype == 'O':
            data[column] = pd.to_numeric(data[column], errors='coerce')
    
    # Create datetime columns
    data['Date'] = pd.to_datetime(
        data['Year'].astype(str) + '-' + data['Month'],
        format='%Y-%B',
        errors='coerce'
    )
    data['Month_Year'] = data['Date'].dt.strftime('%b %y')
    
    # Sort by date and drop NaNs
    data = data.sort_values('Date').dropna(subset=['Date'])
    
    # Convert Month_Year to datetime (for some visuals)
    data['Month_Year'] = pd.to_datetime(data['Month_Year'], format='%b %y', errors='coerce')
    
    data = data.dropna()
    
    return data

# -----------------------------------------------------------
# Define a dark theme layout for Plotly figures
# -----------------------------------------------------------
dark_layout = dict(
    template='plotly_dark',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title_font=dict(size=18, family='Arial', color='white'),
    xaxis=dict(
        showgrid=True,
        gridcolor='grey',
        showline=True,
        linewidth=1,
        linecolor='white',
        tickfont=dict(size=12, color='white'),
        title_font=dict(size=14, color='white'),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='grey',
        showline=True,
        linewidth=1,
        linecolor='white',
        tickfont=dict(size=12, color='white'),
        title_font=dict(size=14, color='white'),
    ),
    hovermode='x unified',
    legend=dict(font=dict(color='white'))
)

# -----------------------------------------------------------
# Caching: Create each visualization on demand
# -----------------------------------------------------------

@st.cache_data
def get_vis1(data):
    df = pd.DataFrame(data.groupby(['Year', 'Group'])['Inflation (%)'].mean().reset_index())
    fig = px.line(
        df,
        x='Year',
        y='Inflation (%)',
        color='Group',
        markers=True,
        title='Average Inflation Rate by Group'
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(dark_layout)
    groups = df['Group'].unique()
    buttons = []
    buttons.append(dict(
        label="All",
        method="update",
        args=[{"visible": [True]*len(fig.data)},
              {"title": "Average Inflation Rate for All Groups"}]
    ))
    for grp in groups:
        visible = [trace.name == grp for trace in fig.data]
        buttons.append(dict(
            label=str(grp),
            method="update",
            args=[{"visible": visible},
                  {"title": f"Average Inflation Rate for Group: {grp}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.35,
            y=1.10,
            xanchor='right',
            yanchor='top'
        )]
    )
    return fig

@st.cache_data
def get_vis2(data):
    df = pd.DataFrame(data.groupby(['Year', 'Group'])['Inflation (%)'].mean().reset_index())
    fig = px.line(
        df,
        x='Group',
        y='Inflation (%)',
        color='Year',
        markers=True,
        title='Average Inflation Rate by Years'
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(dark_layout)
    years = df['Year'].unique()
    buttons = []
    buttons.append(dict(
        label="All",
        method="update",
        args=[{"visible": [True] * len(fig.data)},
              {"title": "Average Inflation Rate by Group for All Years"}]
    ))
    for yr in years:
        visible = [trace.name == str(yr) for trace in fig.data]
        buttons.append(dict(
            label=str(yr),
            method="update",
            args=[{"visible": visible},
                  {"title": f"Average Inflation Rate by Group for Year: {yr}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.35,
            y=1.10,
            xanchor='right',
            yanchor='top'
        )]
    )
    return fig

@st.cache_data
def get_vis3(data):
    df = pd.DataFrame(data.groupby(['Month_Year', 'State'])['Inflation (%)'].mean().reset_index())
    fig = px.line(
        df,
        x='Month_Year',
        y='Inflation (%)',
        color='State',
        markers=True,
        title='Average Inflation Rate by States'
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(dark_layout)
    states = df['State'].unique()
    buttons = []
    buttons.append(dict(
        label="All",
        method="update",
        args=[{"visible": [True] * len(fig.data)},
              {"title": "Average Inflation Rate for all States"}]
    ))
    for st_ in states:
        visible = [trace.name == str(st_) for trace in fig.data]
        buttons.append(dict(
            label=str(st_),
            method="update",
            args=[{"visible": visible},
                  {"title": f"Average Inflation Rate for State: {st_}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.35,
            y=1.10,
            xanchor='right',
            yanchor='top'
        )]
    )
    return fig

@st.cache_data
def get_vis4(data):
    df = pd.DataFrame(data.groupby(['Month_Year', 'State'])['Inflation (%)'].mean().reset_index())
    fig = px.line(
        df,
        x='State',
        y='Inflation (%)',
        color='Month_Year',
        markers=True,
        title='Average Inflation Rate for Months and Year'
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(dark_layout)
    month_years = df['Month_Year'].unique()
    buttons = []
    buttons.append(dict(
        label="All",
        method="update",
        args=[{"visible": [True] * len(fig.data)},
              {"title": "Average Inflation Rate for all months and Years"}]
    ))
    for mn_yr in month_years:
        visible = [trace.name == str(mn_yr) for trace in fig.data]
        buttons.append(dict(
            label=str(mn_yr),
            method="update",
            args=[{"visible": visible},
                  {"title": f"Average Inflation Rate for month and Year: {mn_yr}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.35,
            y=1.10,
            xanchor='right',
            yanchor='top'
        )]
    )
    return fig

@st.cache_data
def get_vis5(data):
    months_list = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    traces = []
    for month in months_list:
        month_data = data[data['Month'] == month]
        if not month_data.empty:
            group_data = month_data.groupby('Year')['Inflation (%)'].median().reset_index()
            trace = go.Bar(
                x=group_data['Year'],
                y=group_data['Inflation (%)'],
                name=month,
                marker=dict(
                    color='rgb(150, 95, 100)',
                    line=dict(width=1, color='white')
                ),
                visible=False
            )
        else:
            trace = go.Bar(
                x=[],
                y=[],
                name=month,
                visible=False
            )
        traces.append(trace)
    if traces:
        traces[0]['visible'] = True
    buttons = []
    for i, month in enumerate(months_list):
        visibility = [False] * len(months_list)
        visibility[i] = True
        buttons.append(dict(
            label=month,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Average Inflation in {month} Across Years"}]
        ))
    layout = go.Layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=0.05,
            y=1.15,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        )],
        title=dict(
            text=f"Average Inflation in {months_list[0]} Across Years",
            font=dict(size=18, family='Arial', color='white'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Year",
            tickmode='linear',
            dtick=1,
            title_font=dict(size=14, color='white'),
            tickfont=dict(size=12, color='white'),
            showgrid=True,
            gridcolor='grey',
            showline=True,
            linewidth=1,
            linecolor='white',
        ),
        yaxis=dict(
            title="Average Inflation (%)",
            title_font=dict(size=14, color='white'),
            tickfont=dict(size=12, color='white'),
            showgrid=True,
            gridcolor='grey',
            showline=True,
            linewidth=1,
            linecolor='white',
        ),
        margin=dict(l=80, r=40, t=100, b=80),
        hovermode='x unified',
        legend=dict(
            font=dict(size=12, color='white'),
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.15
        )
    )
    fig = go.Figure(data=traces, layout=layout)
    return fig

@st.cache_data
def get_vis6(data):
    # Prepare data for Contribution Analysis
    df = data.copy()
    df['Month_Year_str'] = df['Month_Year'].dt.strftime('%b %y')
    unique_months = sorted(
        df['Month_Year_str'].unique(),
        key=lambda x: pd.to_datetime(x, format='%b %y')
    )
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'domain'}, {'type': 'xy'}]],
        subplot_titles=("Contribution Pie Chart", "Contribution Stacked Bar Chart"),
        horizontal_spacing=0.30
    )
    trace_indices = []
    all_traces = []
    for month in unique_months:
        snapshot = df[df['Month_Year_str'] == month]
        group_contrib = snapshot.groupby('Group')['Inflation (%)'].median().reset_index()
        pie = go.Pie(
            labels=group_contrib['Group'],
            values=group_contrib['Inflation (%)'],
            textinfo='percent+label',
            name=month
        )
        curr_idx = []
        fig.add_trace(pie, row=1, col=1)
        curr_idx.append(len(all_traces))
        all_traces.append(pie)
        group_contrib['dummy'] = 'Inflation Contribution'
        temp = px.bar(
            group_contrib,
            x='dummy',
            y='Inflation (%)',
            color='Group',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        for trace in temp.data:
            fig.add_trace(trace, row=1, col=2)
            curr_idx.append(len(all_traces))
            all_traces.append(trace)
        trace_indices.append(curr_idx)
    fig.update_layout(barmode='stack')
    total = len(all_traces)
    buttons = []
    for i, month in enumerate(unique_months):
        vis = [False] * total
        for idx in trace_indices[i]:
            vis[idx] = True
        buttons.append(dict(
            label=month,
            method="update",
            args=[{"visible": vis},
                  {"title": f"Contribution Analysis for {month}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=0.5,
            y=1.2,
            xanchor='center',
            yanchor='top'
        )],
        title=f"Contribution Analysis for {unique_months[0]}" if unique_months else "Contribution Analysis",
        **dark_layout,
        xaxis_title="",
        yaxis_title="Average Inflation (%)",
        legend_title="Group"
    )
    return fig

@st.cache_data
def get_vis7_hist(data):
    fig = px.histogram(
        data,
        x='Index',
        color='Group',
        facet_col='Group',
        facet_col_wrap=3,
        template='plotly_dark',
        title='Distribution of Index Values by Group',
        labels={'Index': 'Index Value'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(bargap=0.1)
    return fig

@st.cache_data
def get_vis7_box(data):
    fig = px.box(
        data,
        x='Group',
        y='Index',
        title='Box Plot of Index Values by Group',
        template='plotly_dark',
        labels={'Index': 'Index Value', 'Group': 'Group'},
        color='Group',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    return fig

@st.cache_data
def get_vis8(data):
    fig = px.line(
        data,
        x='Date',
        y='Inflation (%)',
        title='Dynamic Time Window Analysis of Inflation'
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(dark_layout)
    fig.update_layout(dict(
        xaxis=dict(
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
        )
    ))
    return fig

@st.cache_data
def get_vis9(data):
    agg_year = data.groupby(['Year', 'Sector'])['Inflation (%)'].mean().reset_index()
    agg_month_year = data.groupby(['Month_Year', 'Sector'])['Inflation (%)'].mean().reset_index()
    sectors = data['Sector'].dropna().unique()
    fig = go.Figure()
    for sec in sectors:
        df_sec = agg_year[agg_year['Sector'] == sec]
        fig.add_trace(go.Scatter(
            x=df_sec['Year'],
            y=df_sec['Inflation (%)'],
            mode='lines+markers',
            name=sec,
            line=dict(width=2),
            marker=dict(size=8)
        ))
    timeline_buttons = [
        dict(
            label="Year",
            method="update",
            args=[
                {"x": [agg_year[agg_year['Sector'] == sec]['Year'] for sec in sectors],
                 "y": [agg_year[agg_year['Sector'] == sec]['Inflation (%)'] for sec in sectors]},
                {"title": "Average Inflation Rate by Year for Sectors"}
            ]
        ),
        dict(
            label="Month_Year",
            method="update",
            args=[
                {"x": [agg_month_year[agg_month_year['Sector'] == sec]['Month_Year'] for sec in sectors],
                 "y": [agg_month_year[agg_month_year['Sector'] == sec]['Inflation (%)'] for sec in sectors]},
                {"title": "Average Inflation Rate by Month_Year for Sectors"}
            ]
        )
    ]
    sector_buttons = [
        dict(
            label="All",
            method="update",
            args=[{"visible": [True]*len(sectors)},
                  {"title": "Average Inflation Rate for All Sectors"}]
        )
    ]
    for i, sec in enumerate(sectors):
        vis = [False]*len(sectors)
        vis[i] = True
        sector_buttons.append(dict(
            label=sec,
            method="update",
            args=[{"visible": vis},
                  {"title": f"Average Inflation Rate for Sector: {sec}"}]
        ))
    fig.update_layout(
        dark_layout,
        updatemenus=[
            dict(
                buttons=timeline_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top",
                active=0,
                name="Timeline"
            ),
            dict(
                buttons=sector_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.35,
                xanchor="left",
                y=1.15,
                yanchor="top",
                active=0,
                name="Sector"
            )
        ]
    )
    return fig

@st.cache_data
def get_vis10(data):
    df = data.groupby(['Group', 'Sector'])['Inflation (%)'].mean().reset_index()
    fig = px.bar(
        df,
        x='Group',
        y='Inflation (%)',
        color='Sector',
        barmode='group',
        title='Aggregated Inflation by Group and Sector'
    )
    fig.update_traces(marker_line=dict(width=1, color='white'))
    fig.update_layout(dark_layout)
    return fig

@st.cache_data
def get_vis11(data):
    df = data.groupby(['Month_Year', 'Sector'])['Inflation (%)'].mean().reset_index()
    window = 5
    df['moving_std'] = df.groupby('Sector')['Inflation (%)'].transform(lambda x: x.rolling(window, min_periods=1).std())
    fig = px.line(
        df,
        x='Month_Year',
        y='moving_std',
        color='Sector',
        markers=True,
        title='Moving Standard Deviation of Inflation Rate by Sector'
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(dark_layout)
    sectors = df['Sector'].unique()
    buttons = []
    buttons.append(dict(
        label="All",
        method="update",
        args=[{"visible": [True] * len(fig.data)},
              {"title": "Moving Standard Deviation of Inflation Rate by Sector: All"}]
    ))
    for sec in sectors:
        visibility = [trace.name == sec for trace in fig.data]
        buttons.append(dict(
            label=str(sec),
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Moving Standard Deviation of Inflation Rate for Sector: {sec}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.15,
            y=1.15,
            xanchor="right",
            yanchor="top",
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        )]
    )
    return fig

@st.cache_data
def get_vis12(data):
    df = data.groupby(['Month_Year', 'Group'])['Inflation (%)'].mean().reset_index()
    vol = df.groupby('Group')['Inflation (%)'].std().reset_index()
    vol.rename(columns={'Inflation (%)': 'Overall Volatility'}, inplace=True)
    fig = px.bar(
        vol,
        x='Group',
        y='Overall Volatility',
        color='Group',
        title='Overall Inflation Volatility by Group',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_traces(marker_line=dict(width=1, color='white'))
    fig.update_layout(dark_layout)
    return fig

# -----------------------------------------------------------
# Main Streamlit App with Lazy Loading (Tabs)
# -----------------------------------------------------------
def main():
    st.title("Inflation Dashboard")

    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")
    
    if uploaded_file is not None:
        data = load_data(uploaded_file)

    # Create tabs for each visualization; figures are created only when needed
        tabs = st.tabs([
            "Vis 1: Inflation by Group (Year)",
            "Vis 2: Inflation by Years (Group)",
            "Vis 3: Inflation by States (Month_Year)",
            "Vis 4: Inflation by State (Month_Year as Color)",
            "Vis 5: Median Inflation by Month",
            "Vis 6: Contribution Analysis",
            "Vis 7A: Distribution (Histogram)",
            "Vis 7B: Distribution (Boxplot)",
            "Vis 8: Dynamic Time Window",
            "Vis 9: Inflation Rate by Sectors (Year vs. Month_Year)",
            "Vis 10: Aggregated Inflation by Group & Sector",
            "Vis 11: Moving Std Dev by Sector",
            "Vis 12: Overall Volatility by Group"
        ])

        with tabs[0]:
            st.plotly_chart(get_vis1(data), use_container_width=True)
        with tabs[1]:
            st.plotly_chart(get_vis2(data), use_container_width=True)
        with tabs[2]:
            st.plotly_chart(get_vis3(data), use_container_width=True)
        with tabs[3]:
            st.plotly_chart(get_vis4(data), use_container_width=True)
        with tabs[4]:
            st.plotly_chart(get_vis5(data), use_container_width=True)
        with tabs[5]:
            st.plotly_chart(get_vis6(data), use_container_width=True)
        with tabs[6]:
            st.plotly_chart(get_vis7_hist(data), use_container_width=True)
        with tabs[7]:
            st.plotly_chart(get_vis7_box(data), use_container_width=True)
        with tabs[8]:
            st.plotly_chart(get_vis8(data), use_container_width=True)
        with tabs[9]:
            st.plotly_chart(get_vis9(data), use_container_width=True)
        with tabs[10]:
            st.plotly_chart(get_vis10(data), use_container_width=True)
        with tabs[11]:
            st.plotly_chart(get_vis11(data), use_container_width=True)
        with tabs[12]:
            st.plotly_chart(get_vis12(data), use_container_width=True)
    
    else:
        st.sidebar.info("Please upload your CSV file.")

if __name__ == "__main__":
    main()
