import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# 1. Page Configuration
st.set_page_config(
    page_title="Kenya Green Horizon Storyboard",
    page_icon="🍃",
    layout="wide"
)

# 2. Inject Custom Fonts (Lato) and Global Old-School Styles
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght=0,300;0,400;0,700;1,400&display=swap');
        
        html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
            font-family: 'Lato', sans-serif !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] {
            font-weight: 400 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85rem !important;
        }
        /* Structured Old School Callout Boxes */
        .translator-note {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #10b981;
            padding: 15px;
            margin-bottom: 15px;
        }
        .forecast-note {
            background-color: #fdf2f8;
            border: 1px solid #fbcfe8;
            border-left: 4px solid #db2777;
            padding: 15px;
            margin-bottom: 15px;
            color: #831843;
        }
    </style>
""", unsafe_allow_html=True)

# Reusable Function to enforce rigid, high-contrast grid lines
def apply_old_school_layout(fig, title, x_title, y_title):
    fig.update_layout(
        font_family="Lato",
        title=dict(text=title, font=dict(size=16, weight="bold")),
        xaxis=dict(
            title=x_title,
            showgrid=True,
            gridwidth=1,
            gridcolor='#e2e8f0',
            showline=True,
            linewidth=1.5,
            linecolor='#64748b',
            mirror=True
        ),
        yaxis=dict(
            title=y_title,
            showgrid=True,
            gridwidth=1,
            gridcolor='#e2e8f0',
            showline=True,
            linewidth=1.5,
            linecolor='#64748b',
            mirror=True
        ),
        margin=dict(l=50, r=30, t=50, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            bordercolor='#cbd5e1',
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified"
    )

# 3. Data Loading Engine
@st.cache_data
def load_data():
    df = pd.read_csv("API_KEN_DS2_en_csv_v2_5938.csv", skiprows=4)
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all', axis=1)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load file. Verify 'API_KEN_DS2_en_csv_v2_5938.csv' is present. Error: {e}")
    st.stop()

# Helper to Extract Timelines
def get_indicator_timeline(indicator_name):
    row = df[df['Indicator Name'] == indicator_name]
    if row.empty:
        return pd.Series(dtype=float)
    year_cols = [col for col in df.columns if col.isdigit()]
    timeline = row[year_cols].T
    timeline.columns = ['Value']
    timeline.index = timeline.index.astype(int)
    timeline['Value'] = pd.to_numeric(timeline['Value'], errors='coerce')
    return timeline.dropna()

def get_latest_val_and_year(timeline_df, start, end):
    filtered = timeline_df[(timeline_df.index >= start) & (timeline_df.index <= end)]
    if not filtered.empty:
        idx = filtered.index[-1]
        return filtered.loc[idx, 'Value'], idx
    return None, None

# Forecast Engine
def forecast_next_5_years(timeline_df):
    if timeline_df.empty or len(timeline_df) < 5:
        return pd.DataFrame()
    recent_data = timeline_df.tail(15)
    X = recent_data.index.values.reshape(-1, 1)
    y = recent_data['Value'].values
    model = LinearRegression()
    model.fit(X, y)
    last_actual_year = timeline_df.index[-1]
    future_years = np.array(range(last_actual_year + 1, last_actual_year + 6)).reshape(-1, 1)
    predictions = model.predict(future_years)
    return pd.DataFrame({'Projected Value': predictions}, index=future_years.flatten())

# 4. Sidebar Controls
year_columns = [int(col) for col in df.columns if col.isdigit()]
min_year, max_year = min(year_columns), max(year_columns)

st.sidebar.header("Green Navigation")
page = st.sidebar.radio(
    "Go To:", 
    [
        "1. Environmental Vital Signs", 
        "2. The Power Grid Mix", 
        "3. Carbon Emissions & Forests",
        "4. Future Green Horizons"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Timeline Window")
selected_years = st.sidebar.slider(
    "Select Target Window",
    min_value=min_year,
    max_value=max_year,
    value=(1995, max_year)
)
start_yr, end_yr = selected_years

# Extract Target Green Indicators
forest_df = get_indicator_timeline("Forest area (% of land area)")
hydro_df = get_indicator_timeline("Electricity production from hydroelectric sources (% of total)")
oil_df = get_indicator_timeline("Electricity production from oil sources (% of total)")
co2_agri = get_indicator_timeline("Carbon dioxide (CO2) emissions from Agriculture (Mt CO2e)")
co2_build = get_indicator_timeline("Carbon dioxide (CO2) emissions from Building (Energy) (Mt CO2e)")
co2_defor = get_indicator_timeline("Carbon dioxide (CO2) net fluxes from LULUCF - Deforestation (Mt CO2e)")

# ==========================================
# PAGE 1: ENVIRONMENTAL VITAL SIGNS
# ==========================================
if page == "1. Environmental Vital Signs":
    st.title("Environmental Vital Signs: Kenya's Green Footprint")
    st.markdown("A macro evaluation of Kenya's structural landscape markers and green asset baseline values.")
    st.markdown("---")
    
    forest_val, forest_yr = get_latest_val_and_year(forest_df, start_yr, end_yr)
    hydro_val, hydro_yr = get_latest_val_and_year(hydro_df, start_yr, end_yr)
    oil_val, oil_yr = get_latest_val_and_year(oil_df, start_yr, end_yr)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"Forest Canopy Cover ({forest_yr})", value=f"{forest_val:.2f}%" if forest_val else "No Data")
        st.caption("Total land space occupied by natural forests.")
    with col2:
        st.metric(label=f"Hydroelectric Share ({hydro_yr})", value=f"{hydro_val:.2f}%" if hydro_val else "No Data")
        st.caption("Percentage of electricity generated by water currents.")
    with col3:
        st.metric(label=f"Oil Power Dependence ({oil_yr})", value=f"{oil_val:.2f}%" if oil_val else "No Data")
        st.caption("Percentage of power supplied by burning petroleum fuel.")
        
    st.markdown("---")
    
    col_l, col_r = st.columns([3, 2])
    with col_l:
        # High contrast timeline
        combined_mix = pd.DataFrame(index=range(start_yr, end_yr + 1)).join(hydro_df).rename(columns={'Value': 'Hydro'}).join(oil_df).rename(columns={'Value': 'Oil'}).dropna(how='all')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=combined_mix.index, y=combined_mix['Hydro'], name="Hydro Power (%)", line=dict(color='#0284c7', width=2)))
        fig.add_trace(go.Scatter(x=combined_mix.index, y=combined_mix['Oil'], name="Oil/Thermal Power (%)", line=dict(color='#dc2626', width=2)))
        apply_old_school_layout(fig, "The Power Grid Grid Baseline History", "Year", "Grid Share Percentage (%)")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_r:
        st.markdown("""
        <div class="translator-note">
            This overview gauges where Kenya gets its everyday electric energy from.<br><br>
            When the <strong>blue line (hydro)</strong> dips, it is usually a sign of severe droughts drying out river reservoirs. When it dips, the country historically had to fire up the <strong>red line (oil generators)</strong>, which makes electricity both more expensive and more polluting.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: THE POWER GRID MIX
