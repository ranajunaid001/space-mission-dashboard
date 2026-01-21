"""
Space Missions Dashboard
Interactive dashboard to visualize and analyze historical space mission data from 1957 onwards.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from data_functions import (
    getMissionCountByCompany,
    getSuccessRate,
    getMissionsByDateRange,
    getTopCompaniesByMissionCount,
    getMissionStatusCount,
    getMissionsByYear,
    getMostUsedRocket,
    getAverageMissionsPerYear
)

# Page configuration
st.set_page_config(
    page_title="Space Missions Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Header styling */
    .main-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px 0;
        border-bottom: 2px solid #4a9eff;
        margin-bottom: 30px;
    }
    
    .logo-container {
        position: relative;
        width: 70px;
        height: 70px;
    }
    
    .logo-circle {
        position: absolute;
        border-radius: 50%;
        border: 3px solid;
        opacity: 0.9;
    }
    
    .circle-1 {
        width: 45px;
        height: 45px;
        top: 0;
        left: 5px;
        border-color: #4a9eff;
        background: rgba(74, 158, 255, 0.2);
    }
    
    .circle-2 {
        width: 45px;
        height: 45px;
        top: 15px;
        left: 25px;
        border-color: #ff6b6b;
        background: rgba(255, 107, 107, 0.2);
    }
    
    .circle-3 {
        width: 45px;
        height: 45px;
        top: 25px;
        left: 0;
        border-color: #4ecdc4;
        background: rgba(78, 205, 196, 0.2);
    }
    
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4a9eff, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .subtitle-text {
        color: #888;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1e1e3f 0%, #2a2a4a 100%);
        border: 1px solid #3a3a5a;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4a9eff;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #aaa;
        margin-top: 5px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(30, 30, 63, 0.5);
        border: 1px solid #3a3a5a;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Data table styling */
    .dataframe {
        font-size: 0.85rem;
    }
    
    /* Section headers */
    .section-header {
        color: #4ecdc4;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 25px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #3a3a5a;
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
    """Create the 3 overlapping circles logo."""
    return """
    <div class="logo-container">
        <div class="logo-circle circle-1"></div>
        <div class="logo-circle circle-2"></div>
        <div class="logo-circle circle-3"></div>
    </div>
    """


def main():
    # Load data
    df = load_data()
    
    # Header with logo
    st.markdown(f"""
    <div class="main-header">
        {create_logo()}
        <div>
            <h1 class="title-text">Space Missions Dashboard</h1>
            <p class="subtitle-text">Exploring {len(df):,} missions from 1957 to 2022</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("## 🎛️ Filters")
    
    # Date range filter
    st.sidebar.markdown("### 📅 Date Range")
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )
    
    # Handle single date selection
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
    
    # Company filter
    st.sidebar.markdown("### 🏢 Company")
    companies = ['All'] + sorted(df['Company'].unique().tolist())
    selected_company = st.sidebar.selectbox("Select company", companies)
    
    # Mission status filter
    st.sidebar.markdown("### 🎯 Mission Status")
    statuses = ['All'] + sorted(df['MissionStatus'].unique().tolist())
    selected_status = st.sidebar.selectbox("Select status", statuses)
    
    # Rocket status filter
    st.sidebar.markdown("### 🚀 Rocket Status")
    rocket_statuses = ['All'] + sorted(df['RocketStatus'].unique().tolist())
    selected_rocket_status = st.sidebar.selectbox("Select rocket status", rocket_statuses)
    
    # Apply filters
    filtered_df = df.copy()
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= start_date) & 
        (filtered_df['Date'].dt.date <= end_date)
    ]
    
    if selected_company != 'All':
        filtered_df = filtered_df[filtered_df['Company'] == selected_company]
    
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['MissionStatus'] == selected_status]
    
    if selected_rocket_status != 'All':
        filtered_df = filtered_df[filtered_df['RocketStatus'] == selected_rocket_status]
    
    # Summary Statistics
    st.markdown('<p class="section-header">📊 Summary Statistics</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{len(filtered_df):,}</p>
            <p class="metric-label">Total Missions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        success_count = len(filtered_df[filtered_df['MissionStatus'] == 'Success'])
        success_rate = (success_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{success_rate:.1f}%</p>
            <p class="metric-label">Success Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{filtered_df['Company'].nunique()}</p>
            <p class="metric-label">Companies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{filtered_df['Rocket'].nunique()}</p>
            <p class="metric-label">Rocket Types</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{filtered_df['Location'].nunique()}</p>
            <p class="metric-label">Launch Sites</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualizations
    st.markdown('<p class="section-header">📈 Visualizations</p>', unsafe_allow_html=True)
    
    # Row 1: Two charts side by side
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Visualization 1: Missions Over Time
        st.markdown("#### 🕐 Missions Over Time")
        st.markdown("""
        <small style="color: #888;">
        <b>Why this visualization:</b> A line chart reveals temporal trends in space exploration activity, 
        showing the Space Race peak, post-Cold War decline, and recent commercial space boom.
        </small>
        """, unsafe_allow_html=True)
        
        yearly_missions = filtered_df.groupby('Year').size().reset_index(name='Missions')
        
        fig1 = px.line(
            yearly_missions, 
            x='Year', 
            y='Missions',
            markers=True
        )
        fig1.update_traces(
            line=dict(color='#4a9eff', width=2),
            marker=dict(size=6, color='#4ecdc4')
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Year'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Number of Missions'),
            height=350,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with chart_col2:
        # Visualization 2: Mission Status Distribution
        st.markdown("#### 🎯 Mission Status Distribution")
        st.markdown("""
        <small style="color: #888;">
        <b>Why this visualization:</b> A donut chart provides an immediate visual breakdown of mission outcomes, 
        highlighting the overall reliability of space missions and identifying failure patterns.
        </small>
        """, unsafe_allow_html=True)
        
        status_counts = filtered_df['MissionStatus'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        colors = {
            'Success': '#4ecdc4',
            'Failure': '#ff6b6b',
            'Partial Failure': '#ffa94d',
            'Prelaunch Failure': '#845ef7'
        }
        
        fig2 = px.pie(
            status_counts, 
            values='Count', 
            names='Status',
            hole=0.5,
            color='Status',
            color_discrete_map=colors
        )
        fig2.update_traces(textposition='outside', textinfo='percent+label')
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            height=350,
            margin=dict(l=40, r=40, t=40, b=40),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Two more charts
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        # Visualization 3: Top Companies by Mission Count
        st.markdown("#### 🏆 Top 10 Companies by Missions")
        st.markdown("""
        <small style="color: #888;">
        <b>Why this visualization:</b> A horizontal bar chart ranks organizations by launch activity, 
        revealing which entities have dominated space exploration throughout history.
        </small>
        """, unsafe_allow_html=True)
        
        top_companies = filtered_df['Company'].value_counts().head(10).reset_index()
        top_companies.columns = ['Company', 'Missions']
        top_companies = top_companies.sort_values('Missions', ascending=True)
        
        fig3 = px.bar(
            top_companies,
            x='Missions',
            y='Company',
            orientation='h',
            color='Missions',
            color_continuous_scale=['#1a1a3e', '#4a9eff', '#4ecdc4']
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Number of Missions'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=''),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with chart_col4:
        # Visualization 4: Success Rate by Top Companies
        st.markdown("#### 📊 Success Rate by Top Companies")
        st.markdown("""
        <small style="color: #888;">
        <b>Why this visualization:</b> A bar chart comparing success rates reveals which organizations 
        have the most reliable track records, beyond just volume of launches.
        </small>
        """, unsafe_allow_html=True)
        
        # Get top 10 companies by mission count
        top_10_companies = filtered_df['Company'].value_counts().head(10).index.tolist()
        
        success_rates = []
        for company in top_10_companies:
            company_df = filtered_df[filtered_df['Company'] == company]
            total = len(company_df)
            success = len(company_df[company_df['MissionStatus'] == 'Success'])
            rate = (success / total * 100) if total > 0 else 0
            success_rates.append({'Company': company, 'Success Rate': rate, 'Total Missions': total})
        
        success_df = pd.DataFrame(success_rates).sort_values('Success Rate', ascending=True)
        
        fig4 = px.bar(
            success_df,
            x='Success Rate',
            y='Company',
            orientation='h',
            color='Success Rate',
            color_continuous_scale=['#ff6b6b', '#ffa94d', '#4ecdc4'],
            hover_data=['Total Missions']
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Success Rate (%)', range=[0, 100]),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=''),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Data Table Section
    st.markdown('<p class="section-header">📋 Mission Data Table</p>', unsafe_allow_html=True)
    
    # Table controls
    table_col1, table_col2, table_col3 = st.columns([2, 2, 2])
    
    with table_col1:
        search_term = st.text_input("🔍 Search missions", placeholder="Enter mission name...")
    
    with table_col2:
        sort_by = st.selectbox("Sort by", ['Date', 'Company', 'Mission', 'Rocket', 'MissionStatus'])
    
    with table_col3:
        sort_order = st.radio("Order", ['Descending', 'Ascending'], horizontal=True)
    
    # Apply search and sorting
    display_df = filtered_df.copy()
    
    if search_term:
        display_df = display_df[
            display_df['Mission'].str.contains(search_term, case=False, na=False) |
            display_df['Company'].str.contains(search_term, case=False, na=False) |
            display_df['Rocket'].str.contains(search_term, case=False, na=False)
        ]
    
    ascending = sort_order == 'Ascending'
    display_df = display_df.sort_values(sort_by, ascending=ascending)
    
    # Select columns to display
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
            "RocketStatus": st.column_config.TextColumn("Rocket Status", width="small"),
            "Price": st.column_config.NumberColumn("Price (M$)", width="small", format="%.2f")
        }
    )
    
    st.markdown(f"<p style='color: #888; font-size: 0.85rem;'>Showing {len(display_df_final):,} of {len(filtered_df):,} filtered missions</p>", unsafe_allow_html=True)
    
    # Footer with additional stats using the required functions
    st.markdown('<p class="section-header">🔢 Quick Stats (Using Required Functions)</p>', unsafe_allow_html=True)
    
    func_col1, func_col2, func_col3 = st.columns(3)
    
    with func_col1:
        st.markdown("**Most Used Rocket:**")
        st.code(getMostUsedRocket())
        
        st.markdown("**Status Counts:**")
        status_dict = getMissionStatusCount()
        for status, count in status_dict.items():
            st.markdown(f"- {status}: {count:,}")
    
    with func_col2:
        st.markdown("**Top 5 Companies:**")
        top5 = getTopCompaniesByMissionCount(5)
        for company, count in top5:
            st.markdown(f"- {company}: {count:,}")
    
    with func_col3:
        st.markdown("**Missions by Decade:**")
        for decade_start in range(1960, 2030, 10):
            avg = getAverageMissionsPerYear(decade_start, decade_start + 9)
            st.markdown(f"- {decade_start}s: {avg:.1f} avg/year")


if __name__ == "__main__":
    main()
