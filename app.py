"""
Space Missions Dashboard
A minimalist, Jony Ive-inspired interface for exploring space mission data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from data_functions import (
    GetMissionCountByCompany,
    GetSuccessRate,
    GetMissionsByDateRange,
    GetTopCompaniesByMissionCount,
    GetMissionStatusCount,
    GetMissionsByYear,
    GetMostUsedRocket,
    GetAverageMissionsPerYear
)

# Page configuration
st.set_page_config(
    page_title="Space Missions",
    page_icon="○",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist CSS - Light theme with colors
st.markdown("""
<style>
    /* Import clean font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Force light theme on everything */
    .stApp {
        background-color: #fafafa !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header area - force light */
    header[data-testid="stHeader"] {
        background-color: #fafafa !important;
    }
    
    /* Sidebar - light theme */
    [data-testid="stSidebar"] {
        background-color: #f5f5f7 !important;
        border-right: 1px solid #e5e5e5;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #f5f5f7 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1d1d1f !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #1d1d1f !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #1d1d1f !important;
    }
    
    /* Sidebar select boxes */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d1d6 !important;
        color: #1d1d1f !important;
    }
    
    [data-testid="stSidebar"] .stDateInput > div > div > input {
        background-color: #ffffff !important;
        border: 1px solid #d1d1d6 !important;
        color: #1d1d1f !important;
    }
    
    /* Main content text */
    .stMarkdown, .stText, p, span, label {
        color: #1d1d1f !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1d1d1f !important;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Metric styling - ultra minimal */
    .metric-container {
        text-align: center;
        padding: 30px 20px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1d1d1f !important;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #86868b !important;
        margin-top: 8px;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Section headers */
    .section-header {
        color: #1d1d1f !important;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 50px 0 25px 0;
        letter-spacing: -0.3px;
    }
    
    /* Filter labels */
    .filter-label {
        font-size: 0.75rem;
        color: #86868b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    /* Clean divider */
    .divider {
        height: 1px;
        background: #e5e5e5;
        margin: 40px 0;
    }
    
    /* Stats footer */
    .stats-label {
        font-size: 0.75rem;
        color: #86868b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .stats-value {
        font-size: 1rem;
        color: #1d1d1f !important;
        font-weight: 400;
    }
    
    /* Hide Streamlit branding and header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Data table - light theme */
    .stDataFrame {
        background-color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
    }
    
    /* Search input */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #d1d1d6 !important;
        color: #1d1d1f !important;
    }
    
    /* Select boxes in main area */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d1d6 !important;
        color: #1d1d1f !important;
    }
    
    /* Captions */
    .stCaption {
        color: #86868b !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache the space missions data."""
    df = pd.read_csv('space_missions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df


def create_logo():
    """Create 3 overlapping circles logo with vibrant colors."""
    return """
    <svg width="50" height="50" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="35" cy="38" r="24" fill="rgba(74, 158, 255, 0.5)" stroke="#4a9eff" stroke-width="2.5"/>
        <circle cx="65" cy="38" r="24" fill="rgba(255, 107, 107, 0.5)" stroke="#ff6b6b" stroke-width="2.5"/>
        <circle cx="50" cy="62" r="24" fill="rgba(78, 205, 196, 0.5)" stroke="#4ecdc4" stroke-width="2.5"/>
    </svg>
    """


# Minimal layout with vibrant colors
COLORS = {
    'primary': '#1d1d1f',
    'secondary': '#86868b',
    'accent': '#4a9eff',
    'success': '#4ecdc4',
    'failure': '#ff6b6b',
    'warning': '#ffa94d',
    'purple': '#845ef7',
    'background': '#fafafa',
    'card': '#ffffff',
    'border': '#e5e5e5'
}


def main():
    # Load data
    df = load_data()
    
    # Header with logo
    col_logo, col_title = st.columns([0.5, 5])
    
    with col_logo:
        st.markdown(create_logo(), unsafe_allow_html=True)
    
    with col_title:
        st.title("Space Missions")
        st.caption(f"{len(df):,} missions from 1957–2022")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Sidebar filters - minimal
    st.sidebar.markdown("<p class='filter-label'>Filters</p>", unsafe_allow_html=True)
    
    # Reset button with subtle styling
    st.sidebar.markdown("""
        <style>
        div[data-testid="stSidebar"] button[kind="secondary"] {
            background-color: #f0f0f0 !important;
            color: #666666 !important;
            border: 1px solid #e0e0e0 !important;
            font-weight: 400 !important;
        }
        div[data-testid="stSidebar"] button[kind="secondary"]:hover {
            background-color: #e5e5e5 !important;
            border: 1px solid #d0d0d0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("Reset", use_container_width=True):
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Date range
    st.sidebar.markdown("<p class='filter-label'>Date Range</p>", unsafe_allow_html=True)
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    # Handle incomplete date selection
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        # If only one date selected, use full range to avoid errors
        start_date = min_date
        end_date = max_date
        st.sidebar.caption("⚠️ Select both dates for range filter")
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Company filter
    st.sidebar.markdown("<p class='filter-label'>Company</p>", unsafe_allow_html=True)
    companies = ['All Companies'] + sorted(df['Company'].unique().tolist())
    selected_company = st.sidebar.selectbox("Company", companies, label_visibility="collapsed")
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Mission status filter
    st.sidebar.markdown("<p class='filter-label'>Mission Status</p>", unsafe_allow_html=True)
    statuses = ['All Statuses'] + sorted(df['MissionStatus'].unique().tolist())
    selected_status = st.sidebar.selectbox("Status", statuses, label_visibility="collapsed")
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Rocket status filter
    st.sidebar.markdown("<p class='filter-label'>Rocket Status</p>", unsafe_allow_html=True)
    rocket_statuses = ['All'] + sorted(df['RocketStatus'].unique().tolist())
    selected_rocket_status = st.sidebar.selectbox("Rocket Status", rocket_statuses, label_visibility="collapsed")
    
    # Apply filters
    filtered_df = df.copy()
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= start_date) & 
        (filtered_df['Date'].dt.date <= end_date)
    ]
    
    if selected_company != 'All Companies':
        filtered_df = filtered_df[filtered_df['Company'] == selected_company]
    
    if selected_status != 'All Statuses':
        filtered_df = filtered_df[filtered_df['MissionStatus'] == selected_status]
    
    if selected_rocket_status != 'All':
        filtered_df = filtered_df[filtered_df['RocketStatus'] == selected_rocket_status]
    
    # Summary Statistics - minimal cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    success_count = len(filtered_df[filtered_df['MissionStatus'] == 'Success'])
    success_rate = (success_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{len(filtered_df):,}</p>
            <p class="metric-label">Missions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{success_rate:.1f}%</p>
            <p class="metric-label">Success Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{filtered_df['Company'].nunique()}</p>
            <p class="metric-label">Companies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{filtered_df['Rocket'].nunique()}</p>
            <p class="metric-label">Rockets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{filtered_df['Location'].nunique()}</p>
            <p class="metric-label">Launch Sites</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Visualizations - clean and minimal
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Visualization 1: Missions Over Time
        st.markdown("<p class='section-header'>Missions Over Time</p>", unsafe_allow_html=True)
        st.caption("Annual launch frequency showing historical trends in space exploration activity.")
        
        yearly_missions = filtered_df.groupby('Year').size().reset_index(name='Missions')
        
        fig1 = px.area(
            yearly_missions, 
            x='Year', 
            y='Missions'
        )
        fig1.update_traces(
            line=dict(color=COLORS['accent'], width=2),
            fillcolor='rgba(74, 158, 255, 0.15)'
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1d1d1f', size=12),
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.08)', 
                title='Year',
                titlefont=dict(color='#1d1d1f', size=12),
                tickfont=dict(color='#1d1d1f', size=11),
                linecolor=COLORS['border']
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.08)', 
                title='Missions',
                titlefont=dict(color='#1d1d1f', size=12),
                tickfont=dict(color='#1d1d1f', size=11),
                linecolor=COLORS['border']
            ),
            height=320,
            margin=dict(l=20, r=20, t=20, b=40),
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with chart_col2:
        # Visualization 2: Mission Status Distribution
        st.markdown("<p class='section-header'>Mission Outcomes</p>", unsafe_allow_html=True)
        st.caption("Distribution of mission results across all launches.")
        
        status_counts = filtered_df['MissionStatus'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # Vibrant colors for status
        status_colors = {
            'Success': '#4ecdc4',
            'Failure': '#ff6b6b',
            'Partial Failure': '#ffa94d',
            'Prelaunch Failure': '#845ef7'
        }
        
        fig2 = px.pie(
            status_counts, 
            values='Count', 
            names='Status',
            hole=0.6,
            color='Status',
            color_discrete_map=status_colors
        )
        fig2.update_traces(
            textposition='inside', 
            textinfo='percent',
            textfont=dict(size=12, color='#ffffff'),
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1d1d1f', size=12),
            height=350,
            margin=dict(l=20, r=20, t=20, b=60),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color='#1d1d1f')
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: More visualizations
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        # Visualization 3: Top Companies
        st.markdown("<p class='section-header'>Leading Organizations</p>", unsafe_allow_html=True)
        st.caption("Top 10 companies by total number of launches.")
        
        top_companies = filtered_df['Company'].value_counts().head(10).reset_index()
        top_companies.columns = ['Company', 'Missions']
        top_companies = top_companies.sort_values('Missions', ascending=True)
        
        fig3 = px.bar(
            top_companies,
            x='Missions',
            y='Company',
            orientation='h',
            color='Missions',
            color_continuous_scale=['#4a9eff', '#4ecdc4']
        )
        fig3.update_layout(coloraxis_showscale=False)
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1d1d1f', size=12),
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.08)', 
                title='Number of Missions',
                titlefont=dict(color='#1d1d1f', size=12),
                tickfont=dict(color='#1d1d1f', size=11),
                linecolor=COLORS['border']
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0)', 
                title='',
                tickfont=dict(color='#1d1d1f', size=11),
                linecolor='rgba(0,0,0,0)'
            ),
            height=350,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with chart_col4:
        # Visualization 4: Success Rate by Company
        st.markdown("<p class='section-header'>Success Rate by Company</p>", unsafe_allow_html=True)
        st.caption("Reliability comparison of top 10 launch providers.")
        
        top_10_companies = filtered_df['Company'].value_counts().head(10).index.tolist()
        
        if len(top_10_companies) > 0:
            success_rates = []
            for company in top_10_companies:
                company_df = filtered_df[filtered_df['Company'] == company]
                total = len(company_df)
                success = len(company_df[company_df['MissionStatus'] == 'Success'])
                rate = (success / total * 100) if total > 0 else 0
                success_rates.append({'Company': company, 'Success Rate': rate})
            
            success_df = pd.DataFrame(success_rates).sort_values('Success Rate', ascending=True)
            
            fig4 = px.bar(
                success_df,
                x='Success Rate',
                y='Company',
                orientation='h',
                color='Success Rate',
                color_continuous_scale=['#ff6b6b', '#ffa94d', '#4ecdc4']
            )
            fig4.update_layout(coloraxis_showscale=False)
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1d1d1f', size=12),
                xaxis=dict(
                    gridcolor='rgba(0,0,0,0.08)', 
                    title='Success Rate (%)',
                    titlefont=dict(color='#1d1d1f', size=12),
                    tickfont=dict(color='#1d1d1f', size=11),
                    range=[0, 100],
                    linecolor=COLORS['border']
                ),
                yaxis=dict(
                    gridcolor='rgba(0,0,0,0)', 
                    title='',
                    tickfont=dict(color='#1d1d1f', size=11),
                    linecolor='rgba(0,0,0,0)'
                ),
                height=350,
                margin=dict(l=20, r=20, t=20, b=40)
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Data Table - minimal
    st.markdown("<p class='section-header'>Mission Data</p>", unsafe_allow_html=True)
    
    # Simple search and sort
    col_search, col_sort, col_order = st.columns([3, 2, 2])
    
    with col_search:
        search_term = st.text_input("Search", placeholder="Search missions...", label_visibility="collapsed")
    
    with col_sort:
        sort_by = st.selectbox("Sort", ['Date', 'Company', 'Mission', 'Rocket', 'MissionStatus'], label_visibility="collapsed")
    
    with col_order:
        sort_order = st.selectbox("Order", ['Newest First', 'Oldest First'], label_visibility="collapsed")
    
    # Apply search and sorting
    display_df = filtered_df.copy()
    
    if search_term:
        display_df = display_df[
            display_df['Mission'].str.contains(search_term, case=False, na=False) |
            display_df['Company'].str.contains(search_term, case=False, na=False) |
            display_df['Rocket'].str.contains(search_term, case=False, na=False)
        ]
    
    ascending = sort_order == 'Oldest First'
    display_df = display_df.sort_values(sort_by, ascending=ascending)
    
    # Select columns
    display_columns = ['Date', 'Company', 'Mission', 'Rocket', 'Location', 'MissionStatus', 'RocketStatus', 'Price']
    display_df_final = display_df[display_columns].copy()
    display_df_final['Date'] = display_df_final['Date'].dt.strftime('%Y-%m-%d')
    
    # Display table
    st.dataframe(
        display_df_final,
        use_container_width=True,
        height=400,
        column_config={
            "Date": st.column_config.TextColumn("Date", width="small"),
            "Company": st.column_config.TextColumn("Company", width="medium"),
            "Mission": st.column_config.TextColumn("Mission", width="medium"),
            "Rocket": st.column_config.TextColumn("Rocket", width="medium"),
            "Location": st.column_config.TextColumn("Location", width="large"),
            "MissionStatus": st.column_config.TextColumn("Status", width="small"),
            "RocketStatus": st.column_config.TextColumn("Rocket", width="small"),
            "Price": st.column_config.NumberColumn("Price ($M)", width="small", format="%.1f")
        }
    )
    
    st.caption(f"Showing {len(display_df_final):,} of {len(filtered_df):,} missions")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Quick Stats footer - minimal
    st.markdown("<p class='section-header'>Quick Reference</p>", unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown("<p class='stats-label'>Most Used Rocket</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='stats-value'>{GetMostUsedRocket()}</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='stats-label'>Mission Outcomes</p>", unsafe_allow_html=True)
        status_dict = GetMissionStatusCount()
        for status, count in status_dict.items():
            st.markdown(f"<p class='stats-value'>{status}: {count:,}</p>", unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("<p class='stats-label'>Top 5 Organizations</p>", unsafe_allow_html=True)
        top5 = GetTopCompaniesByMissionCount(5)
        for company, count in top5:
            st.markdown(f"<p class='stats-value'>{company}: {count:,}</p>", unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("<p class='stats-label'>Average Missions per Year</p>", unsafe_allow_html=True)
        for decade_start in range(1960, 2030, 10):
            avg = GetAverageMissionsPerYear(decade_start, decade_start + 9)
            st.markdown(f"<p class='stats-value'>{decade_start}s: {avg:.1f}</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
