import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Solar PV ROI Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SIDEBAR INPUTS
# ==========================================
st.sidebar.title("☀️ Solar Parameters")
st.sidebar.markdown("Configure your system constraints and geographical data.")

# Currency Toggle
currency = st.sidebar.selectbox("Select Currency", ["$", "₹"])

# Default values dynamically adjust based on currency selection
default_bill = 150.0 if currency == "$" else 3000.0
default_cost_kwh = 0.15 if currency == "$" else 8.0
cost_per_kw = 1500 if currency == "$" else 60000

bill = st.sidebar.number_input(f"Monthly Electricity Bill ({currency})", min_value=1.0, value=default_bill, step=10.0)
cost_per_kwh = st.sidebar.number_input(f"Avg Cost per kWh ({currency})", min_value=0.01, value=default_cost_kwh, step=0.01)
roof_area = st.sidebar.number_input("Available Rooftop Area (sq ft)", min_value=50.0, value=1000.0, step=50.0)
psh = st.sidebar.slider("Avg Peak Sun Hours / Day", min_value=3.0, max_value=6.0, value=4.5, step=0.1)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Engineering Assumptions:**
* **Performance Ratio (PR):** 75% (0.75)  
* **Panel Degradation:** 0.5% per Year  
* **Space Req:** ~100 sq ft per 1 kW  
* **CO₂ Offset:** 0.85 lbs per kWh
""")

# ==========================================
# MATHEMATICAL LOGIC & MODELING
# ==========================================
# 1. Calculate Monthly kWh
monthly_kwh = bill / cost_per_kwh

# 2. Calculate Required System Size
# Formula: System Size = Monthly kWh / (30 * Peak Sun Hours * Efficiency Factor)
pr_factor = 0.75
required_system_size = monthly_kwh / (30 * psh * pr_factor)

# 3. Bound system size by available roof area (1 kW = 100 sq ft)
max_system_size_by_roof = roof_area / 100.0
actual_system_size = min(required_system_size, max_system_size_by_roof)

# 4. Total Setup Cost
total_cost = actual_system_size * cost_per_kw

# 5. Financial Modeling (15-Year Lifecycle)
annual_kwh_yr1 = actual_system_size * psh * 30 * 12 * pr_factor
degradation_rate = 0.005 # 0.5% per year

years = list(range(1, 16))
net_cash_flows = []
cumulative_savings = 0
break_even_year = None

for year in years:
    # Apply yearly degradation
    yearly_generation = annual_kwh_yr1 * ((1 - degradation_rate) ** (year - 1))
    yearly_savings = yearly_generation * cost_per_kwh
    
    cumulative_savings += yearly_savings
    net_position = cumulative_savings - total_cost
    net_cash_flows.append(net_position)
    
    # Identify the first year we go positive
    if net_position >= 0 and break_even_year is None:
        break_even_year = year

# 6. Environmental Impact
annual_co2_offset = annual_kwh_yr1 * 0.85 # in lbs

# ==========================================
# MAIN UI & OUTPUTS
# ==========================================
st.title("Interactive Solar PV Forecasting & ROI Dashboard")
st.markdown("Model optimal solar array sizing, energy yield forecasts, and financial payback periods based on grid conditions and area constraints.")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

# Format logic for displaying constraints safely
if actual_system_size == max_system_size_by_roof and required_system_size > max_system_size_by_roof:
    size_delta = f"Bounded by roof (Req: {required_system_size:.1f}kW)"
else:
    size_delta = "Meets 100% of load"

col1.metric("Recommended System Size", f"{actual_system_size:.2f} kW", delta=size_delta, delta_color="off")
col2.metric("Estimated Setup Cost", f"{currency}{total_cost:,.0f}")
col3.metric("Est. Payback Period", f"{break_even_year} Years" if break_even_year else "> 15 Years")
col4.metric("Annual CO₂ Offset", f"{annual_co2_offset:,.0f} lbs")

# ==========================================
# PLOTLY VISUALIZATION
# ==========================================
st.markdown("### 15-Year Financial Lifecycle Analysis")

# Create dynamic bar colors (Red for negative, Green for positive)
bar_colors = ['#e74c3c' if val < 0 else '#2ecc71' for val in net_cash_flows]

fig = go.Figure(data=[
    go.Bar(
        x=years,
        y=net_cash_flows,
        marker_color=bar_colors,
        text=[f"{currency}{val:,.0f}" for val in net_cash_flows],
        textposition='auto'
    )
])

fig.update_layout(
    xaxis_title="Timeline (Years)",
    yaxis_title=f"Net Financial Position ({currency})",
    template="plotly_dark",
    margin=dict(l=0, r=0, t=30, b=0),
    height=450
)

# Add Break-Even Line Annotation
fig.add_hline(y=0, line_dash="dash", line_color="white")

st.plotly_chart(fig, use_container_width=True)