# ==========================================
elif page == "2. The Power Grid Mix":
    st.title("The Power Grid: Moving Away From Dirty Fuel")
    st.markdown("A deep-dive review of structural transitions across Kenya's electricity production sectors.")
    st.markdown("---")
    
    combined_grid = pd.DataFrame(index=range(start_yr, end_yr + 1)).join(hydro_df).rename(columns={'Value': 'Hydro'}).join(oil_df).rename(columns={'Value': 'Oil'}).dropna(how='all')
    
    fig_grid = go.Figure()
    fig_grid.add_trace(go.Bar(x=combined_grid.index, y=combined_grid['Hydro'], name="Clean Hydroelectric generation", marker_color='#0ea5e9'))
    fig_grid.add_trace(go.Bar(x=combined_grid.index, y=combined_grid['Oil'], name="Dirty Oil/Thermal generation", marker_color='#64748b'))
    apply_old_school_layout(fig_grid, "Annual Power Resource Generation Balance Tracker", "Year", "Generation Share Percentage (%)")
    fig_grid.update_layout(barmode='stack')
    st.plotly_chart(fig_grid, use_container_width=True)
    
    st.markdown("""
    <div class="translator-note">
       Think of this stacked bar chart as a visual recipe of Kenya's electricity. The <strong>blue section</strong> is clean energy from rain and rivers, while the <strong>grey section</strong> is fossil fuel. Over the decades, you can look for moments where the grey bars shrink—this indicates Kenya successfully bringing non-fossil alternative grids (like massive geothermal wells) online!
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 3: CARBON EMISSIONS & FORESTS
# ==========================================
elif page == "3. Carbon Emissions & Forests":
    st.title("Sector Emissions & Natural Carbon Storage Sinks")
    st.markdown("Evaluating where carbon dioxide emissions are generated across the economy, vs the state of our forest buffers.")
    st.markdown("---")
    
    col_em_l, col_em_r = st.columns(2)
    
    with col_em_l:
        st.subheader("1. Emissions Breakdown by Economic Source")
        combined_co2 = pd.DataFrame(index=range(start_yr, end_yr + 1)).join(co2_agri).rename(columns={'Value': 'Agriculture'}).join(co2_build).rename(columns={'Value': 'Buildings/Energy'}).join(co2_defor).rename(columns={'Value': 'Deforestation'}).dropna(how='all')
        
        fig_co2 = go.Figure()
        fig_co2.add_trace(go.Scatter(x=combined_co2.index, y=combined_co2['Agriculture'], name="Farming & Livestock", line=dict(color='#eab308', width=2)))
        fig_co2.add_trace(go.Scatter(x=combined_co2.index, y=combined_co2['Buildings/Energy'], name="Buildings & Urban Power", line=dict(color='#ef4444', width=2)))
        fig_co2.add_trace(go.Scatter(x=combined_co2.index, y=combined_co2['Deforestation'], name="Forest Clearing", line=dict(color='#b45309', width=2, dash='dot')))
        apply_old_school_layout(fig_co2, "Sector Carbon Fingerprints (Mt CO2e)", "Year", "Million Tons of CO2")
        st.plotly_chart(fig_co2, use_container_width=True)
        
        st.markdown("""
        <div class="translator-note">
            Not all pollution comes from cars and factories. In Kenya, a huge portion of emissions tracks back to <strong>Building & Urban Power (red line)</strong> and <strong>Forest Clearing (brown line)</strong>. This chart highlights exactly which sectors need modern green solutions the most.
        </div>
        """, unsafe_allow_html=True)
        
    with col_em_r:
        st.subheader("2. Total Forest Preservation Coverage")
        
        # 1. Properly filter the dataframe slice inside the column block
        f_filtered = forest_df[(forest_df.index >= start_yr) & (forest_df.index <= end_yr)]
        
        fig_for = go.Figure()
        
        if not f_filtered.empty:
            # 2. Extract values cleanly using ['Value'] to ensure correct array formatting
            fig_for.add_trace(go.Scatter(
                x=f_filtered.index, 
                y=f_filtered['Value'], 
                name="Forest Area Cover", 
                line=dict(color='#10b981', width=2), 
                fill='tozeroy', 
                fillcolor='rgba(16, 185, 129, 0.1)'
            ))
            
            apply_old_school_layout(fig_for, "National Forest Canopy Share Status Tracker", "Year", "Percentage of Total Land Space (%)")
            
            # 3. Old school manual framing rules to handle narrow timeline zooms cleanly
            fig_for.update_layout(
                yaxis=dict(
                    range=[0, 15],  # Holds a safe baseline from 0% up to 15% forest cover
                    tickformat=".1f"  # Restricts numbers to exactly one clean decimal point (e.g., 6.3%)
                )
            )
            st.plotly_chart(fig_for, use_container_width=True)
        else:
            st.warning("No forest preservation data available for the selected timeframe.")
            
        st.markdown("""
        <div class="translator-note">
            Forests act as the planet's lungs, sucking up dirty carbon dioxide emissions directly out of the air. This <strong>green grid area</strong> tracks Kenya's forest canopy cover over time. Line slanting downward means we are losing our best natural shield against climate change.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 4: FUTURE GREEN HORIZONS
# ==========================================
elif page == "4. Future Green Horizons":
    st.title("Future Green Horizons: 5-Year Environmental Trends")
    st.markdown("Projecting baseline asset trends over a rolling 5-year statistical matrix based on historical velocities.")
    st.markdown("---")
    
    st.subheader("Select Environmental Variable to Project")
    choice = st.selectbox("Choose Target Variable:", ["Forest Area Canopy Cover (%)", "Hydroelectric Generation Grid Share (%)"])
    
    if choice == "Forest Area Canopy Cover (%)":
        target = forest_df
        lbl = "Projected Forest Coverage (%)"
        title_t = "Statistical Forest Area Path Trajectory"
    else:
        target = hydro_df
        lbl = "Projected Hydro Share (%)"
        title_t = "Statistical Hydro Generation Path Trajectory"
        
    fc_df = forecast_next_5_years(target)
    
    if not fc_df.empty:
        col_g, col_t = st.columns([3, 2])
        with col_g:
            h_years = target.index
            h_vals = target['Value'].values
            p_years = fc_df.index
            p_vals = fc_df['Projected Value'].values
            
            fig_f = go.Figure()
            fig_f.add_trace(go.Scatter(x=h_years, y=h_vals, name="Actual History Records", line=dict(color='#0f172a', width=2)))
            fig_f.add_trace(go.Scatter(x=p_years, y=p_vals, name="5-Year Mathematical Projection", line=dict(color='#db2777', width=2.5, dash='dash')))
            fig_f.add_trace(go.Scatter(x=[h_years[-1], p_years[0]], y=[h_vals[-1], p_vals[0]], showlegend=False, line=dict(color='#db2777', width=2, dash='dash')))
            
            apply_old_school_layout(fig_f, title_t, "Year", "Value Percentage (%)")
            st.plotly_chart(fig_f, use_container_width=True)
            
        with col_t:
            st.markdown("""
            <div class="forecast-note">
                <strong>Statistical Forecasting Rule Box:</strong><br>
                This trend line captures modern momentum from the last 15 recorded points to extend a projection arrow out towards 2030. It evaluates what our world will look like if policies and tree-planting initiatives stay at current speeds.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Projected Green Table Matrix")
            df_disp = fc_df.copy()
            df_disp['Projected Value'] = df_disp['Projected Value'].apply(lambda x: f"{x:.2f}%")
            st.table(df_disp.reset_index().rename(columns={'index': 'Year'}))