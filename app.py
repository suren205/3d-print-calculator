import streamlit as st

# Set up the web page title and icon
st.set_page_config(page_title="3D Print Cost & ROI Calculator", page_icon="🖨️", layout="centered")

# App Header
st.title("🖨️ 3D Print Cost & ROI Calculator")
st.markdown("Calculate the *true* cost of your 3D prints, protect your business from failed prints, and set profitable retail prices.")
st.markdown("---")

# Sidebar Configuration for Global Settings
st.sidebar.header("⚙️ Global Rates Setup")
electricity_rate = st.sidebar.number_input("Electricity Rate ($ per kWh)", min_value=0.00, value=0.15, step=0.01, format="%.2f")
labor_rate = st.sidebar.number_input("Your Labor Rate ($ per Hour)", min_value=0.00, value=20.00, step=1.00, format="%.2f")
printer_wattage = st.sidebar.number_input("Printer Power Consumption (Watts)", min_value=0, value=150, step=10)
printer_depreciation = st.sidebar.number_input("Machine Wear/Depreciation ($ per Hour)", min_value=0.00, value=0.25, step=0.05, format="%.2f")

# Main Dashboard Grid
col1, col2 = st.columns(2)

with col1:
    st.header("📦 Material & Print Specs")
    spool_cost = st.number_input("Filament Spool Cost ($)", min_value=0.00, value=25.00, step=1.00, format="%.2f")
    spool_weight = st.number_input("Spool Total Weight (Grams)", min_value=1, value=1000, step=100)
    print_weight = st.number_input("Model Print Weight (Grams, incl. supports)", min_value=0.0, value=150.0, step=5.0)
    print_time = st.number_input("Estimated Print Time (Hours)", min_value=0.0, value=6.5, step=0.5)

with col2:
    st.header("💼 Business Variables")
    labor_time = st.number_input("Post-Processing / Setup Labor (Hours)", min_value=0.0, value=0.5, step=0.1)
    failure_rate = st.slider("Buffer for Failed Prints (%)", min_value=0, max_value=50, value=10, step=5)
    markup = st.slider("Desired Profit Margin Markup (%)", min_value=0, max_value=300, value=50, step=10)

st.markdown("---")

# Core Mathematical Logic Calculations
cost_per_gram = spool_cost / spool_weight
material_cost = print_weight * cost_per_gram

electricity_consumed = (printer_wattage / 1000) * print_time
electricity_cost = electricity_consumed * electricity_rate

machine_wear_cost = print_time * printer_depreciation
labor_cost = labor_time * labor_rate

# Subtotal of baseline operational costs
base_production_cost = material_cost + electricity_cost + machine_wear_cost + labor_cost

# Apply print failure buffers and financial markup structures
failure_buffer_cost = base_production_cost * (failure_rate / 100)
total_manufacturing_cost = base_production_cost + failure_buffer_cost
profit_margin_value = total_manufacturing_cost * (markup / 100)
recommended_retail_price = total_manufacturing_cost + profit_margin_value

# Displaying Results & Breakdown Visuals
st.header("📊 Price Summary & Cost Breakdown")

# Big bold metrics at a glance
metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    st.metric(label="Total Production Cost (with failure buffer)", value=f"${total_manufacturing_cost:.2f}")
with metric_col2:
    st.color_picker("Suggested Price Metric Accent", "#4CAF50", disabled=True, label_visibility="collapsed")
    st.subheader(f"Suggested Retail Price: **${recommended_retail_price:.2f}**")

# Detailed line-item breakdown list
st.markdown("### 🔍 Line-Item Breakdown")
st.write(f"- **Material Cost ({print_weight}g used):** ${material_cost:.2f}")
st.write(f"- **Electricity Cost ({electricity_consumed:.3f} kWh):** ${electricity_cost:.2f}")
st.write(f"- **Machine Wear & Maintenance:** ${machine_wear_cost:.2f}")
st.write(f"- **Hands-on Labor Cost:** ${labor_cost:.2f}")
st.write(f"- **Risk Protection (Failed Print Buffer):** ${failure_buffer_cost:.2f}")
st.write(f"- **Net Profit Generation:** ${profit_margin_value:.2f}")

st.markdown("---")
st.caption("Powered by your custom Micro-SaaS engine. Ready for cloud deployment.")